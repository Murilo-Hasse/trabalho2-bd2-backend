from flask_restful.reqparse import RequestParser
from typing import TypedDict

#adicionar os serializers aqui

funcao_serializer: RequestParser = RequestParser()
funcao_serializer.add_argument('descricao', type=str, help='Campo obrigatório não preenchido', required=True)

endereco_serializer: RequestParser = RequestParser()
endereco_serializer.add_argument('logradouro', type=str, help='Endereço não preenchido', required=True)
endereco_serializer.add_argument('numero', type=int, help='Número não preenchido/não é um número válido', required=True)
endereco_serializer.add_argument('cep', type=str, help='CEP não preenchido', required=True)
endereco_serializer.add_argument('bairro', type=str, help='Bairro não preenchido', required=True)
