from flask_mongoalchemy import MongoAlchemy
from car import app
from car.domain.car import Car


db = MongoAlchemy(app)


class Cars(db.Document):
    fix_id = db.StringField()
    user_id = db.StringField()
    name = db.StringField()


class CarRepository:
    def create(self, fix_id, user_id, name):
        car = Cars(fix_id=fix_id, user_id=user_id, name=name)
        car.save()
        return car.mongo_id

    def get(self, car_id):
        if self.exists(car_id):
            car = Cars.query.get(car_id)
            return Car(car_id=car.mongo_id, fix_id=car.fix_id, user_id=car.user_id, name=car.name)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        cars = []
        cars_paged = Cars.query.paginate(page=page_number, per_page=page_size)
        for car in cars_paged.items:
            cars.append(Car(car_id=car.mongo_id, fix_id=car.fix_id, user_id=car.user_id, name=car.name))
        is_prev_num = (cars_paged.prev_num > 0)
        is_next_num = (cars_paged.next_num <= cars_paged.pages)
        return cars, is_prev_num, is_next_num
        return cars

    def delete(self, car_id):
        if self.exists(car_id):
            car = Cars.query.get(car_id)
            car.remove()

    def exists(self, car_id):
        result = Cars.query.get(car_id)
        return result is not None
