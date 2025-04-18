import tkinter as tk
from tkinter import messagebox, ttk
from controllers.usuario_controller import (
    criar_usuario, alterar_senha_usuario, excluir_usuario, listar_usuarios
)

class AdminUserManageView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.atualizar_lista()

    def create_widgets(self):
        tk.Label(self, text="Gerenciar Usuários", font=("Arial", 14, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "usuario", "perfil"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("usuario", text="Usuário")
        self.tree.heading("perfil", text="Perfil")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.frm = tk.Frame(self)
        self.frm.pack(pady=10)

        tk.Label(self.frm, text="Usuário:").grid(row=0, column=0)
        self.entry_usuario = tk.Entry(self.frm)
        self.entry_usuario.grid(row=0, column=1)

        tk.Label(self.frm, text="Senha:").grid(row=1, column=0)
        self.entry_senha = tk.Entry(self.frm, show="*")
        self.entry_senha.grid(row=1, column=1)

        tk.Label(self.frm, text="Perfil:").grid(row=2, column=0)
        self.perfil_var = tk.StringVar(value="consulta")
        self.perfil_menu = ttk.Combobox(self.frm, textvariable=self.perfil_var, values=["admin", "consulta"])
        self.perfil_menu.grid(row=2, column=1)

        tk.Button(self.frm, text="Criar Usuário", command=self.criar_usuario).grid(row=3, columnspan=2, pady=5)

        self.botao_alterar = tk.Button(self, text="Alterar Senha do Selecionado", command=self.alterar_senha)
        self.botao_alterar.pack(pady=5)

        self.botao_excluir = tk.Button(self, text="Excluir Selecionado", command=self.excluir_usuario)
        self.botao_excluir.pack(pady=5)

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        usuarios = listar_usuarios()
        for u in usuarios:
            self.tree.insert("", "end", values=(u["id"], u["usuario"], u["perfil"]))

    def criar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        perfil = self.perfil_var.get()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Usuário e senha são obrigatórios.")
            return

        try:
            criar_usuario(usuario, senha, perfil)
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso.")
            self.entry_usuario.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar usuário: {e}")

    def alterar_senha(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Selecione", "Selecione um usuário na lista.")
            return

        usuario_id = self.tree.item(item)['values'][0]
        nova_senha = tk.simpledialog.askstring("Nova Senha", "Digite a nova senha:", show="*")

        if nova_senha:
            alterar_senha_usuario(usuario_id, nova_senha)
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso.")

    def excluir_usuario(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Selecione", "Selecione um usuário para excluir.")
            return

        usuario_id = self.tree.item(item)['values'][0]

        confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este usuário?")
        if confirmar:
            excluir_usuario(usuario_id)
            messagebox.showinfo("Removido", "Usuário excluído com sucesso.")
            self.atualizar_lista()
