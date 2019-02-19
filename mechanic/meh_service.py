from mechanic import app
from flask_restful import Api
from mechanic.rest_api.meh_resource import MechanicCreateResource

from mechanic.rest_api.meh_resource import MechanicListResource
from mechanic.rest_api.meh_resource import MechanicResource
from mechanic.repository.meh_repository import Mechanic


api = Api(app)
service_namespace = "/mehs"

api.add_resource(MechanicListResource, "/mehs")
api.add_resource(MechanicResource, "/mehs/<meh_id>")
api.add_resource(MechanicCreateResource, "/mehs/create")


if __name__ == '__main__':
    app.run(port=5001, debug=True)