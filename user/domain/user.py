import json

class User:
    def __init__(self, user_id, l_name, admin, status):
        self.id = user_id
        self.l_name = l_name
        self.admin = admin
        self.status = status


    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        else:
            return self.id == other.id and self.l_name == other.l_name and \
                   self.admin == other.admin and self.status == status

    def to_json(self):
        dictr = {'user_id': str(self.id), 'l_name': self.l_name, 'admin': self.admin,
                 'status': self.status}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return User(user_id=decoded_object['user_id'],
                    l_name=decoded_object['l_name'], admin=decoded_object['admin'], status=decoded_object['status'])