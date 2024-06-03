from flask_restful import Resource, abort
import serializers
import models
from typing import Any
from pony.orm import db_session, select
from http import HTTPStatus
import dicts
import validators
import utils
import mixins

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
    

class GrupoList(Resource, mixins.ListMixin):
    query = models.Grupo.select()

#GET E POST
class ProdutoList(Resource, mixins.ListMixin):
    query = select((p.codigo, p.descricao, p.valor, p.quantidade, p.imagem, p.fornecedor.nome, p.grupo.descricao) for p in models.Produto)
    dict = dicts.Produto
    
    def post(self):
        args: dicts.Produto = serializers.produto_post_serializer.parse_args().copy()
        
        if args['imagem'] == None:
            args['imagem'] = ''
        
        if len(args['imagem']) >= 1:
            b64_img_str = args['imagem']
            args['extensao_imagem'] = args['extensao_imagem'].replace('.', ''.lower())
            img_link = utils.decode_and_upload_to_dropbox(b64_img_str, args['descricao'], args['extensao_imagem'])
            del args['extensao_imagem']
            
            args['imagem'] = img_link
            
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
        

class FormaPagamentoList(Resource, mixins.ListMixin):
    query = models.FormaDePagamento.select()
                             
