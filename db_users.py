from mongoengine import *
from datetime import datetime

connect(host="mongodb://127.0.0.1:27017/ekko?directConnection=true&serverSelectionTimeoutMS=2000")

class Users(Document):
    id = SequenceField(primary_key = True)
    name = StringField()
    email = StringField()
    password = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

# Create a new user in the database
def create_new_user(name, email, password):
    new_user = Users(
        name = name,
        email = email,
        password = password,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    new_user.save()


def check_email_found(given_email):
    user = Users.objects(email = given_email).first()
    return user


def check_password_of_user(email, password):
    user = Users.objects(Q(email = email) & Q(password = password)).first()

    return user