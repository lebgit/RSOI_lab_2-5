import unittest
import jsonpickle
import requests
from config import current_config
from fix.domain.fix import Fix


class TestMagCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'date_time': '10.10.2010'}
        res = requests.post(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        fix = Fix.from_json(res.content)
        requests.delete(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH + "/%s" % str(fix.id))


class TestMagResource(unittest.TestCase):
    def test_get_right(self):
        payload = {'date_time': '10.10.2010'}
        res = requests.post(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        fix = Fix.from_json(res.content)
        res = requests.get(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                           "/%s" % str(fix.id))
        self.assertEqual(res.status_code, 200)
        requests.delete(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH + "/%s" % str(fix.id))

    def test_get_false(self):
        res = requests.get(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                           "/5bd897f8af")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        payload = {'date_time': '10.10.2010'}
        res = requests.post(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        fix = Fix.from_json(res.content)
        res = requests.delete(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                              "/%s" % str(fix.id))
        self.assertEqual(res.status_code, 204)

    def test_patch_buy_right(self):
        payload = {'date_time': '10.10.2010'}
        res = requests.post(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        fix = Fix.from_json(res.content)
        payload = {'car_id': '14832288', 'status': 'fix'}
        res = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/%s" % fix.id, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        payload['status'] = 'return'
        requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                       "/%s" % fix.id, data=jsonpickle.encode(payload))
        requests.delete(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH + "/%s" % str(fix.id))
    def test_patch_buy_error(self):

        payload = {'car_id': '14832288', 'status': 'return'}
        res = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/148888888", data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)

    def test_patch_return_right(self):
        payload = {'date_time': '10.10.2010'}
        res = requests.post(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        fix = Fix.from_json(res.content)
        payload = {'car_id': '14832288', 'status': 'fix'}
        requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/%s" % fix.id, data=jsonpickle.encode(payload))
        payload['status'] = 'return'
        res = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/%s" % fix.id, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        requests.delete(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH + "/%s" % str(fix.id))



    def test_patch_return_error(self):
        payload = {'car_id': '14832288', 'status': 'return'}
        res = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/148888888", data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)

    def test_patch_addmeh_right(self):
        payload = {'date_time': '10.10.2010'}
        res = requests.post(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        fix = Fix.from_json(res.content)
        payload = {'meh_id': '14832288', 'status': 'mehadd'}
        res = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/%s" % fix.id, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        payload['status'] = 'mehrem'
        requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                       "/%s" % fix.id, data=jsonpickle.encode(payload))
        requests.delete(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH + "/%s" % str(fix.id))

    def test_patch_addmeh_error(self):
        payload = {'meh_id': '14832288', 'status': 'mehadd'}
        res = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/148888888", data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)

    def test_patch_remmeh_right(self):
        payload = {'date_time': '10.10.2010'}
        res = requests.post(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        fix = Fix.from_json(res.content)
        payload = {'meh_id': '14832288', 'status': 'mehadd'}
        requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                       "/%s" % fix.id, data=jsonpickle.encode(payload))
        payload['status'] = 'mehrem'
        res = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/%s" % fix.id, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        requests.delete(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH + "/%s" % str(fix.id))

    def test_patch_remmeh_error(self):
        payload = {'meh_id': '14832288', 'status': 'mehrem'}
        res = requests.patch(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH +
                             "/148888888", data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestMagListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.FIX_SERVICE_URL + current_config.FIX_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
