from pony.orm import select, db_session
from abc import ABC, abstractmethod
from flask_restful import abort
from http import HTTPStatus
import models
import dicts
import re

class Validator(ABC):
    def __init__(self, obj) -> None:
        self.__obj = obj
        self.validate(self.__obj)
    
    @abstractmethod
    def validate(self, obj): ...
    

class EnderecoValidator(Validator):
    def validate(self, obj: dicts.Endereco):
        self.validate_cep(obj['cep'])
        
    def validate_cep(self, cep: str):
        if len(cep) != 8:
            abort(HTTPStatus.BAD_REQUEST, message="O CEP informado não é valido")
            

class ProdutoValidator(Validator):
    def validate(self, obj: dicts.Produto):
        self.validate_name(obj["descricao"])
        self.validate_number(obj["quantidade"], "quantidade")
        self.validate_number(obj["valor"], "preço")
        self.validate_group(obj["grupo"])
        self.validate_user(obj["fornecedor"])
        
        
    def validate_name(self, name: str) -> None:
        if len(name) < 5:
            abort(HTTPStatus.BAD_REQUEST, message="Nome inválido, diga um nome maior")
        
        padrao = re.compile(r'^[a-zA-Z0-9\s.,-]+$')
        abort(HTTPStatus.BAD_REQUEST, message="Nome inválido, tem caracteres inválidos") if not padrao.match(name) else None
    
    def validate_number(self, number: float | int, nome_campo: str) -> None:
        if number < 0.01:
            abort(HTTPStatus.BAD_REQUEST, message=f'O valor do {nome_campo} é inválido!')
            
    def validate_group(self, group_id: int):
        with db_session:
            codigo = select(max(grupo.codigo) for grupo in models.Grupo).first()
            if group_id > codigo:
                abort(HTTPStatus.BAD_REQUEST, message='O grupo informado não existe')
            
            group = select(grupo for grupo in models.Grupo if grupo.codigo == group_id)[:]
            if not group:
                abort(HTTPStatus.BAD_REQUEST, message='O grupo informado não existe')
    
    def validate_user(self, user_id: int):
        with db_session:
            codigo = select(max(pessoa.codigo) for pessoa in models.Pessoa).first()
            if user_id > codigo:
                abort(HTTPStatus.BAD_REQUEST, message='O fornecedor informado não existe')
            
            user = select(user for user in models.Pessoa if user.codigo == user_id)[:]
            if not user:
                abort(HTTPStatus.BAD_REQUEST, message='O fornecedor informado não existe')
            