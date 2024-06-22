-- Criação do grupo de usuarios cadastrados
CREATE ROLE grupo_usuario;

--Dar permissão a consultar na tabela produto. Restrição pela politica do acesso prórpio
GRANT SELECT ON TABLE produto TO grupo_usuario;

--Dar permissão a consultar na tabela venda. Restrição pela politica do acesso prórpio
GRANT SELECT ON venda TO grupo_usuario;

--Dar permissão a consultar na tabela produto. Acesso total
GRANT SELECT ON produto TO grupo_usuario;
