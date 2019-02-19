from user import app
from flask_restful import Api
from user.rest_api.user_resource import *
from user.repository.user_repository import Users


api = Api(app)
service_namespace = "/users"

api.add_resource(UserListRes, "/users")
api.add_resource(UserResource, "/users/<user_id>")
api.add_resource(UserCreateResource, "/users/create")
api.add_resource(UserAuthorizationResource, "/users/auth/token")
api.add_resource(UserTokenResource, "/users/token")


if __name__ == '__main__':
    app.run(port=5004, debug=True)