import flask
import jsonpickle
import requests
from flask_restful import Resource, reqparse
from fix.domain.fix import Fix
from mechanic.domain.meh import Mechanic
from car.domain.car import Car
from user.domain.user import User
from config import current_config
from gateway import app, replay_request_queue
import json
from gateway.queues.car_return_handling import Request
from flask import Flask, render_template




class GatewayCarResource(Resource):



    def get(self, car_id):
        app.logger.info('Получен запрос на получение информации о машине с идентификатором %s' % car_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        response = requests.get(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH + "/%s" % car_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Информация о машине с идентификатором %s успещно получена' % car_id)
        else:
            app.logger.warning('Информация о тмашине с идентификатором %s не может быть получена' % car_id)
        return result


class GatewayCarListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка билетов')
        try:
            args = self.parser.parse_args(strict=True)
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество билетов на странице: %d' % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        payload = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка билетов успешно обработан')
        else:
            app.logger.warning('Список билетов не может быть получен')
        return result


class GatewayFixResource(Resource):
    def get(self, fix_id):
        app.logger.info('Получен запрос на получение подробной информации о мастерской с идентификатором %s' % fix_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        response_fix = requests.get(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                                       "/%s" % fix_id)
        if response_fix.status_code == 200:
            app.logger.info('Запрос на получение информации о мастерской с идентификатором %s успешно обработан'
                            % fix_id)
        else:
            app.logger.warning('Информация о мастерской с идентификатором %s не модет быть получена' % fix_id)
            result = flask.Response(status=response_fix.status_code, headers=response_fix.headers.items(),
                                    response=response_fix.content)
            return result

        fix = Fix.from_json(response_fix.content)
        meh_ids = fix.meh_ids
        response = fix.to_json()+'\n'
        if meh_ids != []:
            for meh_id in meh_ids:
                try:
                    response_meh = requests.get(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                                                  "/%s" % meh_id)
                except:
                    response_meh = None
                if response_meh is not None and response_meh.status_code == 200:
                    app.logger.info('Запрос на получение информации о механике с идентификатором %s успешно обработан'
                                    % meh_id)
                    meh = Mechanic.from_json(response_meh.content)
                    response = response + '\n' + meh.to_json()
                else:
                    app.logger.warning('Информация о фильме с идентификатором %s не модет быть получена' % meh_id)
                    meh = {'meh_id': 'Information is not available', 'name': 'Information is not available',
                             'lvl': 'Information is not available', 'year': 'Information is not available'}
                    response = response + '\n' + json.dumps(meh)
        response=response +'\n'
        result = flask.Response(status=response_fix.status_code, headers=response_fix.headers.items(),
                                response=response)
        app.logger.info('Запрос на получение подробной информации о мезанике с идентификатором %s успешно обработан'
                        % fix_id)
        return result

class GatewayFixResourcePatch(Resource):
    def patch(self, fix_id):
        app.logger.info('Получен запрос на устройство механика в мастерскую с идентификатором %s' % fix_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        paybuy = jsonpickle.decode(flask.request.data)
        payload = {'meh_id':paybuy["meh_id"],'status':paybuy["status"]}
        res = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/%s" % fix_id, data=jsonpickle.encode(payload))
        result = flask.Response(status=res.status_code, headers=res.headers.items(),
                                response=res.content)

        if res.status_code == 201:
            app.logger.info('Механик устроен/уволен')
        else:
            app.logger.warning('Механик не устроен/уволен')
        return result


class GatewayFixCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание масерской')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        try:
            response = requests.post(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=flask.request.data)
        except:
            paybuy = { 'date_time': '12.11.2018_20:00'}
            response = requests.post(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                                     current_config.CREATE_PATH, data = jsonpickle.encode(paybuy))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 201:
            app.logger.info('Мастерская успешно создана')
        else:
            app.logger.warning('Мастерсая не может быть создана')
        return result


class GatewayFixListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение список мастерских')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %s; количество мастерских на странице: %s' % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        paybuy = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH, params=paybuy)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка мастерских успешно обработан')
        else:
            app.logger.warning('Список мастерских не может быть получен')
        return result


class GatewayMehResource(Resource):
    def get(self, meh_id):
        app.logger.info('Получен запрос на получение информации о механике с идентификатором %s' % meh_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        response = requests.get(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                                "/%s" % meh_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о механике с идентификатором %s успешно обработан' % meh_id)
        else:
            app.logger.warning('Информация о механике с идентификатором %s не может быть получена' % meh_id)
        return result

    def delete(self, meh_id):
        app.logger.info('Получен запрос на увольнение механика с идентификатором %s' % meh_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        flag=0
        try:
            paybuy = jsonpickle.decode(flask.request.data)
            payload = {'meh_id': meh_id, 'status': 'mehrem'}
            response = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/%s" % paybuy["fix_id"], data=jsonpickle.encode(payload))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
            if response.status_code == 201:
                app.logger.info('Механик уволен')
            else:
                app.logger.warning('Механик не уволен')
                return result
        except:
            flag=1
        response = requests.delete(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                                   "/%s" % meh_id)

        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 204:
            app.logger.info('Механик с идентификатором %s успешно уволен' % meh_id)
        else:
            app.logger.warning('Механике с идентификатором %s не может быть уволен' % meh_id)
            if flag==0:
                payload = {'meh_id': meh_id, 'status': 'mehadd'}
                response = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                                      "/%s" % paybuy["fix_id"], data=jsonpickle.encode(payload))
                result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)

        return result


class GatewayMehCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание механика')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        try:
            response = requests.post(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=flask.request.data)
        except:
            paybuy = {'name': 'Vasya', 'lvl': '1', 'year': '2001'}
            response = requests.post(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=jsonpickle.encode(paybuy))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 201:
            app.logger.info('Механик успешно создан')
        else:
            app.logger.warning('Механик не может быть создан')
        return result


class GatewayMehListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка механиков')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        page = args['page']
        page_size = args['page_size']
        app.logger.info('Номер страницы: %s; количество механиков на странице: %s' % (args['page'], args['page_size']))
        paybuy = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH, params=paybuy)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка механиков успешно обработан')
        else:
            app.logger.warning('Список механиков не может быть получен')
        return result


class GatewayUserResource(Resource):
    def get(self, user_id):
        app.logger.info('Получен запрос на получение информации о пользователе с идентификатором %s' % user_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о пользователе с идентификатором %s успешно обработан'
                            % user_id)
        else:
            app.logger.warning('Информация о пользователе с идентификатором %s не может быть получена' % user_id)
        return result
    def delete(self, user_id):
        app.logger.info('Получен запрос на удаление пользователя с идентификатором %s' % user_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        response = requests.delete(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 204:
            app.logger.info('Запрос на получение удаление пользователя с идентификатором %s успешно обработан'
                            % user_id)
        else:
            app.logger.warning('Удаление пользователя с идентификатором %s не получилось' % user_id)
        return result

class GatewayUserCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание пользователя')
        try:
            response = requests.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=flask.request.data)
        except:
            paybuy = {'l_name': 'test', 'password': 'test', 'admin': 'false'}
            response = requests.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=jsonpickle.encode(paybuy))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 201:
            app.logger.info('Механик успешно создан')
        else:
            app.logger.warning('Механик не может быть создан')
        return result
class GatewayUserTokenResource(Resource):
    def get(self):
        app.logger.info('Получен запрос на получение информации о пользователе ')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']
        app.logger.info('Запрос на получение информации о пользователе с идентификатором %s успешно обработан ')

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о пользователе с идентификатором %s успешно обработан')
        else:
            app.logger.warning('Информация о пользователе с идентификатором не может быть получена')
        return result
class GatewayUserListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка пользователей')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        try:
            args = self.parser.parse_args(strict=True)
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество пользователей на странице: %d'
                        % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        payload = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка пользователей успешно обработан')
        else:
            app.logger.warning('Список пользователей не может быть получен')
        return result


class GatewayAuthorization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("l_name", type=str)
    parser.add_argument("password", type=str)

    def get(self):
        app.logger.info('Получен запрос на аутентификацию')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        args = self.parser.parse_args(strict=True)
        login = args['l_name']
        password = args['password']
        payload = {'l_name': login, 'password': password}
        response = req.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           current_config.GET_TOKEN_URL_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        app.logger.info(response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на авторизацию успешно обработан')
        else:
            app.logger.warning('Авторизация не может быть произведена')
        return result


class GatewayApiAuthorization(Resource):
    def post(self):
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        payload = jsonpickle.decode(flask.request.data)
        client_id = payload['client_id']
        response = req.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH + "/auth/token",
                            data=jsonpickle.encode({'client_id': client_id}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def get(self):
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        payload = flask.request.data
        response = req.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH + "/token",
                            data=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на авторизацию успешно обработан')
        else:
            app.logger.warning('Авторизация не может быть произведена')
        return result


class GatewayFixCar(Resource):
    def post(self):
        app.logger.info('Получен запрос на починку автомобиля')
        paybuy = jsonpickle.decode(flask.request.data)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token': token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        user=User.from_json(response.content)

        paybuy1 = {'fix_id': str(paybuy["fix_id"]), 'user_id': user.id, 'name': str(paybuy["name"])}

        response = requests.post(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH +
                                     current_config.CREATE_PATH, jsonpickle.encode(paybuy1))
        car = Car.from_json(response.content)
        if response.status_code == 201:
            app.logger.info('Товар с идентификатором %s успешно создан' % str(car.id))
        else:
            app.logger.warning('Товар не может быть создан')
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)


        paybuy2 = {'car_id': str(car.id), 'status': 'fix'}

        response = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/%s"% paybuy["fix_id"], jsonpickle.encode(paybuy2))
        if response.status_code == 201:
            app.logger.error('Заявки в мастерскую %s  оформлена'
                             % paybuy["fix_id"])
        else:
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            app.logger.info('Магазин %s не существуета'
                            % (paybuy["fix_id"]))
            requests.delete(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH + "/" +
                            paybuy2['car_id'])
            return result

        paybuy3 = {'status': 'fix'}
        response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                  "/%s" % paybuy1["user_id"], jsonpickle.encode(paybuy3))
        if response.status_code == 201:
            app.logger.info('Услуга успешно заказана')
        else:
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            paybuy2['status'] = 'return'
            requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH + "/%s" % paybuy["fix_id"], jsonpickle.encode(paybuy1))
            requests.delete(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH + "/" +
                            paybuy2['car_id'])
            app.logger.warning('Услуга не может быть заказана')
        return result


class GatewayReturnCar(Resource):
  #  user_id = "5c5d83337162371f144dfeb0"

    def delete(self, car_id):
        app.logger.info('Получен запрос на возврат машины')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token': token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        response = requests.get(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH +
                                "/%s" % car_id)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о машине с идентификатором %s успешно обработан'
                            % car_id)
        else:
            app.logger.warning('Информация о машине с идентификатором %s не может быть получена' % car_id)
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        car = Car.from_json(response.content) #jsonpickle.decode(response.content)

        paybuy1 = {'car_id': car.id, 'status': 'return'}
        try:
            response = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH + "/%s" %
                                  car.fix_id, jsonpickle.encode(paybuy1))
            if response.status_code == 201:
                app.logger.info('Возврат автомобиля для пользователя %s успешно произведен' % car.user_id)
            else:
                app.logger.warning('Освобождение места на сеансе не может быть завершено, добавление запроса в очередь')
                replay_request_queue.send_message(
                    jsonpickle.encode(Request("CAR_RETURN", data={"fix_id": car.fix_id,
                                                                     "payload": paybuy1})),
                    "car_return_handling_request")
        except:
            app.logger.warning('Освобождение места на сеансе не может быть завершено, добавление запроса в очередь')
            replay_request_queue.send_message(
                jsonpickle.encode(Request("CAR_RETURN", data={"fix_id": car.fix_id,
                                                                 "payload": paybuy1})),
                "car_return_handling_request")
        finally:

            paybuy2 = {'status': 'return'}
            response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH + "/%s"
                                  % car.user_id, jsonpickle.encode(paybuy1))
            if response.status_code == 201:
                app.logger.info('Освобождение места в мастерской завершен')
            else:
                app.logger.warning('Освобождение места в мастерской не может быть завершено')
                result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
                paybuy1['status'] = 'fix'
                requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                           "/", jsonpickle.encode(paybuy2))
                return result

            response = requests.delete(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH +
                                   "/%s" % car_id)
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
            if response.status_code == 204:
                app.logger.info('Машина с идентификатором %s успешно удален' % car_id)
            else:
                paybuy2['status'] = 'fix'
                requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/%s" % car.user_id, jsonpickle.encode(paybuy2))
                paybuy1['status'] = 'fix'
                requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                           "/", jsonpickle.encode(paybuy1))
                app.logger.warning('Машина с идентификатором %s не может быть удален' % car_id)
            return result
