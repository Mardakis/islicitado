import bcrypt
import logging
from config.db_config import get_db_connection

class AuthController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def autenticar(self, usuario, senha):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE nome = %s", (usuario,))
            resultado = cursor.fetchone()
            conn.close()
            
            if not resultado:
                return {'sucesso': False, 'mensagem': 'Usuário ou senha inválidos'}
            
            if self.verificar_senha(senha, resultado['senha']):
                self.logger.info(f"Login bem-sucedido para usuário: {usuario}")
                return {
                    'sucesso': True,
                    'mensagem': 'Login realizado com sucesso',
                    'usuario': resultado['nome'],
                    'admin': resultado.get('admin', False)
                }
            else:
                self.logger.warning(f"Tentativa de login mal-sucedida para usuário: {usuario}")
                return {'sucesso': False, 'mensagem': 'Usuário ou senha inválidos'}
        
        except Exception as e:
            self.logger.error(f"Erro durante autenticação: {str(e)}")
            return {'sucesso': False, 'mensagem': f'Erro durante autenticação: {str(e)}'}

    def hash_senha(self, senha_texto):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(senha_texto.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verificar_senha(self, senha_texto, senha_hash):
        return bcrypt.checkpw(senha_texto.encode('utf-8'), senha_hash.encode('utf-8'))

    def criar_usuario(self, nome_usuario, senha, admin=False):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuario WHERE nome = %s", (nome_usuario,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return {'sucesso': False, 'mensagem': 'Nome de usuário já existe'}
            
            senha_hash = self.hash_senha(senha)
            cursor.execute(
                "INSERT INTO usuario (nome, senha, admin) VALUES (%s, %s, %s)",
                (nome_usuario, senha_hash, admin)
            )
            conn.commit()
            conn.close()

            self.logger.info(f"Usuário criado: {nome_usuario}, admin: {admin}")
            return {'sucesso': True, 'mensagem': 'Usuário criado com sucesso'}
        
        except Exception as e:
            self.logger.error(f"Erro ao criar usuário: {str(e)}")
            return {'sucesso': False, 'mensagem': f'Erro ao criar usuário: {str(e)}'}


# === FUNÇÕES AUXILIARES ATUALIZADAS COM BCRYPT ===

def verificar_ou_criar_admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuario WHERE perfil = 'admin'")
    admin = cursor.fetchone()

    if not admin:
        usuario = "admin"
        senha = "admin123"
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
        perfil = "admin"

        cursor.execute("""
            INSERT INTO usuario (nome, senha, perfil)
            VALUES (%s, %s, %s)
        """, (usuario, senha_hash, perfil))
        conn.commit()

        print("🛡️ Usuário administrador criado:")
        print(f"   Login: {usuario}")
        print(f"   Senha: {senha}")

    cursor.close()
    conn.close()


def criar_usuario(nome_usuario, senha, perfil):
    conn = get_db_connection()
    cursor = conn.cursor()
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    cursor.execute("INSERT INTO usuario (nome, senha, perfil) VALUES (%s, %s, %s)",
                   (nome_usuario, senha_hash, perfil))
    conn.commit()
    cursor.close()
    conn.close()


def alterar_senha_usuario(usuario_id, nova_senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()

    cursor.execute("UPDATE usuario SET senha = %s WHERE id = %s", (senha_hash, usuario_id))
    conn.commit()
    cursor.close()
    conn.close()
