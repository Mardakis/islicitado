from config.db_config import conectar
from datetime import datetime
import logging

class LogService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def registrar_acao(self, usuario_id, tipo_acao, descricao, referencia_id=None, tabela_referencia=None):
        """
        Registra uma ação no sistema para fins de auditoria
        
        Args:
            usuario_id (int): ID do usuário que realizou a ação
            tipo_acao (str): Tipo da ação (CRIAR, ATUALIZAR, EXCLUIR, CONSULTAR, etc)
            descricao (str): Descrição da ação
            referencia_id (int, opcional): ID do registro afetado
            tabela_referencia (str, opcional): Nome da tabela afetada
        
        Returns:
            bool: True se o log foi registrado com sucesso
        """
        conn = conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO log_acoes (
                    usuario_id, 
                    tipo_acao, 
                    descricao, 
                    referencia_id, 
                    tabela_referencia, 
                    data_hora, 
                    ip_origem
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    usuario_id,
                    tipo_acao,
                    descricao,
                    referencia_id,
                    tabela_referencia,
                    datetime.now(),
                    '127.0.0.1'  # Em uma implementação real, obter IP do cliente
                )
            )
            conn.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao registrar log: {str(e)}")
            conn.rollback()
            return False
            
        finally:
            conn.close()
    
    def listar_logs(self, filtros=None, limit=100):
        """
        Lista logs de ações do sistema
        
        Args:
            filtros (dict, opcional): Filtros para a consulta
            limit (int, opcional): Limite de registros retornados
        
        Returns:
            list: Lista de logs encontrados
        """
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT l.*, u.usuario as nome_usuario
            FROM log_acoes l
            LEFT JOIN usuarios u ON l.usuario_id = u.id
            WHERE 1=1
        """
        params = []
        
        if filtros:
            if 'usuario_id' in filtros and filtros['usuario_id']:
                query += " AND l.usuario_id = %s"
                params.append(filtros['usuario_id'])
                
            if 'tipo_acao' in filtros and filtros['tipo_acao']:
                query += " AND l.tipo_acao = %s"
                params.append(filtros['tipo_acao'])
                
            if 'data_inicio' in filtros and filtros['data_inicio']:
                query += " AND l.data_hora >= %s"
                params.append(filtros['data_inicio'])
                
            if 'data_fim' in filtros and filtros['data_fim']:
                query += " AND l.data_hora <= %s"
                params.append(filtros['data_fim'])
                
            if 'tabela_referencia' in filtros and filtros['tabela_referencia']:
                query += " AND l.tabela_referencia = %s"
                params.append(filtros['tabela_referencia'])
        
        query += " ORDER BY l.data_hora DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        logs = cursor.fetchall()
        conn.close()
        
        return logs
    
    def listar_acoes_processo(self, processo_id):
        """
        Lista todas as ações realizadas em um processo específico
        
        Args:
            processo_id (int): ID do processo
        
        Returns:
            list: Lista de logs relacionados ao processo
        """
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            """
            SELECT l.*, u.usuario as nome_usuario
            FROM log_acoes l
            LEFT JOIN usuarios u ON l.usuario_id = u.id
            WHERE l.tabela_referencia = 'processos' AND l.referencia_id = %s
            ORDER BY l.data_hora DESC
            """,
            (processo_id,)
        )
        
        logs = cursor.fetchall()
        conn.close()
        
        return logs
