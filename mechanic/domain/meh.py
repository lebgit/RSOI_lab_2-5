import json


class Mechanic:
    def __init__(self, meh_id, name, lvl, year):
        self.id = meh_id
        self.name = name
        self.lvl = lvl
        self.year = year

    def __eq__(self, other):
        if not isinstance(other, Mechanic):
            return False
        else:
            return self.id == other.id and self.name == other.name and self.year == other.year and \
                   self.lvl == other.lvl

    def to_json(self):
        dictr = {'meh_id': str(self.id), 'name': self.name, 'year': self.year, 'lvl': self.lvl}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Mechanic(meh_id=decoded_object["meh_id"], name=decoded_object["name"],
                     lvl=decoded_object["lvl"], year=decoded_object["year"])
