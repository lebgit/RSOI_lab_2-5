from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort, Markup
from gui.utils import do_create_meh, do_get_meh, do_delete_meh, do_get_paginated_meh, do_get_paginated_fix , do_rem_meh
import json

mod = Blueprint('mehs', __name__)

def fp():
    result = do_get_paginated_fix(1, 100, request.cookies)
    if result.success:
        if result.response.status_code == 200:
            fixes_obj = result.response.content
            fixs_str = (str(fixes_obj)).split('\\n')
            n = len(fixs_str)
            fixs_str[0] = fixs_str[0][2:]
            fixs_str[n - 1] = fixs_str[n - 1][0:-1]
            fixs_str.remove(fixs_str[n - 1])
            return fixs_str
    flash("Мастерские не найдены", "error")
    return 404

@mod.route('/mehs/')
def index():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    return render_template("/mehs/index.html")


@mod.route('/mehs/create', methods=['GET', 'POST'])
def create():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        return render_template("/mehs/create.html")
    else:
        failed = False
        if 'name' not in request.form or request.form['name']=='':
            flash('Имя не задано', "error")
            failed = True

        if 'lvl' not in request.form or request.form['lvl']=='':
            flash('Стаж не задано', "error")
            failed = True

        if 'year' not in request.form or request.form['year']=='':
            flash('Год не задана', "error")
            failed = True

        if failed:
            return redirect(url_for('mehs.create'))

        name = request.form['name']
        lvl = request.form['lvl']
        year = request.form['year']
        result = do_create_meh(name, lvl, year,request.cookies)
        if result.success:
            if result.response.status_code == 201:
                flash('Фильм успешно добавлен', "info")
                response = redirect('mehs/create')
                return response
            else:
                flash(result.response.content.decode('utf-8'), "error")
                return redirect(url_for('mehs.create'))
        else:
            flash(result.error)
            return redirect(url_for('mehs.create'), "error")


@mod.route('/mehs/get', methods=['GET', 'POST'])
def get():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        return render_template("/mehs/get.html", meh_found = False)
    else:
        if 'meh_id' not in request.form or request.form['meh_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('mehs.get'))
        else:
            meh_id = request.form["meh_id"]
            result = do_get_meh(meh_id,request.cookies)

            if result.success:
                if result.response.status_code == 200:
                    meh = json.loads(result.response.content)
                    return render_template("/mehs/get.html", meh=meh, meh_found=True)
                else:
                    flash("Фильм не найден", "error")
                    return redirect(url_for('mehs.get'))
            else:
                flash(result.error, "error")
                return redirect(url_for('mehs.get'))


@mod.route('/mehs/delete/<meh_id>', methods=['GET', 'POST'])
def delete(meh_id):
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        fixes = []
        fixs_str=fp()
        flag2 = 0
        if fixs_str!=404:
            for fix in fixs_str:
                if fix != "":
                    fixl = json.loads(bytes(fix, 'utf8'))
                    ar = fixl["meh_ids"]
                    for i in range(len(ar)):
                        if meh_id == (ar[i-1]):
                            flag2 = 1
                            fixes.append(fixl["fix_id"])
            if fixes!=[]:
                return render_template("/mehs/delete.html", meh_id=meh_id,fix_id=fixes,flag2=flag2)
            else:
                return render_template("/mehs/delete.html", meh_id=meh_id,flag2=flag2)
        else:
            return redirect(url_for('mehs.index'))
    else:

        if request.form['submit'] == 'Нет':
            return redirect(url_for('mehs.get_all'))

        if request.form['submit'] == 'Да':
            if request.form["flag2"] == '0':
                result = do_delete_meh(meh_id,'',request.cookies )
            else:
                result = do_delete_meh(meh_id,request.form["flag2"],request.cookies)

            if result.success:
                if result.response.status_code == 204:
                    flash('Фильм успешно удален', "info")
                    response = redirect(url_for('mehs.get_all'))
                    return response
                else:
                    flash("Фильм не найден", "error")
                    return redirect(url_for('mehs.get_all'))
            else:
                flash(result.error, "error")
                return redirect(url_for('mehs.get_all'))


@mod.route('/movies/get_all')
def get_all():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('mehs.get_all', page=1))
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_meh(page, 10,request.cookies)
        if result.success:
            if result.response.status_code == 200:
                mehs_obj = result.response.content
                mehs_str = (str(mehs_obj)).split('\\n')
                n = len(mehs_str)
                mehs_str.remove(mehs_str[0])
                n = n-1
                mehs_str[n-1] = mehs_str[n-1][0:-1]
                mehs = []
                dictr = json.loads(mehs_str[n-1])
                mehs_str.remove(mehs_str[n-1])
                for meh in mehs_str:
                    meh1 = bytes(meh, 'utf8')
                    mehs.append(json.loads(meh1))
                fixes = []

                fixs_str = fp()
                if fixs_str!=404:
                    for fix in fixs_str:
                        if fix != "":
                            fixl = json.loads(bytes(fix, 'utf8'))
                            ar = fixl["meh_ids"]
                            for i in range(len(ar)):
                                meh_id = (ar[i - 1])
                                if meh_id not in fixes:
                                    fixes.append(meh_id)
                    return render_template("/mehs/get_all.html", mehs=mehs,fixes=fixes, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
                else:
                    return redirect(url_for('mehs.index'))
            else:
                flash("Механики не найдены", "error")
                return redirect(url_for('mehs.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('mehs.index'))

@mod.route('/fixes/patchadd', methods=['GET', 'POST'])
def patchadd():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        meh_id = request.args['meh_id']
        fixes = []
        fixes_str = fp()
        if fixes_str!=404:
            for fix in fixes_str:
                if fix != "":
                    fixl = json.loads(bytes(fix, 'utf8'))
                    datetime = str(fixl["datetime"])
                    dictionary = {"fix_id": fixl["fix_id"],
                                    "date_time": datetime}
                    fixes.append(dictionary)
            return render_template("/mehs/patchadd.html", fixes=fixes,meh_id=meh_id)
        else:
            return redirect(url_for('mehs.index'))
    else:
        if 'fix_id' not in request.form or request.form['fix_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('mehs.get_all'))
        else:
            fix_id = request.form['fix_id']
            meh_id = request.args['meh_id']
            result = do_rem_meh(fix_id, meh_id, "mehadd",request.cookies)
            if result.success:
                if result.response.status_code == 201:
                    flash("Механик устроен", "info")

                    return render_template("/fixes/get_all.html")
                else:
                    flash("Механик не устроен", "error")
                    return redirect(url_for('fixes.get_all'))
            else:
                flash(result.error, "error")
                return redirect(url_for('fixes.get_all'))