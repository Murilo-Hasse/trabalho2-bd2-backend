--grupo pra criação de cadastro
CREATE ROLE padrao with password '1234';

-- 2. Concessão de permissões para criar outros usuários
ALTER USER padrao WITH CREATEROLE;

-- 3. Concessão de permissões para inserir dados em uma tabela específica
GRANT INSERT ON minha_tabela TO padrao;

-- Revogar execução de todas as funções no esquema public (ou outro esquema específico)
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM padrao;

-- Revogar qualquer outra permissão que não seja necessária
REVOKE ALL ON SCHEMA public FROM padrao;

--Garante que usuario padrão possa executar a função de registro
GRANT EXECUTE ON FUNCTION user_table_to_user TO padrao;
GRANT TRIGGER ON pessoa TO padrao;

--------------------------------------------------------------
-- Criação do grupo de usuarios cadastrados
CREATE ROLE grupo_usuario;

--Dar permissão a consultar na tabela produto.
GRANT SELECT ON TABLE produto TO grupo_usuario;

--Dar permissão a consultar na tabela venda.
GRANT SELECT ON venda TO grupo_usuario;
