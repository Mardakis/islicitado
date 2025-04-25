from config.db_config import get_db_connection
import logging
from datetime import datetime

class Item:
    def __init__(self, id=None, processo_id=None, nome_item=None, unidade=None, 
                quantidade_total=0, quantidade_disponivel=0, valor_unitario=0.0,
                fornecedor_id=None):
        self.id = id
        self.processo_id = processo_id
        self.nome_item = nome_item
        self.unidade = unidade
        self.quantidade_total = quantidade_total
        self.quantidade_disponivel = quantidade_disponivel
        self.valor_unitario = valor_unitario
        self.fornecedor_id = fornecedor_id
        self.logger = logging.getLogger(__name__)
    
    def salvar(self):
        """Salva ou atualiza o item no banco de dados"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            if self.id is None:
                # Novo item
                cursor.execute(
                    """
                    INSERT INTO itens (
                        processo_id, nome_item, unidade, quantidade_total, 
                        quantidade_disponivel, valor_unitario, fornecedor_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        self.processo_id, self.nome_item, self.unidade, 
                        self.quantidade_total, self.quantidade_disponivel, 
                        self.valor_unitario, self.fornecedor_id
                    )
                )
                self.id = cursor.lastrowid
            else:
                # Atualizar item existente
                cursor.execute(
                    """
                    UPDATE itens SET 
                        processo_id = %s, 
                        nome_item = %s, 
                        unidade = %s, 
                        quantidade_total = %s, 
                        quantidade_disponivel = %s, 
                        valor_unitario = %s,
                        fornecedor_id = %s
                    WHERE id = %s
                    """,
                    (
                        self.processo_id, self.nome_item, self.unidade, 
                        self.quantidade_total, self.quantidade_disponivel, 
                        self.valor_unitario, self.fornecedor_id, self.id
                    )
                )
            
            conn.commit()
            self.logger.info(f"Item {self.nome_item} salvo com sucesso")
            return True
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Erro ao salvar item {self.nome_item}: {str(e)}")
            return False
        finally:
            conn.close()
    
    def registrar_consumo(self, quantidade):
        """Registra o consumo de uma quantidade do item"""
        if quantidade <= 0:
            return False
            
        if quantidade > self.quantidade_disponivel:
            return False
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Atualizar quantidade disponível
            nova_qtd = self.quantidade_disponivel - quantidade
            cursor.execute(
                "UPDATE itens SET quantidade_disponivel = %s WHERE id = %s",
                (nova_qtd, self.id)
            )
            
            # Registrar o consumo na tabela de histórico
            cursor.execute(
                """
                INSERT INTO consumo_itens (
                    item_id, processo_id, quantidade, data_consumo
                ) VALUES (%s, %s, %s, %s)
                """,
                (self.id, self.processo_id, quantidade, datetime.now())
            )
            
            conn.commit()
            self.quantidade_disponivel = nova_qtd
            self.logger.info(f"Consumo registrado: Item {self.id}, Qtd {quantidade}")
            return True
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Erro ao registrar consumo: {str(e)}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_id(item_id):
        """Busca um item pelo ID"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM itens WHERE id = %s", (item_id,))
        resultado = cursor.fetchone()
        conn.close()
        
        if not resultado:
            return None
        
        return Item(
            id=resultado['id'],
            processo_id=resultado['processo_id'],
            nome_item=resultado['nome_item'],
            unidade=resultado['unidade'],
            quantidade_total=resultado['quantidade_total'],
            quantidade_disponivel=resultado['quantidade_disponivel'],
            valor_unitario=resultado['valor_unitario'],
            fornecedor_id=resultado.get('fornecedor_id')
        )
    
    @staticmethod
    def itens_por_processo(processo_id):
        """Retorna todos os itens de um processo"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            """
            SELECT i.*, f.razao_social as fornecedor_nome
            FROM itens i
            LEFT JOIN fornecedores f ON i.fornecedor_id = f.id
            WHERE i.processo_id = %s
            ORDER BY i.nome_item
            """, 
            (processo_id,)
        )
        
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    @staticmethod
    def historico_consumo(item_id=None, processo_id=None, periodo=None):
        """
        Retorna o histórico de consumo de itens
        
        Args:
            item_id (int, opcional): Filtrar por ID do item
            processo_id (int, opcional): Filtrar por ID do processo
            periodo (dict, opcional): Período de datas {inicio, fim}
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT c.*, i.nome_item, i.unidade, p.numero_processo
            FROM consumo_itens c
            JOIN itens i ON c.item_id = i.id
            JOIN processos p ON c.processo_id = p.id
            WHERE 1=1
        """
        params = []
        
        if item_id:
            query += " AND c.item_id = %s"
            params.append(item_id)
            
        if processo_id:
            query += " AND c.processo_id = %s"
            params.append(processo_id)
            
        if periodo:
            if 'inicio' in periodo and periodo['inicio']:
                query += " AND c.data_consumo >= %s"
                params.append(periodo['inicio'])
                
            if 'fim' in periodo and periodo['fim']:
                query += " AND c.data_consumo <= %s"
                params.append(periodo['fim'])
        
        query += " ORDER BY c.data_consumo DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
