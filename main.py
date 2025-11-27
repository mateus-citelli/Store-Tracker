from tkinter import *
import tkinter as tk
from classes_estoque import Estoque, BotaoVoltar, CriarJanela, PlaceholderEntry, ListaProdutos
import json
import os
# importe as classes POO que você criou em CRUD (ou nome do arquivo que você salvou)
from CRUD import CreateProduto, ReadProduto, RemoverProdutoWindow, EditarProdutoWindow
#Classes CreateProduto e ReadProduto criadas por Túlio, classes EditarProdutoWindow e RemoverProdutoWindow criadas por Mateus

estoque = Estoque()

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

    # lista de checkboxes (os quadradinhos para o filtro)
    checkboxes = []

    button_fechar = BotaoVoltar(
        janela_google, text="Voltar", bg='#1A73E8', fg='white', font=('Arial 20'))
    button_fechar.place(x=1770, y=930)

    # FRAME SUPERIOR COM A LOGO (dashboard)
    frame_superior_dashboard = tk.Frame(janela_google, bg="#f2f2f2", height=130)
    frame_superior_dashboard.pack(fill="x")

    label_dashboard = tk.Label(frame_superior_dashboard, text="dashboard", bg="#f2f2f2", fg="#7b7b7b", font=("Arial", 16, "bold"))
    label_dashboard.place(relx=0.12, y=65, anchor='center')

    # Exibe produtos no frame_resultados
    # Exibe os produtos usando a classe ReadProduto (instância usada também para atualizar quando necessário)
    read_produto = ReadProduto(janela_google, estoque)

    # abrir_janela_cadastro passa a usar 'produtos' global; a função interna chamará salvar_produtos
    button_cadastrar = tk.Button(frame_superior_dashboard, text="cadastrar", bg="#f2f2f2", fg="#4a4ae0", font=("Arial", 16, "bold"), bd=0, cursor="hand2", command=lambda: CreateProduto(janela_google, estoque, read_produto))
    button_cadastrar.place(relx=0.29, y=65, anchor='center')

    logo = PhotoImage(file="superestoque3000.png")
    lbl_logo = tk.Label(frame_superior_dashboard, image=logo, bg="#f2f2f2")
    lbl_logo.image = logo
    lbl_logo.place(relx=0.5, y=65, anchor='center')

    button_excluir = tk.Button(frame_superior_dashboard, text="excluir", bg="#f2f2f2", fg="#4a4ae0", font=("Arial", 16, "bold"), bd=0, cursor="hand2", command=lambda: RemoverProdutoWindow(janela_google, estoque, read_produto))
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

        quadrado = tk.Label(janela_google, text="", bg="white", width=2,
                            height=1, relief="solid", borderwidth=1, cursor='hand2')
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
    criar_checkbox("Data de adição", 18, 470)
    criar_checkbox("Preço de venda", 18, 510)
    criar_checkbox("Código do produto", 18, 550)
    criar_checkbox("Fornecedor", 18, 590)

    def limpar_filtro():
        for quadrado, marcado in checkboxes:
            quadrado.config(bg="white", text="", fg="black")
            marcado["valor"] = False

    button_limparfiltro = tk.Button(master=janela_google, text='Limpar filtro', bg='#1A73E8', fg='white', font=('Arial', 20), cursor='hand2', command=limpar_filtro)
    button_limparfiltro.place(x=15, y=640)

    # -------------------------------------------------------
    button_editar = tk.Button(frame_superior_dashboard, text="editar", bg="#f2f2f2", fg="#4a4ae0", font=("Arial", 16, "bold"), bd=0, cursor="hand2", command=lambda: EditarProdutoWindow(janela_google, estoque, read_produto))
    button_editar.place(relx=0.70, y=65, anchor='center')


def login_janela3(login_janela):
    janela_avancar = CriarJanela(login_janela, 500, 250, "Insira sua senha", '#202124')

    entry_senha = PlaceholderEntry(master=janela_avancar, placeholder="Senha", show='*')
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

    button_fecharsenha = BotaoVoltar(janela_avancar, text="Voltar", bg='#1A73E8', fg='white')
    button_fecharsenha.place(x=440, y=210)

    botao_esqueceusenha2 = tk.Button(master=janela_avancar, text="Esqueceu a senha?", command=lambda: janelaesqueceuAsenha(janela_avancar), bg='#1A73E8', fg='white', cursor='hand2')
    botao_esqueceusenha2.place(relx=0.5, rely=0.70, anchor='center')


