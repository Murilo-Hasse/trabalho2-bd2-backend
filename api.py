from flask import Flask
from flask_restful import Api
import views

app: Flask = Flask(__file__)
api: Api =  Api(app)

api.add_resource(views.Endereco, '/endereco/')

api.add_resource(views.ProdutoList, '/produtos/')
api.add_resource(views.Produtos, '/produtos/<int:produto_id>/')

api.add_resource(views.GrupoList, '/grupos/')

if __name__ == '__main__':
    app.run(debug=True)