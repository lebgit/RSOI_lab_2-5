from mechanic import app
from flask_restful import Resource, abort, reqparse
from mechanic.repository.meh_repository import MehRepository
import jsonpickle
import flask
import json

repo = MehRepository()


def abort_if_meh_doesnt_exist(meh_id):
    if not repo.exists(meh_id):
        app.logger.error('Механика с идентификатором %s не существует!', meh_id)
        abort(404, message="Mechanic {} doesn't exist".format(meh_id))


class MechanicResource(Resource):
    def get(self, meh_id):
        app.logger.info('Получен запрос на получение информации о Механике с идентификатором %s' % meh_id)
        abort_if_meh_doesnt_exist(meh_id)
        meh = repo.get(meh_id)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = meh.to_json()
        app.logger.info('Запрос на получение информации о Механике с идентификатором %s успешно обработан' % meh_id)
        return response

    def delete(self, meh_id):
        app.logger.info('Получен запрос на увольнение Механика с идентификатором %s' % meh_id)
        abort_if_meh_doesnt_exist(meh_id)
        repo.delete(meh_id)
        response = app.make_response("Mechanic %s deleted successfully" % meh_id)
        response.status_code = 204
        app.logger.info('Механик с идентификатором %s успешно уволен' % meh_id)
        return response


class MechanicCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание Механика')
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {'name': 'vasya', 'lvl': '15', 'year': '60'}
        meh_id = repo.create(payload["name"], payload["lvl"], payload["year"])
        meh = repo.get(meh_id)
        response = app.make_response("")
        response.status_code = 201
        response.content_type = "application/json"
        response.data = meh.to_json() #jsonpickle.encode(meh)
        app.logger.info('Механик с идентификатором %s успешно создан' % meh_id)
        return response


class MechanicListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        repo = MehRepository()
        app.logger.info('Получен запрос на получение списка фильмов')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество фильмов на странице: %d' % (args['page'], args['page_size']))
        mehs_list, is_prev_page, is_next_page = repo.read_paginated(page_number=args['page'],
                                                                      page_size=args['page_size'])
        mehs = ''
        for movie in mehs_list:
            mehs += "\n" + movie.to_json()
        dictr = {"is_prev_page": is_prev_page, "is_next_page": is_next_page}
        mehs += "\n" + json.dumps(dictr)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = mehs
        app.logger.info('Запрос на получение списка фильмов успешно обработан')
        return response