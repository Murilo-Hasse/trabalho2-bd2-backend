from typing import TypedDict
from abc import ABC

class Endereco(TypedDict):
    logradouro: str
    numero: int
    cep: str
    bairro: str
    codigo: None | int
    

class ProdutoList(TypedDict):
    codigo: None | int
    descricao: str
    valor: float
    quantidade: int
    imagem: None | str
    fornecedor: str
    grupo: str
    