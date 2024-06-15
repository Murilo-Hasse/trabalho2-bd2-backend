from flask import Flask
from utils import PostgresConnection
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import views

app: Flask = Flask(__file__)
api: Api = Api(app)

api.add_resource(views.Login, '/login/')

#api.add_resource(views.Endereco, '/endereco/')
#api.add_resource(views.ProdutoList, '/produtos/')
#api.add_resource(views.Produtos, '/produtos/<int:produto_id>/')
#api.add_resource(views.GrupoList, '/grupos/')
#api.add_resource(views.FormaPagamentoList, '/formaspagamento/')

connection = PostgresConnection(user='postgres', password='postgres')
connection.retrieve_from_query("SELECT * FROM endereco;")

if __name__ == '__main__':
    app.run(debug=True)
