from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_get_paginated_cars, do_get_car, do_add_car, do_return_car,do_logout,do_get_paginated_fix,do_get_user_tok
import json

mod = Blueprint('cars', __name__)


@mod.route('/cars/')
def index():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    return render_template("/cars/index.html")


@mod.route('/cars/get', methods=['GET', 'POST'])
def get():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        return render_template("/cars/get.html", ticket_found = False)
    else:
        if 'car_id' not in request.form or request.form['car_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('cars.get'))
        else:
            car_id = request.form["car_id"]
            result = do_get_car(car_id,request.cookies)

            if result.success:
                if result.response.status_code == 200:
                    car = json.loads(result.response.content)
                    return render_template("/cars/get.html", car=car, car_found=True)
                else:
                    flash("Машину не найден", "error")
                    return redirect(url_for('cars.get'))
            else:
                flash(result.error, "error")
                return redirect(url_for('cars.get'))


@mod.route('/cars/add', methods=['GET', 'POST'])
def add():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        result = do_get_paginated_fix(1, 100, request.cookies)
        if result.success:
            if result.response.status_code == 200:
                fixes_obj = result.response.content
                fixes_str = (str(fixes_obj)).split('\\n')
                n = len(fixes_str)
                fixes_str[0] = fixes_str[0][2:]
                fixes_str[n - 1] = fixes_str[n - 1][0:-1]
                fixes = []
                fixes_str.remove(fixes_str[n - 1])
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
                                      "date_time": datetime}
                        fixes.append(dictionary)
            #user_id=request.args['user_id']
            return render_template("/cars/add.html", fixes=fixes)
    else:
        fix_id = request.form['fix_id']
        name = request.form['name']
        result = do_add_car(fix_id, name, request.cookies)
        #flash(request.cookies, 'info')
        if result.success:
            #flash(result.response.status_code, 'info')
            if result.response.status_code == 201:
                flash('Запрос на починку успешно добавлен', 'info')
                return redirect(url_for('cars.get_all'))
            elif result.response.status_code == 403:
                do_logout()
                return redirect(url_for('users.login'))
            else:
                flash('Запрос на починку не может быть добавлен', 'error')
                return redirect(url_for('cars.get_all'))
        else:
            flash(result.error, 'error')
            return redirect(url_for('cars.get_all'))




@mod.route('/cars/ret' ,methods=['GET', 'POST'])
def ret():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        car_id = request.args['car_id']
        return render_template("/cars/ret.html", car_id=car_id)
    else:
        if request.form['submit'] == 'Нет':
            return redirect(url_for('mehs.get_all'))

        if request.form['submit'] == 'Да':
            car_id =request.args['car_id']
            result = do_return_car(car_id, request.cookies)
            if result.success:
                if result.response.status_code == 204:
                    flash('Возврат машины успешно произведен', 'info')
                    return redirect(url_for('menu.index'))
                elif result.response.status_code == 403:
                    do_logout()
                    return redirect(url_for('users.login'))
                else:
                    flash('Возврат машины не может быть произведен', 'error')
                    return redirect(url_for('menu.index'))
            else:
                flash(result.error, 'error')
            return redirect(url_for('menu.index'))


@mod.route('/cars/get_all')
def get_all():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('cars.get_all', page=1))
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_cars(page, 10,request.cookies)
        if result.success:
            if result.response.status_code == 200:
                cars_obj = result.response.content
                cars_str = (str(cars_obj)).split('\\n')
                n = len(cars_str)
                cars_str[0] = cars_str[0][2:]
                cars_str[n-1] = cars_str[n-1][0:-1]
                cars = []
                dictr = json.loads(cars_str[n-1])
                cars_str.remove(cars_str[n-1])
                for car in cars_str:
                    if car != '':
                        carl = bytes(car, 'utf8')
                        cars.append(json.loads(carl))
                return render_template("/cars/get_all.html", cars=cars, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            else:
                flash("Машины не найдены", "error")
                return redirect(url_for('cars.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('cars.index'))

@mod.route('/cars/get1', methods=['GET', 'POST'])
def get1():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'car_id' not in request.args:
            flash('Идентификатор не задан', "error")
            return redirect(url_for('cars.get'))
        else:
            car_id = request.args.get('car_id', 1, type=str)
            result = do_get_car(car_id,request.cookies)

            if result.success:
                if result.response.status_code == 200:
                    car = json.loads(result.response.content)
                    result=do_get_user_tok(request.cookies)
                    user=json.loads(result.response.content)
                    return render_template("/cars/get1.html", car=car, car_found=True, admin=user['admin'])
                else:
                    flash("Мащина не найдена", "error")
                    return redirect(url_for('cars.get'))
            else:
                flash(result.error, "error")
                return redirect(url_for('cars.get'))