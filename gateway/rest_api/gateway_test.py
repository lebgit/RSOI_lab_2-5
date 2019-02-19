import unittest
import jsonpickle
import requests
from config import current_config
from fix.domain.fix import Fix
from mechanic.domain.meh import Mechanic
from car.domain.car import Car


class TestGatewayCarResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.CAR_SERVICE_PATH
                           + "/5c409fa37162370450f2f5f8")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.CAR_SERVICE_PATH
                           + "/5bd8842")
        self.assertEqual(res.status_code, 404)


class TestGatewayCarListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.CAR_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.CAR_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayFixResource(unittest.TestCase):
    # def test_get_right(self):
    #     res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MAG_SERVICE_PATH
    #                        + "/5bfbb05b102bd23cdc85f75a")
    #     self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.CAR_SERVICE_PATH
                           + "/5bd0aa41af13")
        self.assertNotEqual(res.status_code, 200)


class TestGatewayFixCreateResource(unittest.TestCase):
    def test_post_right(self):
        payload = {'meh_id': '5c409e117162372684e0d0a9', 'date_time': '22.11.2018_10:15'}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.FIX_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        fix = Fix.from_json(res.content)
        requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.FIX_SERVICE_PATH +
                        "/%s" % str(fix.id))

    def test_post_error(self):
        payload = {'fix_id': '5c409e117162372684e0d0a9', 'datetime': '22.11.2018_10:15'}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.CAR_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestGatewayFixListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.FIX_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.FIX_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayMehResource(unittest.TestCase):
    def test_get_right(self):
         res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MECHANIC_SERVICE_PATH
                            + "/5c409e117162372684e0d0a9")
         self.assertEqual(res.status_code, 200)
    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MECHANIC_SERVICE_PATH
                           + "/5bd0a513")
        self.assertNotEqual(res.status_code, 200)

    def test_delete_right(self):
        payload = {'name': 'lol', 'lvl': '13', 'year': '1978'}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.MECHANIC_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        meh = Mechanic.from_json(res.content)
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              current_config.MECHANIC_SERVICE_PATH + "/%s" % str(meh.id))
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              current_config.MECHANIC_SERVICE_PATH + "/0")
        self.assertNotEqual(res.status_code, 204)


class TestGatewayMehCreateResource(unittest.TestCase):
    def test_post_right(self):
        payload = {'name': 'lol', 'lvl': '13', 'year': '1978'}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.MECHANIC_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        meh = Mechanic.from_json(res.content)
        requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MECHANIC_SERVICE_PATH +
                        "/%s" % str(meh.id))

    def test_post_error(self):
        payload = {'name': 'lol', 'lvl': '13', 'year': 1978}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.MECHANIC_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestGatewayMehListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.MECHANIC_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.MECHANIC_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayUserResource(unittest.TestCase):
    def test_get_right(self):
         res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.USER_SERVICE_PATH
                            + "/5c409dbd71623707b8b646ef")
         self.assertEqual(res.status_code, 200)

    def test_get_with_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.USER_SERVICE_PATH
                           + "/5bd0")
        self.assertNotEqual(res.status_code, 200)


class TestGatewayUserListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.USER_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.USER_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayBuyProd(unittest.TestCase):
    def test_post_right(self):
         payload = {'fix_id': '5c409fbe7162372270cf9460', 'name': 'tesla'}
         res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/cars/add',
                             data=jsonpickle.encode(payload))
         self.assertEqual(res.status_code, 201)
         car = Car.from_json(res.content)
         requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                         '/cars/return/%s' % str(car.id))

    def test_post_error(self):
        payload = {'mag_id': '5c409fbe7162', 'name': 'lolkekch'}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/cars/add',
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestGatewayReturnProd(unittest.TestCase):
    def test_delete_right(self):
        payload = {'fix_id': '5c409fbe7162372270cf9460', 'name': 'tesla'}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/cars/add',
                            data=jsonpickle.encode(payload))
        car = Car.from_json(res.content)
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                             '/cars/return/%s' % str(car.id))
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              '/return/5bd8a540af13')
        self.assertNotEqual(res.status_code, 204)


if __name__ == '__main__':
    unittest.main()
