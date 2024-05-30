from faker import Faker
from typing import Callable
import threading
import requests
import random
import os

faker = Faker('PT_BR', seed=854789547395743958)

NUMERO_FUNCOES = 3
NUMERO_GRUPOS = 6
NUMERO_TIPOS_CONTATOS = 3
FORMAS_PAGAMENTO = 4

def save_to_file(file_path: str):
    def wrapper(func: Callable[[int], str]):
        def inner(quantidade: int):
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass
            with open(file_path, 'w', encoding='utf-8') as file:
                lines_to_write = func(quantidade)
                file.write(lines_to_write)
        return inner
    return wrapper


def gerar_cep() -> int:
    primeiro_parte = 85601
    segundo_parte = str(random.randint(0, 999)).zfill(3)
    
    return f'{primeiro_parte}{segundo_parte}'


def gerar_cep_e_trazer_informacoes() -> dict:
    cep: int = gerar_cep()
    url = f'https://viacep.com.br/ws/{cep}/json/'
    data = requests.get(url).json()
    
    while('erro' in data):
        cep = gerar_cep()
        url = f'https://viacep.com.br/ws/{cep}/json/'
        data = requests.get(url).json()
        
    return data


enderecos_lock = threading.Lock()
enderecos = ''

def gerar_endereco() -> str:
    global enderecos
    data = gerar_cep_e_trazer_informacoes()
    logradouro = data['logradouro']
    cep = str(data['cep']).replace('-', '')
    bairro = data['bairro']
    numero = random.randint(1, 9999)
            
    query = f"INSERT INTO Endereco(logradouro, numero, cep, bairro) VALUES ('{logradouro}', {numero}, '{cep}', '{bairro}');\n"
    
    with enderecos_lock:
        enderecos += query


@save_to_file('inserts/enderecos.sql')
def gerar_varios_enderecos(quantidade: int) -> str:
    global enderecos
    enderecos = []  # Resetando a lista antes de gerar novos endereços
    
    threads = []
    for _ in range(quantidade):
        thread = threading.Thread(target=gerar_endereco)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return ''.join(enderecos)

if __name__ == '__main__':
    #gerar_varios_enderecos(820)
    ...
