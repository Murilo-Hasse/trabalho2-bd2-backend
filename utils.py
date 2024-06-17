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

    def execute(self, sql_command: str, *args) -> None:
        self.__cursor.execute(sql_command, *args)

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


def upload_image_to_dropbox(img_path: str, img_name: str) -> str:
    DROPBOX_IMG_FOLDER = '/imagens-trabalho-bd2/'
    ABSOLUTE_PATH = DROPBOX_IMG_FOLDER + img_name

    load_dotenv()

    access_token = os.getenv("DROPBOX_API_KEY")
    assert KeyError, 'Chave de API não encontrada nas variáveis de ambiente no sistema'

    dbx = dropbox.Dropbox(access_token)

    with open(img_path, 'rb') as file:
        dbx.files_upload(file.read(), ABSOLUTE_PATH)

    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
        ABSOLUTE_PATH)

    # transforma o link do dropbox em um link de imagem em si
    return shared_link_metadata.url.replace("www.dropbox.com", "dl.dropboxusercontent.com")


def decode_and_upload_to_dropbox(b64_img_str: str, img_name: str, img_extension: str) -> str:
    """Pega uma imagem em base64 e decodifica ela, depois salva em um arquivo na pasta /img/, e por fim, pega essa imagem e faz o upload dela no dropbox, retornando assim o URL feito pelo dropbox"""
    image_bytes = base64.b64decode(b64_img_str)

    with open(f"""img/{img_name}.{img_extension}""", 'wb') as file:
        file.write(image_bytes)

    url = upload_image_to_dropbox(
        f'img/{img_name}.{img_extension}', f'{img_name}.{img_extension}'
    )

    return url
