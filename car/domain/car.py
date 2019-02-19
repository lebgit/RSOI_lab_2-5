import json


class Car:
    def __init__(self, car_id, fix_id, user_id, name):
        self.id = car_id
        self.fix_id = fix_id
        self.user_id = user_id
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Car):
            return False
        else:
            return self.id == other.id and self.fix_id == other.fix_id and self.user_id == other.user_id \
                   and self.name == other.name

    def to_json(self):
        dictr = {'car_id': str(self.id), 'fix_id': self.fix_id, 'user_id': self.user_id, 'name': self.name}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Car(car_id=decoded_object["car_id"], fix_id=decoded_object["fix_id"], user_id=decoded_object["user_id"],name=decoded_object["name"])