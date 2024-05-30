from flask_restful import Resource, Api, abort
from flask_restful.reqparse import RequestParser, Namespace
import http_status as HttpStatusCode
import serializers
import models
from pony.orm import db_session, select

# adicionar as classes de views aqui

class HelloWorld(Resource):
    def get(self):
        return {'data': 'Hello, World!'}
    

class HelloName(Resource):
    def get(self, name: str):
        return {'data': f'Hello, {name.capitalize()}'}
    
    def post(self, name: str):
        args: dict = serializers.task_request_parser.parse_args().copy()
        
        if args['name'].lower() == 'matheus augusto':
            abort(HttpStatusCode.BAD_REQUEST, message="Vai tomar no cu")
            
        return args, HttpStatusCode.CREATED

