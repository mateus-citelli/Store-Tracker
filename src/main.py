from tkinter import *
import tkinter as tk
from classes_estoque import *
from CRUD import *
import json
import os

armazem = "produtos.json"

# --- Funções de persistência (JSON) ---
def carregar_produtos():
    """Carrega o arquivo JSON; retorna {} se não existir ou estiver vazio."""
    if os.path.exists(armazem):
        try:
            with open(armazem, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Se o JSON estiver inválido, recomeça vazio
            return {}
    else:
        return {}

def salvar_produtos(produtos):
    """Salva o dicionário 'produtos' no arquivo JSON."""
    with open(armazem, "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

def adicionar_produto_json(codigo, nome, quantidade, validade, adicao, fornecedor, imagem):
    """Função utilitária que adiciona e salva no JSON (pode ser usada fora das janelas)."""
    produtos = carregar_produtos()
    produtos[codigo] = {
        "nome": nome,
        "quantidade": quantidade,
        "validade": validade,
        "adicao": adicao,
        "fornecedor": fornecedor,
        "imagem": imagem
    }
    salvar_produtos(produtos)
    print(f"'{nome}' foi adicionado ao estoque.")

# --- Carrega produtos no início (variável global usada pela UI) ---
produtos = carregar_produtos()

# --- Interface Tkinter ---
app = tk.Tk()
app.geometry("500x250")
app.title("Estoque")
app.config(bg='#202124')

label = tk.Label(app, text="Olá, Usuário!", bg='#202124', fg='white')
label.pack(pady=40)

def login_janela():
    janela_login = CriarJanela(app, 500, 250, "Login", '#202124')
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
    janela_google = CriarJanela(login_janela, 1920, 1080, "Splash Page", '#202124')

    # JANELA DE EXCLUIR PRODUTO
    RemoverProdutoWindow(janela_google, estoque, read_produto)

    # lista de checkboxes (os quadradinhos para o filtro)
    checkboxes = []

    button_fechar = tk.Button(master=janela_google, text="Voltar", command=lambda: (janela_google.fechar()), bg='#1A73E8', fg='white', font=('Arial 20'), cursor='hand2')
    button_fechar.place(x=1770, y=930)

    consulteproduto = tk.Label(master=janela_google, text='Consulte o produto', bg='#202124', fg='white', font=('Arial', 20, 'bold'))
    consulteproduto.place(x=15, y=220)

    entry_buscar_produtos = PlaceholderEntry(master=janela_google, placeholder='Digite a informação para busca', width=50, font=("Arial", 10))
    entry_buscar_produtos.place(x=15, y=260)

    button_buscar = tk.Button(master=janela_google, text='Buscar', bg='#3bf502' ,fg='black', font='Arial, 20', cursor='hand2')
    button_buscar.place(x=400, y=240)

    # FRAME SUPERIOR COM A LOGO (dashboard)
    frame_superior_dashboard = tk.Frame(janela_google, bg="#f2f2f2", height=130)
    frame_superior_dashboard.pack(fill="x")

    label_dashboard = tk.Label(frame_superior_dashboard, text="dashboard", bg="#f2f2f2", fg="#7b7b7b", font=("Arial", 16, "bold"))
    label_dashboard.place(relx=0.12, y=65, anchor='center')

    # abrir_janela_cadastro passa a usar 'produtos' global; a função interna chamará salvar_produtos
    button_cadastrar = tk.Button(frame_superior_dashboard, text="cadastrar", bg="#f2f2f2", fg="#4a4ae0", font=("Arial", 16, "bold"), bd=0, cursor="hand2", command=lambda: abrir_janela_cadastro(janela_google))
    button_cadastrar.place(relx=0.29, y=65, anchor='center')

    logo = PhotoImage(file="src\superestoque3000.png")
    lbl_logo = tk.Label(frame_superior_dashboard, image=logo, bg="#f2f2f2")
    lbl_logo.image = logo
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

    Filtrar_por_label = tk.Label(janela_google, text="Filtrar por:", bg='#202124', fg='white', font=('Arial', 18, 'bold'))
    Filtrar_por_label.place(x=15, y=320, anchor='w')

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

    # Janela de resultados
    frame_resultados = tk.Frame(janela_google, bg="#5a5a5a", width=800, height=300)
    frame_resultados.place(x=1110, y=320)

    tk.Label(frame_resultados, text="Código de barras", bg="#5a5a5a", fg="white", font=("Arial", 11, "bold")).place(x=50, y=10)
    tk.Label(frame_resultados, text="Nome do produto", bg="#5a5a5a", fg="white", font=("Arial", 11, "bold")).place(x=200, y=10)
    tk.Label(frame_resultados, text="Data de adição", bg="#5a5a5a", fg="white", font=("Arial", 11, "bold")).place(x=400, y=10)

    # JANELA DE CADASTRO DE PRODUTO
    def abrir_janela_cadastro(login_janela2):
        janela_cadastro = CriarJanela(login_janela2, 800, 500, "Cadastrar Produto", "#5a5a5a")

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

        def cadastrar_produto():
            nome = campos["Nome do produto*"].get().strip()
            qtd = campos["Quantidade*"].get().strip()
            validade = campos["Período de validade*"].get().strip()
            adicao = campos["Data de adição*"].get().strip()
            fornecedor = campos["Fornecedor*"].get().strip()

            if not all([nome, qtd, validade, adicao, fornecedor]):
                mensagem_sucesso.config(text="Preencha todos os campos obrigatórios!", fg="red")
                return

            if not (validade.isdigit() and len(validade) == 8 and adicao.isdigit() and len(adicao) == 8):
                mensagem_sucesso.config(text="As datas devem ter 8 dígitos (ddmmaaaa)!", fg="red")
                return

            # Gera um código simples
            codigo = str(len(produtos) + 1000001)

            produtos[codigo] = {
                "nome": nome,
                "quantidade": qtd,
                "validade": validade,
                "adicao": adicao,
                "fornecedor": fornecedor,
                "imagem": "sem_imagem.png"
            }

            # salva imediatamente no JSON
            salvar_produtos(produtos)

            # Limpa os campos
            for entry in campos.values():
                entry.delete(0, tk.END)
                entry.put_placeholder()

            mensagem_sucesso.config(text="Produto cadastrado com sucesso!", fg="lime")
            print("Produto cadastrado:", produtos[codigo])

        button_cadastar_verde = tk.Button(janela_cadastro, text="CADASTRAR", bg="limegreen", fg="white", font=("Arial", 14, "bold"), cursor='hand2', command=cadastrar_produto)
        button_cadastar_verde.place(x=500, y=430)

        button_voltar_parasplashpage = tk.Button(janela_cadastro, text="VOLTAR", bg='#1A73E8', fg='white', font=("Arial", 14, "bold"), cursor="hand2", command=lambda: (janela_cadastro.fechar()))
        button_voltar_parasplashpage.place(x=660, y=430)

    # MOSTRA O QUE APARECE QUANDO CLICA EM ''Detalhes''
    def mostrar_detalhes(codigo):
        produto = produtos[codigo]
        detalhes = CriarJanela(janela_google, 600, 400, f"Detalhes do Produto - {produto['nome']}", "#555" )
        
        tk.Label(detalhes, text="DETALHES DO PRODUTO", font=("Arial", 14, "bold"), bg="#555", fg="white").place(x=180, y=30)

        for i, (chave, valor) in enumerate(produto.items()):
            if chave!="imagem":
                tk.Label(detalhes, text=f"{chave.capitalize()}*:", bg="#555", fg="white", font=("Arial", 12, "bold")).place(x=50, y=100 + i * 40)
                tk.Label(detalhes, text=valor, bg="#555", fg="white", font=("Arial", 12)).place(x=200, y=100 + i * 40)

        button_voltar = tk.Button(detalhes, text="VOLTAR", bg='#1A73E8', fg='white', command=lambda: (detalhes.fechar()), cursor='hand2')
        button_voltar.place(x=530, y=360)

        img = tk.PhotoImage(file=produto["imagem"])
        label_img = tk.Label(detalhes, image=img, bg="#555")
        label_img.image = img
        label_img.place(x=350, y=100)

    # Exibe produtos no frame_resultados
    for i, (codigo, produto) in enumerate(produtos.items()):
        tk.Label(frame_resultados, text=codigo, bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=50, y=50 + i * 50)
        tk.Label(frame_resultados, text=produto["nome"], bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=200, y=50 + i * 50)
        tk.Label(frame_resultados, text=produto["adicao"], bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=400, y=50 + i * 50)

        tk.Button(frame_resultados, text="DETALHES", bg='#1A73E8', fg='white', command=lambda c=codigo: mostrar_detalhes(c), cursor='hand2').place(x=700, y=48 + i * 50)

    # JANELA DE EDIÇÃO DE PRODUTO (lista)
    def abrir_janela_edicao():
        janela_editar = CriarJanela(janela_google, 800, 500, "Editar Produto","#5a5a5a" )

        tk.Label(janela_editar, text="Edite o produto", bg="#5a5a5a", fg="white",
                 font=("Arial", 20, "bold")).place(relx=0.5, y=40, anchor="center")

        tk.Label(janela_editar, text="Código de barras", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=60, y=100)
        tk.Label(janela_editar, text="Nome do produto", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=250, y=100)
        tk.Label(janela_editar, text="Data de adição", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=440, y=100)

        for i, (codigo, produto) in enumerate(produtos.items()):
            tk.Label(janela_editar, text=codigo, bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=60, y=140 + i * 50)
            tk.Label(janela_editar, text=produto["nome"], bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=250, y=140 + i * 50)
            tk.Label(janela_editar, text=produto["adicao"], bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=440, y=140 + i * 50)

            tk.Button(janela_editar, text="Editar", bg="#f7b731", fg="black",
                      font=("Arial", 10, "bold"), cursor="hand2",
                      command=lambda c=codigo: editar_produto(c, janela_editar)).place(x=640, y=135 + i * 50)

        tk.Button(janela_editar, text="VOLTAR", bg='#1A73E8', fg='white',
                  font=("Arial", 14, "bold"), cursor="hand2",
                  command=lambda: (janela_editar.fechar())).place(x=660, y=430)

    # JANELA DE EDIÇÃO INDIVIDUAL DE PRODUTO
    def editar_produto(codigo, janela_editar):
        produto = produtos[codigo]
        janela_formulario = CriarJanela(janela_editar, 800, 500, "Editar Produto", "#5a5a5a")

        tk.Label(janela_formulario, text="Edite seu produto", bg="#5a5a5a", fg="white",
                 font=("Arial", 20, "bold")).place(relx=0.5, y=40, anchor="center")

        campos = {
            "Nome do produto": PlaceholderEntry(janela_formulario, placeholder="Nome do produto", width=30, color='black'),
            "Quantidade": PlaceholderEntry(janela_formulario, placeholder="Quantidade", width=30, color='black'),
            "Período de validade": PlaceholderEntry(janela_formulario, placeholder="dd/mm/aaaa", width=30, color='black'),
            "Data de adição": PlaceholderEntry(janela_formulario, placeholder="dd/mm/aaaa", width=30, color='black'),
            "Fornecedor": PlaceholderEntry(janela_formulario, placeholder="Fornecedor", width=30, color='black'),
        }

        dados = {
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

        img = tk.PhotoImage(file=produto["imagem"])
        label_img = tk.Label(janela_formulario, image=img, bg="#5a5a5a")
        label_img.image = img
        label_img.place(x=550, y=120)

        mensagem = tk.Label(
        janela_formulario,
        text="Produto editado com sucesso!",
        bg="#5a5a5a",
        fg="#5a5a5a",
        font=("Arial", 12, "bold")
        )
        mensagem.place(x=80, y=400)

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

            # salva no JSON após edição
            salvar_produtos(produtos)

            mensagem.config(text="Produto editado com sucesso!", fg="lime")

            # Fecha a janela de edição individual e a lista e reabre a lista atualizada
            janela_formulario.destroy()
            janela_editar.destroy()
            abrir_janela_edicao()

        tk.Button(janela_formulario, text="Confirmar", bg="limegreen", fg="white", font=("Arial", 14, "bold"), cursor='hand2', command=confirmar_edicao).place(x=500, y=430)

        tk.Button(janela_formulario, text="VOLTAR", bg='#1A73E8', fg='white', font=("Arial", 14, "bold"), cursor="hand2", command=lambda: (janela_formulario.fechar())).place(x=660, y=430)

    button_editar = tk.Button(frame_superior_dashboard, text="editar", bg="#f2f2f2", fg="#4a4ae0", font=("Arial", 16, "bold"), bd=0, cursor="hand2", command=abrir_janela_edicao)
    button_editar.place(relx=0.70, y=65, anchor='center')
        
def login_janela3(login_janela):
    janela_avancar = CriarJanela(login_janela, 500, 250, "Insira sua senha", '#202124')

    entry_senha= PlaceholderEntry(master=janela_avancar, placeholder="Senha", show='*')
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

    button_fecharsenha = tk.Button(master=janela_avancar, text="Voltar", command=lambda: (janela_avancar.fechar()), bg='#1A73E8', fg='white', cursor='hand2')
    button_fecharsenha.place(x=440, y=210)

    botao_esqueceusenha2 = tk.Button(master=janela_avancar, text="Esqueceu a senha?", command=lambda: janelaesqueceuAsenha(janela_avancar), bg='#1A73E8', fg='white', cursor='hand2')
    botao_esqueceusenha2.place(relx=0.5, rely=0.70, anchor='center')

def janelaesqueceuAsenha(login_janela):
    janelaesqueceusenha = CriarJanela(login_janela, 500, 250, "Recuperar senha", '#202124')

    button_fecharrecupesenha = tk.Button(master=janelaesqueceusenha, text="Voltar", command=lambda: (janelaesqueceusenha.fechar()), bg='#1A73E8', fg='white', cursor='hand2')
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
    janelaconfirmação = CriarJanela(janelaesqueceuAsenha, 500, 250, "Confirme sua senha", '#202124')

    trocardesenha = tk.Label(master=janelaconfirmação, text="Trocar de senha", bg='#202124', fg='white', font=('Arial 20'))
    trocardesenha.place(relx=0.5, rely=0.25, anchor='center')

    entrynovasenha=PlaceholderEntry(master=janelaconfirmação, placeholder='Digite sua nova senha')
    entrynovasenha.place(relx=0.5, rely=0.4, anchor='center')

    entryconfirmenovasenha=PlaceholderEntry(master=janelaconfirmação, placeholder='Confirme sua nova senha')
    entryconfirmenovasenha.place(relx=0.5, rely=0.55, anchor='center')

    button_fecharconfirmação=tk.Button(master=janelaconfirmação, text='Voltar', command=lambda: (janelaconfirmação.fechar()), bg='#1A73E8', fg='white', cursor='hand2')
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