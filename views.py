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
    

class GrupoList(Resource):
    def get(self):
        with db_session:
            query = select((grupo.codigo, grupo.descricao) for grupo in models.Grupo)[:]
            grupos = list()
            for grupo in query:
                grupo = {
                    'codigo': grupo[0],
                    'descricao': grupo[1]
                }
                grupos.append(grupo)
            
            return grupos

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
        args: dicts.Produto = serializers.produto_post_serializer.parse_args().copy()
        
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
            
            
            abort(HTTPStatus.NOT_FOUND) if not produto else None
                
            prod = {
                    'codigo': produto[0],
                    'valor': float(produto[1]),
                    'quantidade': produto[2],
                    'imagem': produto[3],
                    'fornecedor': produto[4],
                    'grupo': produto[5],
                }
            
            return prod, HTTPStatus.OK
            
    
    # def patch(self, produto_id): 
    #     args: dicts.Produto = serializers.produto_patch_serializer.parse_args().copy()
    #     with db_session:
    #         produto = select(produto for produto in models.Produto if produto.codigo == produto_id).first()
    #         abort(HTTPStatus.NOT_FOUND) if not produto else None
            
    #         print(args)
    
    def delete(self, produto_id):
        with db_session:
            produto = select(produto for produto in models.Produto if produto.codigo == produto_id).first()
            
            abort(HTTPStatus.NOT_FOUND) if not produto else None
            
            produto.delete()
            
            return '', HTTPStatus.OK
        

class FormaPagamentoList(Resource):
    def get(self):
        with db_session:
            query = select((forma.codigo, forma.descricao) for forma in models.FormaDePagamento)[:]
            formas = list()
            for forma in query:
                form = {
                    'codigo': forma[0],
                    'descricao': forma[1]
                }
                formas.append(form)
            
            return formas
                             
