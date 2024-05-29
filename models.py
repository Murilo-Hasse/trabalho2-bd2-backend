from pony.orm import Database, Required, Optional, Set, PrimaryKey
from pathlib import Path

CURRENT_PATH = Path(__file__).parent
DATABASE_PATH = CURRENT_PATH / 'db.sqlite3'

db = Database()


class Funcao(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    descricao = Required(str, max_len=63)
    
    
class Endereco(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    logradouro = Required(str, max_len=63)
    numero = Required(int)
    cep = Required(str, max_len=8)
    bairro = Required(str, max_len=63)
    
    
class Pessoa(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    nome = Required(str, max_len=45)
    senha = Required(str, max_len=50)
    funcao = Required(Funcao)
    endereco = Required(Endereco)
    
    

if __name__ == '__main__':
    db.bind(provider='sqlite', filename=DATABASE_PATH)
    db.generate_mapping(create_tables=True)