from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class HomePage(Resource):
    def get(self):
        return {"Home_Page": "Home Page"}


api.add_resource(HelloWorld, '/hello')
api.add_resource(HomePage, '/')

if __name__ == '__main__':
    app.run(debug=True)
