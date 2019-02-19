import unittest
import jsonpickle
import requests
from config import current_config
from mechanic.domain.meh import Mechanic


class TestMechanicCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'name': 'test', 'lvl': 'test', 'year': '30'}
        res = requests.post(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        meh = Mechanic.from_json(res.content)
        requests.delete(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH + "/%s" % str(meh.id))


class TestMechanicResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                           "/5c409e117162372684e0d0a9")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                           "/5bd0a513af")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        payload = {'name': 'test', 'lvl': 'test', 'year': '30'}
        res = requests.post(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        meh = Mechanic.from_json(res.content)
        res = requests.delete(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                              "/%s" % str(meh.id))
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        res = requests.delete(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH +
                              "/5bd8ad1daf13c7")
        self.assertEqual(res.status_code, 404)


class TestMechanicListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.MECHANIC_SERVICE_URL + current_config.MECHANIC_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
