import tkinter as tk
from tkinter import messagebox
from controllers.consumo_controller import registrar_consumo
from controllers.item_controller import buscar_todos_itens

class ConsumoView(tk.Frame):
    def __init__(self, master=None, usuario_id=None):
        super().__init__(master)
        self.master = master
        self.usuario_id = usuario_id
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Registrar Consumo de Item", font=("Arial", 14, "bold")).pack(pady=10)

        self.item_var = tk.StringVar(self)
        itens = buscar_todos_itens()
        self.itens_dict = {f"{item['nome']} (ID {item['id']})": item['id'] for item in itens}
        item_names = list(self.itens_dict.keys())
        if item_names:
            self.item_var.set(item_names[0])

        tk.Label(self, text="Item:").pack()
        self.item_dropdown = tk.OptionMenu(self, self.item_var, *item_names)
        self.item_dropdown.pack(pady=5)

        tk.Label(self, text="Quantidade consumida:").pack()
        self.quantidade_entry = tk.Entry(self)
        self.quantidade_entry.pack(pady=5)

        self.registrar_btn = tk.Button(self, text="Registrar Consumo", command=self.registrar_consumo)
        self.registrar_btn.pack(pady=10)

    def registrar_consumo(self):
        item_nome = self.item_var.get()
        item_id = self.itens_dict.get(item_nome)
        try:
            quantidade = int(self.quantidade_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        sucesso, mensagem = registrar_consumo(item_id, self.usuario_id, quantidade)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.quantidade_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", mensagem)