from flask_mongoalchemy import MongoAlchemy
from mechanic import app
from mechanic.domain.meh import Mechanic


db = MongoAlchemy(app)


class Mechanics(db.Document):
    name = db.StringField()
    lvl = db.StringField()
    year = db.StringField()



class MehRepository:
    def create(self, name, lvl, year):
        meh = Mechanics(name=name, lvl=lvl, year=year)
        meh.save()
        return meh.mongo_id

    def get(self, meh_id):
        if self.exists(meh_id):
            meh = Mechanics.query.get(meh_id)
            return Mechanic(meh_id=meh.mongo_id, name=meh.name, lvl=meh.lvl, year=meh.year)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        mehs = []
        mehs_paginated = Mechanics.query.paginate(page=page_number, per_page=page_size)
        for meh in mehs_paginated.items:
            mehs.append(Mechanic(meh_id=meh.mongo_id, name=meh.name, lvl=meh.lvl,
                                year=meh.year))
        is_prev_num = (mehs_paginated.prev_num > 0)
        is_next_num = (mehs_paginated.next_num <= mehs_paginated.pages)
        return mehs, is_prev_num, is_next_num

    def delete(self, meh_id):
        if self.exists(meh_id):
            meh = Mechanics.query.get(meh_id)
            meh.remove()

    def exists(self, meh_id):
        result = Mechanics.query.get(meh_id)
        return result is not None