CREATE OR REPLACE PROCEDURE criar_usuario(nome_usuario VARCHAR, senha VARCHAR)
AS $$
BEGIN
    CREATE USER nome_usuario WITH PASSWORD senha;
END;
$$ LANGUAGE plpgsql;