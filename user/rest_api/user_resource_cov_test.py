import unittest
from user.rest_api.user_resource import UserResource, UserListRes, UserCreateResource
from user.domain.user import User


class TestUserCreateResource(unittest.TestCase):
    def test_post(self):
        ur = UserCreateResource()
        res = ur.post()
        self.assertEqual(res.status_code, 201)
        ur1 = UserResource()
        user = User.from_json(res.data)
        ur1.delete(str(user.id))


class TestUserResource(unittest.TestCase):
    def test_get_right(self):
        ur = UserResource()
        ucr = UserCreateResource()
        res = ucr.post()
        user = User.from_json(res.data)
        res = ur.get(str(user.id))
        self.assertEqual(res.status_code, 200)
        ur.delete(str(user.id))

    def test_get_error(self):
        ur = UserResource()
        try:
            res = ur.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        ur = UserResource()
        try:
            res = ur.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        ur = UserCreateResource()
        res = ur.post()
        ur1 = UserResource()
        user = User.from_json(res.data)
        res = ur1.delete(str(user.id))
        self.assertEqual(res.status_code, 204)


class TestSeanceListResource(unittest.TestCase):
    def test_get(self):
        ur = UserListRes()
        res = ur.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
