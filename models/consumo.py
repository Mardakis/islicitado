from config.db_config import get_db_connection
from datetime import datetime

class Consumo:
    def __init__(self, id=None, item_id=None, usuario_id=None, quantidade=0, data_consumo=None):
        self.id = id
        self.item_id = item_id
        self.usuario_id = usuario_id
        self.quantidade = quantidade
        self.data_consumo = data_consumo or datetime.now()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.id is None:
            query = """
                INSERT INTO consumo (item_id, usuario_id, quantidade, data_consumo)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.item_id, self.usuario_id, self.quantidade, self.data_consumo))
            self.id = cursor.lastrowid
        else:
            query = """
                UPDATE consumo
                SET item_id=%s, usuario_id=%s, quantidade=%s, data_consumo=%s
                WHERE id=%s
            """
            cursor.execute(query, (self.item_id, self.usuario_id, self.quantidade, self.data_consumo, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_by_item_id(item_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM consumo WHERE item_id = %s", (item_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM consumo")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result