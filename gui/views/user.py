from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_get_paginated_user, do_get_user, do_authorization,\
    do_logout,do_get_code,do_get_user_tok,do_get_auth_token,do_create_user
import json

mod = Blueprint('users', __name__)


@mod.route('/users/')
def index():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    flag = request.args['flag']
    return render_template("/users/index.html",flag=flag)

@mod.route('/APIlogin1')
def APIlogin1():
    client_id = 1
    client_secret = 123
    result = do_get_code(client_id)
    if result.success:
        if result.response.status_code == 201:
            code_d = json.loads(result.response.content)
            code = code_d['code']
            response = redirect(url_for('users.APIlogin2', code=code, client_id=client_id, client_secret=client_secret))
            return response
        else:
            flash(result.response.content.decode('utf-8'), 'error')
            return redirect(url_for('users.login'))
    else:
        flash(result.error)
    return redirect(url_for('users.login'))


@mod.route('/APIlogin2')
def APIlogin2():
    client_id = request.args.get('client_id', type=int)
    client_secret = request.args.get('client_secret', type=int)
    code = request.args.get('code', type=str)
    result = do_get_auth_token(client_id, client_secret, code)

    if result.success:
        flash(result.response.status_code, 'info')
        if result.response.status_code == 200:
            response = redirect(url_for('menu.index'))
            response.headers["Set-Cookie"] = result.response.headers["Set-Cookie"]
            g.user = result.response.cookies
            return response
        else:
            flash(result.response.content.decode('utf-8'))
            return redirect(url_for('users.login'))
    else:
        flash(result.error)
    return redirect(url_for('users.login'))
@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("/users/login.html")
    else:
        fail = False
        if 'l_name' not in request.form or request.form['l_name'] == '':
            flash('Логин не задан', "error")
            fail = True
        if 'password' not in request.form or request.form['password'] == '':
            flash('Пароль не задан', "error")
            fail = True
        if fail:
            return redirect(url_for('users.login'))
        l_name = request.form['l_name']
        password = request.form['password']
        result = do_authorization(l_name, password)
        if result.success:
            if result.response.status_code == 200:
                response = redirect(url_for('menu.index'))

                response.headers["Set-Cookie"] = result.response.headers["Set-Cookie"]
                #flash(result.response.cookies, 'info')
                g.user = result.response.cookies
                #g.logged_in = True
                return response

            else:
                flash(result.response.content.decode('utf-8'))
                return redirect(url_for('users.login'))
        else:
            flash(result.error)
        return redirect(url_for('users.login'))


@mod.route('/users/logout')
def logout():
    result = do_logout()
    response = redirect(url_for(result.redirect))
    response.delete_cookie('token')
    return response


@mod.route('/users/get/<user_id>')
def get(user_id):
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        result = do_get_user(user_id,request.cookies)
        if result.success:
            if result.response.status_code == 200:
                user = json.loads(result.response.content)
                return render_template("/users/get.html", user = user)
            else:
                flash('Юзер не найде существует.', "error")
                return redirect(url_for('users.get_all'), "error")
        else:
            flash(result.error, "error")
            return redirect(url_for('users.get_all'), "error")

@mod.route('/users/get1/')
def get1():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        result = do_get_user_tok(request.cookies)
        if result.success:
            if result.response.status_code == 200:
                user = json.loads(result.response.content)
                flag=user['status']
                return render_template("/users/get1.html", user = user,flag=flag)
            else:
                flash('Ошибка Юзер Не найден перезайди', "error")
                return redirect(url_for('users.get_all'), "error")
        else:
            flash(result.error, "error")
            return redirect(url_for('users.get_all'), "error")


@mod.route('/users/get_all')
def get_all():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('users.get_all', page=1))
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_user(page, 10,request.cookies)
        if result.success:
            if result.response.status_code == 200:
                users_obj = result.response.content
                users_str = (str(users_obj)).split('\\n')
                n = len(users_str)
                users_str[0] = users_str[0][2:]
                users = []
                users_str[n-1] = users_str[n-1][0:-1]
                dictr = json.loads(users_str[n-1])
                users_str.remove(users_str[n-1])
                for user in users_str:
                    if user != "":
                        user1 = bytes(user, 'utf8')
                        users.append(json.loads(user1))
                return render_template("/users/get_all.html", users=users, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            else:
                flash("Потльзователь не найден", "error")
                return redirect(url_for('menu.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('menu.index'))

@mod.route('/create', methods=['GET', 'POST'])
def create():
    flag = 1
    if not g.logged_in:
        flag = 0
    if request.method == 'GET':
            if flag == 1:
                result = do_get_user_tok(request.cookies)
                if result.success:
                    if result.response.status_code == 200:
                        user = json.loads(result.response.content)
                        if user['admin']!= 'True':
                            flag = 0
            return render_template("/users/create.html", flag=flag)
    else:
        failed = False
        if 'l_name' not in request.form or request.form['l_name']=='':
            flash('Логин не задана', "error")
            failed = True
        if 'password' not in request.form or request.form['password']=='':
            flash('Пароль не задана', "error")
            failed = True
        if flag == 1:
            if 'admin' not in request.form or request.form['admin']=='':
                flash('Права не заданы', "error")
                failed = True
        if failed:
            return render_template("/users/create.html")
        if flag == 1:
            result = do_create_user( request.form['l_name'],request.form['password'],request.form['admin'],request.cookies)
        else:
            result = do_create_user(request.form['l_name'], request.form['password'], 'False',
                                    request.cookies)
        if result.success:
            if result.response.status_code == 201:
                flash('Пользователь успешно создан', "info")
                if not g.logged_in:
                    return redirect(url_for('users.login'))
                response = redirect('/users/create')
                return response
            else:
                st = result.response.content.decode('utf-8')
                if st=='':
                    st = str(result.response.content)
                flash(st, "error")
                if not g.logged_in:
                    return redirect(url_for('users.login'))
                return redirect(url_for('users/'))
        else:
            flash(result.error)
            return redirect(url_for('users/'), "error")