from config.db_config import get_db_connection
from datetime import datetime

class Log:
    def __init__(self, id=None, usuario_id=None, acao=None, descricao=None, data=None):
        self.id = id
        self.usuario_id = usuario_id
        self.acao = acao
        self.descricao = descricao
        self.data = data or datetime.now()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO logs (usuario_id, acao, descricao, data)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (self.usuario_id, self.acao, self.descricao, self.data))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM logs ORDER BY data DESC")
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return logs
