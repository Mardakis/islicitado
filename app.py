import tkinter as tk
from tkinter import ttk
import logging
import os
from datetime import datetime
from views.login_view import LoginView

class SistemaLicitacoes:
    def __init__(self):
        # Configurar logging
        self.configurar_logging()
        
        # Configurar a janela principal
        self.root = tk.Tk()
        self.root.title("Sistema de Gestão de Licitações")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Exibir tela de login
        self.exibir_login()
        
        # Iniciar loop principal
        self.root.mainloop()
    
    def configurar_logging(self):
        """Configura o sistema de logs da aplicação"""
        # Criar diretório para logs se não existir
        os.makedirs("logs", exist_ok=True)
        
        # Nome do arquivo de log baseado na data
        log_file = f"logs/sistema_{datetime.now().strftime('%Y-%m-%d')}.log"
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        logging.info("Sistema iniciado")
    
    def configurar_estilo(self):
        """Configura o estilo visual da aplicação"""
        style = ttk.Style()
        
        # Botões
        style.configure("TButton", padding=6, font=("Helvetica", 10))
        style.configure("Primary.TButton", background="#4CAF50", foreground="white")
        style.configure("Secondary.TButton", background="#f0f0f0")
        style.configure("Accent.TButton", background="#2196F3", foreground="white")
        style.configure("Link.TButton", background=None, foreground="#0645AD", borderwidth=0)
        
        # Frames
        style.configure("TFrame", background="#f8f8f8")
        style.configure("TLabelframe", background="#f8f8f8")
        style.configure("TLabelframe.Label", font=("Helvetica", 11, "bold"))
        
        # Outros elementos
        style.configure("TLabel", background="#f8f8f8")
        style.configure("TEntry", padding=5)
    
    def exibir_login(self):
        """Exibe a tela de login"""
        login_view = LoginView(self.root)
        login_view.exibir()

if __name__ == "__main__":
    app = SistemaLicitacoes()
