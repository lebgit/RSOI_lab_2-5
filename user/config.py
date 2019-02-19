class Config(object):
    DEBUG = False
    TESTING = False
    MONGOALCHEMY_DATABASE_URI = ""
    SECRET_KEY = "qwerty1234"
    MONGOALCHEMY_TRACK_MODIFICATIONS = False
    USER_SERVICE_PATH = "/users"
    USER_URL_PATH = "/<user_id>"

    GATEWAY_URL_PATH = "/gateway/api"
    CHECK_ROLE_URL_PATH = "/auth/check_role"
    GET_TOKEN_URL_PATH = "/auth/token"
    TOKEN_CHECK_ID_URL_PATH = "/auth/token/check_id"


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5004
    USER_SERVICE_URL = "http://127.0.0.1:%d" % PORT
    GATEWAY_SERVICE_URL = "http://127.0.0.1:5000"

    MONGOALCHEMY_DATABASE_URI = "mongodbl+psycopg2://tester:111@localhost/users_db"
    TOKEN_EXPIRATION_TIME = 2000

current_config = DevelopmentConfig()