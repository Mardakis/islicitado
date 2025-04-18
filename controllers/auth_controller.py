import bcrypt
from config.db_config import get_db_connection
import logging

class AuthController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def autenticar(self, usuario, senha):
        """
        Autentica um usuário no sistema
        
        Args:
            usuario (str): Nome de usuário
            senha (str): Senha do usuário
            
        Returns:
            dict: Resultado da autenticação com status e informações
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Buscar usuário pelo nome de usuário
            cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (usuario,))
            resultado = cursor.fetchone()
            conn.close()
            
            if not resultado:
                return {
                    'sucesso': False,
                    'mensagem': 'Usuário ou senha inválidos'
                }
            
            # Verificar a senha
            # Nota: Precisará atualizar o banco para usar hashes
            # Para implementação inicial, mantive a lógica atual para comparação direta
            if resultado['senha'] == senha:
                # Log de sucesso
                self.logger.info(f"Login bem-sucedido para usuário: {usuario}")
                
                return {
                    'sucesso': True,
                    'mensagem': 'Login realizado com sucesso',
                    'usuario': resultado['usuario'],
                    'admin': bool(resultado['admin'])
                }
            else:
                # Log de falha
                self.logger.warning(f"Tentativa de login mal-sucedida para usuário: {usuario}")
                
                return {
                    'sucesso': False,
                    'mensagem': 'Usuário ou senha inválidos'
                }
        
        except Exception as e:
            self.logger.error(f"Erro durante autenticação: {str(e)}")
            return {
                'sucesso': False,
                'mensagem': f'Erro durante autenticação: {str(e)}'
            }
    
    def hash_senha(self, senha_texto):
        """
        Gera um hash seguro para a senha
        
        Args:
            senha_texto (str): Senha em texto puro
            
        Returns:
            str: Hash da senha
        """
        # Gerar salt aleatório
        salt = bcrypt.gensalt()
        
        # Gerar hash
        hashed = bcrypt.hashpw(senha_texto.encode('utf-8'), salt)
        
        # Retornar como string
        return hashed.decode('utf-8')
    
    def verificar_senha(self, senha_texto, senha_hash):
        """
        Verifica se uma senha corresponde ao hash armazenado
        
        Args:
            senha_texto (str): Senha em texto puro
            senha_hash (str): Hash armazenado
            
        Returns:
            bool: True se a senha estiver correta
        """
        return bcrypt.checkpw(senha_texto.encode('utf-8'), senha_hash.encode('utf-8'))
    
    def criar_usuario(self, nome_usuario, senha, admin=False):
        """
        Cria um novo usuário no sistema
        
        Args:
            nome_usuario (str): Nome do usuário
            senha (str): Senha em texto puro
            admin (bool): Se o usuário é administrador
            
        Returns:
            dict: Resultado da operação
        """
        try:
            # Verificar se usuário já existe
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuario WHERE nome = %s", (nome_usuario,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return {
                    'sucesso': False,
                    'mensagem': 'Nome de usuário já existe'
                }
            
            # Hash da senha
            senha_hash = self.hash_senha(senha)
            
            # Inserir usuário
            cursor.execute(
                "INSERT INTO usuario (nome, senha, admin) VALUES (%s, %s, %s)",
                (nome_usuario, senha_hash, admin)
            )
            conn.commit()
            conn.close()
            
            self.logger.info(f"Usuário criado: {nome_usuario}, admin: {admin}")
            return {
                'sucesso': True,
                'mensagem': 'Usuário criado com sucesso'
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao criar usuário: {str(e)}")
            return {
                'sucesso': False,
                'mensagem': f'Erro ao criar usuário: {str(e)}'
            }
import hashlib
from config.db_config import get_db_connection

def verificar_ou_criar_admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuario WHERE perfil = 'admin'")
    admin = cursor.fetchone()

    if not admin:
        usuario = "admin"
        senha = "admin123"
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
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
import hashlib
from config.db_config import get_db_connection

def criar_usuario(nome_usuario, senha, perfil):
    conn = get_db_connection()
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    cursor.execute("INSERT INTO usuario (nome, senha, perfil) VALUES (%s, %s, %s)",
                   (nome_usuario, senha_hash, perfil))
    conn.commit()
    cursor.close()
    conn.close()

def alterar_senha_usuario(usuario_id, nova_senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()

    cursor.execute("UPDATE usuario SET senha = %s WHERE id = %s", (senha_hash, usuario_id))
    conn.commit()
    cursor.close()
    conn.close()

def excluir_usuario(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuario WHERE id = %s", (usuario_id,))
    conn.commit()
    cursor.close()
    conn.close()

def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, usuario, perfil FROM usuario ORDER BY nome")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios
