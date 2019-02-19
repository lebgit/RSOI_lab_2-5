from flask_mongoalchemy import MongoAlchemy
from user import app
from user.tokenu import Token
from user.domain.user import User
import jsonpickle
import hashlib
db = MongoAlchemy(app)


class Users(db.Document):
    l_name = db.StringField()
    status = db.StringField()
    password = db.StringField()
    admin = db.StringField()
    token = db.StringField()



class UserRep:

    def create(self, l_name,password, admin):
        status = 0
        token = Token.generate(l_name).serialize()
        user = Users(l_name=l_name,password=self.hash_password(password), admin=admin, status=jsonpickle.encode(status),token=str(token))
        user.save()
        return user.mongo_id

    def get(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            return User(user_id=user.mongo_id, l_name=user.l_name,
                        admin=user.admin, status=user.status)
        else:
            return None

    def hash_password(self, password):
        tmp1 = str(password).encode('utf8')
        tmp = hashlib.sha256(tmp1).hexdigest()
        return tmp


    def read_paginated(self, page_number, page_size):
        users = []
        users_paged = Users.query.paginate(page=page_number, per_page=page_size)

        for user in users_paged.items:
            users.append(User(user_id=user.mongo_id, status=user.status, l_name=user.l_name,
                              admin=user.admin))
        is_prev_num = (users_paged.prev_num > 0)
        is_next_num = (users_paged.next_num <= users_paged.pages)
        return users, is_prev_num, is_next_num

    def delete(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            user.remove()

    def get_real_user_by_token(self, token):
        user = self.get_by_token(token)
        if user is None:
            return user
        return User(user_id=user.mongo_id,  l_name=user.l_name, admin=user.admin, status=user.status)


    def get_by_token(self, token):
        if not Token.is_expired(token):
            login = Token.get_value(token)
            user = self.get_user_by_login(login)
            return user
        return None

    def check_password(self, hash_password, password):
        p1 = self.hash_password(password)
        p2 = hash_password
        return p1 == p2

    def refresh_token(self, token):
        user_id = Token.get_value(token)
        if self.exists(user_id):
            t = Token.refresh(token)
            user = self.get(user_id)
            user.token = t
            user.save()
            return t
        return None

    def assign_car(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            if jsonpickle.decode(user.status) == '1':
                return False
            user.status = jsonpickle.encode(1)
            user.save()
            return True
        return False

    def remove_car(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            if jsonpickle.decode(user.status) == '0':
                return False
            user.status = jsonpickle.encode(0)
            user.save()
            return True
        return False

    def get_token(self, login, password):
        if self.login_exists(login):
            if self.check_password_for_user(login, password):
                user = self.get_user_by_login(login)
                app.logger.info(login)
                t = Token.generate(login).serialize()
                user.token = str(t)
                user.save()
                return t
        return None

    def get_code(self, client_id):
        if client_id == 1:
            return '1488'
        return None

    def get_token_for_auth(self, client_id, client_secret, code):
        if client_id == 1:
            if code == '1488':
                user_id = '5c6421a27162372134114298'
                user = Users.query.get(user_id)
                app.logger.info(user.l_name)

                t = Token.generate(user.l_name).serialize()
                user.token = str(t)
                user.save()
                return t
        return None

    def check_password_for_user(self, login, password):
        if self.login_exists(login):
            user = self.get_user_by_login(login)
            return self.check_password(user.password, password)

    def login_exists(self, login):
        result = Users.query.filter(Users.l_name == login)
        return result is not None

    def get_user_by_login(self, login):
        return Users.query.filter(Users.l_name == login).first()

    def exists(self, user_id):
        result = Users.query.get(user_id)
        return result is not None


