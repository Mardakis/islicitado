from config.db_config import get_db_connection
import logging

class Fornecedor:
    def __init__(self, id=None, cnpj=None, razao_social=None, nome_fantasia=None, 
                 email=None, telefone=None, endereco=None, cidade=None, estado=None, 
                 representante=None, situacao='Ativo'):
        self.id = id
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.representante = representante
        self.situacao = situacao  # Ativo, Inativo, Suspenso, etc.
        self.logger = logging.getLogger(__name__)
    
    def salvar(self):
        """Salva ou atualiza o fornecedor no banco de dados"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            if self.id is None:
                # Novo fornecedor
                cursor.execute(
                    """
                    INSERT INTO fornecedores (
                        cnpj, razao_social, nome_fantasia, email, telefone, 
                        endereco, cidade, estado, representante, situacao
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        self.cnpj, self.razao_social, self.nome_fantasia, self.email, 
                        self.telefone, self.endereco, self.cidade, self.estado, 
                        self.representante, self.situacao
                    )
                )
                self.id = cursor.lastrowid
            else:
                # Atualizar fornecedor existente
                cursor.execute(
                    """
                    UPDATE fornecedores SET 
                        cnpj = %s, 
                        razao_social = %s, 
                        nome_fantasia = %s, 
                        email = %s, 
                        telefone = %s, 
                        endereco = %s, 
                        cidade = %s, 
                        estado = %s, 
                        representante = %s, 
                        situacao = %s
                    WHERE id = %s
                    """,
                    (
                        self.cnpj, self.razao_social, self.nome_fantasia, self.email, 
                        self.telefone, self.endereco, self.cidade, self.estado, 
                        self.representante, self.situacao, self.id
                    )
                )
            
            conn.commit()
            self.logger.info(f"Fornecedor {self.razao_social} salvo com sucesso")
            return True
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Erro ao salvar fornecedor {self.razao_social}: {str(e)}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_id(fornecedor_id):
        """Busca um fornecedor pelo ID"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM fornecedores WHERE id = %s", (fornecedor_id,))
        resultado = cursor.fetchone()
        conn.close()
        
        if not resultado:
            return None
        
        return Fornecedor(
            id=resultado['id'],
            cnpj=resultado['cnpj'],
            razao_social=resultado['razao_social'],
            nome_fantasia=resultado['nome_fantasia'],
            email=resultado['email'],
            telefone=resultado['telefone'],
            endereco=resultado['endereco'],
            cidade=resultado['cidade'],
            estado=resultado['estado'],
            representante=resultado['representante'],
            situacao=resultado['situacao']
        )
    
    @staticmethod
    def buscar_por_cnpj(cnpj):
        """Busca um fornecedor pelo CNPJ"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM fornecedores WHERE cnpj = %s", (cnpj,))
        resultado = cursor.fetchone()
        conn.close()
        
        if not resultado:
            return None
        
        return Fornecedor(
            id=resultado['id'],
            cnpj=resultado['cnpj'],
            razao_social=resultado['razao_social'],
            nome_fantasia=resultado['nome_fantasia'],
            email=resultado['email'],
            telefone=resultado['telefone'],
            endereco=resultado['endereco'],
            cidade=resultado['cidade'],
            estado=resultado['estado'],
            representante=resultado['representante'],
            situacao=resultado['situacao']
        )
    
    @staticmethod
    def listar_todos(apenas_ativos=True):
        """Lista todos os fornecedores"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if apenas_ativos:
            cursor.execute("SELECT * FROM fornecedores WHERE situacao = 'Ativo' ORDER BY razao_social")
        else:
            cursor.execute("SELECT * FROM fornecedores ORDER BY razao_social")
            
        resultados = cursor.fetchall()
        conn.close()
        
        return [Fornecedor(
            id=row['id'],
            cnpj=row['cnpj'],
            razao_social=row['razao_social'],
            nome_fantasia=row['nome_fantasia'],
            email=row['email'],
            telefone=row['telefone'],
            endereco=row['endereco'],
            cidade=row['cidade'],
            estado=row['estado'],
            representante=row['representante'],
            situacao=row['situacao']
        ) for row in resultados]
    
    @staticmethod
    def buscar(filtros=None):
        """Busca fornecedores com base nos filtros fornecidos"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM fornecedores WHERE 1=1"
        params = []
        
        if filtros:
            if 'cnpj' in filtros and filtros['cnpj']:
                query += " AND cnpj LIKE %s"
                params.append(f"%{filtros['cnpj']}%")
            
            if 'razao_social' in filtros and filtros['razao_social']:
                query += " AND razao_social LIKE %s"
                params.append(f"%{filtros['razao_social']}%")
            
            if 'nome_fantasia' in filtros and filtros['nome_fantasia']:
                query += " AND nome_fantasia LIKE %s"
                params.append(f"%{filtros['nome_fantasia']}%")
                
            if 'cidade' in filtros and filtros['cidade']:
                query += " AND cidade LIKE %s"
                params.append(f"%{filtros['cidade']}%")
                
            if 'estado' in filtros and filtros['estado']:
                query += " AND estado = %s"
                params.append(filtros['estado'])
                
            if 'situacao' in filtros and filtros['situacao']:
                query += " AND situacao = %s"
                params.append(filtros['situacao'])
        
        query += " ORDER BY razao_social"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        
        return [Fornecedor(
            id=row['id'],
            cnpj=row['cnpj'],
            razao_social=row['razao_social'],
            nome_fantasia=row['nome_fantasia'],
            email=row['email'],
            telefone=row['telefone'],
            endereco=row['endereco'],
            cidade=row['cidade'],
            estado=row['estado'],
            representante=row['representante'],
            situacao=row['situacao']
        ) for row in resultados]
