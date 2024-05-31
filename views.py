from flask_restful import Resource, abort
import serializers
import models
from pony.orm import db_session, select
from http import HTTPStatus
import dicts
import validators

# adicionar as classes de views aqui

class Endereco(Resource):
    def post(self):
        with db_session:
            endereco: dicts.Endereco = serializers.endereco_serializer.parse_args().copy()
            
            endereco['cep'] = endereco['cep'].replace('-', '')
            
            validators.EnderecoValidator(endereco)
            
            endereco['logradouro'] = endereco['logradouro'].capitalize()
            endereco['bairro'] = endereco['bairro'].capitalize()
            models.Endereco(**endereco)

            query = select(max(e.codigo,) for e in models.Endereco).first()
        
        endereco['codigo'] = query
        return endereco, HTTPStatus.CREATED

#GET E POST
class ProdutoList(Resource):
    def get(self):
        with db_session:
            query = select((produto.codigo, 
                            produto.valor, 
                            produto.quantidade, 
                            produto.imagem, 
                            produto.fornecedor.nome, 
                            produto.grupo.descricao) 
                           for produto in models.Produto)[:]
            
            products = list()
            for product in query:
                prod = {
                    'codigo': product[0],
                    'valor': float(product[1]),
                    'quantidade': product[2],
                    'imagem': product[3],
                    'fornecedor': product[4],
                    'grupo': product[5],
                }
                products.append(prod)
            
            return products, HTTPStatus.OK
    
    def post(self):
        args: dicts.ProdutoList = serializers.produto_post_serializer.parse_args().copy()
        
        if args['imagem'] == None:
            args['imagem'] = ''
            
        validators.ProdutoValidator(args)    
        
        with db_session:
            models.Produto(**args)
            codigo = select(max(produto.codigo) for produto in models.Produto).first()
        args['codigo'] = codigo
        
        return args, HTTPStatus.CREATED
        
#GET, PATCH, DELETE
class Produtos(Resource):
    def get(self, produto_id):
        with db_session:
            produto = select((produto.codigo, 
                            produto.valor, 
                            produto.quantidade, 
                            produto.imagem, 
                            produto.fornecedor.nome, 
                            produto.grupo.descricao) 
                             for produto in models.Produto if produto.codigo == produto_id).first()
            
            
            if not produto:
                abort(HTTPStatus.NOT_FOUND)
                
            prod = {
                    'codigo': produto[0],
                    'valor': float(produto[1]),
                    'quantidade': produto[2],
                    'imagem': produto[3],
                    'fornecedor': produto[4],
                    'grupo': produto[5],
                }
            
            return prod, HTTPStatus.OK
            
    
    def patch(self, produto_id): ...
    
    def delete(self, produto_id):
        with db_session:
            produto = select(produto for produto in models.Produto if produto.codigo == produto_id).first()
            
            if not produto:
                abort(HTTPStatus.NOT_FOUND)
            
            produto.delete()
            
            return '', HTTPStatus.OK
                             
