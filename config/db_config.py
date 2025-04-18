import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conexao = mysql.connector.connect(
            host='localhost',          # ou IP do servidor
            user='root',               # usuário do banco
            password='admin', # altere para a senha do seu MySQL
            database='islicitado'      # nome do banco de dados
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"[Erro na conexão] {e}")
        return None
