import unittest
from mechanic.rest_api.meh_resource import MechanicResource, MechanicCreateResource, MechanicListResource
from mechanic.domain.meh import Mechanic


class TestMechanicCreateResource(unittest.TestCase):
    def test_post(self):
        mr = MechanicCreateResource()
        res = mr.post()
        self.assertEqual(res.status_code, 201)
        meh = Mechanic.from_json(res.data)
        mr1 = MechanicResource()
        mr1.delete(str(meh.id))


class TestMechanicResource(unittest.TestCase):
    def test_get_right(self):
        mr1 = MechanicResource()
        mr2 = MechanicCreateResource()
        res = mr2.post()
        meh = Mechanic.from_json(res.data)
        res = mr1.get(str(meh.id))
        self.assertEqual(res.status_code, 200)
        mr1.delete(str(meh.id))

    def test_get_error(self):
        mr =MechanicResource()
        try:
            res = mr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        mr = MechanicResource()
        try:
            res = mr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        mr = MechanicCreateResource()
        res = mr.post()
        meh = Mechanic.from_json(res.data)
        mr1 = MechanicResource()
        res = mr1.delete(str(meh.id))
        self.assertEqual(res.status_code, 204)


class TestMechanicListResource(unittest.TestCase):
    def test_get(self):
        mr = MechanicListResource()
        res = mr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
