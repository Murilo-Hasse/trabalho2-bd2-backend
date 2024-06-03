from pony.orm import Database, Required, Optional, Set, PrimaryKey, set_sql_debug, db_session, select
from decimal import Decimal
from datetime import datetime

db = Database()

class Funcao(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    descricao = Required(str, max_len=63)
    pessoas = Set('Pessoa')


class Endereco(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    logradouro = Required(str, max_len=63)
    numero = Required(int)
    cep = Required(str, max_len=8)
    bairro = Required(str, max_len=63)
    pessoas = Set('Pessoa')


class Pessoa(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    nome = Required(str, max_len=45)
    senha = Required(str, max_len=50)
    funcao = Required(Funcao)
    endereco = Required(Endereco)
    contatos = Set('PessoaContato')
    produtos = Set('Produto')
    vendas = Set('Venda')


class TipoContato(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    descricao = Required(str, max_len=63)
    contatos = Set('PessoaContato')


class PessoaContato(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    pessoa = Required(Pessoa)
    tipo = Required(TipoContato)
    valor = Required(str, max_len=127)


class FormaDePagamento(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    descricao = Required(str, max_len=63)
    vendas = Set('Venda')
    

class Grupo(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    descricao = Required(str, max_len=63)
    produtos = Set('Produto')


class Produto(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    descricao = Required(str, max_len=255)
    valor = Required(Decimal, precision=10, scale=2)
    quantidade = Required(int)
    imagem = Optional(str, max_len=1023)
    fornecedor = Required(Pessoa)
    grupo = Required(Grupo)
    itens = Set('Item')


class Venda(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    horario = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    valor_total = Optional(Decimal, precision=10, scale=2)
    funcionario = Required(Pessoa)
    forma_pagamento = Required(FormaDePagamento)
    itens = Set('Item')


class Item(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    quantidade = Required(int)
    valor_parcial = Required(Decimal, precision=10, scale=2)
    produto = Required(Produto)
    venda = Required(Venda)


set_sql_debug(True)
db.bind(provider='sqlite', filename='db.sqlite3')
db.generate_mapping(create_tables=True)

if __name__ == '__main__':
    @db_session 
    def criar_funcao(nome_funcao: str) -> None:
        Funcao(descricao=nome_funcao)

    criar_funcao('Gerente')
        
    with db_session:
        query = Funcao.select(lambda func: func)[:]
        print(query[0].codigo, query[0].descricao)
