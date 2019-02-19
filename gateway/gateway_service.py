from mechanic import app
from flask_restful import Api
from gateway.rest_api.gateway_api import *
from gateway.queues.car_return_handling import CarReturnHandling
api = Api(app)

api.add_resource(GatewayFixCar, "/gateway/api/cars/add")
api.add_resource(GatewayReturnCar, "/gateway/api/cars/ret" + "/<car_id>")
api.add_resource(GatewayCarResource, "/gateway/api/cars" + "/<car_id>")
api.add_resource(GatewayCarListResource, "/gateway/api/cars")
api.add_resource(GatewayFixResource, "/gateway/api/fixes" + "/<fix_id>")
api.add_resource(GatewayFixListResource, "/gateway/api/fixes")
api.add_resource(GatewayFixCreateResource, "/gateway/api/fixes/create")
api.add_resource(GatewayFixResourcePatch, "/gateway/api/fixes/add" + "/<fix_id>")
api.add_resource(GatewayMehResource, "/gateway/api/mehs" + "/<meh_id>")
api.add_resource(GatewayMehListResource, "/gateway/api/mehs")
api.add_resource(GatewayMehCreateResource, "/gateway/api/mehs/create")
api.add_resource(GatewayUserResource, "/gateway/api/users" + "/<user_id>")
api.add_resource(GatewayUserListResource, "/gateway/api/users")
api.add_resource(GatewayAuthorization, "/gateway/api/users/auth/token")
api.add_resource(GatewayApiAuthorization, "/gateway/api/users/auth")
api.add_resource(GatewayUserTokenResource,"/gateway/api/users/token")
api.add_resource(GatewayUserCreateResource,"/gateway/api/users/create")




if __name__ == '__main__':
    car_return_thread = CarReturnHandling()
    car_return_thread.start()

    app.run(debug=True)