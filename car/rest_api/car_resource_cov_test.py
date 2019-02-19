import unittest
from car.rest_api.car_resource import CarCreateResource, CarListResource, CarResource
from car.domain.car import Car


class TestCarCreateResource(unittest.TestCase):
    def test_post(self):
        tr = CarCreateResource()
        res = tr.post()
        self.assertEqual(res.status_code, 201)
        tr1 = CarResource()
        fix = Car.from_json(res.data)
        tr1.delete(str(fix.id))


class TestCarResource(unittest.TestCase):
    def test_get_right(self):
        tr = CarResource()
        tcr = CarCreateResource()
        res = tcr.post()
        car = Car.from_json(res.data)
        res = tr.get(str(car.id))
        self.assertEqual(res.status_code, 200)
        tr.delete(str(car.id))

    def test_get_error(self):
        tr = CarResource()
        try:
            res = tr.get("qwerty")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        tr = CarResource()
        try:
            res = tr.delete("qwerty")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        tr = CarCreateResource()
        res = tr.post()
        tr1 = CarResource()
        fix = Car.from_json(res.data)
        res = tr1.delete(str(fix.id))
        self.assertEqual(res.status_code, 204)


class TestCarListResource(unittest.TestCase):
    def test_get(self):
        tr = CarListResource()
        res = tr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
