from fix import app
from flask_restful import Resource, abort, reqparse
from fix.repository.fix_repository import FixRepository
import jsonpickle
import flask
import json

repo = FixRepository()


def abort_if_fix_doesnt_exist(fix_id):
    if not repo.exists(fix_id):
        app.logger.error('Мастерская с идентификатором %s не существует!', fix_id)
        abort(404, message="Fix {} doesn't exist".format(fix_id))


class FixResource(Resource):
    def get(self, fix_id):
        app.logger.info('Получен запрос на получение информации о мастерской с идентификатором %s' % fix_id)
        abort_if_fix_doesnt_exist(fix_id)
        fix = repo.get(fix_id)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = fix.to_json() #jsonpickle.encode(mag)
        app.logger.info('Запрос на получение информации о мастерской с идентификатором %s успешно обработан' % fix_id)
        return response

    def delete(self, fix_id):
        app.logger.info('Получен запрос на удаление мастерской с идентификатором %s' % fix_id)
        abort_if_fix_doesnt_exist(fix_id)
        repo.delete(fix_id)
        response = app.make_response("Fix %s deleted successfully" % fix_id)
        response.status_code = 204
        app.logger.info('Мастерская с идентификатором %s успешно удален' % fix_id)
        return response

    def patch(self, fix_id):
        app.logger.info('Получен запрос на заказ починки/возврат авто хозяину с идентификатором %s' % fix_id)
        abort_if_fix_doesnt_exist(fix_id)
        paybuy = jsonpickle.decode(flask.request.data)
        if paybuy["status"] == "fix":
            app.logger.info('Принятие заказа')
            res = repo.add_car(fix_id, paybuy["car_id"])
            if res:
                response = app.make_response("")
                response.content_type = "application/json"
                response.status_code = 201
                app.logger.info('Заявка %s успешно принята' % fix_id)
            else:
                response = app.make_response("Fix don't exist!")
                response.content_type = "application/json"
                response.status_code = 404
                app.logger.warning('Мастерской %s не существует, заказ не принят'
                                   % fix_id)
        if paybuy["status"] == "return":
            app.logger.info('Возврат машины')
            res = repo.rem_car(fix_id, paybuy["car_id"])
            if res:
                response = app.make_response("")
                response.content_type = "application/json"
                response.status_code = 201
                app.logger.info('Возврат машины хозяину %s успешно совершон' % fix_id)
            else:
                response = app.make_response("Fix don't exist!")
                response.content_type = "application/json"
                response.status_code = 404
                app.logger.warning('Возврат машины хозяину %s не может быть завершен'
                                   % fix_id)
        if paybuy["status"] == "mehadd":
            app.logger.info('Устройство механика')
            res = repo.add_meh(fix_id, paybuy["meh_id"])
            if res:
                response = app.make_response("")
                response.content_type = "application/json"
                response.status_code = 201
                app.logger.info('Устройство механика в %s успешно принята' % fix_id)
            else:
                response = app.make_response("Fix don't exist!")
                response.content_type = "application/json"
                response.status_code = 404
                app.logger.warning('Мастерской %s не существует, неудача'
                                   % fix_id)
        if paybuy["status"] == "mehrem":
            app.logger.info('Увольнение механика')
            res = repo.rem_meh(fix_id, paybuy["meh_id"])
            if res:
                response = app.make_response("")
                response.content_type = "application/json"
                response.status_code = 201
                app.logger.info('Увольнение механика в %s успешно совершено' % fix_id)
            else:
                response = app.make_response("Fix don't exist!")
                response.content_type = "application/json"
                response.status_code = 404
                app.logger.warning('Увольнение в %s не может быть завершен'
                                   % fix_id)

        fix = repo.get(fix_id)
        response.data = fix.to_json()  #jsonpickle.encode(mag)
        return response


class FixCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание мастерской')
        try:
            paybuy = jsonpickle.decode(flask.request.data)
        except:
            paybuy = {'date_time': '12.11.2018_20:00'}
        fix_id = repo.create( paybuy['date_time'])
        fix = repo.get(fix_id)
        response = app.make_response("")
        response.status_code = 201
        response.content_type = "application/json"
        response.data = fix.to_json()  #jsonpickle.encode(mag)
        app.logger.info('Мастерская с идентификатором %s успешно создан' % fix_id)
        return response



class FixListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        repo = FixRepository()
        app.logger.info('Получен запрос на получение списка сеансов')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество сеансов на странице: %d' % (args['page'], args['page_size']))
        fixes_list, is_prev_page, is_next_page = repo.read_paginated(page_number=args['page'],
                                                                       page_size=args['page_size'])
        fixes = ''
        for fix in fixes_list:
            fixes += fix.to_json() + '\n'
        dictr = {"is_prev_page": is_prev_page, "is_next_page": is_next_page}
        fixes += "\n" + json.dumps(dictr)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = fixes
        app.logger.info('Запрос на получение списка сеансов успешно обработан')
        return response