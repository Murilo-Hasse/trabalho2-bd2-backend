from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import views

app: Flask = Flask(__file__)
CORS(app)
api: Api = Api(app)

api.add_resource(views.Login, '/login/')

api.add_resource(views.Endereco, '/endereco/')
api.add_resource(views.ProdutoList, '/produtos/')
api.add_resource(views.Produtos, '/produtos/<int:produto_id>/')
api.add_resource(views.GrupoList, '/grupos/')
api.add_resource(views.FormaPagamentoList, '/formaspagamento/')
api.add_resource(views.Compra, '/compra/')
api.add_resource(views.ComprasList, '/compras/<int:usuario_id>/')

if __name__ == '__main__':
    app.run(debug=True)
