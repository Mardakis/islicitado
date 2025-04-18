import tkinter as tk
from tkinter import filedialog, messagebox
from controllers.anexo_controller import salvar_anexo_temp
from controllers.processo_controller import buscar_todos_processos

class AnexoView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Anexar Ata a Processo", font=("Arial", 14, "bold")).pack(pady=10)

        self.processo_var = tk.StringVar()
        processos = buscar_todos_processos()
        self.processos_dict = {f"{p['titulo']} (ID {p['id']})": p['id'] for p in processos}
        processo_nomes = list(self.processos_dict.keys())
        if processo_nomes:
            self.processo_var.set(processo_nomes[0])

        tk.Label(self, text="Processo:").pack()
        self.processo_menu = tk.OptionMenu(self, self.processo_var, *processo_nomes)
        self.processo_menu.pack(pady=5)

        self.selecionar_btn = tk.Button(self, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.selecionar_btn.pack(pady=10)

    def selecionar_arquivo(self):
        arquivo_path = filedialog.askopenfilename()
        if not arquivo_path:
            return

        processo_nome = self.processo_var.get()
        processo_id = self.processos_dict.get(processo_nome)
        nome_arquivo = arquivo_path.split("/")[-1]

        sucesso, msg = salvar_anexo_temp(arquivo_path, nome_arquivo, processo_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)
