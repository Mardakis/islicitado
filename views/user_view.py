
import PySimpleGUI as sg
from controllers.processo_controller import ProcessoController

class UserView:
    def __init__(self, usuario_logado, auth_controller, processo_controller):
        self.usuario = usuario_logado
        self.auth_controller = auth_controller
        self.controller = processo_controller
        self.window = None

    def iniciar(self):
        sg.theme('BlueMono')

        layout = [
            [sg.Text(f'Bem-vindo, {self.usuario["nome"]}', font=('Helvetica', 14), text_color='blue')],
            [sg.Text('🔍 Buscar processo:'), sg.InputText(key='busca'), sg.Button('Pesquisar')],
            [sg.Text('Status:'), sg.Combo(['Todos', 'Em andamento', 'Concluído', 'Cancelado'], default_value='Todos', key='status')],
            [sg.Button('Atualizar Lista')],
            [sg.Listbox(values=[], size=(80, 15), key='lista_processos', enable_events=True)],
            [sg.Button('Ver Detalhes'), sg.Button('Sair')]
        ]

        self.window = sg.Window('Painel do Usuário - Processos', layout, finalize=True)
        self.atualizar_lista_processos()

        while True:
            event, values = self.window.read()
            if event in (sg.WINDOW_CLOSED, 'Sair'):
                break
            elif event == 'Atualizar Lista':
                self.atualizar_lista_processos()
            elif event == 'Pesquisar':
                self.atualizar_lista_processos(filtro=values['busca'], status=values['status'])
            elif event == 'Ver Detalhes':
                self.ver_detalhes(values)

        self.window.close()

    def atualizar_lista_processos(self, filtro=None, status='Todos'):
        processos = self.controller.listar_processos()

        if status and status != 'Todos':
            processos = [p for p in processos if p['status'].lower() == status.lower()]

        if filtro:
            processos = [p for p in processos if filtro.lower() in p['descricao'].lower()]

        lista_formatada = [f"{p['numero']} - {p['descricao']} [{p['status']}]" for p in processos]
        self.window['lista_processos'].update(lista_formatada)
        self.processos = processos

    def ver_detalhes(self, values):
        try:
            selecionado = values['lista_processos'][0]
            idx = self.window['lista_processos'].Values.index(selecionado)
            processo = self.processos[idx]

            detalhes = f"""
Número: {processo['numero']}
Descrição: {processo['descricao']}
Status: {processo['status']}
Data de Abertura: {processo.get('data_abertura', 'N/A')}
Última Atualização: {processo.get('ultima_atualizacao', 'N/A')}
            """

            sg.popup_scrolled('📄 Detalhes do Processo', detalhes.strip(), size=(60, 15))
        except IndexError:
            sg.popup('Selecione um processo na lista para ver os detalhes.')
