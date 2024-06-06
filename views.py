from flask_restful import Resource, abort
from utils import PostgresConnection
from exceptions import WrongPasswordError
import json
import serializers
import models
from http import HTTPStatus
import dicts
import validators
import utils
import mixins

# adicionar as classes de views aqui

class Login(Resource):
    def post(self):
        args: dict = serializers.login_serializer.parse_args().copy()
        
        try:
            PostgresConnection(**args)
        except WrongPasswordError as error:
            return abort(HTTPStatus.BAD_REQUEST, message=error.args)
        
        
