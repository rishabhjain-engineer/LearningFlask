from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'

db = SQLAlchemy(app)


class UserDB(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    publicid = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(100))


class TodoDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True)
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


class User(Resource):

    def post(self):
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        password = generate_password_hash(data['password'], method='sha256')

        new_user = UserDB(publicid=str(uuid.uuid4()), firstname=firstname, lastname=lastname, email=email, pwdhash=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "New user created successfully."})

    def get(self):
        users = UserDB.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['public_id'] = user.publicid
            user_data['firstname'] = user.firstname
            user_data['lastname'] = user.lastname
            user_data['email'] = user.email
            output.append(user_data)

        return jsonify({'users': output})

    def delete(self):
        return ''

    def put(self):
        return ''


api.add_resource(User, '/user')

if __name__ == "__main__":
    app.run(debug=True)
