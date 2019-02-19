import itsdangerous
from user.config import current_config
import dateutil.parser
import datetime
import base64


serializer = itsdangerous.Serializer(current_config.SECRET_KEY)


class Token:
    def __init__(self, value, expiration):
        self.value = value
        self.expiration = expiration.isoformat()

    @staticmethod
    def generate(value):
        return Token(value, datetime.datetime.now() +
                     datetime.timedelta(0, current_config.TOKEN_EXPIRATION_TIME))

    def serialize(self):
        result = serializer.dumps(self.__dict__)
        return base64.b64encode(str.encode(result))

    @staticmethod
    def is_expired(token_string):
        if token_string is None:
            return True
        token_string = base64.b64decode(token_string) #base64.b64decode(str.encode(token_string.decode('utf-8')))
        token = serializer.loads(token_string)
        return dateutil.parser.parse(token['expiration']) < datetime.datetime.now()

    @staticmethod
    def check_value(token_string, value):
        if token_string is None:
            return False
        token_string = base64.b64decode(token_string)
        token = serializer.loads(token_string)
        return token['value'] == value

    @staticmethod
    def get_value(token_string):
        if token_string is None:
            return False
        token_string = base64.b64decode(token_string)
        token = serializer.loads(token_string)
        return token['value']

    @staticmethod
    def refresh(token_string):
        token_string = base64.b64decode(token_string)
        token = serializer.loads(token_string)
        token['expiration'] = (datetime.datetime.now() +
                               datetime.timedelta(seconds=current_config.TOKEN_EXPIRATION_TIME)).isoformat()
        return base64.b64encode(str.encode(serializer.dumps(token)))