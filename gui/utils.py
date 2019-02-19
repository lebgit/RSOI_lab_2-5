
from functools import wraps
from flask import g, url_for, flash, abort, request, redirect, make_response
import requests
import requests.exceptions
from gui.config import current_config
import jsonpickle


class Result:
    def __init__(self, success, response=None, error=None, redirect=None):
        self.success = success
        self.error = error
        self.redirect = redirect
        self.response = response


def request_handler(redirect_url):
    def wrap(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                request_result = f(*args, **kwargs)
                return Result(success=True, redirect=redirect_url, response=request_result)
            except requests.exceptions.Timeout as e:
                return Result(success=False, error='Время ожидания ответа превышено. Повторите запрос позже')
            except requests.exceptions.ConnectionError as e:
                return Result(success=False, error='В данный момент сервис недоступен. Повторите запрос позже')
            except requests.exceptions.RequestException as e:
                return Result(success=False, error='Произошла ошибка. Повторите запрос позже')
        return decorated_function
    return wrap

@request_handler(redirect_url='users.login')
def do_get_code(client_id):
    result = gateway_api_request(current_config.USER_SERVICE_PATH+"/auth", 'POST',
                                 data={'client_id': client_id})
    return result


@request_handler(redirect_url='users.login')
def do_get_auth_token(client_id, client_secret, code):
    result = gateway_api_request(current_config.USER_SERVICE_PATH+"/auth", 'GET',
                                 data={'client_id': client_id, 'client_secret': client_secret, 'code': code})
    return result

@request_handler(redirect_url='cars.index')
def do_get_paginated_cars(page, page_size,cookies):
    result = gateway_api_request(current_config.CAR_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)), cookies=cookies)
    return result


@request_handler(redirect_url='cars.index')
def do_get_car(car_id,cookies):
    result = gateway_api_request(current_config.CAR_SERVICE_PATH+'/'+car_id, 'GET', cookies=cookies)
    return result


@request_handler(redirect_url='cars.index')
def do_add_car(fix_id, name, cookies):
    flash((current_config.CAR_SERVICE_PATH+'/add', 'POST', {'fix_id': fix_id, 'name': name}, cookies),'info')
    result = gateway_api_request(current_config.CAR_SERVICE_PATH+'/add', 'POST', {'fix_id': fix_id,'name':name}, cookies=cookies)
    return result


@request_handler(redirect_url='cars.index')
def do_return_car(car_id,cookies):
    result = gateway_api_request(current_config.CAR_SERVICE_PATH+'/ret/'+car_id, 'DELETE', cookies=cookies)
    return result


@request_handler(redirect_url='fixes.index')
def do_get_paginated_user(page, page_size,cookies):
    result = gateway_api_request(current_config.USER_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)), cookies=cookies)
    return result


@request_handler(redirect_url='users.login')
def do_authorization(login, password):
    result = gateway_api_request(current_config.USER_SERVICE_PATH+current_config.GET_TOKEN_URL_PATH, 'GET',
                                 params=(('l_name', login), ('password', password)))
    return result
@request_handler(redirect_url='menu.index')
def do_logout():
    response = make_response("")
    if 'token' in request.cookies:
        response.delete_cookie('token')
    return response

@request_handler(redirect_url='fixes.index')
def do_get_user(user_id,cookies):
    result = gateway_api_request(current_config.USER_SERVICE_PATH+'/'+user_id, 'GET', cookies=cookies)
    return result


@request_handler(redirect_url='mehs.get_all')
def do_create_fix( date_time,cookies):
    result = gateway_api_request(current_config.FIX_SERVICE_PATH + current_config.CREATE_PATH, 'POST',
                                 {
                                  'date_time': date_time}, cookies=cookies)
    return result


@request_handler(redirect_url='fixes.index')
def do_get_paginated_fix(page, page_size,cookies):
    result = gateway_api_request(current_config.FIX_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)), cookies=cookies)
    return result


@request_handler(redirect_url='fixes.index')
def do_get_fix(fix_id,cookies):
    result = gateway_api_request(current_config.FIX_SERVICE_PATH+'/'+fix_id, 'GET', cookies=cookies)
    return result


@request_handler(redirect_url='mehs.index')
def do_create_meh(name, lvl, year,cookies):
    result = gateway_api_request(current_config.MECHANIC_SERVICE_PATH + current_config.CREATE_PATH, 'POST',
                                 {'name': name, 'lvl': lvl, 'year': year}, cookies=cookies)
    return result
@request_handler(redirect_url='users.index')
def do_create_user(l_name, password, admin,cookies):
    result = gateway_api_request(current_config.USER_SERVICE_PATH + current_config.CREATE_PATH, 'POST',
                                 {'l_name': l_name, 'password': password, 'admin': admin}, cookies=cookies)
    return result


@request_handler(redirect_url='mehs.index')
def do_get_meh(meh_id,cookies):
    result = gateway_api_request(current_config.MECHANIC_SERVICE_PATH + '/' + meh_id, 'GET', cookies=cookies)
    return result


@request_handler(redirect_url='mehs.index')
def do_get_paginated_meh(page, page_size,cookies):
    result = gateway_api_request(current_config.MECHANIC_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)), cookies=cookies)
    return result


@request_handler(redirect_url='mehs.index')
def do_delete_meh(meh_id,fix_id,cookies):
    result = gateway_api_request(current_config.MECHANIC_SERVICE_PATH + '/' + meh_id, 'DELETE',{'fix_id':fix_id}, cookies=cookies)
    return result
@request_handler(redirect_url='fixes.index')
def do_rem_meh(fix_id, meh_id,status,cookies):
    result = gateway_api_request(current_config.FIX_SERVICE_PATH + '/add/' +fix_id, 'PATCH',{'meh_id': meh_id,'status':status}, cookies=cookies)
    return result

@request_handler(redirect_url='fixes.index')
def do_get_user_tok(cookies):
    result = gateway_api_request(current_config.USER_SERVICE_PATH + '/token', 'GET', cookies=cookies)
    return result

def gateway_api_request(service_path, method, data=None, params=None, cookies=None):
    if method == 'GET':
        data = jsonpickle.encode(data)
        return requests.get(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                            + service_path, data=data, params=params, cookies=cookies)
    elif method == 'POST':
        data = jsonpickle.encode(data)
        return requests.post(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                             + service_path, data=data, params=params,
                             cookies=cookies)
    elif method == 'PUT':
        return requests.put(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                            + service_path, data, params=params, cookies=cookies)
    elif method == 'DELETE':
        data = jsonpickle.encode(data)
        return requests.delete(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                               + service_path,data=data, cookies=cookies)
    elif method == 'PATCH':
        data = jsonpickle.encode(data)
        return requests.patch(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                              + service_path, data=data, cookies=cookies)
    else:
        abort(400)