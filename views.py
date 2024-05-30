from flask_restful import Resource, Api, abort
from flask_restful.reqparse import RequestParser, Namespace
import http_status as HttpStatusCode
import serializers
import models
from pony.orm import db_session, select, desc

# adicionar as classes de views aqui

class HelloWorld(Resource):
    def get(self):
        with db_session:
            funcoes = select(func for func in models.Funcao)[:]
            funcs = list()
            for func in funcoes:
                funcs.append(
                    {
                        'id': func.codigo,
                        'descricao': func.descricao
                    }
                )
            
        return funcs
    
    def post(self):
        args: dict = serializers.funcao_serializer.parse_args().copy()
        with db_session:
            models.Funcao(descricao=args['descricao'])
            
            query = select(func for func in models.Funcao).order_by(desc(models.Funcao.codigo))[:1][0]
        
        return {
                    'id': query.codigo,
                    'descricao': query.descricao
                }
    

class HelloName(Resource):
    def get(self, name: str):
        return {'data': f'Hello, {name.capitalize()}'}
    
    def post(self, name: str):
        args: dict = serializers.task_request_parser.parse_args().copy()
        
        if args['name'].lower() == 'matheus augusto':
            abort(HttpStatusCode.BAD_REQUEST, message="Vai tomar no cu")
            
        return args, HttpStatusCode.CREATED

