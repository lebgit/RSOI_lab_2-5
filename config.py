class Config(object):
    DEBUG = False
    TESTING = False
    GATEWAY_PATH = "/gateway/api"

    CREATE_PATH = "/create"

    MECHANIC_SERVICE_PATH = "/mehs"

    FIX_SERVICE_PATH = "/fixes"

    CAR_SERVICE_PATH = "/cars"

    USER_SERVICE_PATH = "/users"

    GET_TOKEN_URL_PATH = "/auth/token"

    PORT = 5000
    GATEWAY_URL = "http://127.0.0.1:5000"
    MECHANIC_SERVICE_URL = "http://127.0.0.1:5001"
    FIX_SERVICE_URL = "http://127.0.0.1:5002"
    CAR_SERVICE_URL = "http://127.0.0.1:5003"
    USER_SERVICE_URL = "http://127.0.0.1:5004"


current_config = Config()