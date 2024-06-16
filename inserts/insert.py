import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from os import getenv

ROOT_FOLDER = Path(__file__).parent.parent
INSERTS_FOLDER = ROOT_FOLDER / 'inserts'


class PostgresConnection:
    def __init__(self, user: str | None = None, password: str | None = None) -> None:
        load_dotenv()
        self.__host: str | None = getenv('HOST')
        self.__database: str | None = getenv('DATABASE')
        self.__user: str | None = user
        self.__password: str | None = password
        self.__port: str | None = getenv('PORT')

        if self.__port is None:
            self.__port = '5432'

        __credentials = {
            'host': self.__host,
            'database': self.__database,
            'user': self.__user,
            'password': self.__password,
            'port': self.__port
        }
        self.__connection = psycopg2.connect(**__credentials)

        self.__cursor = self.__connection.cursor()

    def __del__(self):
        self.__cursor.close() if hasattr(PostgresConnection, '__cursor') else None
        if hasattr(PostgresConnection, '__connection'):
            self.__connection.commit()
            self.__connection.close()

    def execute(self, sql_command: str) -> None:
        self.__cursor.execute(sql_command)

    def commit(self) -> None:
        self.__connection.commit()


if __name__ == '__main__':
    connection = PostgresConnection('postgres', 'admin')

    files = [str(file) for file in INSERTS_FOLDER.iterdir()
             if str(file).endswith('.sql')]

    files.sort()

    for file in files:
        with open(file, 'r', encoding='utf-8') as file:
            content = file.readlines()
            for line in content:
                connection.execute(line)

    connection.commit()
