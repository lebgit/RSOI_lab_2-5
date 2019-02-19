import unittest
from mechanic.repository.meh_repository import MehRepository
from mechanic.domain.meh import Mechanic
from flask_mongoalchemy import fields


class TestMehRepository(unittest.TestCase):
    def test_create(self):
        rep = MehRepository()
        id1 = rep.create('a', 'a', '10')
        id2 = rep.create('a', 'a', '10')
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)

    def test_get_right(self):
        rep = MehRepository()
        meh_id = rep.create('a', 'a', '100')
        meh1 = rep.get(meh_id)
        meh2 = Mechanic(meh_id=fields.ObjectId(meh_id), name='a', lvl='a', year='100')
        self.assertEqual(meh1, meh2)
        rep.delete(meh_id)

    def test_get_none(self):
        rep = MehRepository()
        meh = rep.get('5bd8ad')
        self.assertIsNone(meh)

    def test_exists_true(self):
        rep = MehRepository()
        meh_id = rep.create('a', 'a', '100')
        boolean = rep.exists(meh_id)
        self.assertTrue(boolean)
        rep.delete(meh_id)

    def test_exists_false(self):
        rep = MehRepository()
        boolean = rep.exists('5bd8ad1daf')
        self.assertFalse(boolean)

    def test_read_paginated(self):
        rep = MehRepository()
        mehs = rep.read_paginated(1, 5)
        self.assertLessEqual(len(mehs), 5)

    def test_delete_existed(self):
        rep = MehRepository()
        id1 = rep.create('a', 'a', '10')
        rep.delete(id1)
        self.assertFalse(rep.exists(id1))


if __name__ == '__main__':
    unittest.main()
