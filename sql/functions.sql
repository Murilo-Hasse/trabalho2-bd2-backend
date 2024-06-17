CREATE OR REPLACE FUNCTION cadastrar_venda (
    codigo_produto INTEGER
    quantidade_a_vender INTEGER,
    usuario INTEGER,
    forma_pagamento INTEGER
)
RETURNS venda%ROWTYPE AS $$
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