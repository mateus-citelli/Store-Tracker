from tkinter import *
import tkinter as tk

class PlaceholderEntry(tk.Entry):
    """Classe personalizada para Entry com placeholder text"""
    def __init__(self, master=None, placeholder="", color='grey', show=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.real_show = show
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        self.bind("<KeyRelease>", self.scroll_text)
        
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self.config(show='')

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            if self.real_show:
                self.config(show=self.real_show)

    def focus_out(self, *args):
        if not super().get():
            self.config(show='')
            self.put_placeholder()

    def get(self):
        content = super().get()
        if content == self.placeholder:
            return ""
        return content
    
    def scroll_text(self, event=None):
        self.xview_moveto(1)

app = tk.Tk()
app.geometry("500x250")
app.title("Estoque")
app.config(bg='#202124')

label = tk.Label(app, text="Olá, Usuário!", bg='#202124', fg='white')
label.pack(pady=40)

def login_janela():
    app.withdraw()
    janela_login = tk.Toplevel(app)
    janela_login.geometry("500x250")
    janela_login.title("Login")
    janela_login.config(bg='#202124')
    janela_login.protocol("WM_DELETE_WINDOW", lambda: (janela_login.destroy(), app.deiconify()))


    mensagem_ou = tk.Label(master=janela_login, text="Ou", bg='#202124', fg='white')
    mensagem_ou.place(relx=0.5, rely=0.35, anchor='center')

    button_googlelogar = tk.Button(master=janela_login, text="Entre com Google", command=lambda: login_janela2(janela_login), bg='#1A73E8', fg='white', cursor='hand2')
    button_googlelogar.place(relx=0.5, rely=0.25, anchor='center')
    
    entry_usuarioOuE_mail = PlaceholderEntry(master=janela_login, placeholder="E-mail ou usuário")
    entry_usuarioOuE_mail.place(relx=0.5, rely=0.45, anchor='center')
    
    button_avancar = tk.Button(master=janela_login, text="Avançar", state="disabled", command=lambda: login_janela3(janela_login), bg='#1A73E8', fg='white', disabledforeground="#b8bfba", cursor='hand2')
    button_avancar.place(relx=0.5, rely=0.6, anchor='center')

    botao_esqueceusenha = tk.Button(master=janela_login, text="Esqueceu a senha?", command=lambda: janelaesqueceuAsenha(janela_login), bg='#1A73E8', fg='white', cursor='hand2')
    botao_esqueceusenha.place(relx=0.5, rely=0.75, anchor='center')
    
    def check_entry_usuarioOuE_mail(event=None):
        if entry_usuarioOuE_mail.get().strip():
            button_avancar.configure(state="normal")
        else:
            button_avancar.configure(state="disabled")
    
    entry_usuarioOuE_mail.bind("<KeyRelease>", check_entry_usuarioOuE_mail)

button_login = tk.Button(master=app, text="Login", command=login_janela, bg='#1A73E8', fg='white', activebackground="#1558b0", cursor='hand2')
button_login.place(relx=0.5, rely=0.5, anchor='center')

def login_janela2(login_janela):
    login_janela.withdraw()
    janela_google = tk.Toplevel(login_janela)
    janela_google.geometry("1920x1080")
    janela_google.title("Splash Page")
    janela_google.config(bg='#202124')

    #JANELA DE EXCLUIR PRODUTO =============================================================================================================================================
    def abrir_janela_excluir():
        # esconde a splash
        janela_google.withdraw()
        janela_excluir = tk.Toplevel(janela_google)
        janela_excluir.geometry("900x600")
        janela_excluir.title("Excluir Produto")
        janela_excluir.config(bg="#5a5a5a")

        tk.Label(janela_excluir, text="Exclua o produto", bg="#5a5a5a", fg="white",
             font=("Arial", 20, "bold")).pack(pady=18)

        frame_box = tk.Frame(janela_excluir, bg="#4d4d4d", padx=20, pady=20)
        frame_box.pack(pady=10)

    # Cabeçalho
        tk.Label(frame_box, text="", bg="#4d4d4d", width=3).grid(row=0, column=0)  # espaço para radiobutton
        tk.Label(frame_box, text="Código de barras", bg="#4d4d4d", fg="white", font=("Arial", 12, "bold"), width=18).grid(row=0, column=1)
        tk.Label(frame_box, text="Nome do produto", bg="#4d4d4d", fg="white", font=("Arial", 12, "bold"), width=25).grid(row=0, column=2)
        tk.Label(frame_box, text="Data de adição", bg="#4d4d4d", fg="white", font=("Arial", 12, "bold"), width=18).grid(row=0, column=3)

    # variável que guarda o código selecionado
        selecionado = tk.StringVar(value="")  # vazio por padrão

    # Preenche as linhas com radiobuttons
        for i, (codigo, produto) in enumerate(produtos.items(), start=1):
            rb = tk.Radiobutton(frame_box, variable=selecionado, value=codigo, bg="#4d4d4d", activebackground="#4d4d4d",
                            highlightthickness=0)
            rb.grid(row=i, column=0, padx=(5,15))

            tk.Label(frame_box, text=codigo, bg="#4d4d4d", fg="white", font=("Arial", 11)).grid(row=i, column=1)
            tk.Label(frame_box, text=produto["nome"], bg="#4d4d4d", fg="white", font=("Arial", 11)).grid(row=i, column=2)
            tk.Label(frame_box, text=produto["adicao"], bg="#4d4d4d", fg="white", font=("Arial", 11)).grid(row=i, column=3)

    # Mensagem de feedback (mesmo estilo das outras telas: escondida inicialmente)
        mensagem_excluir = tk.Label(
            janela_excluir,
            text="Produto excluído com sucesso!",
            bg="#5a5a5a",
            fg="#5a5a5a",  # invisível no início
            font=("Arial", 12, "bold")
            )
        mensagem_excluir.pack(pady=(20,0), anchor="w", padx=20)

    # Função que realiza a exclusão
        def confirmar_exclusao():
            codigo_sel = selecionado.get()  #codigo_sel será o código do produto selecionado
            if not codigo_sel:  #se nenhum produto foi selecionado
                mensagem_excluir.config(text="Selecione um produto para excluir.", fg="red")
                return

        # Remove do dicionário
            if codigo_sel in produtos:
                del produtos[codigo_sel]
            else:
                mensagem_excluir.config(text="Produto não encontrado.", fg="red")
                return
        
            mensagem_excluir.config(text="Produto excluído com sucesso!", fg="lime")

        # opcional: deseleciona para evitar tentativa repetida
            selecionado.set("")
    
        # Botões inferior: EXCLUIR e VOLTAR
        tk.Button(janela_excluir, text="EXCLUIR", bg="#ff5733", fg="white", font=("Arial", 14, "bold"),
              cursor="hand2", command=confirmar_exclusao).place(relx=0.75, rely=0.9, anchor='center')

        tk.Button(janela_excluir, text="VOLTAR", bg='#1A73E8', fg='white', font=("Arial", 12),
              cursor="hand2", command=lambda: (janela_excluir.destroy(), janela_google.deiconify())).place(relx=0.9, rely=0.9, anchor='center')
    #======================================================================================================================================================================

    #lista de checkboxes (os quadradinhos para o filtro)
    checkboxes = []

    button_fechar = tk.Button(master=janela_google, text="Voltar", command=lambda: (janela_google.destroy(), login_janela.deiconify()), bg='#1A73E8', fg='white', font=('Arial 20'), cursor='hand2')
    button_fechar.place(x=1770, y=930)

    consulteproduto = tk.Label(master=janela_google, text='Consulte o produto', bg='#202124', fg='white', font=('Arial', 20, 'bold'))
    consulteproduto.place(x=15, y=220)

    entry_buscar_produtos = PlaceholderEntry(master=janela_google, placeholder='Digite a informação para busca', width=50, font=("Arial", 10))
    entry_buscar_produtos.place(x=15, y=260)

    button_buscar = tk.Button(master=janela_google, text='Buscar', bg='#3bf502' ,fg='black', font='Arial, 20', cursor='hand2')
    button_buscar.place(x=400, y=240)

    # ==========================
    # FRAME SUPERIOR COM A LOGO (dashboard)
    # ==========================
    frame_superior_dashboard = tk.Frame(janela_google, bg="#f2f2f2", height=130)
    frame_superior_dashboard.pack(fill="x")

    label_dashboard = tk.Label(frame_superior_dashboard, text="dashboard", bg="#f2f2f2", fg="#7b7b7b", font=("Arial", 16, "bold"))
    label_dashboard.place(relx=0.12, y=65, anchor='center')

    button_cadastrar = tk.Button(frame_superior_dashboard, text="cadastrar", bg="#f2f2f2", fg="#4a4ae0", font=("Arial", 16, "bold"), bd=0, cursor="hand2", command=lambda: abrir_janela_cadastro(janela_google, produtos))
    button_cadastrar.place(relx=0.29, y=65, anchor='center')

    logo = PhotoImage(file="src\superestoque3000.png")
    lbl_logo = tk.Label(frame_superior_dashboard, image=logo, bg="#f2f2f2")
    lbl_logo.image = logo  # evita que o Python limpe a imagem da memória
    lbl_logo.place(relx=0.5, y=65, anchor='center')

    button_excluir = tk.Button(frame_superior_dashboard, text="excluir", bg="#f2f2f2", fg="#4a4ae0", font=("Arial", 16, "bold"), bd=0, cursor="hand2", command=abrir_janela_excluir)
    button_excluir.place(relx=0.87, y=65, anchor='center')


    # ---------- Função para criar os quadradinhos ----------
    def criar_checkbox(texto, x, y):
        marcado = {"valor": False}

        def alternar():
            if not marcado["valor"]:
                quadrado.config(bg="#4CAF50", text="✓", fg="white")
                marcado["valor"] = True
            else:
                quadrado.config(bg="white", text="", fg="black")
                marcado["valor"] = False

        quadrado = tk.Label(janela_google, text="", bg="white", width=2, height=1, relief="solid", borderwidth=1, cursor='hand2')
        quadrado.place(x=x, y=y)
        quadrado.bind("<Button-1>", lambda event: alternar())

        texto_label = tk.Label(janela_google, text=texto, bg='#202124', fg='white', font=("Arial", 12))
        texto_label.place(x=x + 40, y=y - 2)

        checkboxes.append((quadrado, marcado))
    # -------------------------------------------------------

    # Título
    Filtrar_por_lable = tk.Label(janela_google, text="Filtrar por:", bg='#202124', fg='white', font=('Arial', 18, 'bold'))
    Filtrar_por_lable.place(x=15, y=320, anchor='w')

    # Checkboxes relacionados ao estoque
    criar_checkbox("Nome do produto", 18, 350)
    criar_checkbox("Quantidade", 18, 390)
    criar_checkbox("Data de validade", 18, 430)
    criar_checkbox("Preço de compra", 18, 470)
    criar_checkbox("Preço de venda", 18, 510)
    criar_checkbox("Código do produto", 18, 550)
    criar_checkbox("Fornecedor", 18, 590)

    def limpar_filtro():
        for quadrado, marcado in checkboxes:
            quadrado.config(bg="white", text="", fg="black")
            marcado["valor"] = False

    button_limparfiltro = tk.Button(master=janela_google, text='Limpar filtro', bg='#1A73E8', fg='white', font=('Arial', 20), cursor='hand2', command=limpar_filtro)
    button_limparfiltro.place(x=15, y=640)

    # ---------- Janela cinza de resultados ----------
    frame_resultados = tk.Frame(janela_google, bg="#5a5a5a", width=800, height=300)
    frame_resultados.place(x=1110, y=320)

    # ====================== Exibe produtos no frame cinza ======================
    tk.Label(frame_resultados, text="Código de barras", bg="#5a5a5a", fg="white", font=("Arial", 11, "bold")).place(x=50, y=10)
    tk.Label(frame_resultados, text="Nome do produto", bg="#5a5a5a", fg="white", font=("Arial", 11, "bold")).place(x=200, y=10)
    tk.Label(frame_resultados, text="Data de adição", bg="#5a5a5a", fg="white", font=("Arial", 11, "bold")).place(x=400, y=10)


    # Lista de produtos
    produtos = {
    "1589082": {"nome": "Maçã", "quantidade": "30", "validade": "05/09/2025", "adicao": "05/09/2025", "fornecedor": "Super Frutas", "imagem": "src\maça.png"},
    "1642547": {"nome": "Arroz", "quantidade": "50", "validade": "08/09/2025", "adicao": "08/09/2025", "fornecedor": "Alimentos BR", "imagem": "src\Arroz.png"},
    "3159028": {"nome": "Leite Integral", "quantidade": "20", "validade": "28/08/2025", "adicao": "28/08/2025", "fornecedor": "Laticínios Sul", "imagem": "src\leite.png"}
}
    #JANELA DE CADASTRO DE PRODUTO
    def abrir_janela_cadastro(login_janela2, produtos):
        login_janela2.withdraw()
        janela_cadastro = tk.Toplevel(janela_google)
        janela_cadastro.geometry("800x500")
        janela_cadastro.title("Cadastrar Produto")
        janela_cadastro.config(bg="#5a5a5a")

        cadastro_label = tk.Label(janela_cadastro, text="Cadastre o produto", bg="#5a5a5a", fg="white", font=("Arial", 20, "bold"))
        cadastro_label.place(relx=0.5, y=40, anchor="center")

    # Campos de entrada
        campos = {
        "Nome do produto*": PlaceholderEntry(janela_cadastro, placeholder="Nome do produto", width=30),
        "Quantidade*": PlaceholderEntry(janela_cadastro, placeholder="Quantidade", width=30),
        "Período de validade*": PlaceholderEntry(janela_cadastro, placeholder="dd/mm/aaaa", width=30),
        "Data de adição*": PlaceholderEntry(janela_cadastro, placeholder="dd/mm/aaaa", width=30),
        "Fornecedor*": PlaceholderEntry(janela_cadastro, placeholder="Fornecedor", width=30),
        }

        for i, (label, entry) in enumerate(campos.items()):
            tk.Label(janela_cadastro, text=label, bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=80, y=120 + i * 50)
            entry.place(x=300, y=120 + i * 50)

        mensagem_sucesso = tk.Label(
            janela_cadastro,
            text="Produto cadastrado com sucesso!",
            bg="#5a5a5a",
            fg="#5a5a5a",  # inicialmente "escondido"
            font=("Arial", 12, "bold"))
        mensagem_sucesso.place(x=80, y=400)

    # Função para cadastrar
        def cadastrar_produto():
            nome = campos["Nome do produto*"].get().strip() #Pega o que o usuário digitou
            qtd = campos["Quantidade*"].get().strip() #Pega o que o usuário digitou
            validade = campos["Período de validade*"].get().strip() #Pega o que o usuário digitou
            adicao = campos["Data de adição*"].get().strip() #Pega o que o usuário digitou
            fornecedor = campos["Fornecedor*"].get().strip() #Pega o que o usuário digitou

            if not all([nome, qtd, validade, adicao, fornecedor]):
                mensagem_sucesso.config(text="Preencha todos os campos obrigatórios!", fg="red")
                return

            if not (validade.isdigit() and len(validade) == 8 and adicao.isdigit() and len(adicao) == 8):
                mensagem_sucesso.config(text="As datas devem ter 8 dígitos (ddmmaaaa)!", fg="red")
                return

        # Gera um código de barras simples (pode ser melhorado)
            codigo = str(len(produtos) + 1000001)

            produtos[codigo] = {
            "nome": nome,
            "quantidade": qtd,
            "validade": validade,
            "adicao": adicao,
            "fornecedor": fornecedor,
            "imagem": "sem_imagem.png"
        }

        # Limpa os campos
            for entry in campos.values():
                entry.delete(0, tk.END) #0 é a posição inicial (primeiro caractere) e tk.END é a posição final
                entry.put_placeholder() #recoloca o texto cinza de dica, como ''Nome do produto'' ou ''Quantidade''

        # Mostra a mensagem de sucesso
            mensagem_sucesso.config(text="Produto cadastrado com sucesso!", fg="lime")

            print("Produto cadastrado:", produtos[codigo])

        button_cadastar_verde=tk.Button(janela_cadastro, text="CADASTRAR", bg="limegreen", fg="white", font=("Arial", 14, "bold"), cursor="hand2", command=cadastrar_produto)
        button_cadastar_verde.place(x=500, y=430)

        button_voltar_parasplashpage=tk.Button(janela_cadastro, text="VOLTAR", bg='#1A73E8', fg='white', font=("Arial", 14, "bold"), cursor="hand2", command=lambda: (janela_cadastro.destroy(), janela_google.deiconify()))
        button_voltar_parasplashpage.place(x=660, y=430)
    #===================================================================================================================================================
    #Mostra o que aparece quando clica em ''Detalhes''===================================================================================================================
    def mostrar_detalhes(codigo):
        janela_google.withdraw()
        produto = produtos[codigo]  # busca o produto pelo código
        detalhes = tk.Toplevel(janela_google)
        detalhes.title(f"Detalhes do Produto - {produto['nome']}")
        detalhes.geometry("600x400")
        detalhes.configure(bg="#555")

        tk.Label(detalhes, text="DETALHES DO PRODUTO", font=("Arial", 14, "bold"), bg="#555", fg="white").place(x=180, y=30)

    # cria os labels dinamicamente com base nas chaves do dicionário
        for i, (chave, valor) in enumerate(produto.items()):
            if chave!="imagem":
                tk.Label(detalhes, text=f"{chave.capitalize()}*:", bg="#555", fg="white", font=("Arial", 12, "bold")).place(x=50, y=100 + i * 40)
                tk.Label(detalhes, text=valor, bg="#555", fg="white", font=("Arial", 12)).place(x=200, y=100 + i * 40)

        button_voltar = tk.Button(detalhes, text="VOLTAR", bg='#1A73E8', fg='white', command=lambda: (detalhes.destroy(), janela_google.deiconify()), cursor='hand2')
        button_voltar.place(x=530, y=360)

        img = tk.PhotoImage(file=produto["imagem"])
        label_img = tk.Label(detalhes, image=img, bg="#555")
        label_img.image = img  # 👈 evita o bug da imagem sumir
        label_img.place(x=350, y=100)
    #======================================================================================================================================================================

    for i, (codigo, produto) in enumerate(produtos.items()):
        tk.Label(frame_resultados, text=codigo, bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=50, y=50 + i * 50)
        tk.Label(frame_resultados, text=produto["nome"], bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=200, y=50 + i * 50)
        tk.Label(frame_resultados, text=produto["adicao"], bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=400, y=50 + i * 50)

    # botão detalhes passa o código como argumento
        tk.Button(frame_resultados, text="DETALHES", bg='#1A73E8', fg='white', command=lambda c=codigo: mostrar_detalhes(c), cursor='hand2').place(x=700, y=48 + i * 50)

     # ===========================================================
    # JANELA DE EDIÇÃO DE PRODUTO
    # ============================================================================================================================================================
    def abrir_janela_edicao():
        janela_google.withdraw()
        janela_editar = tk.Toplevel(janela_google)
        janela_editar.geometry("800x500")
        janela_editar.title("Editar Produto")
        janela_editar.config(bg="#5a5a5a")

        tk.Label(janela_editar, text="Edite o produto", bg="#5a5a5a", fg="white",
                 font=("Arial", 20, "bold")).place(relx=0.5, y=40, anchor="center")

        # Cabeçalho da tabela
        tk.Label(janela_editar, text="Código de barras", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=60, y=100)
        tk.Label(janela_editar, text="Nome do produto", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=250, y=100)
        tk.Label(janela_editar, text="Data de adição", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=440, y=100)

        # Exibir os produtos com botão "Editar"
        for i, (codigo, produto) in enumerate(produtos.items()):
            tk.Label(janela_editar, text=codigo, bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=60, y=140 + i * 50)
            tk.Label(janela_editar, text=produto["nome"], bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=250, y=140 + i * 50)
            tk.Label(janela_editar, text=produto["adicao"], bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=440, y=140 + i * 50)

            tk.Button(janela_editar, text="Editar", bg="#f7b731", fg="black",
                      font=("Arial", 10, "bold"), cursor="hand2",
                      command=lambda c=codigo: editar_produto(c, janela_editar)).place(x=640, y=135 + i * 50)

        tk.Button(janela_editar, text="VOLTAR", bg='#1A73E8', fg='white',
                  font=("Arial", 14, "bold"), cursor="hand2",
                  command=lambda: (janela_editar.destroy(), janela_google.deiconify())).place(x=660, y=430)
    #==============================================================================================================================================================
    #JANELA DE EDIÇÃO INDIVIDUAL DE PRODUTO
    #==============================================================================================================================================================
    def editar_produto(codigo, janela_editar):
        janela_editar.withdraw()
        produto = produtos[codigo]
        janela_formulario = tk.Toplevel(janela_editar)
        janela_formulario.geometry("800x500")
        janela_formulario.title("Editar Produto")
        janela_formulario.config(bg="#5a5a5a")

        tk.Label(janela_formulario, text="Edite seu produto", bg="#5a5a5a", fg="white",
                 font=("Arial", 20, "bold")).place(relx=0.5, y=40, anchor="center")

        # Campos de entrada
        campos = {
            "Nome do produto": PlaceholderEntry(janela_formulario, placeholder="Nome do produto", width=30, color='black'),
            "Quantidade": PlaceholderEntry(janela_formulario, placeholder="Quantidade", width=30, color='black'),
            "Período de validade": PlaceholderEntry(janela_formulario, placeholder="dd/mm/aaaa", width=30, color='black'),
            "Data de adição": PlaceholderEntry(janela_formulario, placeholder="dd/mm/aaaa", width=30, color='black'),
            "Fornecedor": PlaceholderEntry(janela_formulario, placeholder="Fornecedor", width=30, color='black'),
        }

        # Preencher campos com dados atuais
        dados = {                           #Esse dicionário não tem nada a ver com a interface. Ele é só uma estrutura na memória com os valores atuais do produto que veio do dicionário produtos.
                "Nome do produto": produto["nome"],
                "Quantidade": produto["quantidade"],
                "Período de validade": produto["validade"],
                "Data de adição": produto["adicao"],
                "Fornecedor": produto["fornecedor"]
                }

        for chave, valor in dados.items():
            campos[chave].delete(0, tk.END)
            campos[chave].insert(0, valor)

        for i, (label, entry) in enumerate(campos.items()):
            tk.Label(janela_formulario, text=label + ":", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=80, y=120 + i * 50)
            entry.place(x=300, y=120 + i * 50)

        # Imagem do produto
        img = tk.PhotoImage(file=produto["imagem"])
        label_img = tk.Label(janela_formulario, image=img, bg="#5a5a5a")
        label_img.image = img
        label_img.place(x=550, y=120)

        mensagem = tk.Label(
        janela_formulario,
        text="Produto editado com sucesso!",
        bg="#5a5a5a",
        fg="#5a5a5a",  # mesma cor do fundo = invisível no início
        font=("Arial", 12, "bold")
        )
        mensagem.place(x=80, y=400)

         # Função para confirmar a edição
        def confirmar_edicao():
            nome = campos["Nome do produto"].get().strip()
            qtd = campos["Quantidade"].get().strip()
            validade = campos["Período de validade"].get().strip()
            adicao = campos["Data de adição"].get().strip()
            fornecedor = campos["Fornecedor"].get().strip()

            if not all([nome, qtd, validade, adicao, fornecedor]):
                mensagem.config(text="Preencha todos os campos obrigatórios!", fg="red")
                return

            if not (validade.isdigit() and len(validade) == 8 and adicao.isdigit() and len(adicao) == 8):
                mensagem.config(text="As datas devem ter 8 dígitos (ddmmaaaa)!", fg="red")
                return

            produto.update({
                "nome": nome,
                "quantidade": qtd,
                "validade": validade,
                "adicao": adicao,
                "fornecedor": fornecedor
            })

            mensagem.config(text="Produto editado com sucesso!", fg="lime")

            # Fecha a janela de edição individual e a lista
            janela_formulario.destroy()
            janela_editar.destroy()
            
            # Reabre a janela "Edite o produto" com os dados atualizados
            abrir_janela_edicao()

        tk.Button(janela_formulario, text="Confirmar", bg="limegreen", fg="white", font=("Arial", 14, "bold"), cursor="hand2", command=confirmar_edicao).place(x=500, y=430)

        tk.Button(janela_formulario, text="VOLTAR", bg='#1A73E8', fg='white', font=("Arial", 14, "bold"), cursor="hand2", command=lambda: (janela_formulario.destroy(), janela_editar.deiconify())).place(x=660, y=430)
    #==============================================================================================================================================================  
    button_editar = tk.Button(frame_superior_dashboard, text="editar", bg="#f2f2f2", fg="#4a4ae0", font=("Arial", 16, "bold"), bd=0, cursor="hand2", command=abrir_janela_edicao)
    button_editar.place(relx=0.70, y=65, anchor='center')
        

def login_janela3(login_janela):
    login_janela.withdraw()
    janela_avancar = tk.Toplevel(login_janela)
    janela_avancar.geometry("500x250")
    janela_avancar.title("Insira sua senha")
    janela_avancar.config(bg='#202124')

    entry_senha= PlaceholderEntry(master=janela_avancar, placeholder="Senha", show='*') # pode usar show="*" para não mostrar a senha digitada
    entry_senha.place(relx=0.5, rely=0.3, anchor='center')
    
    button_avancarsenha = tk.Button(master=janela_avancar, text="Entrar", state="disabled", command=lambda: login_janela2(janela_avancar), bg='#1A73E8', fg='white', disabledforeground="#b8bfba", cursor='hand2')
    button_avancarsenha.place(relx=0.5, rely=0.5, anchor='center')
    
    def check_entry_senha(event=None):
        texto = entry_senha.get().strip()
        if texto:
            button_avancarsenha.configure(state="normal")
        else:
            button_avancarsenha.configure(state="disabled")
    
    entry_senha.bind("<KeyRelease>", check_entry_senha)

    button_fecharsenha = tk.Button(master=janela_avancar, text="Voltar", command=lambda: (janela_avancar.destroy(), login_janela.deiconify()), bg='#1A73E8', fg='white', cursor='hand2')
    button_fecharsenha.place(x=440, y=210)

    botao_esqueceusenha2 = tk.Button(master=janela_avancar, text="Esqueceu a senha?", command=lambda: janelaesqueceuAsenha(janela_avancar), bg='#1A73E8', fg='white', cursor='hand2')
    botao_esqueceusenha2.place(relx=0.5, rely=0.70, anchor='center')

def janelaesqueceuAsenha(login_janela):
    login_janela.withdraw()
    janelaesqueceusenha = tk.Toplevel(login_janela)
    janelaesqueceusenha.geometry("500x250")
    janelaesqueceusenha.title("Recuperar senha")
    janelaesqueceusenha.config(bg='#202124')

    button_fecharrecupesenha = tk.Button(master=janelaesqueceusenha, text="Voltar", command=lambda: (janelaesqueceusenha.destroy(), login_janela.deiconify()), bg='#1A73E8', fg='white', cursor='hand2')
    button_fecharrecupesenha.place(x=440, y=210)

    trocardesenha = tk.Label(master=janelaesqueceusenha, text="Trocar de senha", bg='#202124', fg='white', font=('Arial 20'))
    trocardesenha.place(relx=0.5, rely=0.25, anchor='center')

    entry_login_email= PlaceholderEntry(master=janelaesqueceusenha, placeholder=('Login/e-mail'))
    entry_login_email.place(relx=0.5, rely=0.40, anchor='center')

    mensagemaviso = tk.Label(master=janelaesqueceusenha, text="Nós iremos enviar um código de recuperação de acesso no seu e-mail. \nPor favor digitar no campo abaixo", bg='#202124', fg='white')
    mensagemaviso.place(relx=0.5, rely=0.55, anchor='center')

    entry_codigo= PlaceholderEntry(master=janelaesqueceusenha, placeholder=('Código de recuperação'))
    entry_codigo.place(relx=0.5, rely=0.70, anchor='center')

    trocarasenha = tk.Button(master=janelaesqueceusenha, text='Trocar de senha',command=lambda: janelaconfirmação(janelaesqueceusenha) , state='disabled', bg='#1A73E8', fg='white', disabledforeground="#b8bfba", cursor='hand2')
    trocarasenha.place(relx=0.5, rely=0.85, anchor='center')

    def verificar_codigo(event=None):
        codigo = entry_codigo.get().strip()
        if len(codigo) == 6 and codigo.isdigit():
            trocarasenha.config(state='normal')
        else:
            trocarasenha.config(state='disabled')

    entry_codigo.bind("<KeyRelease>", verificar_codigo)

    enviar_codigo= tk.Button(master=janelaesqueceusenha, text='Enviar código', command=lambda: print("Código enviado!"), bg='#1A73E8', fg='white', cursor='hand2')
    enviar_codigo.place(relx=0.75, rely=0.4, anchor='center')

def janelaconfirmação(janelaesqueceuAsenha):
    janelaesqueceuAsenha.withdraw()
    janelaconfirmação = tk.Toplevel(janelaesqueceuAsenha)
    janelaconfirmação.geometry('500x250')
    janelaconfirmação.title('Confirme sua senha')
    janelaconfirmação.config(bg='#202124')

    trocardesenha = tk.Label(master=janelaconfirmação, text="Trocar de senha", bg='#202124', fg='white', font=('Arial 20'))
    trocardesenha.place(relx=0.5, rely=0.25, anchor='center')

    entrynovasenha=PlaceholderEntry(master=janelaconfirmação, placeholder='Digite sua nova senha')
    entrynovasenha.place(relx=0.5, rely=0.4, anchor='center')

    entryconfirmenovasenha=PlaceholderEntry(master=janelaconfirmação, placeholder='Confirme sua nova senha')
    entryconfirmenovasenha.place(relx=0.5, rely=0.55, anchor='center')

    button_fecharconfirmação=tk.Button(master=janelaconfirmação, text='Voltar', command=lambda: (janelaconfirmação.destroy(), janelaesqueceuAsenha.deiconify()), bg='#1A73E8', fg='white', cursor='hand2')
    button_fecharconfirmação.place(x=440, y=210)

    confirmar_senha= tk.Button(master=janelaconfirmação, text='Confirmar', command=lambda: (janelaconfirmação.destroy(), login_janela(), print("Sua senha foi redefinida com sucesso!")), state='disabled', bg='#1A73E8', fg='white', disabledforeground="#b8bfba", cursor='hand2')
    confirmar_senha.place(relx=0.5, rely=0.70, anchor='center')

    def verificar_confirmação(event=None):
        novasenha = entrynovasenha.get().strip()
        confirmarsenha = entryconfirmenovasenha.get().strip()
        if novasenha==confirmarsenha:
            confirmar_senha.config(state='normal')
        else:
            confirmar_senha.config(state='disabled')
    
    entrynovasenha.bind("<KeyRelease>", verificar_confirmação)
    entryconfirmenovasenha.bind("<KeyRelease>", verificar_confirmação)


app.mainloop()