import dbconnection
import bcrypt


class User:

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @classmethod
    def create_new_user(cls, user):
        collection_name = dbconnection.db["admins"]
        record = {"name": user.name, "email": user.email, "password": user.password}
        response = collection_name.insert_one(record)
        return response.acknowledged


