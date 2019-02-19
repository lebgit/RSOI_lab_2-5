class Config(object):
    DEBUG = True
    TESTING = True
    GATEWAY_SERVICE_PATH = "/gateway/api"

    CREATE_PATH = "/create"

    MECHANIC_SERVICE_PATH = "/mehs"
    MECHANIC_URL_PATH = "/<mehs_id>"

    FIX_SERVICE_PATH = "/fixes"
    FIX_URL_PATH = "/<fixes_id>"

    CAR_SERVICE_PATH = "/cars"
    CAR_URL_PATH = "/<cars_id>"

    USER_SERVICE_PATH = "/users"
    USER_URL_PATH = "/<user_id>"

    SECRET_KEY = "qwerty1234"

    GET_TOKEN_URL_PATH = "/auth/token"


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5005
    GUI_SERVICE_URL = "http://127.0.0.1:%d" % PORT
    GATEWAY_SERVICE_URL = "http://127.0.0.1:5000"
    USER_SERVICE_URL = "http://127.0.0.1:5004"

current_config = DevelopmentConfig()