from flask import Flask
from flask_restful import Api
import views

app: Flask = Flask(__file__)
api: Api =  Api(app)

api.add_resource(views.Funcoes, '/funcoes/')
api.add_resource(views.Endereco, '/endereco/')

if __name__ == '__main__':
    app.run(debug=True)