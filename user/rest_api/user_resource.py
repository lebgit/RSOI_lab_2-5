from user import app
from flask_restful import Resource, abort, reqparse
from user.repository.user_repository import UserRep
import jsonpickle
import flask
import json


repo = UserRep()


def abort_if_user_doesnt_exist(user_id):
    if not repo.exists(user_id):
        app.logger.error('Пользователя с идентификатором %s не существует!', user_id)
        abort(404, message="User {} doesn't exist".format(user_id))


class UserResource(Resource):
    def get(self, user_id):
        repo = UserRep()
        app.logger.info('Получен запрос на получение информации о пользователе с идентификатором %s' % user_id)
        abort_if_user_doesnt_exist(user_id)
        user = repo.get(user_id)
        response = app.make_response("")
        response.status_code = 200
        response.data = user.to_json()
        response.content_type = "application/json"
        app.logger.info('Запрос на получение информации о пользователе с идентификатором %s успешно обработан'
                        % user_id)
        return response
    def delete(self, user_id):
        app.logger.info('Получен запрос на удаление пользователя с идентификатором %s' % user_id)
        abort_if_user_doesnt_exist(user_id)
        repo.delete(user_id)
        response = app.make_response("User %s deleted successfully" % user_id)
        response.status_code = 204
        app.logger.info('Пользователь с идентификатором %s успешно удален' % user_id)
        return response

    def patch(self, user_id):
        app.logger.info('Получен запрос на покупку/возврат товара для пользователя с идентификатором %s' % user_id)
        abort_if_user_doesnt_exist(user_id)
        payload = jsonpickle.decode(flask.request.data)
        if payload["status"] == "fix":
            app.logger.info('Заявка на починку машины')
            repo.assign_car(user_id)
        else:
            app.logger.info('Возврат машины ')
            repo.remove_car(user_id)
        user = repo.get(user_id)
        response = app.make_response("")
        response.status_code = 201
        response.data = user.to_json()
        response.content_type = "application/json"
        if payload["status"] == "fix":
            app.logger.info('Заявка на починку машины для пользователя %s успешно произведена'% user_id)
        else:
            app.logger.info('Возврат машины  для пользователя %s успешно произведен'% user_id)
        return response


class UserCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание пользователя')
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {'l_name': 'test','password':'test', 'admin': 'test'}
        user_id = repo.create( payload["l_name"], payload["password"],payload["admin"])
        user = repo.get(user_id)
        response = app.make_response("")
        response.status_code = 201
        response.data = user.to_json()
        response.content_type = "application/json"
        app.logger.info('Запрос на создание нового пользователя успешно обработан, идентификатор: %s' % user_id)
        return response

class UserTokenResource(Resource):
    def get(self):
        repo = UserRep()
        app.logger.info('Получен запрос на получение пользователя по токену')
        payload = jsonpickle.decode(flask.request.data)
        token = payload['token']
        user = repo.get_real_user_by_token(token)
        if user is not None:
            response = app.make_response("Пользователь получен по токену")
            response.status_code = 200
            response.data = user.to_json()
            response.content_type = "application/json"
            return response
        response = app.make_response("Ошибка получения пользователя по токену")
        response.status_code = 403
        return response

    def post(self):
        repo = UserRep()
        app.logger.info('Получен запрос на получение пользователя по токену')
        payload = jsonpickle.decode(flask.request.data)
        app.logger.info(payload)
        client_id = payload['client_id']
        client_secret = payload['client_secret']

        code = payload['code']
        t = repo.get_token_for_auth(client_id, client_secret, code)

        if t is not None:
            response = app.make_response("Token was generated")
            response.status_code = 200
            app.logger.info(t)
            response.set_cookie("token", value=t)
            return response
        response = app.make_response("Неверные данные")
        response.status_code = 403
        return response


class UserAuthorizationResource(Resource):
    def post(self):
        repo = UserRep()
        payload = jsonpickle.decode(flask.request.data)
        client_id = payload['client_id']
        code = repo.get_code(client_id)
        if code is not None:
            response = app.make_response("Authorization code was generated")
            response.status_code = 201
            response.data = json.dumps({"code": code})
            response.content_type = "application/json"
            return response
        response = app.make_response("Ошибка генеации кода")
        response.status_code = 404
        return response

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("l_name", type=str)
        parser.add_argument("password", type=str)
        repo = UserRep()
        app.logger.info('Получен запрос на аутентификацию')
        args = parser.parse_args(strict=True)
        #payload = jsonpickle.decode(flask.request.data)
        token = repo.get_token(args['l_name'], args['password'])
        if token is not None:
            user = repo.get_by_token(token)
            if user is not None:
                response = app.make_response("Token was generated")
                app.logger.info(token)
                response.status_code = 200
                response.set_cookie("token", value=token)
                return response
        response = app.make_response("Неверный логин или пароль")
        response.status_code = 403
        return response


class UserListRes(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        repo = UserRep()
        app.logger.info('Получен запрос на получение списка пользователей')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество пользователей на странице: %d' % (args['page'], args['page_size']))
        users_list, is_prev_page, is_next_page = repo.read_paginated(page_number=args['page'], page_size=args['page_size'])
        users = ''
        for user in users_list:
            users += user.to_json() + '\n'
        dictr = {"is_prev_page": is_prev_page, "is_next_page": is_next_page}
        users += "\n" + json.dumps(dictr)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = users
        app.logger.info('Запрос на получение списка пользователей успешно обработан')
        return response


