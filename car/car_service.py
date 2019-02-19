from car import app
from flask_restful import Api
from car.rest_api.car_resource import *
from car.repository.car_repository import Cars


api = Api(app)
service_namespace = "/cars"

api.add_resource(CarListResource, "/cars")
api.add_resource(CarResource, "/cars/<car_id>")
api.add_resource(CarCreateResource, "/cars/create")


if __name__ == '__main__':
    app.run(port=5003, debug=True)