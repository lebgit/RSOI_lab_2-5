import unittest
import jsonpickle
import requests
from config import current_config
from user.domain.user import User


class TestUserCreateResource(unittest.TestCase):
    def test_post(self):
        paybuy = {'l_name': 'test', 'p_name': 'test'}
        res = requests.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(paybuy))
        self.assertEqual(res.status_code, 201)
        user = User.from_json(res.content)
        requests.delete(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH + "/%s" % str(user.id))


class TestUserResource(unittest.TestCase):
    def test_get_right(self):
         res = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +"/5c409dbd71623707b8b646ef")
         self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +"/5bd0a351")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        paybuy = { 'l_name': 'test', 'p_name': 'test'}
        res = requests.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(paybuy))
        user = User.from_json(res.content)
        res = requests.delete(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                              "/%s" % str(user.id))
        self.assertEqual(res.status_code, 204)

    # def test_patch_buy(self):
    #     paybuy = {'prod_id': '5bd8a49aaf13c7ea848cb9e2', 'status': 'buy'}
    #     res = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
    #                          "/5bd967f5af13c767ca5524bb", data=jsonpickle.encode(paybuy))
    #     self.assertEqual(res.status_code, 201)
    #     paybuy['status'] = 'return'
    #     requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
    #                    "/5bd967f5af13c767ca5524bb", data=jsonpickle.encode(paybuy))

    # def test_patch_return(self):
    #     paybuy = {'prod_id': '5bd8a49aaf13c7ea848cb9e2', 'status': 'buy'}
    #     requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
    #                    "/5bd967f5af13c767ca5524bb", data=jsonpickle.encode(paybuy))
    #     paybuy['status'] = 'return'
    #     res = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
    #                          "/5bd967f5af13c767ca5524bb", data=jsonpickle.encode(paybuy))
    #     self.assertEqual(res.status_code, 201)


class TestSeanceListResource(unittest.TestCase):
    def test_get(self):
        paybuy = (('page', 1), ('page_size', 7))
        res = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH, params=paybuy)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
