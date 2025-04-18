from config.db_config import get_db_connection
from datetime import datetime

class Anexo:
    def __init__(self, id=None, nome_arquivo=None, caminho=None, processo_id=None, data_upload=None):
        self.id = id
        self.nome_arquivo = nome_arquivo
        self.caminho = caminho
        self.processo_id = processo_id
        self.data_upload = data_upload or datetime.now()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.id is None:
            query = """
                INSERT INTO anexos (nome_arquivo, caminho, processo_id, data_upload)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.nome_arquivo, self.caminho, self.processo_id, self.data_upload))
            self.id = cursor.lastrowid
        else:
            query = """
                UPDATE anexos
                SET nome_arquivo = %s, caminho = %s, processo_id = %s, data_upload = %s
                WHERE id = %s
            """
            cursor.execute(query, (self.nome_arquivo, self.caminho, self.processo_id, self.data_upload, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_by_processo(processo_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM anexos WHERE processo_id = %s", (processo_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
