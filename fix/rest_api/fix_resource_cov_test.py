import unittest
from fix.rest_api.fix_resource import FixResource, FixListResource, FixCreateResource
from fix.domain.fix import Fix


class TestFixCreateResource(unittest.TestCase):
    def test_post(self):
        sr = FixCreateResource()
        res = sr.post()
        self.assertEqual(res.status_code, 201)
        sr1 = FixResource()
        fix = Fix.from_json(res.data)
        sr1.delete(str(fix.id))


class TestFixResource(unittest.TestCase):
    def test_get_right(self):
        scr = FixCreateResource()
        sr = FixResource()
        res = scr.post()
        fix = Fix.from_json(res.data)
        res = sr.get(str(fix.id))
        self.assertEqual(res.status_code, 200)
        sr.delete(str(fix.id))

    def test_get_error(self):
        sr = FixResource()
        try:
            res = sr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        sr = FixResource()
        try:
            res = sr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        sr = FixCreateResource()
        res = sr.post()
        sr1 = FixResource()
        fix = Fix.from_json(res.data)
        res = sr1.delete(str(fix.id))
        self.assertEqual(res.status_code, 204)
    # def test_patch_right(self):
    #     sr = FixCreateResource()
    #     res = sr.post()
    #     sr1 = FixResource()
    #     fix = Fix.from_json(res.data)
    #     res = sr1.patch(fix.id)



class TestMagListResource(unittest.TestCase):
    def test_get(self):
        sr = FixListResource()
        res = sr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
