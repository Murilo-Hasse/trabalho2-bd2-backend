from flask_restful.reqparse import RequestParser

# adicionar os serializers aqui

login_serializer: RequestParser = RequestParser()
login_serializer.add_argument(
    'user', type=str, help='Usuário não preenchido', required=True
)
login_serializer.add_argument(
    'password', type=str, help='Senha não preenchida', required=True
)


user_post_serializer: RequestParser = RequestParser()
user_post_serializer.add_argument(
    'nome', type=str, required=True, help='Nome não especificado'
)
user_post_serializer.add_argument(
    'email', type=str, required=True, help='E-Mail não especificado'
)
user_post_serializer.add_argument(
    'documento', type=str, required=True, help='CPF/CNPJ não especificado'
)
user_post_serializer.add_argument(
    'senha', type=str, required=True, help='Senha não especificada'
)
user_post_serializer.add_argument(
    'logradouro', type=str, required=True, help="Logradouro não especificado!"
)
user_post_serializer.add_argument(
    'numero', type=int, required=True, help="Número da casa não fornecido!"
)
user_post_serializer.add_argument(
    'cep', type=str, required=True, help='CEP Não informado!'
)
user_post_serializer.add_argument(
    'bairro', type=str, required=True, help='Bairro não informado!'
)

compra_serializer: RequestParser = RequestParser()
compra_serializer.add_argument('quantidade', required=False, type=int)
compra_serializer.add_argument(
    'forma_pagamento', required=True, help='forma de pagamento não especificada', type=int
)
compra_serializer.add_argument(
    'codigo_produto', required=True, help='Produto não especificado', type=int
)
compra_serializer.add_argument(
    'usuario', required=True, help='Usuário não especificado', type=int
)
