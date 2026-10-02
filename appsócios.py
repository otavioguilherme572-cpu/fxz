import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "clube_futebol.db"

# ----------------- BANCO DE DADOS ----------------- #

def init_db():
    """Inicializa o banco de dados e cria a tabela de sócios se não existir."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS socios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_socio TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT
            )
        """)
        conn.commit()

def cadastrar_socio(num_socio: str, nome: str, cpf: str, telefone: str, email: str, endereco: str) -> tuple[bool, str]:
    """Insere um novo sócio no banco de dados."""
    num_socio = num_socio.strip()
    nome = nome.strip()
    cpf = cpf.strip()
    telefone = telefone.strip()
    email = email.strip()
    endereco = endereco.strip()

    # Validação de campos obrigatórios
    if not num_socio or not nome or not cpf:
        return False, "Número de Sócio, Nome e CPF são campos obrigatórios."

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO socios (numero_socio, nome, cpf, telefone, email, endereco)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (num_socio, nome, cpf, telefone, email, endereco))
            conn.commit()
            return True, "Sócio cadastrado com sucesso!"
    except sqlite3.IntegrityError as e:
        msg = str(e)
        if "numero_socio" in msg:
            return False, "O número de sócio informado já está cadastrado."
        elif "cpf" in msg:
            return False, "O CPF informado já está cadastrado."
        else:
            return False, "Número de sócio ou CPF já cadastrado no sistema."
    except Exception as e:
        return False, f"Erro ao cadastrar sócio: {e}"

def listar_socios() -> list:
    """Retorna todos os sócios cadastrados ordenados pelo nome."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT numero_socio, nome, cpf, telefone, email, endereco FROM socios ORDER BY nome ASC")
        return cursor.fetchall()

# ----------------- INTERFACE GRÁFICA (TKINTER) ----------------- #

class AppClubeFutebol:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Gestão de Sócios - Clube de Futebol")
        self.root.geometry("750x600")
        self.root.minsize(700, 550)

        # Configuração de Estilo Visual (ttk)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"), foreground="#1B5E20")
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        
        # Sistema de Abas (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Aba 1: Cadastro
        self.tab_cadastro = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_cadastro, text="Novo Cadastro")

        # Aba 2: Lista de Sócios
        self.tab_lista = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_lista, text="Sócios Cadastrados")

        self.montar_tela_cadastro()
        self.montar_tela_lista()

    # --- ABA DE CADASTRO ---
    def montar_tela_cadastro(self):
        title = ttk.Label(self.tab_cadastro, text="Cadastro de Sócio Torcedor", style="Header.TLabel")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Configuração dos campos do formulário
        labels = [
            ("Número de Sócio *:", "entry_num_socio"),
            ("Nome Completo *:", "entry_nome"),
            ("CPF *:", "entry_cpf"),
            ("Telefone:", "entry_telefone"),
            ("E-mail:", "entry_email"),
            ("Endereço:", "entry_endereco")
        ]

        self.entries = {}

        for idx, (text, var_name) in enumerate(labels, start=1):
            lbl = ttk.Label(self.tab_cadastro, text=text, font=("Arial", 10))
            lbl.grid(row=idx, column=0, sticky="w", pady=6, padx=(0, 10))
            
            entry = ttk.Entry(self.tab_cadastro, font=("Arial", 10), width=45)
            entry.grid(row=idx, column=1, sticky="ew", pady=6)
            self.entries[var_name] = entry

        self.tab_cadastro.columnconfigure(1, weight=1)

        # Painel de Botões
        frame_botoes = ttk.Frame(self.tab_cadastro)
        frame_botoes.grid(row=len(labels)+1, column=0, columnspan=2, pady=(20, 0), sticky="e")

        btn_limpar = ttk.Button(frame_botoes, text="Limpar", command=self.limpar_campos)
        btn_limpar.pack(side="left", padx=5)

        btn_salvar = ttk.Button(frame_botoes, text="Salvar Sócio", command=self.salvar_cadastro)
        btn_salvar.pack(side="left", padx=5)

    def salvar_cadastro(self):
        num_socio = self.entries["entry_num_socio"].get()
        nome = self.entries["entry_nome"].get()
        cpf = self.entries["entry_cpf"].get()
        telefone = self.entries["entry_telefone"].get()
        email = self.entries["entry_email"].get()
        endereco = self.entries["entry_endereco"].get()

        sucesso, msg = cadastrar_socio(num_socio, nome, cpf, telefone, email, endereco)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_tabela_socios()
            self.notebook.select(self.tab_lista)  # Redireciona para a lista de sócios
        else:
            messagebox.showwarning("Atenção", msg)

    def limpar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    # --- ABA DE LISTAGEM ---
    def montar_tela_lista(self):
        title = ttk.Label(self.tab_lista, text="Quadro de Sócios do Clube", style="Header.TLabel")
        title.pack(anchor="w", pady=(0, 15))

        # Tabela de Dados (Treeview)
        columns = ("num_socio", "nome", "cpf", "telefone", "email", "endereco")
        self.tree = ttk.Treeview(self.tab_lista, columns=columns, show="headings", height=15)

        self.tree.heading("num_socio", text="Nº Sócio")
        self.tree.heading("nome", text="Nome Completo")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("endereco", text="Endereço")

        self.tree.column("num_socio", width=90, anchor="center")
        self.tree.column("nome", width=150)
        self.tree.column("cpf", width=110, anchor="center")
        self.tree.column("telefone", width=100)
        self.tree.column("email", width=140)
        self.tree.column("endereco", width=150)

        # Barra de Rolagem (Scrollbar)
        scrollbar = ttk.Scrollbar(self.tab_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botões de Ação
        frame_acoes = ttk.Frame(self.tab_lista)
        frame_acoes.pack(fill="x", pady=(10, 0))

        btn_atualizar = ttk.Button(frame_acoes, text="Atualizar Lista", command=self.atualizar_tabela_socios)
        btn_atualizar.pack(side="left", padx=5)

        self.atualizar_tabela_socios()

    def atualizar_tabela_socios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for socio in listar_socios():
            self.tree.insert("", "end", values=socio)

# ----------------- EXECUÇÃO ----------------- #

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = AppClubeFutebol(root)
    root.mainloop()