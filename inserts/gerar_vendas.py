import random

from ..utils import PostgresConnection

def gerar_venda():
    produto = 106
    while produto == 131:
        produto = random.randint(106, 143)
    forma_pagamento = random.randint(1, 4)
    pessoa = random.choice([i for i in range(1, 6)] + [j for j in range(17, 23)])
    quantidade = random.randint(1, 5)
    
    return f'SELECT inserir_venda({produto}, {quantidade}, {pessoa}, {forma_pagamento});'


if __name__ == '__main__':
    conn = PostgresConnection('postgres', 'admin')
    
    try:
        for _ in range(1, 1459):
            conn.retrieve_one_from_query(gerar_venda())
    except Exception as e:
        conn.rollback()

