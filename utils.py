from dotenv import load_dotenv
import dropbox
import base64
import os


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
