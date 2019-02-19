import unittest
import jsonpickle
import requests
from config import current_config
from car.domain.car import Car


class TestProdCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'fix_id': '3221488228','user_id': '123456', 'name': 'suzuki'}
        res = requests.post(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        car = Car.from_json(res.content)
        requests.delete(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH +
                        "/%s" % str(car.id))


class TestProdResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH +
                           "/5c409fa37162370450f2f5f8")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH +
                           "/dich")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        payload = {'fix_id': '123', 'user_id': '321', 'name': 'opel'}
        res = requests.post(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        car = Car.from_json(res.content)
        res = requests.delete(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH +
                              "/%s" % car.id)
        self.assertEqual(res.status_code, 204)


class TestProdListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.CAR_SERVICE_URL + current_config.CAR_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
