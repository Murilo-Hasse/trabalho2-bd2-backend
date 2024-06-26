CREATE OR REPLACE FUNCTION user_table_to_user()
RETURNS TRIGGER AS $$
DECLARE
    last_user pessoa%ROWTYPE;
    email TEXT;
    passwd TEXT;
BEGIN
    SELECT * INTO last_user 
    FROM pessoa 
    ORDER BY codigo DESC 
    LIMIT 1;

    email := quote_ident(last_user.email);
    passwd := last_user.senha;

	EXECUTE 'CREATE USER ' || email || ' WITH PASSWORD ' || quote_literal(passwd);
	EXECUTE 'ALTER GROUP grupo_usuario ADD USER ' || email;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER create_user
AFTER INSERT ON pessoa
FOR EACH ROW
EXECUTE FUNCTION user_table_to_user();
