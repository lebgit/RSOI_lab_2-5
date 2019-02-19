import unittest
import jsonpickle
import requests
from config import current_config
from gateway.rest_api.gateway_api import GatewayMehCreateResource, GatewayMehListResource, GatewayUserResource
from gateway.rest_api.gateway_api import GatewayReturnCar
from gateway.rest_api.gateway_api import GatewayFixCreateResource, GatewayFixListResource, GatewayMehResource
from gateway.rest_api.gateway_api import GatewayCarResource, GatewayCarListResource, GatewayFixResource, GatewayFixResourcePatch
from mechanic.rest_api.meh_resource import MechanicResource, MechanicCreateResource
from fix.rest_api.fix_resource import FixResource, FixCreateResource
from car.rest_api.car_resource import CarResource, CarCreateResource
from user.rest_api.user_resource import UserResource, UserCreateResource

from fix.domain.fix import Fix
from car.domain.car import Car
from user.domain.user import User
from mechanic.domain.meh import Mechanic

class TestGatewayCarResource(unittest.TestCase):
    def test_get_right(self):
        tr = CarResource()
        tcr = CarCreateResource()
        res = tcr.post()
        car = Car.from_json(res.data)
        gtr = GatewayCarResource()
        res = gtr.get(str(car.id))
        self.assertEqual(res.status_code, 200)
        tr.delete(str(car.id))

    def test_get_error(self):
        gtr = GatewayCarResource()
        try:
            res = gtr.get("5bd88423")
        except:
            self.assertTrue(True)


class TestGatewayCarListResource(unittest.TestCase):
    def test_get(self):
        sr = GatewayCarListResource()
        res = sr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayFixResource(unittest.TestCase):
     def test_get_right(self):
         sr = FixResource()
         scr = FixCreateResource()
         res = scr.post()
         fix = Fix.from_json(res.data)
         gsr = GatewayFixResource()
         res = gsr.get(str(fix.id))
         self.assertEqual(res.status_code, 200)
         sr.delete(str(fix.id))
     def test_get_error(self):
        gtr = GatewayFixResource()
        try:
            res = gtr.get("5bd88423")
        except:
            self.assertTrue(True)

     def test_patch_add_right(self):
         sr = FixResource()
         scr = FixCreateResource()
         res = scr.post()
         fix = Fix.from_json(res.data)
         mr = MechanicResource()
         mcr = MechanicCreateResource()
         resm = mcr.post()
         meh = Mechanic.from_json(resm.data)
         payload = {'meh_id': meh.id, 'status': 'mehadd'}
         res = requests.patch(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/fixes/add'+'/%s' % fix.id,
                             data= jsonpickle.encode(payload))
         self.assertEqual(res.status_code, 201)
         sr.delete(str(fix.id))
         mr.delete(str(meh.id))

     def test_patch_rem_right(self):
         sr = FixResource()
         scr = FixCreateResource()
         res = scr.post()
         fix = Fix.from_json(res.data)
         mr = MechanicResource()
         mcr = MechanicCreateResource()
         resm = mcr.post()
         meh = Mechanic.from_json(resm.data)
         payload = {'meh_id': meh.id, 'status': 'mehadd'}
         res = requests.patch(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/fixes/add' + '/%s' % fix.id,
                              data=jsonpickle.encode(payload))
         payload = {'meh_id': meh.id, 'status': 'mehrem'}
         res = requests.patch(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/fixes/add' + '/%s' % fix.id,
                              data=jsonpickle.encode(payload))
         self.assertEqual(res.status_code, 201)
         sr.delete(str(fix.id))
         mr.delete(str(meh.id))


class TestGatewayFixCreateResource(unittest.TestCase):
     def test_post(self):
         gsr = GatewayFixCreateResource()
         res = gsr.post()
         self.assertEqual(res.status_code, 201)
         sr = FixResource()
         mag = Fix.from_json(res.data)
         sr.delete(str(mag.id))


class TestGatewayFixListResource(unittest.TestCase):
    def test_get(self):
        gsr = GatewayFixListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayMehResource(unittest.TestCase):
    def test_get_right(self):
        mr = MechanicResource()
        mcr = MechanicCreateResource()
        res = mcr.post()
        meh = Mechanic.from_json(res.data)
        gmr = GatewayMehResource()
        res = gmr.get(str(meh.id))
        self.assertEqual(res.status_code, 200)
        mr.delete(str(meh.id))

    def test_get_error(self):
        gmr = GatewayMehResource()
        try:
            res = gmr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        gmr = GatewayMehResource()
        try:
            res = gmr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        gmr = GatewayMehCreateResource()
        res = gmr.post()
        meh = Mechanic.from_json(res.data)
        gmr1 = GatewayMehResource()
        res = gmr1.delete(str(meh.id))
        self.assertEqual(res.status_code, 204)


class TestGatewayMehCreateResource(unittest.TestCase):
    def test_post(self):
        gmr = GatewayMehCreateResource()
        res = gmr.post()
        self.assertEqual(res.status_code, 201)
        mr = MechanicResource()
        meh = Mechanic.from_json(res.data)
        mr.delete(str(meh.id))


class TestGatewayMehListResource(unittest.TestCase):
    def test_get(self):
        gsr = GatewayMehListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayUserResource(unittest.TestCase):
    def test_get_right(self):
        ur = UserResource()
        ucr = UserCreateResource()
        res = ucr.post()
        user = User.from_json(res.data)
        gur = GatewayUserResource()
        res = gur.get(str(user.id))
        self.assertEqual(res.status_code, 200)
        ur.delete(str(user.id))

    def test_get_error(self):
        gur = GatewayUserResource()
        try:
            res = gur.get("5bd0a351")
        except:
            self.assertTrue(True)


class TestGatewayUserListResource(unittest.TestCase):
    def test_get(self):
        gsr = GatewayMehListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayReturnCar(unittest.TestCase):
    def test_delete_right(self):
        sr = FixResource()
        ur = UserResource()
        scr = FixCreateResource()
        r = scr.post()
        fix = Fix.from_json(r.data)
        u = UserCreateResource()
        us = u.post()
        user = User.from_json(us.data)
        payload = {'fix_id': fix.id, 'name': 'suzuki','user_id':user.id}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/cars/add',
                            data=jsonpickle.encode(payload))
        #sr.delete(fix.id)
        car = Car.from_json(res.content)
        ret_prod = GatewayReturnCar()
        res = ret_prod.delete(car.id)
        self.assertEqual(res.status_code, 204)
        ur.delete(user.id)
        sr.delete(fix.id)



    def test_delete_error(self):
        ret_prod = GatewayReturnCar()
        res = ret_prod.delete("5bd897f8")
        self.assertNotEqual(res.status_code, 204)


if __name__ == '__main__':
    unittest.main()
