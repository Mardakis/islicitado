
from models.processo import Processo
from models.item import Item
from datetime import datetime
import logging

class ProcessoController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def criar_processo(self, dados_processo, itens):
        try:
            if not dados_processo.get('numero_processo'):
                return {'sucesso': False, 'mensagem': 'Número do processo é obrigatório'}
            if not dados_processo.get('nome_processo'):
                return {'sucesso': False, 'mensagem': 'Nome do processo é obrigatório'}

            try:
                if dados_processo.get('validade'):
                    datetime.strptime(dados_processo['validade'], '%Y-%m-%d')
            except ValueError:
                return {'sucesso': False, 'mensagem': 'Data de validade inválida. Use o formato YYYY-MM-DD'}

            if not itens or len(itens) == 0:
                return {'sucesso': False, 'mensagem': 'É necessário adicionar pelo menos um item'}

            processo = Processo(
                numero_processo=dados_processo['numero_processo'],
                nome_processo=dados_processo['nome_processo'],
                validade=dados_processo['validade']
            )

            processo.itens = itens
            processo_id = processo.salvar()

            self.logger.info(f"Processo criado com sucesso. ID: {processo_id}")
            return {
                'sucesso': True,
                'mensagem': 'Processo criado com sucesso',
                'processo_id': processo_id
            }

        except Exception as e:
            self.logger.error(f"Erro ao criar processo: {str(e)}")
            return {'sucesso': False, 'mensagem': f'Erro ao criar processo: {str(e)}'}
    
    def buscar_processos(self, filtros=None):
        try:
            return Processo.buscar(filtros)
        except Exception as e:
            self.logger.error(f"Erro ao buscar processos: {str(e)}")
            return []

    def listar_processos(self):
        return self.buscar_processos()

    def editar_processo(self, processo_id, dados_atualizados):
        try:
            processo = Processo.buscar_por_id(processo_id)
            if not processo:
                return {'sucesso': False, 'mensagem': 'Processo não encontrado'}

            if 'nome_processo' in dados_atualizados:
                processo.nome_processo = dados_atualizados['nome_processo']

            if 'validade' in dados_atualizados:
                try:
                    datetime.strptime(dados_atualizados['validade'], '%Y-%m-%d')
                    processo.validade = dados_atualizados['validade']
                except ValueError:
                    return {'sucesso': False, 'mensagem': 'Data de validade inválida. Use o formato YYYY-MM-DD'}

            processo.salvar()

            self.logger.info(f"Processo {processo_id} atualizado com sucesso")
            return {
                'sucesso': True,
                'mensagem': 'Processo atualizado com sucesso'
            }

        except Exception as e:
            self.logger.error(f"Erro ao editar processo {processo_id}: {str(e)}")
            return {'sucesso': False, 'mensagem': f'Erro ao editar processo: {str(e)}'}

    def registrar_consumo(self, processo_id, item_id, quantidade):
        try:
            if quantidade <= 0:
                return {'sucesso': False, 'mensagem': 'A quantidade deve ser maior que zero'}

            item = Item.buscar_por_id(item_id)
            if not item:
                return {'sucesso': False, 'mensagem': 'Item não encontrado'}

            if item.processo_id != int(processo_id):
                return {'sucesso': False, 'mensagem': 'Item não pertence ao processo informado'}

            if item.quantidade_disponivel < quantidade:
                return {
                    'sucesso': False,
                    'mensagem': f'Quantidade indisponível. Disponível: {item.quantidade_disponivel}'
                }

            sucesso = item.registrar_consumo(quantidade)
            if sucesso:
                self.logger.info(f"Consumo registrado: Processo {processo_id}, Item {item_id}, Qtd {quantidade}")
                return {'sucesso': True, 'mensagem': 'Consumo registrado com sucesso'}
            else:
                return {'sucesso': False, 'mensagem': 'Erro ao registrar consumo'}

        except Exception as e:
            self.logger.error(f"Erro ao registrar consumo: {str(e)}")
            return {'sucesso': False, 'mensagem': f'Erro ao registrar consumo: {str(e)}'}

    def obter_processos_a_vencer(self, dias=30):
        try:
            return Processo.processos_a_vencer(dias)
        except Exception as e:
            self.logger.error(f"Erro ao buscar processos a vencer: {str(e)}")
            return []
