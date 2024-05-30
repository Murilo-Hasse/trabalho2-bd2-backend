from flask_restful import Resource, Api, abort
from flask_restful.reqparse import RequestParser, Namespace
import serializers
import models
from pony.orm import db_session, select, desc
from http import HTTPStatus
import dicts
import validators

# adicionar as classes de views aqui

class Endereco(Resource):
    def post(self):
        with db_session:
            endereco: dicts.Endereco = serializers.endereco_serializer.parse_args().copy()
            
            validators.EnderecoValidator(endereco)
            
            endereco['logradouro'] = endereco['logradouro'].capitalize()
            endereco['bairro'] = endereco['bairro'].capitalize()
            models.Endereco(**endereco)

            query = select(max(e.codigo,) for e in models.Endereco).first()
        
        endereco['codigo'] = query
        return endereco, HTTPStatus.CREATED

class Funcoes(Resource):
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
                }, HTTPStatus.CREATED

