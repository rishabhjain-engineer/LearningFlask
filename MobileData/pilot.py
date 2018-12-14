from flask import Flask, request, jsonify, session
from flask_restful import Resource, Api
from databaseModel import db, User
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
db.init_app(app)

app.secret_key = "development-key"


class UserInfo(Resource):

    def post(self):
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        email = request.json['email']
        password = request.json['password']

        newuser = User(firstname, lastname, email, password)
        db.session.add(newuser)
        db.session.commit()

        return jsonify("Success")

    def get(self):
        return jsonify("hello get request")


api.add_resource(UserInfo, "/signup")

if __name__ == "__main__":
    app.run(host='192.168.2.10', debug=True)
