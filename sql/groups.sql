-- Criação do grupo de usuarios cadastrados
CREATE ROLE grupo_usuario;

--Dar permissão a consultar na tabela produto. Restrição pela politica do acesso prórpio
GRANT SELECT ON TABLE pessoa TO grupo_usuario;

--Dar permissão a consultar na tabela venda. Restrição pela politica do acesso prórpio
GRANT SELECT ON TABLE venda TO grupo_usuario;

--Dar permissão a consultar na tabela produto. Acesso total
GRANT SELECT ON TABLE produto TO grupo_usuario;

GRANT SELECT ON TABLE grupo TO grupo_usuario;

GRANT SELECT ON TABLE formapagamento TO grupo_usuario;

GRANT INSERT ON TABLE  produto TO grupo_usuario;

GRANT INSERT ON TABLE  venda TO grupo_usuario;
