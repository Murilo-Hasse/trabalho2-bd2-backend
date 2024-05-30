from abc import ABC, abstractmethod
from flask_restful import abort
from http import HTTPStatus
import dicts

class Validator(ABC):
    def __init__(self, obj) -> None:
        self.__obj = obj
        self.validate(self.__obj)
    
    @abstractmethod
    def validate(self, value): ...
    

class EnderecoValidator(Validator):
    def validate(self, obj: dicts.Endereco):
        self.validate_cep(obj['cep'])
        
    def validate_cep(self, cep: str):
        if '-' in cep:
            abort(HTTPStatus.BAD_REQUEST, message="O CEP deve ser apenas números")
            
        if len(cep) != 8:
            abort(HTTPStatus.BAD_REQUEST, message="O CEP informado não é valido")
        