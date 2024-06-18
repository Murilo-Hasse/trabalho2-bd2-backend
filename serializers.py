from flask_restful.reqparse import RequestParser

# adicionar os serializers aqui

login_serializer: RequestParser = RequestParser()
login_serializer.add_argument(
    'user', type=str, help='Usuário não preenchido', required=True)
login_serializer.add_argument(
    'password', type=str, help='Senha não preenchida', required=True)


user_post_serializer: RequestParser = RequestParser()
user_post_serializer.add_argument(
    'nome', type=str, required=True, help='Nome não especificado')
user_post_serializer.add_argument(
    'documento', type=str, required=True, help='CPF/CNPJ não especificado')
user_post_serializer.add_argument(
    'senha', type=str, required=True, help='Senha não especificada')


endereco_serializer: RequestParser = RequestParser()
endereco_serializer.add_argument(
    'logradouro', type=str, help='Endereço não preenchido', required=True)
endereco_serializer.add_argument(
    'numero', type=int, help='Número não preenchido/não é um número válido', required=True)
endereco_serializer.add_argument(
    'cep', type=str, help='CEP não preenchido', required=True)
endereco_serializer.add_argument(
    'bairro', type=str, help='Bairro não preenchido', required=True)

produto_post_serializer: RequestParser = RequestParser()
produto_post_serializer.add_argument('nome', type=str)
produto_post_serializer.add_argument(
    'descricao', type=str, help='Nome do item não informado', required=True)
produto_post_serializer.add_argument(
    'valor', type=float, help='Valor do produto não informado/não é um número válido', required=True)
produto_post_serializer.add_argument(
    'quantidade', type=int, help='Quantidade do produto não informada/não é um número válido', required=True)
produto_post_serializer.add_argument(
    'imagem', type=str, help='A imagem não está em base64', required=False, default=None)
produto_post_serializer.add_argument(
    'fornecedor', type=int, help='Fornecedor não informado/não é válido', required=True)
produto_post_serializer.add_argument(
    'grupo', type=int, help='Grupo não informado/não é válido', required=True)
produto_post_serializer.add_argument(
    'extensao_imagem', type=str, help='A extensão da imagem não foi fornecida!')

compra_serializer: RequestParser = RequestParser()
compra_serializer.add_argument('quantidade', required=False, type=int)
compra_serializer.add_argument(
    'forma_pagamento', required=True, help='forma de pagamento não especificada', type=int)
compra_serializer.add_argument(
    'codigo_produto', required=True, help='Produto não especificado', type=int)
compra_serializer.add_argument(
    'usuario', required=True, help='Usuário não especificado', type=int)
