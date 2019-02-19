import unittest
from car.repository.car_repository import CarRepository
from car.domain.car import Car
from flask_mongoalchemy import fields


class TestProdRepository(unittest.TestCase):
    def test_create(self):
        rep = CarRepository()
        id1 = rep.create('1488322', '3212313', 'opel')
        id2 = rep.create('1488322', '3212313', 'opel')
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)

    def test_get_right(self):
        rep = CarRepository()
        car_id = rep.create(fix_id='1488322', user_id='3212313', name='opel')
        car1 = rep.get(car_id)
        car2 = Car(car_id=fields.ObjectId(car_id), fix_id='1488322', user_id='3212313', name='opel')
        self.assertEqual(car1, car2)
        rep.delete(car_id)

    def test_get_error(self):
        rep = CarRepository()
        car = rep.get('1488322')
        self.assertIsNone(car)

    def test_read_paginated(self):
        rep = CarRepository()
        cars = rep.read_paginated(1, 5)
        self.assertLessEqual(len(cars), 5)

    def test_delete_existed(self):
        rep = CarRepository()
        id1 = rep.create('1488322228', '3212313', 'mazda')
        rep.delete(id1)
        self.assertFalse(rep.exists(id1))

    def test_exists_true(self):
        rep = CarRepository()
        car_id = rep.create(fix_id='1488322228', user_id='3212313', name='mazda')
        boolean = rep.exists(car_id)
        self.assertTrue(boolean)
        rep.delete(car_id)

    def test_exists_false(self):
        rep = CarRepository()
        boolean = rep.exists('1234qwerty')
        self.assertFalse(boolean)


if __name__ == '__main__':
    unittest.main()
