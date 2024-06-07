CREATE OR REPLACE FUNCTION user_table_to_user()
RETURNS TRIGGER AS $$
DECLARE
    last_user usuario%ROWTYPE;
    usr VARCHAR;
    passwd VARCHAR;
BEGIN
    SELECT * INTO last_user 
    FROM usuario 
    ORDER BY codigo DESC 
    LIMIT 1;

    usr := last_user.nome;
    passwd := last_user.senha;

    CREATE USER usr WITH PASSWORD passwd;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER create_user
AFTER INSERT ON usuario
FOR EACH ROW
EXECUTE FUNCTION user_table_to_user();


