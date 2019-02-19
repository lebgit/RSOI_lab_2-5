from car import app
from flask_restful import Resource, abort, reqparse
from car.repository.car_repository import CarRepository
import jsonpickle
import flask
import json

repo = CarRepository()


def car_doesnt_exist(car_id):
    if not repo.exists(car_id):
        app.logger.error('Машины с id %s не существует!', car_id)
        abort(404, message="Car {} doesn't exist".format(car_id))


class CarResource(Resource):
    def get(self, car_id):
        app.logger.info('Получен запрос на получение информации о машине с id %s' % car_id)
        car_doesnt_exist(car_id)
        car = repo.get(car_id)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = car.to_json()
        app.logger.info('Запрос на получение информации о машине с id %s успешно обработан'
                        % car_id)
        return response

    def delete(self, car_id):
        app.logger.info('Получен запрос на удаление машины с id %s' % car_id)
        car_doesnt_exist(car_id)
        repo.delete(car_id)
        response = app.make_response("Car %s deleted successfully" % car_id)
        response.status_code = 204
        app.logger.info('Машина с id %s успешно удалена' % car_id)
        return response


class CarCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на починку машины')
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {"fix_id": "3221488228", "user_id": "5c4088187162371830b13a0d", "name": 'suzuki'}
        car_id = repo.create(payload["fix_id"],payload["user_id"], payload["name"])
        car = repo.get(car_id)
        response = app.make_response("")
        response.content_type = "application/json"
        response.status_code = 201
        response.data = car.to_json()
        app.logger.info('Запрос на починку машины с id %s успешно создан ' % car_id)
        return response


class CarListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        repo = CarRepository()
        app.logger.info('Получен запрос на получение списка машин')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество машин на странице: %d' % (args['page'], args['page_size']))
        car_list, is_prev_page, is_next_page = repo.read_paginated(page_number=args['page'], page_size=args['page_size'])
        cars = ''
        for car in car_list:
            cars += car.to_json() + '\n'
        dictr = {"is_prev_page": is_prev_page, "is_next_page": is_next_page}
        cars += "\n" + json.dumps(dictr)
        response = app.make_response("")
        response.content_type = "application/json"
        response.status_code = 200
        response.data = cars
        app.logger.info('Запрос на получение списка билетов успешно обработан')
        return response