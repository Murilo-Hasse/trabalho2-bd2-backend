from flask_restful import Resource, abort
from utils import PostgresConnection
from exceptions import WrongPasswordError
import serializers
from http import HTTPStatus
# adicionar as classes de views aqui

connection = PostgresConnection(user='postgres', password='postgres')


class Login(Resource):
    def post(self):
        args: dict = serializers.login_serializer.parse_args().copy()

        try:
            PostgresConnection(**args)
        except WrongPasswordError as error:
            return abort(HTTPStatus.BAD_REQUEST, message=error.args)

        del args['password']

        return args


class GrupoList(Resource):
    def get(self):
        query = connection.retrieve_from_query('SELECT * FROM grupo;')

        return query


class FormaPagamentoList(Resource):
    def get(self):
        return connection.retrieve_from_query('SELECT * FROM formapagamento;')
