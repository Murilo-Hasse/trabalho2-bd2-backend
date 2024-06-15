DROP TABLE IF EXISTS item CASCADE;
DROP TABLE IF EXISTS produto CASCADE;
DROP TABLE IF EXISTS venda CASCADE;
DROP TABLE IF EXISTS pessoacontato CASCADE;
DROP TABLE IF EXISTS pessoa CASCADE;
DROP TABLE IF EXISTS tipocontato CASCADE;
DROP TABLE IF EXISTS formapagamento CASCADE;
DROP TABLE IF EXISTS endereco CASCADE;
DROP TABLE IF EXISTS funcao CASCADE;
DROP TABLE IF EXISTS grupo;


CREATE TABLE IF NOT EXISTS funcao (
    codigo SERIAL PRIMARY KEY,
    descricao VARCHAR(63) NOT NULL
);

CREATE TABLE IF NOT EXISTS endereco (
    codigo SERIAL PRIMARY KEY,
    logradouro VARCHAR(63) NOT NULL,
    numero INTEGER NOT NULL,
    cep VARCHAR(8),
    bairro VARCHAR(63)
);

CREATE TABLE IF NOT EXISTS pessoa (
    codigo BIGSERIAL PRIMARY KEY,
    nome VARCHAR(45) NOT NULL,
    documento VARCHAR(14) NOT NULL,
    senha VARCHAR(50) NOT NULL,
    codigo_funcao INTEGER,
    codigo_endereco INTEGER,
    FOREIGN KEY (codigo_funcao) REFERENCES funcao(codigo)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (codigo_endereco) REFERENCES endereco(codigo)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS tipocontato (
    codigo SERIAL PRIMARY KEY,
    descricao VARCHAR(63) NOT NULL
);

CREATE TABLE IF NOT EXISTS pessoacontato (
    codigo_pessoa INTEGER,
    codigo_tipo INTEGER,
    PRIMARY KEY (codigo_pessoa, codigo_tipo),
    FOREIGN KEY (codigo_pessoa) REFERENCES pessoa(codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (codigo_tipo) REFERENCES tipocontato(codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS formapagamento (
    codigo SERIAL PRIMARY KEY,
    descricao VARCHAR(63) NOT NULL
);

CREATE TABLE IF NOT EXISTS grupo (
    codigo SERIAL PRIMARY KEY,
    descricao VARCHAR(63) NOT NULL
);

CREATE TABLE IF NOT EXISTS venda (
    codigo BIGSERIAL PRIMARY KEY,
    horario TIMESTAMP DEFAULT (NOW()::TIMESTAMP(0)) NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    codigo_funcionario INTEGER NOT NULL,
    codigo_forma_pagamento INTEGER NOT NULL,
    FOREIGN KEY (codigo_funcionario) REFERENCES pessoa(codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (codigo_forma_pagamento) REFERENCES formapagamento(codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS produto (
    codigo BIGSERIAL PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    imagem VARCHAR(1023),
    quantidade INTEGER NOT NULL,
    codigo_fornecedor INTEGER NOT NULL,
    grupo INTEGER NOT NULL,
    FOREIGN KEY (codigo_fornecedor) REFERENCES pessoa(codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (grupo) REFERENCES grupo(codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS item (
    codigo BIGSERIAL PRIMARY KEY,
    quantidade INTEGER NOT NULL,
    valor_parcial DECIMAL(10, 2),
    codigo_produto INTEGER NOT NULL,
    codigo_venda INTEGER NOT NULL,
    FOREIGN KEY (codigo_produto) REFERENCES produto(codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (codigo_venda) REFERENCES venda(codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);