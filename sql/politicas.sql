
GRANT SELECT ON pessoa TO grupo_usuario;

ALTER TABLE pessoa ENABLE ROW LEVEL SECURITY;

--Politica do acesso próprio, usuarios convencionais (usuários da aplicação), só terão acesso aos seus próprios dados, a forma de garantir isso tornando a visibilidade dos dados das tabelas apenas aqueles que o documento for igual 
CREATE POLICY acesso_proprio_pessoa
ON pessoa
FOR SELECT
TO grupo_usuario
USING (documento  = current_user);

ALTER TABLE pessoa FORCE ROW LEVEL SECURITY;
