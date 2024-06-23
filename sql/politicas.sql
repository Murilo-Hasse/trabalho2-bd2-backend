--Habilita o controle de acesso na tabela
ALTER TABLE pessoa ENABLE ROW LEVEL SECURITY;

--Politica do acesso próprio, usuarios convencionais (usuários da aplicação), só terão acesso aos seus próprios dados, a forma de garantir isso tornando a visibilidade dos dados das tabelas apenas aqueles que o documento for igual 
CREATE POLICY acesso_proprio_pessoa
ON pessoa
FOR SELECT
TO grupo_usuario
USING (email  = current_user); 

ALTER TABLE pessoa FORCE ROW LEVEL SECURITY;
-------------------------------------------------
--Habilita o controle de acesso na tabela
ALTER TABLE venda ENABLE ROW LEVEL SECURITY;
 
CREATE POLICY acesso_proprio_venda
ON venda
FOR SELECT
TO grupo_usuario
USING (EXISTS (
        SELECT 1
        FROM pessoa AS P
        WHERE P.codigo = venda.codigo_usuario
          AND P.email = current_user
    ));

ALTER TABLE pessoa FORCE ROW LEVEL SECURITY;
