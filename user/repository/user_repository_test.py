import unittest
from user.repository.user_repository import UserRep
from user.domain.user import User
from flask_mongoalchemy import fields


class TestUserRepository(unittest.TestCase):
    def test_create(self):
        rep = UserRep()
        id1 = rep.create('l_name', 'admin')
        id2 = rep.create('l_name', 'admin')
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)


    def test_get_error(self):
        rep = UserRep()
        user = rep.get('1234')
        self.assertIsNone(user)



    def test_delete_existed(self):
        rep = UserRep()

        id1 = rep.create('l_name', 'admin')
        rep.delete(id1)
        self.assertFalse(rep.exists(id1))

    def test_assign_ticket_true(self):
        rep = UserRep()
        user_id = rep.create('l_name', 'admin')
        boolean = rep.assign_car(user_id)
        self.assertTrue(boolean)
        rep.delete(user_id)

    def test_assign_ticket_false(self):
        rep = UserRep()
        boolean = rep.assign_car('123')
        self.assertFalse(boolean)

    def test_remove_ticket_true(self):
        rep = UserRep()
        user_id = rep.create( 'l_name', 'admin' )
        rep.assign_car(user_id)
        boolean = rep.remove_car(user_id)
        self.assertTrue(boolean)
        rep.delete(user_id)

    def test_remove_ticket_false(self):
        rep = UserRep()
        boolean = rep.remove_car('5bd0a397')
        self.assertFalse(boolean)

    def test_exists_true(self):
        rep = UserRep()
        user_id = rep.create('l_name', 'admin', )
        boolean = rep.exists(user_id)
        self.assertTrue(boolean)
        rep.delete(user_id)

    def test_exists_false(self):
        rep = UserRep()
        boolean = rep.exists('5bd8ad1daf')
        self.assertFalse(boolean)

    def test_read_paginated(self):
        rep = UserRep()
        users = rep.read_paginated(1, 5)
        self.assertLessEqual(len(users), 5)


if __name__ == '__main__':
    unittest.main()
