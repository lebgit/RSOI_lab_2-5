from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_create_fix, do_get_paginated_fix, do_get_fix , do_rem_meh
import json

mod = Blueprint('fixes', __name__)


@mod.route('/fixes/')
def index():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    flag = request.args['flag']
    return render_template("/fixes/index.html",flag=flag)


@mod.route('/fixes/get/<fix_id>', methods=['GET', 'POST'])
def get(fix_id):
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        result = do_get_fix(fix_id,request.cookies)
        if result.success:
            if result.response.status_code == 200:
                tmp = str(result.response.content)
                list_sm = tmp.split('\\n')
                fix = list_sm[0]
                fix = fix[2:]
                fix_d = json.loads(fix)
                datetime = str(fix_d["datetime"])
                ar = fix_d["car_ids"]
                md=fix_d["meh_ids"]
                dictionaryf={"fix_id": fix_d["fix_id"], "meh_ids": md, "car_ids": ar,"date_time":datetime}
                n = len(list_sm)
                list_sm[0] = list_sm[0][2:]
                list_sm[n-1] = list_sm[n-1][0:-1]
                mehs = []
                list_sm.remove(list_sm[0])

                for meh in list_sm:
                    if meh != "" :
                        mehl = json.loads(bytes(meh, 'utf8'))
                        #ar = mehl["meh_id"]
                        dictionarym = {"meh_id": mehl["meh_id"], "name": mehl["name"],
                                      "lvl": mehl["lvl"],
                                      "year": mehl["year"]}
                        mehs.append(dictionarym)

                #meh_d = json.loads(meh)
                return render_template("/fixes/get.html", fix=dictionaryf, mehs=mehs, number_of_cars= len(ar)+1,cars=ar)
            else:
                flash('Ошибка. Мастерской не существует.', "error")
                return redirect(url_for('fixes.get_all'), "error")
        else:
            flash(result.error, "error")
            return redirect(url_for('fixes.get_all'), "error")


@mod.route('/fixes/create', methods=['GET', 'POST'])
def create():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
            return render_template("/fixes/create.html")
    else:
        failed = False
        if 'date_time' not in request.form or request.form['date_time']=='':
            flash('Дата создания не задана', "error")
            failed = True
        if failed:
            return render_template("/fixes/create.html")

        result = do_create_fix( request.form['date_time'],request.cookies)
        if result.success:
            if result.response.status_code == 201:
                flash('Сеанс успешно создан', "info")
                response = redirect('fixes/get_all')
                return response
            else:
                st = result.response.content.decode('utf-8')
                if st=='':
                    st = str(result.response.content)
                flash(st, "error")
                return redirect(url_for('fixes/get_all'))
        else:
            flash(result.error)
            return redirect(url_for('fixes/get_all'), "error")


@mod.route('/fixes/get_all')
def get_all():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('fixes.get_all', page=1))
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_fix(page, 10,request.cookies)
        if result.success:
            if result.response.status_code == 200:
                fixes_obj = result.response.content
                fixes_str = (str(fixes_obj)).split('\\n')
                n = len(fixes_str)
                fixes_str[0] = fixes_str[0][2:]
                fixes_str[n-1] = fixes_str[n-1][0:-1]
                fixes = []
                dictr = json.loads(fixes_str[n-1])
                fixes_str.remove(fixes_str[n-1])
                for fix in fixes_str:
                    if fix != "":
                        fixl = json.loads(bytes(fix, 'utf8'))
                        ar = fixl["car_ids"]
                        ar1 = fixl["meh_ids"]
                        number_of_mehs = len(ar1)
                        number_of_cars = len(ar)
                        datetime = str(fixl["datetime"])
                        dictionary = {"fix_id": fixl["fix_id"], "number_of_mehs": number_of_mehs,
                                      "number_of_cars": number_of_cars,
                                      "date_time":datetime}
                        fixes.append(dictionary)
                return render_template("/fixes/get_all.html", fixes=fixes, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            else:
                flash("Мастерские не найдены", "error")
                return redirect(url_for('fixes.index', flag='FALSE'))
        else:
            flash(result.error, "error")
            return redirect(url_for('fixes.index', flag='FALSE'))


@mod.route('/fixes/patchrem', methods=['GET', 'POST'])
def patchrem():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        fix_id = request.args['fix_id']
        meh_id = request.args['meh_id']
        return render_template("/fixes/patchrem.html",fix_id = fix_id, meh_id = meh_id)
    else:
        if 'meh_id' not in request.args or request.args['meh_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('fixes.get',fix_id=request.args['fix_id']))
        else:
            fix_id = request.args['fix_id']
            meh_id = request.args['meh_id']
            result = do_rem_meh(fix_id, meh_id, "mehrem",request.cookies)

            if result.success:
                if result.response.status_code == 201:
                    flash("Механик уволен", "info")

                    return render_template("/fixes/get_all.html")
                else:
                    flash("Механик не уволен", "error")
                    return redirect(url_for('fixes.get_all'))
            else:
                flash(result.error, "error")
                return redirect(url_for('fixes.get_all'))
