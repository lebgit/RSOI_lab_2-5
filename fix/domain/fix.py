import json


class Fix:
    def __init__(self, fix_id, meh_ids, date_time, car_ids):
        self.id = fix_id
        self.car_ids = car_ids
        self.date_time = date_time
        self.meh_ids = meh_ids

    def __eq__(self, other):
        if not isinstance(other, Fix):
            return False
        else:
            return self.id == other.id and self.car_ids == other.car_ids and self.date_time == other.date_time and \
                   self.meh_ids == other.meh_ids

    def to_json(self):
        dictr = {'fix_id': str(self.id),  'datetime': self.date_time,
                 'meh_ids': self.meh_ids, 'car_ids': self.car_ids}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Fix(fix_id=decoded_object["fix_id"], car_ids=decoded_object['car_ids'],
                      date_time=decoded_object["datetime"], meh_ids=decoded_object['meh_ids'])