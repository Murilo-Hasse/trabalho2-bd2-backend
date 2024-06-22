from flask_restful import Resource, abort
from flask import request
from utils import PostgresConnection, WrongPasswordError, decode_and_upload_to_dropbox
import serializers
from http import HTTPStatus
from typing import Any
from datetime import datetime
from psycopg2.errors import RaiseException, InsufficientPrivilege

admin_connection = PostgresConnection(user='postgres', password='admin')

connection_pool: dict[int, PostgresConnection] = {}


def connected(func):
    def wrapper(*args, **kwargs):
        user = request.headers.get('user')
        if not user:
            abort(
                HTTPStatus.BAD_REQUEST, message='Usuário não especificado nos Headers da request!'
            )
            return
        global connection_pool
        if int(user) not in connection_pool:
            abort(
                HTTPStatus.UNAUTHORIZED, message='Usuário não está logado'
            )
        connection = connection_pool.get(int(user))
        try:
            func(*args, **kwargs, connection=connection)
        except InsufficientPrivilege:
            connection.rollback() if connection is not None else None
            abort(
                HTTPStatus.FORBIDDEN, message='Você não tem privilégio o suficiente'
            )
        return
    return wrapper


def retrieve_last_created(table_name: str, connection: PostgresConnection) -> dict[str, Any]:
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

        args['user'] = args['user'].encode('utf-8').decode('utf-8')
        args['password'] = args['password'].encode('utf-8').decode('utf-8')

        try:
            pg_connection = PostgresConnection(**args)
        except WrongPasswordError as error:
            return abort(HTTPStatus.BAD_REQUEST, message=error.args)

        user_info = admin_connection.retrieve_one_from_query(
            f"""
            SELECT
                codigo,
                nome
            FROM
                pessoa
            WHERE
                email = '{args['user']}'
                AND
                senha = '{args['password']}'
            """
        )
        global connection_pool
        if user_info['codigo'] not in connection_pool:
            connection_pool[user_info['codigo']] = pg_connection

        return user_info


class Cadastro(Resource):
    def post(self):
        args: dict = serializers.user_post_serializer.parse_args()

        name = args['nome']
        email = args['email']
        documento = args['documento'] \
            .replace('.', '') \
            .replace('-', '') \
            .replace('/', '')
        senha = args['senha']
        logradouro = args['logradouro']
        numero = args['numero']
        cep = args['cep'].replace('.', '').replace('-', '')
        bairro = args['bairro']

        try:
            result = admin_connection.retrieve_one_from_query(f"""SELECT * FROM cadastrar_usuario(
                '{name}', '{email}', '{documento}', '{senha}', '{logradouro}',
                {numero}, '{cep}', '{bairro}'
            )""")

            admin_connection.commit()

            del result['senha']

            return result
        except RaiseException:
            admin_connection.rollback()
            abort(HTTPStatus.BAD_REQUEST, message="Usuário já está cadastrado!")


class GrupoList(Resource):
    """Classe responsável pelos métodos relacionados aos grupos, neste caso só tem o método GET, o qual irá retornar uma lista contendo todos os grupos"""
    @connected
    def get(self, connection: PostgresConnection):
        return connection.retrieve_many_from_query('SELECT * FROM grupo;')


class FormaPagamentoList(Resource):
    @connected
    def get(self, connection: PostgresConnection):
        return connection.retrieve_many_from_query('SELECT * FROM formapagamento;')


