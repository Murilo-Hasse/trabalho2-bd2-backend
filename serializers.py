from flask_restful.reqparse import RequestParser

#adicionar os serializers aqui

endereco_serializer: RequestParser = RequestParser()
endereco_serializer.add_argument('logradouro', type=str, help='Endereço não preenchido', required=True)
endereco_serializer.add_argument('numero', type=int, help='Número não preenchido/não é um número válido', required=True)
endereco_serializer.add_argument('cep', type=str, help='CEP não preenchido', required=True)
endereco_serializer.add_argument('bairro', type=str, help='Bairro não preenchido', required=True)

produto_post_serializer: RequestParser = RequestParser()
produto_post_serializer.add_argument('descricao', type=str, help='Nome do item não informado', required=True)
produto_post_serializer.add_argument('valor', type=float, help='Valor do produto não informado/não é um número válido', required=True)
produto_post_serializer.add_argument('quantidade', type=int, help='Quantidade do produto não informada/não é um número válido', required=True)
produto_post_serializer.add_argument('imagem', type=str, help='A imagem não está em base64', required=False, default=None)
produto_post_serializer.add_argument('fornecedor', type=int, help='Fornecedor não informado/não é válido', required=True)
produto_post_serializer.add_argument('grupo', type=int, help='Grupo não informado/não é válido', required=True)

produto_patch_serializer: RequestParser = RequestParser()
produto_post_serializer.add_argument('descricao', type=str)
produto_post_serializer.add_argument('valor', type=float)
produto_post_serializer.add_argument('quantidade', type=int)
produto_post_serializer.add_argument('imagem', type=str)
produto_post_serializer.add_argument('fornecedor', type=int)
produto_post_serializer.add_argument('grupo', type=int)