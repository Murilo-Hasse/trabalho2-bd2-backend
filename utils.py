from dotenv import load_dotenv
import dropbox
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
    
    #transforma o link do dropbox em um link de imagem em si
    return shared_link_metadata.url.replace("www.dropbox.com", "dl.dropboxusercontent.com")

if __name__ == "__main__":
    print(f'link da imagem = {upload_image_to_dropbox("img/ryzen_2.jpg", "ryzen_3.jpg")}')

