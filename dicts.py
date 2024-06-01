from typing import TypedDict
from abc import ABC

class Endereco(TypedDict):
    logradouro: str
    numero: int
    cep: str
    bairro: str
    codigo: None | int
    

class Produto(TypedDict):
    codigo: None | int
    descricao: None | str
    valor: None | float
    quantidade: None | int
    imagem: None | str
    fornecedor: None | str
    grupo: None | str
    extensao_imagem: None | str
    