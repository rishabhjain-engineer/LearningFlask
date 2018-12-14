from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort
from models import db, User
from flask_restful import Resource, Api
from forms import SignupForm, LoginForm


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
db.init_app(app)

app.secret_key = "development-key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about_fun():
    return render_template("about.html")


@app.route("/home")
def home():
    # By checking below current session holds any email, we maintain the state.
    # if no email is registered in the session , refrain user to go to home page, instead navigate to login page.
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate == "False":
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                print("==============Rishabh IF=========")
                return redirect(url_for('home'))
            else:
                print("==============Rishabh ELSE=========")
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template("login.html", form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():

    if 'email' in session:
        return redirect(url_for('home'))

    form = SignupForm()

    if request.method == 'GET':
        return render_template("signup.html", form=form)

    elif request.method == 'POST':
        if form.validate() == False:
            return render_template("signup.html", form=form)
        else:
            newuser = User(firstname=form.first_name.data,
                           lastname=form.last_name.data,
                           email=form.email.data,
                           password=form.password.data)

            db.session.add(newuser)
            db.session.commit()
            session['email'] = newuser.email
            print("==============Rishabh=========")
            return redirect(url_for('home'))
            # return "Success!"


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


class HelloWorld(Resource):
    """docstring for HelloWorld"""

    def get(self):
        return{'helloooo': 'worldddd'}


api.add_resource(HelloWorld, '/helloWorld')

if __name__ == "__main__":
    app.run(host='192.168.2.10', debug=True)
