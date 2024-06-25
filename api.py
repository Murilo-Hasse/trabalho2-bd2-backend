from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import views

app: Flask = Flask(__file__)
api: Api = Api(app)
CORS(app, resources={r'/*': {'origins': '*', 'allow-headers': '*'}})

api.add_resource(views.Login, '/login/')

api.add_resource(views.ProdutoList, '/produtos/')
api.add_resource(views.Produtos, '/produtos/<int:produto_id>/')
api.add_resource(
    views.PessoaProdutos, '/funcionarioprodutos/<int:funcionario_id>/'
)
api.add_resource(views.GrupoList, '/grupos/')
api.add_resource(views.FormaPagamentoList, '/formaspagamento/')
api.add_resource(views.Compra, '/compra/')
api.add_resource(views.ComprasList, '/compras/<int:usuario_id>/')
api.add_resource(views.Cadastro, '/pessoa/')
api.add_resource(views.Pesquisa, '/pesquisa/<string:query>/')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
