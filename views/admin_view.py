import tkinter as tk
from tkinter import messagebox
from views.dashboard_view import DashboardView
from views.usuario_view import UsuarioView
from views.nota_fiscal_view import NotaFiscalView
from views.busca_processos_view import BuscaProcessosView
from views.consumo_view import ConsumoView
from views.logs_view import LogsView

class AdminView(tk.Frame):
    def __init__(self, master=None, usuario=None):
        super().__init__(master)
        self.master = master
        self.usuario = usuario
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Título / Saudação
        tk.Label(self, text=f"Bem-vindo, {self.usuario['nome']} (Administrador)", font=("Arial", 14, "bold")).pack(pady=10)

        # Menu de botões
        botoes = [
            ("🏠 Dashboard", self.abrir_dashboard),
            ("🔍 Buscar Processos", self.abrir_busca_processos),
            ("📦 Consumo de Itens", self.abrir_consumo),
            ("📁 Notas Fiscais", self.abrir_notas),
            ("👥 Gerenciar Usuários", self.abrir_usuarios),
            ("📜 Logs do Sistema", self.abrir_logs),
            ("🚪 Sair", self.sair)
        ]

        for texto, comando in botoes:
            tk.Button(self, text=texto, command=comando, width=30, font=("Arial", 11)).pack(pady=5)

    def abrir_dashboard(self):
        self._abrir_nova_janela("Dashboard", DashboardView)

    def abrir_busca_processos(self):
        self._abrir_nova_janela("Buscar Processos", BuscaProcessosView)

    def abrir_consumo(self):
        self._abrir_nova_janela("Consumo de Itens", ConsumoView)

    def abrir_notas(self):
        self._abrir_nova_janela("Notas Fiscais", NotaFiscalView)

    def abrir_usuarios(self):
        self._abrir_nova_janela("Gerenciar Usuários", UsuarioView)

    def abrir_logs(self):
        self._abrir_nova_janela("Logs do Sistema", LogsView)

    def sair(self):
        resposta = messagebox.askyesno("Confirmação", "Deseja realmente sair?")
        if resposta:
            self.master.destroy()

    def _abrir_nova_janela(self, titulo, classe_view):
        nova_janela = tk.Toplevel(self.master)
        nova_janela.title(titulo)
        nova_janela.geometry("800x600")
        view = classe_view(nova_janela)
