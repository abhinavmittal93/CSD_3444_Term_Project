import dbconnection
import bcrypt

# Class for the user details
class User:

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # It creates a user in the database with the provided info in the user object
    @classmethod
    def create_new_user(cls, user):
        collection_name = dbconnection.db["admins"]
        record = {"name": user.name, "email": user.email, "password": user.password}
        response = collection_name.insert_one(record)
        return response.acknowledged


