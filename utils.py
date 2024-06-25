from dotenv import load_dotenv
from psycopg2 import OperationalError
from decorators import singleton
import dropbox
import base64
import os
from os import getenv
from typing import Any
import psycopg2


class WrongPasswordError(Exception):
    ...


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

        credentials = {
            'host': self.__host,
            'database': self.__database,
            'user': self.__user,
            'password': self.__password,
            'port': self.__port
        }
        try:
            self.__connection = psycopg2.connect(**credentials)
        except OperationalError:
            raise WrongPasswordError(
                f"Senha incorreta para o usuário '{self.__user}'")

        self.__cursor = self.__connection.cursor()

    def __del__(self):
        if hasattr(PostgresConnection, '__connection'):
            self.__connection.commit()
            self.__connection.close()
            self.__cursor.close()
        
    def commit(self) -> None:
        self.__connection.commit()

    def retrieve_many_from_query(self, query: str) -> list[dict[str, Any]]:
        self.__cursor.execute(query)

        columns = [desc[0] for desc in self.__cursor.description]
        values = self.__cursor.fetchall()

        result = []
        for value in values:
            row = dict(zip(columns, value))
            result.append(row)

        return result

    def retrieve_one_from_query(self, query) -> dict[str, Any]:
        self.__cursor.execute(query)

        columns = [desc[0] for desc in self.__cursor.description]
        values = self.__cursor.fetchall()[0]

        return dict(zip(columns, values))

    def rollback(self) -> None:
        self.__connection.rollback()

