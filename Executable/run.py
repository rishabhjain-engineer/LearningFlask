from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'

db = SQLAlchemy(app)


class UserDB(db.Model):
    __tablename__ = 'users'
    u_id = db.Column(db.Integer, primary_key=True)
    u_publicid = db.Column(db.String(150))
    u_firstname = db.Column(db.String(150))
    u_lastname = db.Column(db.String(150))
    u_username = db.Column(db.String(150), unique=True)
    u_email = db.Column(db.String(150), unique=True)
    u_pwdhash = db.Column(db.String(150))


class TodoDB(db.Model):
    __tablename__ = 'todo'
    todo_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True)
    completed = db.Column(db.Boolean)
    u_id = db.Column(db.Integer)


class User(Resource):

    def post(self):
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        username = data['username']
        password = generate_password_hash(data['password'], method='sha256')

        new_user = UserDB(u_publicid=str(uuid.uuid4()), u_firstname=firstname, u_lastname=lastname, u_username=username, u_email=email, u_pwdhash=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "New user created successfully."})

    def get(self):
        users = UserDB.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['public_id'] = user.u_publicid
            user_data['firstname'] = user.u_firstname
            user_data['lastname'] = user.u_lastname
            user_data['email'] = user.u_email
            user_data['username'] = user.u_username

            todo_ins = TodoDB.query.filter_by(u_id=user.u_id).all()
            todo_out = []
            for todo in todo_ins:
                todo_o = {}
                todo_o['text'] = todo.text
                todo_o['completed'] = todo.completed
                todo_o['todo_id'] = todo.todo_id
                todo_out.append(todo_o)

            user_data['todos'] = todo_out
            output.append(user_data)

        return jsonify({'users': output})


class SpecificUser(Resource):
    def get(self, public_id):
        if public_id is not None:
            user = UserDB.query.filter_by(u_publicid=public_id).first()

            if not user:
                return jsonify({'message': 'No user found'})
            else:
                user_data = {}
                user_data['public_id'] = user.u_publicid
                user_data['firstname'] = user.u_firstname
                user_data['lastname'] = user.u_lastname
                user_data['email'] = user.u_email
                user_data['username'] = user.u_username
                return jsonify({"user": user_data})

    def put(self, public_id):

        user = UserDB.query.filter_by(u_publicid=public_id).first()

        if not user:
            return jsonify({'message': 'No user found'})
        else:
            user.u_email = "updated@elgroupinternational.com"
            db.session.commit()
            return jsonify({"message": "email account updated!!"})

    def delete(self, public_id):

        user = UserDB.query.filter_by(u_publicid=public_id).first()
        if not user:
            return jsonify({'message': 'No user found'})
        else:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "user deleted successfully!!"})


class SpecificTodo(Resource):
    def put(self, todoid):

        todo_instance = TodoDB.query.filter_by(todo_id=todoid).first()

        if not todo_instance:
            return jsonify({"message": "No task found!!"})

        todo_instance.text = "Email to Matt"
        db.session.commit()
        return jsonify({"message": "Task updated!"})


class Todo(Resource):
    def post(self):
        data = request.get_json()
        text = data['text']
        todo_userid = data['user_id']

        new_todo = TodoDB(text=text, completed=False, u_id=todo_userid)
        db.session.add(new_todo)
        db.session.commit()

        return jsonify({'message': 'Task added successfully!'})

    def get(self):
        todoall = TodoDB.query.all()
        output = []
        for todo in todoall:
            todo_data = {}
            todo_data['todo_task'] = todo.text
            todo_data['todo_completed'] = todo.completed
            todo_data['todo_id'] = todo.todo_id
            output.append(todo_data)

        return jsonify({'todos': output})


class Login(Resource):
    def post(self):

        data = request.get_json()
        username = data['username']
        password = data['password']

        if not username or not password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic-realm="Login requierd"'})

        user = UserDB.query.filter_by(u_username=username).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic-realm="Login requierd"'})

        if check_password_hash(user.u_pwdhash, password):

            token = jwt.encode({'publicid': 'UserDB.u_publicid', 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            user_data = {}
            user_data['public_id'] = user.u_publicid
            user_data['firstname'] = user.u_firstname
            user_data['lastname'] = user.u_lastname
            user_data['email'] = user.u_email
            user_data['username'] = user.u_username
            user_data['token'] = token.decode('UTF-8')

            return jsonify({'message': 'Logged in successfully!', 'user': user_data})

        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic-realm="Login requierd"'})


class GettinComplexJson(Resource):
    def post(self):
        data = request.get_json()

        personal_info_output = {}
        personal_info = data['personal_info']
        personal_info_output['firstname'] = personal_info['firstname']
        personal_info_output['lastname'] = personal_info['lastname']
        personal_info_output['email'] = personal_info['email']

        business_info_output = {}
        business_info = data['business_info']
        business_info_output['firstname'] = business_info['firstname']
        business_info_output['lastname'] = business_info['lastname']
        business_info_output['email'] = business_info['email']

        careers = data['career']
        career_output = []
        for c_object in careers:
            c_output = {}
            c_output['co_name'] = c_object['company_name']
            c_output['salary'] = c_object['salary']
            career_output.append(c_output)

        return jsonify({"personal_info": personal_info_output, "business_info": business_info_output, "career": career_output})


api.add_resource(User, '/user')
api.add_resource(SpecificUser, '/user/<public_id>')
api.add_resource(GettinComplexJson, '/complex')
api.add_resource(Login, '/login')
api.add_resource(Todo, '/todo')
api.add_resource(SpecificTodo, '/todo/<todoid>')

if __name__ == "__main__":
    app.run(debug=True)
