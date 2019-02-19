from fix import app
from flask_restful import Api
from fix.rest_api.fix_resource import *
#from mechanic.repository.meh_repository import Mechanics


api = Api(app)
service_namespace = "/fixes"

api.add_resource(FixListResource, "/fixes")
api.add_resource(FixResource, "/fixes/<fix_id>")
api.add_resource(FixCreateResource, "/fixes/create")


if __name__ == '__main__':
    app.run(port=5002, debug=True)