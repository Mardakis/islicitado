from config.db_config import get_db_connection
from datetime import datetime

class Processo:
    def __init__(self, id=None, numero_processo=None, nome_processo=None, validade=None):
        self.id = id
        self.numero_processo = numero_processo
        self.nome_processo = nome_processo
        self.validade = validade
        self.itens = []
    
    def salvar(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            # Inserir novo processo
            cursor.execute(
                "INSERT INTO processos (numero_processo, nome_processo, validade) VALUES (%s, %s, %s)",
                (self.numero_processo, self.nome_processo, self.validade)
            )
            self.id = cursor.lastrowid
            
            # Salvar os itens associados
            for item in self.itens:
                cursor.execute(
                    "INSERT INTO itens (processo_id, nome_item, unidade, quantidade_total, quantidade_disponivel, valor_unitario) VALUES (%s, %s, %s, %s, %s, %s)",
                    (self.id, item['nome'], item['unidade'], item['quantidade'], item['quantidade'], item['valor'])
                )
        else:
            # Atualizar processo existente
            cursor.execute(
                "UPDATE processos SET numero_processo = %s, nome_processo = %s, validade = %s WHERE id = %s",
                (self.numero_processo, self.nome_processo, self.validade, self.id)
            )
        
        conn.commit()
        conn.close()
        return self.id
    
    @staticmethod
    def buscar_por_id(processo_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM processos WHERE id = %s", (processo_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return None
            
        processo = Processo(
            id=result['id'],
            numero_processo=result['numero_processo'],
            nome_processo=result['nome_processo'],
            validade=result['validade']
        )
        
        # Buscar itens associados
        cursor.execute("SELECT * FROM itens WHERE processo_id = %s", (processo_id,))
        itens = cursor.fetchall()
        processo.itens = itens
        
        conn.close()
        return processo
    
    @staticmethod
    def buscar(filtros=None):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT DISTINCT p.id, p.numero_processo, p.nome_processo, p.validade
            FROM processos p
            LEFT JOIN itens i ON i.processo_id = p.id
            WHERE 1=1
        """
        params = []
        
        if filtros:
            if 'numero' in filtros and filtros['numero']:
                query += " AND p.numero_processo LIKE %s"
                params.append(f"%{filtros['numero']}%")
            
            if 'nome' in filtros and filtros['nome']:
                query += " AND p.nome_processo LIKE %s"
                params.append(f"%{filtros['nome']}%")
                
            if 'item' in filtros and filtros['item']:
                query += " AND i.nome_item LIKE %s"
                params.append(f"%{filtros['item']}%")
                
            if 'data_ini' in filtros and filtros['data_ini']:
                query += " AND p.validade >= %s"
                params.append(filtros['data_ini'])
                
            if 'data_fim' in filtros and filtros['data_fim']:
                query += " AND p.validade <= %s"
                params.append(filtros['data_fim'])
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        processos = []
        for row in resultados:
            processo = Processo(
                id=row['id'],
                numero_processo=row['numero_processo'],
                nome_processo=row['nome_processo'],
                validade=row['validade']
            )
            
            # Buscar itens associados
            cursor.execute("SELECT * FROM itens WHERE processo_id = %s", (row['id'],))
            processo.itens = cursor.fetchall()
            
            processos.append(processo)
        
        conn.close()
        return processos
    
    @staticmethod
    def processos_a_vencer(dias=30):
        """Retorna processos que vencerão nos próximos X dias"""
        hoje = datetime.now().strftime('%Y-%m-%d')
        limite = datetime.now()
        limite = limite.replace(day=limite.day + dias)
        limite = limite.strftime('%Y-%m-%d')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM processos WHERE validade BETWEEN %s AND %s",
            (hoje, limite)
        )
        resultados = cursor.fetchall()
        conn.close()
        
        return [Processo(
            id=row['id'],
            numero_processo=row['numero_processo'],
            nome_processo=row['nome_processo'],
            validade=row['validade']
        ) for row in resultados]
