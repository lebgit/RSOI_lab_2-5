import unittest
from fix.repository.fix_repository import FixRepository
from fix.domain.fix import Fix
from flask_mongoalchemy import fields


class TestMagRepository(unittest.TestCase):
    def test_create(self):
        rep = FixRepository()
        id1 = rep.create('01.01.2018_12:00')
        id2 = rep.create('01.01.2018_12:00')
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)

    # def test_get_exists(self):
    #     rep = FixRepository()
    #     fix_id = rep.create('01.01.2018_12:00')
    #     fix1 = rep.get(fix_id)
    #     meh_ids=fix1.meh_ids
    #     car_ids=fix1.car_ids
    #     date_time=fix1.date_time
    #     fix2 = Fix(fix_id=fix1.id, meh_ids=str(meh_ids),
    #                       date_time=date_time, car_ids=str(car_ids))
    #     self.assertEqual(fix1, fix2)
    #     rep.delete(fix_id)

    def test_get_false(self):
        rep = FixRepository()
        mag = rep.get('5bd89b59af1')
        self.assertIsNone(mag)

    def test_read_paginated(self):
        rep = FixRepository()
        fixes = rep.read_paginated(1, 5)
        self.assertLessEqual(len(fixes), 5)

    def test_delete(self):
        rep = FixRepository()
        fix_id = rep.create('01.01.2018_12:00')
        rep.delete(fix_id)
        self.assertFalse(rep.exists(fix_id))

    def test_add_car_true(self):
        rep = FixRepository()
        fix_id = rep.create('01.01.2018_12:00')
        boolean = rep.add_car(fix_id, '1488322')
        self.assertTrue(boolean)
        rep.delete(fix_id)


    def test_add_car_false(self):
        rep = FixRepository()
        boolean = rep.add_car('5bd897f8af', '14488322')
        self.assertFalse(boolean)

    def test_rem_car_true(self):
        rep = FixRepository()
        fix_id = rep.create('01.01.2018_12:00')
        rep.add_car(fix_id, '1432288')
        boolean = rep.rem_car(fix_id, '1432288')
        self.assertTrue(boolean)
        rep.delete(fix_id)

    def test_rem_car_false(self):
        rep = FixRepository()
        boolean = rep.rem_car('888888888', '1488322')
        self.assertFalse(boolean)
        #rep.delete(fix_id)


    def test_add_meh_true(self):
        rep = FixRepository()
        fix_id = rep.create('01.01.2018_12:00')
        boolean = rep.add_meh(fix_id, '1488322')
        self.assertTrue(boolean)
        rep.delete(fix_id)


    def test_add_meh_false(self):
        rep = FixRepository()
        boolean = rep.add_meh('5bd897f8af', '14488322')
        self.assertFalse(boolean)

    def test_rem_meh_true(self):
        rep = FixRepository()
        fix_id = rep.create('01.01.2018_12:00')
        rep.add_meh(fix_id, '1432288')
        boolean = rep.rem_meh(fix_id, '1432288')
        self.assertTrue(boolean)
        rep.delete(fix_id)

    def test_rem_meh_false(self):
        rep = FixRepository()
        boolean = rep.rem_meh('888888888', '1488322')
        self.assertFalse(boolean)
        #rep.delete(fix_id)

    def test_exists(self):
        rep = FixRepository()
        fix_id = rep.create('01.01.2018_12:00')
        boolean = rep.exists(fix_id)
        self.assertTrue(boolean)
        rep.delete(fix_id)


if __name__ == '__main__':
    unittest.main()
