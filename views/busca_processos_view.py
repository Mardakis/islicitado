import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from controllers.processo_controller import ProcessoController
from views.components.custom_widgets import CustomTreeview, StatusBar

class BuscaProcessosView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ProcessoController()
        self.janela = None
        self.tree = None
        self.status_bar = None
        self.filtros = {}
        
        # Variáveis de controle
        self.numero_var = tk.StringVar()
        self.nome_var = tk.StringVar()
        self.item_var = tk.StringVar()
        self.data_ini_var = tk.StringVar()
        self.data_fim_var = tk.StringVar()
        self.mostrar_vencidos_var = tk.BooleanVar(value=False)
        
    def exibir(self):
        """Exibe a tela de busca de processos"""
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Busca de Processos Licitatórios")
        self.janela.geometry("1200x700")
        self.janela.minsize(1000, 600)
        
        # Configurar layout principal
        self.configurar_layout()
        
        # Preencher com dados iniciais
        self.buscar_processos()
    
    def configurar_layout(self):
        """Configura o layout da tela"""
        # Frame principal
        main_frame = ttk.Frame(self.janela)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de filtros
        self.criar_frame_filtros(main_frame)
        
        # Frame de resultados
        self.criar_frame_resultados(main_frame)
        
        # Status Bar
        self.status_bar = StatusBar(self.janela)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.set("Pronto")
    
    def criar_frame_filtros(self, parent):
        """Cria o frame com os filtros de busca"""
        frame_filtros = ttk.LabelFrame(parent, text="Filtros de Busca", padding=(10, 5))
        frame_filtros.pack(fill=tk.X, pady=(0, 10))
        
        # Grid para os filtros
        for i in range(5):
            frame_filtros.columnconfigure(i, weight=1)
        
        # Filtro: Número do Processo
        ttk.Label(frame_filtros, text="Número do Processo:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(frame_filtros, textvariable=self.numero_var).grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        
        # Filtro: Nome do Processo
        ttk.Label(frame_filtros, text="Nome do Processo:").grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ttk.Entry(frame_filtros, textvariable=self.nome_var).grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        
        # Filtro: Item Contido
        ttk.Label(frame_filtros, text="Item Contido:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        ttk.Entry(frame_filtros, textvariable=self.item_var).grid(row=1, column=2, sticky="ew", padx=5, pady=2)
        
        # Filtro: Data Inicial
        ttk.Label(frame_filtros, text="Validade Inicial:").grid(row=0, column=3, sticky="w", padx=5, pady=2)
        ttk.Entry(frame_filtros, textvariable=self.data_ini_var).grid(row=1, column=3, sticky="ew", padx=5, pady=2)
        
        # Filtro: Data Final
        ttk.Label(frame_filtros, text="Validade Final:").grid(row=0, column=4, sticky="w", padx=5, pady=2)
        ttk.Entry(frame_filtros, textvariable=self.data_fim_var).grid(row=1, column=4, sticky="ew", padx=5, pady=2)
        
        # Filtro adicional: Mostrar vencidos
        ttk.Checkbutton(
            frame_filtros, 
            text="Incluir Processos Vencidos", 
            variable=self.mostrar_vencidos_var
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
# Botões de ação
        frame_botoes = ttk.Frame(frame_filtros)
        frame_botoes.grid(row=2, column=2, columnspan=3, sticky="e", padx=5, pady=5)
        
        ttk.Button(
            frame_botoes,
            text="Limpar Filtros",
            command=self.limpar_filtros,
            style="Secondary.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            frame_botoes,
            text="Buscar Processos",
            command=self.buscar_processos,
            style="Primary.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        # Atalhos de datas
        frame_atalhos = ttk.Frame(frame_filtros)
        frame_atalhos.grid(row=3, column=0, columnspan=5, sticky="w", padx=5, pady=5)
        
        ttk.Label(frame_atalhos, text="Atalhos: ").pack(side=tk.LEFT)
        ttk.Button(
            frame_atalhos,
            text="Vigentes",
            command=lambda: self.filtro_rapido("vigentes"),
            style="Link.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            frame_atalhos,
            text="Vencendo 30 dias",
            command=lambda: self.filtro_rapido("30dias"),
            style="Link.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            frame_atalhos,
            text="Vencendo 60 dias",
            command=lambda: self.filtro_rapido("60dias"),
            style="Link.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
    def criar_frame_resultados(self, parent):
        """Cria o frame com a tabela de resultados"""
        frame_resultados = ttk.LabelFrame(parent, text="Processos Encontrados", padding=(10, 5))
        frame_resultados.pack(fill=tk.BOTH, expand=True)
        
        # Criar barra de ferramentas
        toolbar = ttk.Frame(frame_resultados)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(
            toolbar,
            text="Visualizar Detalhes",
            command=self.visualizar_detalhes
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="Exportar Lista",
            command=self.exportar_resultados
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="Gerenciar Atas",
            command=self.gerenciar_atas
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="Registrar Consumo",
            command=self.registrar_consumo
        ).pack(side=tk.LEFT, padx=2)
        
        # Separador
        ttk.Separator(toolbar, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Contador de resultados
        self.contador_label = ttk.Label(toolbar, text="0 processos encontrados")
        self.contador_label.pack(side=tk.RIGHT, padx=5)
        
        # Criar tabela de resultados
        frame_tabela = ttk.Frame(frame_resultados)
        frame_tabela.pack(fill=tk.BOTH, expand=True)
        
        colunas = (
            "id", "numero", "nome", "validade", "status", "itens", "valor_total"
        )
        
        self.tree = CustomTreeview(
            frame_tabela, 
            columns=colunas,
            show="headings",
            selectmode="browse"
        )
        
        # Configurar cabeçalhos
        self.tree.heading("id", text="ID")
        self.tree.heading("numero", text="Número do Processo")
        self.tree.heading("nome", text="Nome do Processo")
        self.tree.heading("validade", text="Validade")
        self.tree.heading("status", text="Status")
        self.tree.heading("itens", text="Itens")
        self.tree.heading("valor_total", text="Valor Total")
        
        # Configurar colunas
        self.tree.column("id", width=50, stretch=False)
        self.tree.column("numero", width=150)
        self.tree.column("nome", width=300)
        self.tree.column("validade", width=100, anchor=tk.CENTER)
        self.tree.column("status", width=100, anchor=tk.CENTER)
        self.tree.column("itens", width=80, anchor=tk.CENTER)
        self.tree.column("valor_total", width=120, anchor=tk.E)
        
        # Adicionar scrollbars
        scrollbar_y = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Posicionar componentes
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Evento de duplo clique
        self.tree.bind("<Double-1>", lambda event: self.visualizar_detalhes())
        
        # Menu de contexto
        self.criar_menu_contexto()
    
    def criar_menu_contexto(self):
        """Cria menu de contexto para a tabela"""
        self.menu_contexto = tk.Menu(self.tree, tearoff=0)
        self.menu_contexto.add_command(label="Visualizar Detalhes", command=self.visualizar_detalhes)
        self.menu_contexto.add_command(label="Editar Processo", command=self.editar_processo)
        self.menu_contexto.add_separator()
        self.menu_contexto.add_command(label="Gerenciar Atas", command=self.gerenciar_atas)
        self.menu_contexto.add_command(label="Registrar Consumo", command=self.registrar_consumo)
        self.menu_contexto.add_separator()
        self.menu_contexto.add_command(label="Exportar Este Processo", command=self.exportar_processo_selecionado)
        
        self.tree.bind("<Button-3>", self.exibir_menu_contexto)
    
    def exibir_menu_contexto(self, event):
        """Exibe o menu de contexto"""
        # Identificar o item clicado
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu_contexto.post(event.x_root, event.y_root)
    
    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.numero_var.set("")
        self.nome_var.set("")
        self.item_var.set("")
        self.data_ini_var.set("")
        self.data_fim_var.set("")
        self.mostrar_vencidos_var.set(False)
    
    def filtro_rapido(self, tipo):
        """Aplica filtros rápidos predefinidos"""
        hoje = datetime.now()
        
        # Limpar filtros atuais
        self.limpar_filtros()
        
        if tipo == "vigentes":
            self.data_ini_var.set(hoje.strftime('%Y-%m-%d'))
            
        elif tipo == "30dias":
            self.data_ini_var.set(hoje.strftime('%Y-%m-%d'))
            data_fim = hoje + timedelta(days=30)
            self.data_fim_var.set(data_fim.strftime('%Y-%m-%d'))
            
        elif tipo == "60dias":
            self.data_ini_var.set(hoje.strftime('%Y-%m-%d'))
            data_fim = hoje + timedelta(days=60)
            self.data_fim_var.set(data_fim.strftime('%Y-%m-%d'))
        
        # Buscar com o filtro aplicado
        self.buscar_processos()
    
    def buscar_processos(self):
        """Executa a busca de processos com os filtros atuais"""
        # Preparar filtros
        filtros = {
            'numero': self.numero_var.get(),
            'nome': self.nome_var.get(),
            'item': self.item_var.get(),
            'data_ini': self.data_ini_var.get(),
            'data_fim': self.data_fim_var.get(),
            'mostrar_vencidos': self.mostrar_vencidos_var.get()
        }
        
        # Atualizar status
        self.status_bar.set("Buscando processos...")
        
        # Limpar tabela
        self.tree.delete(*self.tree.get_children())
        
        try:
            # Buscar processos através do controller
            processos = self.controller.buscar_processos(filtros)
            
            # Preencher tabela com resultados
            hoje = datetime.now().date()
            
            for processo in processos:
                # Calcular status
                status = "Vigente"
                status_tag = "status_vigente"
                
                if processo.validade:
                    validade = datetime.strptime(processo.validade, '%Y-%m-%d').date()
                    dias_restantes = (validade - hoje).days
                    
                    if dias_restantes < 0:
                        status = "Vencido"
                        status_tag = "status_vencido"
                    elif dias_restantes <= 30:
                        status = f"Vence em {dias_restantes} dias"
                        status_tag = "status_alerta"
                
                # Contar itens e calcular valor total
                qtd_itens = len(processo.itens)
                valor_total = sum(item['valor_unitario'] * item['quantidade_total'] for item in processo.itens)
                
                # Inserir na tabela
                item_id = self.tree.insert(
                    "", 
                    "end",
                    values=(
                        processo.id,
                        processo.numero_processo,
                        processo.nome_processo,
                        processo.validade,
                        status,
                        qtd_itens,
                        f"R$ {valor_total:.2f}".replace('.', ',')
                    ),
                    tags=(status_tag,)
                )
            
            # Configurar cores conforme status
            self.tree.tag_configure("status_vigente", background="#e6ffee")
            self.tree.tag_configure("status_alerta", background="#fff9e6")
            self.tree.tag_configure("status_vencido", background="#ffe6e6")
            
            # Atualizar contador de resultados
            qtd_resultados = len(processos)
            self.contador_label.config(
                text=f"{qtd_resultados} {'processo' if qtd_resultados == 1 else 'processos'} encontrado{'s' if qtd_resultados != 1 else ''}"
            )
            
            # Atualizar status
            self.status_bar.set(f"Busca concluída. {qtd_resultados} resultados.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar processos: {str(e)}")
            self.status_bar.set("Erro na busca.")
    
    def visualizar_detalhes(self):
        """Abre a tela de detalhes do processo selecionado"""
        selecionado = self.obter_selecionado()
        if not selecionado:
            return
            
        from views.processo_detalhes_view import ProcessoDetalhesView
        ProcessoDetalhesView(self.janela, selecionado).exibir()
    
    def editar_processo(self):
        """Abre a tela de edição do processo selecionado"""
        selecionado = self.obter_selecionado()
        if not selecionado:
            return
            
        from views.processo_edicao_view import ProcessoEdicaoView
        ProcessoEdicaoView(self.janela, selecionado).exibir()
        # Recarregar após fechar
        self.janela.wait_window(ProcessoEdicaoView.janela)
        self.buscar_processos()
    
    def gerenciar_atas(self):
        """Abre a tela de gerenciamento de atas do processo selecionado"""
        selecionado = self.obter_selecionado()
        if not selecionado:
            return
            
        from views.atas_view import AtasView
        AtasView(self.janela, selecionado).exibir()
    
    def registrar_consumo(self):
        """Abre a tela de registro de consumo para o processo selecionado"""
        selecionado = self.obter_selecionado()
        if not selecionado:
            return
            
        from views.consumo_view import ConsumoView
        ConsumoView(self.janela, selecionado).exibir()
        # Recarregar após fechar
        self.janela.wait_window(ConsumoView.janela)
        self.buscar_processos()
    
    def exportar_resultados(self):
        """Exporta os resultados da busca para um arquivo"""
        from utils.exportacao import exportar_processos
        
        if not self.tree.get_children():
            messagebox.showinfo("Aviso", "Não há processos para exportar.")
            return
        
        try:
            # Obter todos os IDs dos processos na tabela
            ids = [self.tree.item(item)['values'][0] for item in self.tree.get_children()]
            
            # Exportar
            resultado = exportar_processos(ids)
            
            if resultado['sucesso']:
                messagebox.showinfo("Sucesso", resultado['mensagem'])
            else:
                messagebox.showerror("Erro", resultado['mensagem'])
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar resultados: {str(e)}")
    
    def exportar_processo_selecionado(self):
        """Exporta apenas o processo selecionado"""
        selecionado = self.obter_selecionado()
        if not selecionado:
            return
            
        from utils.exportacao import exportar_processos
        try:
            resultado = exportar_processos([selecionado])
            
            if resultado['sucesso']:
                messagebox.showinfo("Sucesso", resultado['mensagem'])
            else:
                messagebox.showerror("Erro", resultado['mensagem'])
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar processo: {str(e)}")
    
    def obter_selecionado(self):
        """Obtém o ID do processo selecionado"""
        selecionado = self.tree.selection()
        
        if not selecionado:
            messagebox.showinfo("Aviso", "Selecione um processo primeiro.")
            return None
            
        # Obter o ID do processo selecionado
        return self.tree.item(selecionado[0], 'values')[0]