def janelaesqueceuAsenha(login_janela):
    janelaesqueceusenha = CriarJanela(login_janela, 500, 250, "Recuperar senha", '#202124')

    button_fecharrecupesenha = BotaoVoltar(janelaesqueceusenha, text="Voltar", bg='#1A73E8', fg='white')
    button_fecharrecupesenha.place(x=440, y=210)

    trocardesenha = tk.Label(master=janelaesqueceusenha, text="Trocar de senha", bg='#202124', fg='white', font=('Arial 20'))
    trocardesenha.place(relx=0.5, rely=0.25, anchor='center')

    entry_login_email = PlaceholderEntry(master=janelaesqueceusenha, placeholder=('Login/e-mail'))
    entry_login_email.place(relx=0.5, rely=0.40, anchor='center')

    mensagemaviso = tk.Label(master=janelaesqueceusenha, text="Nós iremos enviar um código de recuperação de acesso no seu e-mail. \nPor favor digitar no campo abaixo", bg='#202124', fg='white')
    mensagemaviso.place(relx=0.5, rely=0.55, anchor='center')

    entry_codigo = PlaceholderEntry(master=janelaesqueceusenha, placeholder=('Código de recuperação'))
    entry_codigo.place(relx=0.5, rely=0.70, anchor='center')

    trocarasenha = tk.Button(master=janelaesqueceusenha, text='Trocar de senha', command=lambda: janelaconfirmação(janelaesqueceusenha), state='disabled', bg='#1A73E8', fg='white', disabledforeground="#b8bfba", cursor='hand2')
    trocarasenha.place(relx=0.5, rely=0.85, anchor='center')

    def verificar_codigo(event=None):
        codigo = entry_codigo.get().strip()
        if len(codigo) == 6 and codigo.isdigit():
            trocarasenha.config(state='normal')
        else:
            trocarasenha.config(state='disabled')

    entry_codigo.bind("<KeyRelease>", verificar_codigo)

    enviar_codigo = tk.Button(master=janelaesqueceusenha, text='Enviar código', command=lambda: print("Código enviado!"), bg='#1A73E8', fg='white', cursor='hand2')
    enviar_codigo.place(relx=0.75, rely=0.4, anchor='center')


def janelaconfirmação(janelaesqueceuAsenha):
    janelaconfirmação = CriarJanela(janelaesqueceuAsenha, 500, 250, "Confirme sua senha", '#202124')

    trocardesenha = tk.Label(master=janelaconfirmação, text="Trocar de senha", bg='#202124', fg='white', font=('Arial 20'))
    trocardesenha.place(relx=0.5, rely=0.25, anchor='center')

    entrynovasenha = PlaceholderEntry(master=janelaconfirmação, placeholder='Digite sua nova senha')
    entrynovasenha.place(relx=0.5, rely=0.4, anchor='center')

    entryconfirmenovasenha = PlaceholderEntry(master=janelaconfirmação, placeholder='Confirme sua nova senha')
    entryconfirmenovasenha.place(relx=0.5, rely=0.55, anchor='center')

    button_fecharconfirmação = BotaoVoltar(janelaconfirmação, text='Voltar', bg='#1A73E8', fg='white')
    button_fecharconfirmação.place(x=440, y=210)

    confirmar_senha = tk.Button(master=janelaconfirmação, text='Confirmar', command=lambda: (janelaconfirmação.destroy(), login_janela(), print("Sua senha foi redefinida com sucesso!")), state='disabled', bg='#1A73E8', fg='white', disabledforeground="#b8bfba", cursor='hand2')
    confirmar_senha.place(relx=0.5, rely=0.70, anchor='center')

    def verificar_confirmação(event=None):
        novasenha = entrynovasenha.get().strip()
        confirmarsenha = entryconfirmenovasenha.get().strip()
        if novasenha == confirmarsenha:
            confirmar_senha.config(state='normal')
        else:
            confirmar_senha.config(state='disabled')

    entrynovasenha.bind("<KeyRelease>", verificar_confirmação)
    entryconfirmenovasenha.bind("<KeyRelease>", verificar_confirmação)


app.mainloop()
