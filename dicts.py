from typing import TypedDict
from abc import ABC

class Endereco(TypedDict):
    logradouro: str
    numero: int
    cep: str
    bairro: str
    codigo: None | int