class ProdutoList(Resource):
    @connected
    def get(self, connection: PostgresConnection):
        query = """
        SELECT
            produto.codigo AS codigo,
            produto.nome AS nome,
            produto.descricao AS descricao,
            produto.valor AS valor,
            produto.quantidade AS quantidade,
            produto.imagem AS imagem,
            grupo.descricao AS grupo,
            pessoa.codigo AS codigo_fornecedor,
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
    def post(self, connection: PostgresConnection):
        args = serializers.produto_post_serializer.parse_args()

        img_b64 = args['imagem']
        img_extension = args['extensao_imagem']

        img_url = decode_and_upload_to_dropbox(
            img_b64, args['descricao'], img_extension
        )

        del args['extensao_imagem']

        args['imagem'] = img_url
        print(args)

        connection.execute(
            'INSERT INTO produto(nome, descricao, valor, quantidade, imagem, grupo, codigo_fornecedor) VALUES (%s ,%s, %s, %s, %s, %s, %s)',
            list(args.values())
        )
        connection.commit()
        return retrieve_last_created('produto', connection=connection)


class Produtos(Resource):
    @connected
    def get(self, produto_id, connection: PostgresConnection):
        query = f"""
        SELECT
            produto.codigo AS codigo,
            produto.nome AS nome,
            produto.descricao AS descricao,
            produto.valor AS valor,
            produto.quantidade AS quantidade,
            produto.imagem AS imagem,
            grupo.descricao AS grupo,
            pessoa.codigo AS codigo_fornecedor
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


class Compra(Resource):
    @connected
    def post(self, connection: PostgresConnection):
        """
        Método post de registro de vendas, ele começa pegando os argumentos do serializer,
        após isso, ele pega o valor do produto via banco, e também a quantidade que está em estoque,
        para daí checar se é maior que a da venda, se for, passa, se não for, retorna código 400,
        depois disso ele registra a venda, e faz um update na quantidade do item no banco
        para dai retornar o JSON resposa.
        """
        args = serializers.compra_serializer.parse_args()

        quantidade_a_ser_vendido = args['quantidade'] if args['quantidade'] else 1
        codigo_produto = args['codigo_produto']

        try:
            response = connection.retrieve_one_from_query(
                f'''SELECT * FROM cadastrar_venda(
                    {codigo_produto},
                    {quantidade_a_ser_vendido},
                    {args['usuario']},
                    {args['forma_pagamento']}
                )'''
            )
        except RaiseException:
            connection.rollback()
            abort(
                HTTPStatus.BAD_REQUEST,
                message='A quantidade de itens a ser comprada é maior que a quantidade de itens no estoque.'
            )
            return

        for k, v in response.items():
            if isinstance(v, datetime):
                response[k] = str(v)

        return response


class ComprasList(Resource):
    @connected
    def get(self, usuario_id, connection: PostgresConnection):
        response = connection.retrieve_many_from_query(
            f"""
            SELECT
                venda.codigo AS codigo,
                venda.horario AS horario,
                venda.quantidade AS quantidade,
                venda.valor_total AS valor_total,
                formapagamento.descricao AS forma_pagamento,
                produto.nome AS nome_produto,
                produto.imagem AS imagem_produto
            FROM
                venda
            INNER JOIN
                formapagamento
            ON venda.codigo_forma_pagamento = formapagamento.codigo
            INNER JOIN
                produto
            ON venda.codigo_produto = produto.codigo
            WHERE
                codigo_usuario = {usuario_id}
            """
        )
        for hasmap in response:
            for k, v in hasmap.items():
                if isinstance(v, datetime):
                    hasmap[k] = str(v)

        return response


class PessoaProdutos(Resource):
    """Classe destinada a mostrar todos os produtos que uma pessoa está vendendo"""
    @connected
    def get(self, connection: PostgresConnection, funcionario_id: int):
        return connection.retrieve_many_from_query(
            f"""
            SELECT
                produto.codigo AS codigo,
                produto.nome AS nome,
                produto.descricao AS descricao,
                produto.valor AS valor,
                produto.quantidade AS quantidade,
                produto.imagem AS imagem,
                grupo.descricao AS grupo,
                pessoa.codigo AS codigo_fornecedor,
                pessoa.nome AS fornecedor
            FROM
                produto
            INNER JOIN grupo
                ON produto.grupo = grupo.codigo
            INNER JOIN pessoa
                ON produto.codigo_fornecedor = pessoa.codigo
            WHERE
                produto.codigo_fornecedor = {funcionario_id};
            """
        )
