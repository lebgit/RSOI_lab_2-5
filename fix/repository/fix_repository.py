from flask_mongoalchemy import MongoAlchemy
from fix import app
from fix.domain.fix import Fix
import jsonpickle


db = MongoAlchemy(app)


class Fixes(db.Document):
    car_ids = db.StringField()
    date_time = db.StringField()
    meh_ids = db.StringField()


class FixRepository:
    def create(self, date_time):
        car_ids = []
        meh_ids = []
        fix = Fixes(car_ids=jsonpickle.encode(meh_ids), date_time=date_time, meh_ids=jsonpickle.encode(car_ids))
        fix.save()
        return fix.mongo_id

    def get(self, fix_id):
        if self.exists(fix_id):
            fix = Fixes.query.get(fix_id)
            car_ids = jsonpickle.decode(fix.car_ids)
            meh_ids = jsonpickle.decode(fix.meh_ids)
            return Fix(fix_id=fix.mongo_id, meh_ids=meh_ids, date_time=fix.date_time, car_ids=car_ids)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        fixes = []
        fixes_paginated = Fixes.query.paginate(page=page_number, per_page=page_size)
        for fix in fixes_paginated.items:
            car_ids = jsonpickle.decode(fix.car_ids)
            meh_ids = jsonpickle.decode(fix.meh_ids)
            fixes.append(Fix(fix_id=fix.mongo_id, meh_ids=meh_ids, date_time=fix.date_time,
                             car_ids=car_ids,))
        is_prev_num = (fixes_paginated.prev_num > 0)
        is_next_num = (fixes_paginated.next_num <= fixes_paginated.pages)
        return fixes, is_prev_num, is_next_num

    def delete(self, fix_id):
        if self.exists(fix_id):
            fix = Fixes.query.get(fix_id)
            fix.remove()

    def add_car(self, fix_id, car_id):
        if self.exists(fix_id):
            fix = Fixes.query.get(fix_id)
            car_ids = jsonpickle.decode(fix.car_ids)
            car_ids.append(car_id)
            # book_ids = user.book_ids + tuple(str(book_id))
            fix.car_ids = jsonpickle.encode(car_ids)
            fix.save()
            return True
        return False


    def rem_car(self, fix_id, car_id):
        if self.exists(fix_id):
            fix = Fixes.query.get(fix_id)
            car_ids = jsonpickle.decode(fix.car_ids)
            car_ids.remove(car_id)
            fix.car_ids = jsonpickle.encode(car_ids)
            fix.save()
            return True
        return False
    def add_meh(self, fix_id, meh_id):
        if self.exists(fix_id):
            fix = Fixes.query.get(fix_id)
            meh_ids = jsonpickle.decode(fix.meh_ids)
            meh_ids.append(meh_id)
            # book_ids = user.book_ids + tuple(str(book_id))
            fix.meh_ids = jsonpickle.encode(meh_ids)
            fix.save()
            return True
        return False
    def rem_meh(self, fix_id, meh_id):
        if self.exists(fix_id):
            fix = Fixes.query.get(fix_id)
            meh_ids = jsonpickle.decode(fix.meh_ids)
            meh_ids.remove(meh_id)
            fix.meh_ids = jsonpickle.encode(meh_ids)
            fix.save()
            return True
        return False

    def exists(self, fix_id):
        result = Fixes.query.get(fix_id)
        return result is not None