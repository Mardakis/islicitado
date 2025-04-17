from config.db_config import conectar
import logging
from utils.constants import PERMISSOES

class Usuario:
    def __init__(self, id=None, nome=None, usuario=None, email=None, 
                 tipo=None, permissoes=None, ativo=True):
        self.id = id
        self.nome = nome
        self.usuario = usuario
        self.email = email
        self.tipo = tipo  # 'admin', 'gestor', 'usuario'
        self.permissoes = permissoes or []  # Lista de permissões
        self.ativo = ativo
        self.logger = logging.getLogger(__name__)
    
    def tem_permissao(self, permissao):
        """Verifica se o usuário tem uma permissão específica"""
        # Administradores têm todas as permissões
        if self.tipo == 'admin':
            return True
            
        # Verificar nas permissões específicas
        return permissao in self.permissoes
    
    def salvar(self):
        """Salva ou atualiza o usuário no banco de dados"""
        conn = conectar()
        cursor = conn.cursor()
        
        try:
            if self.id is None:
                # Novo usuário
                cursor.execute(
                    """
                    INSERT INTO usuarios (nome, usuario, email, tipo, ativo) 
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (self.nome, self.usuario, self.email, self.tipo, self.ativo)
                )
                self.id = cursor.lastrowid
                
                # Salvar permissões
                for permissao in self.permissoes:
                    cursor.execute(
                        "INSERT INTO usuario_permissoes (usuario_id, permissao) VALUES (%s, %s)",
                        (self.id, permissao)
                    )
            else:
                # Atualizar usuário existente
                cursor.execute(
                    """
                    UPDATE usuarios SET 
                        nome = %s, 
                        usuario = %s, 
                        email = %s, 
                        tipo = %s,
                        ativo = %s
                    WHERE id = %s
                    """,
                    (self.nome, self.usuario, self.email, self.tipo, self.ativo, self.id)
                )
                
                # Atualizar permissões
                cursor.execute("DELETE FROM usuario_permissoes WHERE usuario_id = %s", (self.id,))
                for permissao in self.permissoes:
                    cursor.execute(
                        "INSERT INTO usuario_permissoes (usuario_id, permissao) VALUES (%s, %s)",
                        (self.id, permissao)
                    )
            
            conn.commit()
            self.logger.info(f"Usuário {self.usuario} salvo com sucesso")
            return True
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Erro ao salvar usuário {self.usuario}: {str(e)}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_id(usuario_id):
        """Busca um usuário pelo ID"""
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            conn.close()
            return None
        
        # Buscar permissões
        cursor.execute(
            "SELECT permissao FROM usuario_permissoes WHERE usuario_id = %s", 
            (usuario_id,)
        )
        permissoes = [row['permissao'] for row in cursor.fetchall()]
        
        conn.close()
        
        return Usuario(
            id=resultado['id'],
            nome=resultado['nome'],
            usuario=resultado['usuario'],
            email=resultado['email'],
            tipo=resultado['tipo'],
            permissoes=permissoes,
            ativo=resultado['ativo']
        )
    
    @staticmethod
    def buscar_por_usuario(nome_usuario):
        """Busca um usuário pelo nome de usuário"""
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (nome_usuario,))
        resultado = cursor.fetchone()
        
        if not resultado:
            conn.close()
            return None
        
        # Buscar permissões
        cursor.execute(
            "SELECT permissao FROM usuario_permissoes WHERE usuario_id = %s", 
            (resultado['id'],)
        )
        permissoes = [row['permissao'] for row in cursor.fetchall()]
        
        conn.close()
        
        return Usuario(
            id=resultado['id'],
            nome=resultado['nome'],
            usuario=resultado['usuario'],
            email=resultado['email'],
            tipo=resultado['tipo'],
            permissoes=permissoes,
            ativo=resultado['ativo']
        )
    
    @staticmethod
    def listar_todos(apenas_ativos=True):
        """Lista todos os usuários"""
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        
        if apenas_ativos:
            cursor.execute("SELECT * FROM usuarios WHERE ativo = 1 ORDER BY nome")
        else:
            cursor.execute("SELECT * FROM usuarios ORDER BY nome")
            
        resultados = cursor.fetchall()
        usuarios = []
        
        for row in resultados:
            # Buscar permissões
            cursor.execute(
                "SELECT permissao FROM usuario_permissoes WHERE usuario_id = %s", 
                (row['id'],)
            )
            permissoes = [p_row['permissao'] for p_row in cursor.fetchall()]
            
            usuario = Usuario(
                id=row['id'],
                nome=row['nome'],
                usuario=row['usuario'],
                email=row['email'],
                tipo=row['tipo'],
                permissoes=permissoes,
                ativo=row['ativo']
            )
            usuarios.append(usuario)
        
        conn.close()
        return usuarios
