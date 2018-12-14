from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    pwdhash = db.Column(db.String(54))
    print("==============Rishabh Model Constructor=========")

    def __init__(self, firstname, lastname, email, password):
        print("==============Rishabh===init=======")
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)
        print("==============Rishabh Model=========")
        print(firstname)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
        print("==============Rishabh SET PASSWORD=========")
        print(self.pwdhash)

    def check_password(self, password):
        print("==============Rishabh CHECK PASSWORD=========")
        return check_password_hash(self.pwdhash, password)
