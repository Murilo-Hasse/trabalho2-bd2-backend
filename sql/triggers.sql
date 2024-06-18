CREATE OR REPLACE FUNCTION user_table_to_user()
RETURNS TRIGGER AS $$
DECLARE
    last_user pessoa%ROWTYPE;
    documento TEXT;
    passwd TEXT;
BEGIN
    SELECT * INTO last_user 
    FROM pessoa 
    ORDER BY codigo DESC 
    LIMIT 1;

    documento := quote_ident(last_user.documento);
    passwd := last_user.senha;

    EXECUTE 'CREATE USER ' || documento || ' WITH PASSWORD ' || quote_literal(passwd);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER create_user
AFTER INSERT ON pessoa
FOR EACH ROW
EXECUTE FUNCTION user_table_to_user();


