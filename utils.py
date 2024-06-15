from dotenv import load_dotenv
from psycopg2 import OperationalError
from exceptions import WrongPasswordError
from decorators import singleton
import dropbox
import base64
import os
from os import getenv
from typing import Any
import psycopg2


class PostgresConnection:
    def __init__(self, user: str | None=None, password: str | None=None) -> None:
        load_dotenv()
        self.__host: str | None = getenv('HOST')
        self.__database: str | None = getenv('DATABASE')
        self.__user: str | None = user
        self.__password: str | None = password
        self.__port: str | None = getenv('PORT')

        if self.__port is None:
            self.__port = '5432'

        self.__credentials = {
            'host': self.__host,
            'database': self.__database,
            'user': self.__user,
            'password': self.__password,
            'port': self.__port
        }
        try:
            self.__connection = psycopg2.connect(**self.__credentials)
        except OperationalError:
            raise WrongPasswordError(f"Senha incorreta para o usuário '{self.__user}'")
            
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
    
    def retrieve_from_query(self, query: str) -> list[dict[str, Any]]:
        self.__cursor.execute(query)
        
        columns = [desc[0] for desc in self.__cursor.description]
        values = self.__cursor.fetchall()
        print(values)
        


def upload_image_to_dropbox(img_path: str, img_name: str) -> str:
    DROPBOX_IMG_FOLDER = '/imagens-trabalho-bd2/'
    ABSOLUTE_PATH = DROPBOX_IMG_FOLDER + img_name

    load_dotenv()

    access_token = os.getenv("DROPBOX_API_KEY")
    assert KeyError, 'Chave de API não encontrada nas variáveis de ambiente no sistema'

    dbx = dropbox.Dropbox(access_token)

    with open(img_path, 'rb') as file:
        dbx.files_upload(file.read(), ABSOLUTE_PATH)

    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(ABSOLUTE_PATH)

    # transforma o link do dropbox em um link de imagem em si
    return shared_link_metadata.url.replace("www.dropbox.com", "dl.dropboxusercontent.com")


def decode_b64_to_img(b64_str: str, nome_arquivo: str, extensao_img: str) -> None:
    image_bytes = base64.b64decode(b64_str)

    with open(f"""img/{nome_arquivo}.{extensao_img}""", 'wb') as file:
        file.write(image_bytes)


def decode_and_upload_to_dropbox(b64_img_str: str, img_name: str, img_extension: str) -> str:
    decode_b64_to_img(b64_img_str, img_name, img_extension)
    url = upload_image_to_dropbox(f'img/{img_name}.{img_extension}', f'{img_name}.{img_extension}')

    return url


if __name__ == "__main__":
    with open('img/img_b64.txt') as file:
        b64_img = file.read()

    print(decode_and_upload_to_dropbox(b64_img, 'ryzen', 'jpeg'))
