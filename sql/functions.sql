CREATE OR REPLACE FUNCTION cadastrar_venda (
    codigo_produto INTEGER,
    quantidade_a_vender INTEGER,
    usuario INTEGER,
    forma_pagamento INTEGER
)
RETURNS venda AS $$
DECLARE
    quantidade_estoque INTEGER;
    quantidade_resultante INTEGER;
    valor_produto FLOAT;
    valor_total_compra FLOAT;
    resultado venda%ROWTYPE;
BEGIN
    --Pega a quantidade em estoque e joga na variável
    SELECT 
        quantidade 
    INTO quantidade_estoque 
    FROM produto 
    WHERE codigo = codigo_produto;

    --Verifica se a quantidade a ser vendida é maior que a do estoque
    --Se for maior, então ele lança uma exception (ROLLBACK)
    IF quantidade_a_vender > quantidade_estoque THEN
        RAISE EXCEPTION 'A quantidade em estoque desse produto é menor que a quantidade a ser comprada!';
    END IF;

    --Pega o valor do produto individual e depois calcula o valor total com base na quantidade
    SELECT
        valor
    INTO valor_produto
    FROM produto
    WHERE codigo = codigo_produto;

    valor_total_compra := valor_produto * quantidade_a_vender;

    --Registra a venda do item
    INSERT INTO venda(
        quantidade,
        valor_total,
        codigo_usuario,
        codigo_forma_pagamento,
        codigo_produto
    )
    VALUES (quantidade_a_vender, valor_total_compra, usuario, forma_pagamento, codigo_produto);

    --Atualiza a quantidade em estoque
    quantidade_resultante := quantidade_estoque - quantidade_a_vender;

    UPDATE produto SET quantidade = quantidade_resultante WHERE codigo = codigo_produto;

    --Retorna o item que acabou de ser criado
    SELECT * INTO resultado FROM venda ORDER BY codigo DESC LIMIT 1;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cadastrar_usuario(
    nome VARCHAR,
    email_in VARCHAR,
    documento VARCHAR,
    senha VARCHAR,
    logradouro VARCHAR,
    numero INTEGER,
    cep VARCHAR,
    bairro VARCHAR
)
RETURNS pessoa AS $$
DECLARE
    codigo_endereco INTEGER;
    resultado pessoa%ROWTYPE;
BEGIN
    IF EXISTS (SELECT 1 FROM pessoa WHERE email = email_in) THEN
        RAISE EXCEPTION 'Usuário já cadastrado';
    END IF;
    --Insere o novo endereço do novo usuário
    INSERT INTO endereco (logradouro, numero, cep, bairro) 
    VALUES (
        logradouro,
        numero,
        cep,
        bairro
    );

    --Pega o código desse último endereço criado (para colocar no usuário)
    SELECT codigo INTO codigo_endereco FROM endereco ORDER BY codigo DESC LIMIT 1;

    INSERT INTO pessoa (nome, email, documento, senha, codigo_endereco)
    VALUES (
        nome,
        email_in,
        documento,
        senha,
        codigo_endereco
    );

    SELECT * INTO resultado FROM pessoa ORDER BY codigo DESC LIMIT 1;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;
