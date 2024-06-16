from flask_restful import Resource, abort
from utils import PostgresConnection, WrongPasswordError, decode_and_upload_to_dropbox
import serializers
from http import HTTPStatus
from typing import Any
from datetime import datetime


connection = None
connection = PostgresConnection(user='postgres', password='admin')


def connected(func):
    def wrapper(*args, **kwargs):
        if not connection:
            abort(HTTPStatus.UNAUTHORIZED, message='You are not logged in')
        return func(*args, **kwargs)
    return wrapper


def retrieve_last_created(table_name: str) -> dict[str, Any]:
    """Função que recebe um nome da tabela e retorna todas as informações do último objeto que foi criado, ideal para requisições POST, as quais devem retornar o objeto que foi criado.

    Args:
        table_name: Nome da tabela a qual será pego o último objeto criado

    Returns:
        dict: HashMap contendo as informações do item criado
    """
    return connection.retrieve_one_from_query(
        f'SELECT * FROM {table_name} ORDER BY codigo DESC LIMIT 1;'
    )


class Login(Resource):
    """Classe que contém o método POST para fazer login na aplicação, ela funciona pegando o usuário NO BANCO (Usuário da aplicação = Usuário no banco)"""

    def post(self):
        args: dict = serializers.login_serializer.parse_args().copy()

        try:
            PostgresConnection(**args)
        except WrongPasswordError as error:
            return abort(HTTPStatus.BAD_REQUEST, message=error.args)

        del args['password']

        return args


class GrupoList(Resource):
    """Classe responsável pelos métodos relacionados aos grupos, neste caso só tem o método GET, o qual irá retornar uma lista contendo todos os grupos"""
    @connected
    def get(self):
        return connection.retrieve_many_from_query('SELECT * FROM grupo;')


class FormaPagamentoList(Resource):
    @connected
    def get(self):
        return connection.retrieve_many_from_query('SELECT * FROM formapagamento;')


class Endereco(Resource):
    @connected
    def post(self):
        args = serializers.endereco_serializer.parse_args()

        connection.execute(
            'INSERT INTO endereco(logradouro, numero, cep, bairro) VALUES (%s, %s, %s, %s);',
            list(args.values())
        )
        connection.commit()
        return retrieve_last_created('endereco')


class ProdutoList(Resource):
    @connected
    def get(self):
        query = """
        SELECT
            produto.codigo AS codigo,
            produto.nome AS nome,
            produto.descricao AS descricao,
            produto.valor AS valor,
            produto.quantidade AS quantidade,
            produto.imagem AS imagem,
            grupo.descricao AS grupo,
            pessoa.nome AS fornecedor
        FROM
            produto
        INNER JOIN grupo
            ON produto.grupo = grupo.codigo
        INNER JOIN pessoa
            ON produto.codigo_fornecedor = pessoa.codigo
        WHERE produto.quantidade > 0
        ORDER BY produto.codigo ASC;
        """
        return connection.retrieve_many_from_query(query)

    @connected
    def post(self):
        args = serializers.produto_post_serializer.parse_args()

        img_b64 = args['imagem']
        img_extension = args['extensao_imagem']

        img_url = decode_and_upload_to_dropbox(
            img_b64, args['descricao'], img_extension
        )

        del args['extensao_imagem']

        args['imagem'] = img_url

        connection.execute(
            'INSERT INTO produto(descricao, valor, quantidade, imagem, grupo, codigo_fornecedor) VALUES (%s, %s, %s, %s, %s, %s)',
            list(args.values())
        )
        connection.commit()
        return retrieve_last_created('produto')


class Produtos(Resource):
    @connected
    def get(self, produto_id):
        query = f"""
        SELECT
            produto.codigo AS codigo,
            produto.nome AS nome,
            produto.descricao AS descricao,
            produto.valor AS valor,
            produto.quantidade AS quantidade,
            produto.imagem AS imagem,
            grupo.descricao AS grupo,
            pessoa.nome AS fornecedor
        FROM
            produto
        INNER JOIN grupo
            ON produto.grupo = grupo.codigo
        INNER JOIN pessoa
            ON produto.codigo_fornecedor = pessoa.codigo
        WHERE
            produto.codigo = {produto_id};
        """
        return connection.retrieve_one_from_query(query)

    @connected
    def delete(self, produto_id):
        connection.execute(
            f'DELETE FROM produto WHERE codigo = {produto_id}'
        )
        connection.commit()


class Compra(Resource):
    @connected
    def post(self):
        args = serializers.compra_serializer.parse_args()

        quantidade_a_ser_vendido = args['quantidade'] if args['quantidade'] else 1
        codigo_produto = args['codigo_produto']

        preco_produto, quantidade_em_estoque = connection.retrieve_one_from_query(
            f"SELECT valor, quantidade FROM produto WHERE codigo = {codigo_produto}"
        ).values()

        if quantidade_a_ser_vendido > quantidade_em_estoque:
            abort(HTTPStatus.BAD_REQUEST, message='Não tem tanto produto assim!')

        final_price = preco_produto * quantidade_a_ser_vendido

        connection.execute(
            """
            INSERT INTO venda(quantidade, valor_total, codigo_usuario, codigo_forma_pagamento, codigo_produto) VALUES (%s, %s, %s, %s, %s);
            """, (quantidade_a_ser_vendido, final_price, args['usuario'], args['forma_pagamento'], codigo_produto)
        )
        quantidade_resultante = quantidade_em_estoque - quantidade_a_ser_vendido
        connection.execute(
            f"""
            UPDATE produto SET quantidade = {quantidade_resultante} WHERE codigo = {args['codigo_produto']};
            """
        )
        connection.commit()

        response = retrieve_last_created('venda')

        for k, v in response.items():
            if isinstance(v, datetime):
                response[k] = str(v)

        return response
