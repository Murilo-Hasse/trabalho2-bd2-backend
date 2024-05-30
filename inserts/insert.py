import sqlite3
from pathlib import Path    

ROOT_FOLDER = Path(__file__).parent.parent
DATABASE_PATH = ROOT_FOLDER / 'db.sqlite3'
INSERTS_FOLDER = ROOT_FOLDER / 'inserts'

if __name__ == '__main__':
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    
    files = [str(file) for file in INSERTS_FOLDER.iterdir() if str(file).endswith('.sql')]
    
    for file in files:
        with open(file, 'r') as file:
            content = file.readlines()
            for line in content:
                cursor.execute(line)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    