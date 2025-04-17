import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
from controllers.auth_controller import AuthController

class LoginView:
    def __init__(self, root):
        self.root = root
        self.auth_controller = AuthController()
        self.login_window = None
        
    def exibir(self):
        # Criar uma nova janela de login
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Sistema de Gestão de Licitações - Login")
        self.login_window.geometry("400x500")
        self.login_window.resizable(False, False)
        
        # Centralizar na tela
        window_width = 400
        window_height = 500
        screen_width = self.login_window.winfo_screenwidth()
        screen_height = self.login_window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.login_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        # Frame principal
        main_frame = ttk.Frame(self.login_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Sistema de Gestão de Licitações", 
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 5))
        ttk.Label(main_frame, text="Acesso ao Sistema", 
                 font=("Helvetica", 12)).pack(pady=(0, 20))
        
        # Logo ou ícone (substituir pelo caminho do seu logo)
        try:
            img_path = os.path.join("assets", "logo.png")
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((120, 120))
                logo = ImageTk.PhotoImage(img)
                logo_label = ttk.Label(main_frame, image=logo)
                logo_label.image = logo  # Manter referência
                logo_label.pack(pady=(0, 20))
        except Exception:
            # Se a imagem não estiver disponível, continua sem ela
            pass
        
        # Frame para os campos
        campos_frame = ttk.Frame(main_frame)
        campos_frame.pack(fill=tk.X, pady=10)
        
        # Campos de usuário e senha
        ttk.Label(campos_frame, text="Usuário:", 
                 font=("Helvetica", 10)).pack(anchor="w", pady=(10, 0))
        self.usuario_var = tk.StringVar()
        usuario_entry = ttk.Entry(campos_frame, textvariable=self.usuario_var, width=40)
        usuario_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(campos_frame, text="Senha:", 
                 font=("Helvetica", 10)).pack(anchor="w", pady=(10, 0))
        self.senha_var = tk.StringVar()
        senha_entry = ttk.Entry(campos_frame, textvariable=self.senha_var, show="•", width=40)
        senha_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Botão de login
        ttk.Button(
            campos_frame,
            text="Entrar",
            command=self.realizar_login,
            style="Accent.TButton",
            cursor="hand2"
        ).pack(fill=tk.X, pady=(20, 0))
        
        # Configurar estilo personalizado para botões
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Helvetica", 11))
        
        # Vincular tecla Enter aos campos
        usuario_entry.bind("<Return>", lambda event: senha_entry.focus())
        senha_entry.bind("<Return>", lambda event: self.realizar_login())
        
        # Focar no campo de usuário no início
        usuario_entry.focus_set()
        
        # Informações de rodapé
        ttk.Label(
            main_frame, 
            text="© 2025 Sistema de Gestão de Licitações", 
            font=("Helvetica", 8)
        ).pack(side=tk.BOTTOM, pady=10)
    
    def realizar_login(self):
        usuario = self.usuario_var.get()
        senha = self.senha_var.get()
        
        # Validação básica
        if not usuario or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos")
            return
        
        # Tenta fazer login
        try:
            resultado_login = self.auth_controller.autenticar(usuario, senha)
            
            if resultado_login['sucesso']:
                self.login_window.destroy()
                # Retorna os dados do usuário para abrir a tela adequada
                if resultado_login['admin']:
                    from views.admin_view import AdminView
                    AdminView(self.root, resultado_login['usuario']).exibir()
                else:
                    from views.user_view import UserView
                    UserView(self.root, resultado_login['usuario']).exibir()
            else:
                messagebox.showerror("Erro de Autenticação", resultado_login['mensagem'])
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar login: {str(e)}")
