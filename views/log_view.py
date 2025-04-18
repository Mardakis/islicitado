import tkinter as tk
from tkinter import ttk
from controllers.log_controller import listar_logs

class LogView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Logs de Ações", font=("Arial", 14, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("usuario", "acao", "descricao", "data"), show="headings")
        self.tree.heading("usuario", text="Usuário ID")
        self.tree.heading("acao", text="Ação")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("data", text="Data")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.carregar_logs()

    def carregar_logs(self):
        logs = listar_logs()
        for log in logs:
            self.tree.insert("", "end", values=(
                log["usuario_id"],
                log["acao"],
                log["descricao"],
                log["data"].strftime("%d/%m/%Y %H:%M")
            ))
