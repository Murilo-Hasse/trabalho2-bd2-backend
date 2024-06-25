-- Criação do grupo de usuarios cadastrados
CREATE ROLE grupo_usuario;

--Dar permissão a consultar na tabela produto. Restrição pela politica do acesso prórpio
GRANT SELECT ON TABLE pessoa TO grupo_usuario;

--Dar permissão a consultar na tabela venda. Restrição pela politica do acesso prórpio
GRANT SELECT ON TABLE venda TO grupo_usuario;

--Dar permissão a consultar na tabela produto. Acesso total
GRANT SELECT ON TABLE produto TO grupo_usuario;

--Dar permissão a consultar na tabela grupo. Acesso total
GRANT SELECT ON TABLE grupo TO grupo_usuario;

--Dar permissão a consultar na tabela formapagamento. Acesso total
GRANT SELECT ON TABLE formapagamento TO grupo_usuario;

--Dar permissão para inserir e update na tabela produto. Acesso total
GRANT INSERT ON TABLE  produto TO grupo_usuario;
GRANT UPDATE ON produto TO grupo_usuario;
GRANT USAGE, UPDATE ON SEQUENCE produto_codigo_seq TO grupo_usuario;

--Dar permissão para inserir na tabela venda. Acesso total
GRANT INSERT ON TABLE  venda TO grupo_usuario;
GRANT USAGE, UPDATE ON SEQUENCE venda_codigo_seq TO grupo_usuario;

--Dar permissão de select na view fornecedor, usada para listar informações de produtos;
GRANT SELECT ON fornecedor TO grupo_usuario;
