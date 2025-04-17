from models.fornecedor import Fornecedor
import logging
import re

class FornecedorController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def criar_fornecedor(self, dados):
        """
        Cria um novo fornecedor
        
        Args:
            dados (dict): Dados do fornecedor
            
        Returns:
            dict: Resultado da operação com status e mensagem
        """
        try:
            # Validações
            validacao = self.validar_dados_fornecedor(dados)
            if not validacao['valido']:
                return {'sucesso': False, 'mensagem': validacao['mensagem']}
                
            # Verificar se CNPJ já existe
            if Fornecedor.buscar_por_cnpj(dados['cnpj']):
                return {'sucesso': False, 'mensagem': 'CNPJ já cadastrado no sistema'}
            
            # Criar o fornecedor
            fornecedor = Fornecedor(
                cnpj=dados['cnpj'],
                razao_social=dados['razao_social'],
                nome_fantasia=dados['nome_fantasia'],
                email=dados.get('email'),
                telefone=dados.get('telefone'),
                endereco=dados.get('endereco'),
                cidade=dados.get('cidade'),
                estado=dados.get('estado'),
                representante=dados.get('representante'),
                situacao=dados.get('situacao', 'Ativo')
            )
            
            # Salvar no banco
            if fornecedor.salvar():
                self.logger.info(f"Fornecedor criado com sucesso: {dados['razao_social']}")
                return {
                    'sucesso': True,
                    'mensagem': 'Fornecedor cadastrado com sucesso',
                    'fornecedor_id': fornecedor.id
                }
            else:
                return {'sucesso': False, 'mensagem': 'Erro ao salvar fornecedor no banco de dados'}
            
        except Exception as e:
            self.logger.error(f"Erro ao criar fornecedor: {str(e)}")
            return {'sucesso': False, 'mensagem': f'Erro ao criar fornecedor: {str(e)}'}
    
    def atualizar_fornecedor(self, fornecedor_id, dados):
        """
        Atualiza os dados de um fornecedor existente
        
        Args:
            fornecedor_id (int): ID do fornecedor
            dados (dict): Novos dados
            
        Returns:
            dict: Resultado da operação com status e mensagem
        """
        try:
            # Buscar fornecedor
            fornecedor = Fornecedor.buscar_por_id(fornecedor_id)
            if not fornecedor:
                return {'sucesso': False, 'mensagem': 'Fornecedor não encontrado'}
            
            # Validações (apenas para campos que foram fornecidos)
            dados_validacao = {k: v for k, v in dados.items() if v is not None}
            if dados_validacao:
                validacao = self.validar_dados_fornecedor(dados_validacao, fornecedor_id)
                if not validacao['valido']:
                    return {'sucesso': False, 'mensagem': validacao['mensagem']}
            
            # Atualizar atributos se fornecidos
            for attr in ['cnpj', 'razao_social', 'nome_fantasia', 'email', 'telefone', 
                        'endereco', 'cidade', 'estado', 'representante', 'situacao']:
                if attr in dados and dados[attr] is not None:
                    setattr(fornecedor, attr, dados[attr])
            
            # Salvar alterações
            if fornecedor.salvar():
                self.logger.info(f"Fornecedor {fornecedor_id} atualizado com sucesso")
                return {
                    'sucesso': True,
                    'mensagem': 'Fornecedor atualizado com sucesso'
                }
            else:
                return {'sucesso': False, 'mensagem': 'Erro ao atualizar fornecedor no banco de dados'}
            
        except Exception as e:
            self.logger.error(f"Erro ao atualizar fornecedor {fornecedor_id}: {str(e)}")
            return {'sucesso': False, 'mensagem': f'Erro ao atualizar fornecedor: {str(e)}'}
    
    def buscar_fornecedores(self, filtros=None):
        """
        Busca fornecedores com base nos filtros fornecidos
        
        Args:
            filtros (dict): Filtros para a busca
            
        Returns:
            list: Lista de fornecedores encontrados
        """
        try:
            return Fornecedor.buscar(filtros)
        except Exception as e:
            self.logger.error(f"Erro ao buscar fornecedores: {str(e)}")
            return []
    
    def desativar_fornecedor(self, fornecedor_id):
        """
        Desativa um fornecedor (altera situação para 'Inativo')
        
        Args:
            fornecedor_id (int): ID do fornecedor
            
        Returns:
            dict: Resultado da operação com status e mensagem
        """
        try:
            fornecedor = Fornecedor.buscar_por_id(fornecedor_id)
            if not fornecedor:
                return {'sucesso': False, 'mensagem': 'Fornecedor não encontrado'}
            
            fornecedor.situacao = 'Inativo'
            
            if fornecedor.salvar():
                self.logger.info(f"Fornecedor {fornecedor_id} desativado com sucesso")
                return {
                    'sucesso': True,
                    'mensagem': 'Fornecedor desativado com sucesso'
                }
            else:
                return {'sucesso': False, 'mensagem': 'Erro ao desativar fornecedor'}
                
        except Exception as e:
            self.logger.error(f"Erro ao desativar fornecedor {fornecedor_id}: {str(e)}")
            return {'sucesso': False, 'mensagem': f'Erro ao desativar fornecedor: {str(e)}'}
    
    def validar_dados_fornecedor(self, dados, fornecedor_id=None):
        """
        Valida os dados de um fornecedor
        
        Args:
            dados (dict): Dados a validar
            fornecedor_id (int, opcional): ID do fornecedor (para edição)
            
        Returns:
            dict: Resultado da validação {valido: bool, mensagem: str}
        """
        # Campos obrigatórios
        campos_obrigatorios = ['cnpj', 'razao_social']
        for campo in campos_obrigatorios:
            if campo in dados and not dados[campo]:
                return {
                    'valido': False,
                    'mensagem': f'O campo {campo} é obrigatório'
                }
        
        # Validar CNPJ se fornecido
        if 'cnpj' in dados and dados['cnpj']:
            # Remover caracteres não numéricos
            cnpj = re.sub(r'[^0-9]', '', dados['cnpj'])
            
            # Verificar tamanho
            if len(cnpj) != 14:
                return {
                    'valido': False,
                    'mensagem': 'CNPJ inválido: deve ter 14 dígitos'
                }
            
            # Verificar se já existe (apenas para novos registros ou se mudou o CNPJ)
            if fornecedor_id is None:
                fornecedor_existente = Fornecedor.buscar_por_cnpj(cnpj)
                if fornecedor_existente and fornecedor_existente.id != fornecedor_id:
                    return {
                        'valido': False,
                        'mensagem': 'CNPJ já cadastrado no sistema'
                    }
        
        # Validar e-mail se fornecido
        if 'email' in dados and dados['email']:
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, dados['email']):
                return {
                    'valido': False,
                    'mensagem': 'E-mail inválido'
                }
        
        return {'valido': True, 'mensagem': ''}
