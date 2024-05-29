from flask import Flask
from flask_restful import Api
import views

app: Flask = Flask(__file__)
api: Api =  Api(app)

api.add_resource(views.HelloWorld, '/helloworld/')
api.add_resource(views.HelloName, '/helloname/<string:name>/')

if __name__ == '__main__':
    app.run(debug=True)