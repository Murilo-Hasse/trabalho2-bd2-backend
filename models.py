from pony.orm import Database, Required, Optional, Set, PrimaryKey
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


class FormaDePagamento(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    descricao = Required(str, max_len=63)
    vendas = Set('Venda')


class Produto(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    descricao = Required(str, max_len=255)
    valor = Required(Decimal, precision=10, scale=2)
    quantidade = Required(int)
    fornecedor = Required(Pessoa)
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


db.bind(provider='sqlite', filename='db.sqlite3')
db.generate_mapping(create_tables=True)
