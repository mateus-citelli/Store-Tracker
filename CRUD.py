<<<<<<< Updated upstream
#CRIAR O PRODUTO
import tkinter as tk
from classes_estoque import CriarJanela, PlaceholderEntry, BotaoVoltar

class CreateProduto(CriarJanela):
    def __init__(self, parent, estoque, read_produto):
        super().__init__(parent, 800, 500, "Cadastrar Produto", "#5a5a5a")

        self.estoque = estoque
        self.read_produto = read_produto #salva o read pra atualizar depois

        tk.Label(self, text="Cadastre o produto", bg="#5a5a5a", fg="white",
                 font=("Arial", 20, "bold")).place(relx=0.5, y=40, anchor="center")

        campos = {
            "Nome do produto*": PlaceholderEntry(self, placeholder="Nome do produto", width=30),
            "Quantidade*": PlaceholderEntry(self, placeholder="Quantidade", width=30),
            "Período de validade*": PlaceholderEntry(self, placeholder="dd/mm/aaaa", width=30),
            "Data de adição*": PlaceholderEntry(self, placeholder="dd/mm/aaaa", width=30),
            "Fornecedor*": PlaceholderEntry(self, placeholder="Fornecedor", width=30),
        }

        for i, (label, entry) in enumerate(campos.items()):
            tk.Label(self, text=label, bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=80, y=120 + i * 50)
            entry.place(x=300, y=120 + i * 50)

        mensagem_sucesso = tk.Label(self, text="", bg="#5a5a5a", fg="lime", font=("Arial", 12, "bold"))
        mensagem_sucesso.place(x=80, y=400)

        def cadastrar():

            self.estoque.produtos = self.estoque.carregar_produtos()

            nome = campos["Nome do produto*"].get().strip()
            qtd = campos["Quantidade*"].get().strip()
            validade = campos["Período de validade*"].get().strip()
            adicao = campos["Data de adição*"].get().strip()
            fornecedor = campos["Fornecedor*"].get().strip()

            if not all([nome, qtd, validade, adicao, fornecedor]):
                mensagem_sucesso.config(text="Preencha todos os campos!", fg="red")
                return
            
            if not (validade.isdigit() and len(validade) == 8 and adicao.isdigit() and len(adicao) == 8):
                mensagem_sucesso.config(text="As datas devem ter 8 dígitos (ddmmaaaa)!", fg="red")
                return
            
            if self.estoque.produtos:
                codigo = str(max(map(int, self.estoque.produtos.keys())) + 1)
            else:
                codigo = "1000001"

            self.estoque.produtos[codigo] = {
                "nome": nome,
                "quantidade": qtd,
                "validade": validade,
                "adicao": adicao,
                "fornecedor": fornecedor,
                "imagem": "sem_imagem.png"
            }
            self.estoque.salvar_produtos()

            for entry in campos.values():
                entry.delete(0, tk.END)
                entry.put_placeholder()

            mensagem_sucesso.config(text="Produto cadastrado com sucesso!", fg="lime")

            self.read_produto.atualizar_resultados()

            
        tk.Button(self, text="Cadastrar", bg="limegreen", fg="white",
                  font=("Arial", 14, "bold"), cursor='hand2',
                  command=cadastrar).place(x=500, y=430)

        BotaoVoltar(self, text="Voltar", bg='#1A73E8', fg='white',
                    font=("Arial", 14, "bold")).place(x=660, y=430)
        

'========================================================================================================================================================================='


class ReadProduto:
    def __init__(self, parent, estoque):
        self.parent = parent
        self.estoque = estoque

        # Label "Consulte o produto"
        self.label_consulte = tk.Label(
            master=parent,
            text='Consulte o produto',
            bg='#202124',
            fg='white',
            font=('Arial', 20, 'bold')
        )
        self.label_consulte.place(x=15, y=220)

        # Campo de busca
        self.entry_buscar_produtos = PlaceholderEntry(
            master=parent, placeholder='Digite a informação para busca', width=50, font=("Arial", 10))
        self.entry_buscar_produtos.place(x=15, y=260)

        # Frame onde os resultados serão exibidos
        self.frame_resultados = tk.Frame(parent, bg="#5a5a5a", width=800, height=300)
        self.frame_resultados.place(x=1110, y=320)  # Corrigido para exibir no layout corretamente

        # Cabeçalho da tabela
        tk.Label(self.frame_resultados, text="Código de barras", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=50, y=10)
        tk.Label(self.frame_resultados, text="Nome do produto", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=200, y=10)
        tk.Label(self.frame_resultados, text="Data de adição", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=400, y=10)

        # Botão buscar
        self.button_buscar = tk.Button(
            master=parent,
            text='Buscar',
            bg='#3bf502',
            fg='black',
            font=('Arial', 20),
            cursor='hand2',
            command=self.atualizar_resultados
        )
        self.button_buscar.place(x=400, y=240)

        # Atualiza também com ENTER
        self.entry_buscar_produtos.bind("<Return>", self.atualizar_resultados)

        # Exibe os produtos ao abrir
        self.atualizar_resultados()

    def atualizar_resultados(self, event=None):
        termo = self.entry_buscar_produtos.get().strip().lower()

        # Limpa resultados antigos
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        # Recria cabeçalho
        tk.Label(self.frame_resultados, text="Código de barras", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=50, y=10)
        tk.Label(self.frame_resultados, text="Nome do produto", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=200, y=10)
        tk.Label(self.frame_resultados, text="Data de adição", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=400, y=10)

        # Busca os produtos por nome, adicao ou código
        resultados = []
        for codigo, produto in self.estoque.produtos.items():
            nome = produto.get("nome", "").lower()
            adicao = produto.get("adicao", "")
    
            if (termo in nome) or (termo in codigo) or (termo in adicao):
                resultados.append((codigo, produto))

        # Exibe resultados
        if resultados:
            for i, (codigo, produto) in enumerate(resultados):
                tk.Label(self.frame_resultados, text=codigo, bg="#5a5a5a",
                         fg="white", font=("Arial", 11)).place(x=50, y=50 + i * 50)
                tk.Label(self.frame_resultados, text=produto["nome"], bg="#5a5a5a",
                         fg="white", font=("Arial", 11)).place(x=200, y=50 + i * 50)
                tk.Label(self.frame_resultados, text=produto["adicao"], bg="#5a5a5a",
                         fg="white", font=("Arial", 11)).place(x=400, y=50 + i * 50)

                # Botão de "DETALHES"
                tk.Button(self.frame_resultados, text="DETALHES", bg='#1A73E8', fg='white',
                          cursor='hand2', command=lambda c=codigo: self.mostrar_detalhes(c)).place(x=700, y=48 + i * 50)
        else:
            tk.Label(self.frame_resultados, text="Nenhum produto encontrado.",
                     bg="#5a5a5a", fg="red", font=("Arial", 12, "bold")
                     ).place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_detalhes(self, codigo):
        produto = self.estoque.produtos[codigo]
        detalhes = CriarJanela(self.parent, 600, 400, f"Detalhes do Produto - {produto['nome']}", "#555")

        tk.Label(detalhes, text="DETALHES DO PRODUTO", font=("Arial", 14, "bold"),
                 bg="#555", fg="white").place(x=180, y=30)

        for i, (chave, valor) in enumerate(produto.items()):
            if chave != "imagem":
                tk.Label(detalhes, text=f"{chave.capitalize()}*:", bg="#555", fg="white",
                         font=("Arial", 12, "bold")).place(x=50, y=100 + i * 40)
                tk.Label(detalhes, text=valor, bg="#555", fg="white",
                         font=("Arial", 12)).place(x=200, y=100 + i * 40)

        BotaoVoltar(detalhes, text="VOLTAR", bg='#1A73E8', fg='white').place(x=530, y=360)

        # Exibe imagem do produto (se existir)
        if "imagem" in produto:
            try:
                img = tk.PhotoImage(file=produto["imagem"])
                label_img = tk.Label(detalhes, image=img, bg="#555")
                label_img.image = img
                label_img.place(x=350, y=100)
            except Exception:
                pass
=======
#CRIAR O PRODUTO
import tkinter as tk
from classes_estoque import CriarJanela, PlaceholderEntry, BotaoVoltar, ListaProdutos

class CreateProduto(CriarJanela):
    def __init__(self, parent, estoque, read_produto):
        super().__init__(parent, 800, 500, "Cadastrar Produto", "#5a5a5a")

        self.estoque = estoque
        self.read_produto = read_produto #salva o read pra atualizar depois

        tk.Label(self, text="Cadastre o produto", bg="#5a5a5a", fg="white",
                 font=("Arial", 20, "bold")).place(relx=0.5, y=40, anchor="center")

        campos = {
            "Nome do produto*": PlaceholderEntry(self, placeholder="Nome do produto", width=30),
            "Quantidade*": PlaceholderEntry(self, placeholder="Quantidade", width=30),
            "Período de validade*": PlaceholderEntry(self, placeholder="dd/mm/aaaa", width=30),
            "Data de adição*": PlaceholderEntry(self, placeholder="dd/mm/aaaa", width=30),
            "Fornecedor*": PlaceholderEntry(self, placeholder="Fornecedor", width=30),
        }

        for i, (label, entry) in enumerate(campos.items()):
            tk.Label(self, text=label, bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=80, y=120 + i * 50)
            entry.place(x=300, y=120 + i * 50)

        mensagem_sucesso = tk.Label(self, text="", bg="#5a5a5a", fg="lime", font=("Arial", 12, "bold"))
        mensagem_sucesso.place(x=80, y=400)

        def cadastrar():

            self.estoque.produtos = self.estoque.carregar_produtos()

            nome = campos["Nome do produto*"].get().strip()
            qtd = campos["Quantidade*"].get().strip()
            validade = campos["Período de validade*"].get().strip()
            adicao = campos["Data de adição*"].get().strip()
            fornecedor = campos["Fornecedor*"].get().strip()

            if not all([nome, qtd, validade, adicao, fornecedor]):
                mensagem_sucesso.config(text="Preencha todos os campos!", fg="red")
                return
            
            if not (validade.isdigit() and len(validade) == 8 and adicao.isdigit() and len(adicao) == 8):
                mensagem_sucesso.config(text="As datas devem ter 8 dígitos (ddmmaaaa)!", fg="red")
                return
            
            if self.estoque.produtos:
                codigo = str(max(map(int, self.estoque.produtos.keys())) + 1)
            else:
                codigo = "1000001"

            self.estoque.produtos[codigo] = {
                "nome": nome,
                "quantidade": qtd,
                "validade": validade,
                "adicao": adicao,
                "fornecedor": fornecedor,
                "imagem": "sem_imagem.png"
            }
            self.estoque.salvar_produtos()

            for entry in campos.values():
                entry.delete(0, tk.END)
                entry.put_placeholder()

            mensagem_sucesso.config(text="Produto cadastrado com sucesso!", fg="lime")

            self.read_produto.atualizar_resultados()

            
        tk.Button(self, text="Cadastrar", bg="limegreen", fg="white",
                  font=("Arial", 14, "bold"), cursor='hand2',
                  command=cadastrar).place(x=500, y=430)

        BotaoVoltar(self, text="Voltar", bg='#1A73E8', fg='white',
                    font=("Arial", 14, "bold")).place(x=660, y=430)
        

'========================================================================================================================================================================='


class ReadProduto:
    def __init__(self, parent, estoque):
        self.parent = parent
        self.estoque = estoque

        # Label "Consulte o produto"
        self.label_consulte = tk.Label(
            master=parent,
            text='Consulte o produto',
            bg='#202124',
            fg='white',
            font=('Arial', 20, 'bold')
        )
        self.label_consulte.place(x=15, y=220)

        # Campo de busca
        self.entry_buscar_produtos = PlaceholderEntry(
            master=parent, placeholder='Digite a informação para busca', width=50, font=("Arial", 10))
        self.entry_buscar_produtos.place(x=15, y=260)

        # Frame onde os resultados serão exibidos
        self.frame_resultados = tk.Frame(parent, bg="#5a5a5a", width=800, height=300)
        self.frame_resultados.place(x=1110, y=320)  # Corrigido para exibir no layout corretamente

        # Cabeçalho da tabela
        tk.Label(self.frame_resultados, text="Código de barras", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=50, y=10)
        tk.Label(self.frame_resultados, text="Nome do produto", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=200, y=10)
        tk.Label(self.frame_resultados, text="Data de adição", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=400, y=10)

        # Botão buscar
        self.button_buscar = tk.Button(
            master=parent,
            text='Buscar',
            bg='#3bf502',
            fg='black',
            font=('Arial', 20),
            cursor='hand2',
            command=self.atualizar_resultados
        )
        self.button_buscar.place(x=400, y=240)

        # Atualiza também com ENTER
        self.entry_buscar_produtos.bind("<Return>", self.atualizar_resultados)

        # Exibe os produtos ao abrir
        self.atualizar_resultados()

    def atualizar_resultados(self, event=None):
        termo = self.entry_buscar_produtos.get().strip().lower()

        # Limpa resultados antigos
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        # Recria cabeçalho
        tk.Label(self.frame_resultados, text="Código de barras", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=50, y=10)
        tk.Label(self.frame_resultados, text="Nome do produto", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=200, y=10)
        tk.Label(self.frame_resultados, text="Data de adição", bg="#5a5a5a",
                 fg="white", font=("Arial", 11, "bold")).place(x=400, y=10)

        # Busca os produtos por nome, adicao ou código
        resultados = []
        for codigo, produto in self.estoque.produtos.items():
            nome = produto.get("nome", "").lower()
            adicao = produto.get("adicao", "")
    
            if (termo in nome) or (termo in codigo) or (termo in adicao):
                resultados.append((codigo, produto))

        # Exibe resultados
        if resultados:
            for i, (codigo, produto) in enumerate(resultados):
                tk.Label(self.frame_resultados, text=codigo, bg="#5a5a5a",
                         fg="white", font=("Arial", 11)).place(x=50, y=50 + i * 50)
                tk.Label(self.frame_resultados, text=produto["nome"], bg="#5a5a5a",
                         fg="white", font=("Arial", 11)).place(x=200, y=50 + i * 50)
                tk.Label(self.frame_resultados, text=produto["adicao"], bg="#5a5a5a",
                         fg="white", font=("Arial", 11)).place(x=400, y=50 + i * 50)

                # Botão de "DETALHES"
                tk.Button(self.frame_resultados, text="DETALHES", bg='#1A73E8', fg='white',
                          cursor='hand2', command=lambda c=codigo: self.mostrar_detalhes(c)).place(x=700, y=48 + i * 50)
        else:
            tk.Label(self.frame_resultados, text="Nenhum produto encontrado.",
                     bg="#5a5a5a", fg="red", font=("Arial", 12, "bold")
                     ).place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_detalhes(self, codigo):
        produto = self.estoque.produtos[codigo]
        detalhes = CriarJanela(self.parent, 600, 400, f"Detalhes do Produto - {produto['nome']}", "#555")

        tk.Label(detalhes, text="DETALHES DO PRODUTO", font=("Arial", 14, "bold"),
                 bg="#555", fg="white").place(x=180, y=30)

        for i, (chave, valor) in enumerate(produto.items()):
            if chave != "imagem":
                tk.Label(detalhes, text=f"{chave.capitalize()}*:", bg="#555", fg="white",
                         font=("Arial", 12, "bold")).place(x=50, y=100 + i * 40)
                tk.Label(detalhes, text=valor, bg="#555", fg="white",
                         font=("Arial", 12)).place(x=200, y=100 + i * 40)

        BotaoVoltar(detalhes, text="VOLTAR", bg='#1A73E8', fg='white').place(x=530, y=360)

        # Exibe imagem do produto (se existir)
        if "imagem" in produto:
            try:
                img = tk.PhotoImage(file=produto["imagem"])
                label_img = tk.Label(detalhes, image=img, bg="#555")
                label_img.image = img
                label_img.place(x=350, y=100)
            except Exception:
                pass

#==============================================================================================================================================================================================================================

class RemoverProdutoWindow(CriarJanela):

    def __init__(self, parent, estoque, read_produto=None):
        super().__init__(parent, 900, 600, "Excluir Produto", "#5a5a5a")
        self.estoque = estoque
        self.read_produto = read_produto

        tk.Label(self, text="Exclua o produto", bg="#5a5a5a", fg="white", font=("Arial", 20, "bold")).pack(pady=18)

        frame_box = tk.Frame(self, bg="#4d4d4d", padx=20, pady=20)
        frame_box.pack(pady=10)

        tk.Label(frame_box, text="", bg="#4d4d4d", width=3).grid(row=0, column=0)
        tk.Label(frame_box, text="Código de barras", bg="#4d4d4d", fg="white", font=("Arial", 12, "bold"), width=18).grid(row=0, column=1)
        tk.Label(frame_box, text="Nome do produto", bg="#4d4d4d", fg="white", font=("Arial", 12, "bold"), width=25).grid(row=0, column=2)
        tk.Label(frame_box, text="Data de adição", bg="#4d4d4d", fg="white", font=("Arial", 12, "bold"), width=18).grid(row=0, column=3)

        self.selecionado = tk.StringVar(value="")

        self.estoque.produtos = self.estoque.carregar_produtos()

        self.lista = ListaProdutos(frame_box, self.estoque.produtos, self.selecionado)
        self.lista.exibir_radiobuttonsElabels()

        self.mensagem_excluir = tk.Label(self, text="Produto excluído com sucesso!", bg="#5a5a5a", fg="#5a5a5a", font=("Arial", 12, "bold"))
        self.mensagem_excluir.pack(pady=(20, 0), anchor="w", padx=20)

        bot_excluir = tk.Button(self, text="EXCLUIR", bg="#ff5733", fg="white", font=("Arial", 14, "bold"), cursor="hand2", command=self.confirmar_exclusao)
        bot_excluir.place(relx=0.75, rely=0.9, anchor='center')

        BotaoVoltar(self, text="VOLTAR", bg='#1A73E8', fg='white', font=("Arial", 12)).place(relx=0.9, rely=0.9, anchor='center')

    def confirmar_exclusao(self):
        codigo_sel = self.selecionado.get()
        if not codigo_sel:
            self.mensagem_excluir.config(text="Selecione um produto para excluir.", fg="red")
            return

        if codigo_sel in self.estoque.produtos:
            # remove do dicionário em memória
            del self.estoque.produtos[codigo_sel]
            # salva no JSON
            self.estoque.salvar_produtos()
            self.mensagem_excluir.config(text="Produto excluído com sucesso!", fg="lime")
            self.selecionado.set("")
            
            for w in self.winfo_children():
                w.destroy()
            self.__init__(self.parent, self.estoque, self.read_produto)

            if self.read_produto:
                try:
                    self.read_produto.atualizar_resultados()
                except Exception:
                    pass
        else:
            self.mensagem_excluir.config(text="Produto não encontrado.", fg="red")

#=================================================================================================================================================================================================

class EditarProdutoWindow(CriarJanela):

    def __init__(self, parent, estoque, read_produto=None):
        super().__init__(parent, 800, 500, "Editar Produto", "#5a5a5a")
        self.estoque = estoque
        self.read_produto = read_produto

        tk.Label(self, text="Edite o produto", bg="#5a5a5a", fg="white", font=("Arial", 20, "bold")).place(relx=0.5, y=40, anchor="center")
        tk.Label(self, text="Código de barras", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=60, y=100)
        tk.Label(self, text="Nome do produto", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=250, y=100)
        tk.Label(self, text="Data de adição", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=440, y=100)

        self.estoque.produtos = self.estoque.carregar_produtos()

        for i, (codigo, produto) in enumerate(self.estoque.produtos.items()):
            tk.Label(self, text=codigo, bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=60, y=140 + i * 50)
            tk.Label(self, text=produto.get("nome", ""), bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=250, y=140 + i * 50)
            tk.Label(self, text=produto.get("adicao", ""), bg="#5a5a5a", fg="white", font=("Arial", 11)).place(x=440, y=140 + i * 50)

            tk.Button(self, text="Editar", bg="#f7b731", fg="black", font=("Arial", 10, "bold"), cursor="hand2", command=lambda c=codigo: self.abrir_formulario_edicao(c)).place(x=640, y=135 + i * 50)

        BotaoVoltar(self, text="VOLTAR", bg='#1A73E8', fg='white', font=("Arial", 14, "bold")).place(x=660, y=430)

    def abrir_formulario_edicao(self, codigo):
        produto = self.estoque.produtos.get(codigo)
        if produto is None:
            return

        janela_formulario = CriarJanela(self, 800, 500, "Editar Produto", "#5a5a5a")
        tk.Label(janela_formulario, text="Edite seu produto", bg="#5a5a5a", fg="white", font=("Arial", 20, "bold")).place(relx=0.5, y=40, anchor="center")

        campos = {
            "Nome do produto": PlaceholderEntry(janela_formulario, placeholder="Nome do produto", width=30, color='black'),
            "Quantidade": PlaceholderEntry(janela_formulario, placeholder="Quantidade", width=30, color='black'),
            "Período de validade": PlaceholderEntry(janela_formulario, placeholder="dd/mm/aaaa", width=30, color='black'),
            "Data de adição": PlaceholderEntry(janela_formulario, placeholder="dd/mm/aaaa", width=30, color='black'),
            "Fornecedor": PlaceholderEntry(janela_formulario, placeholder="Fornecedor", width=30, color='black'),
        }

        dados = {
            "Nome do produto": produto.get("nome", ""),
            "Quantidade": produto.get("quantidade", ""),
            "Período de validade": produto.get("validade", ""),
            "Data de adição": produto.get("adicao", ""),
            "Fornecedor": produto.get("fornecedor", "")
        }

        for chave, valor in dados.items():
            campos[chave].delete(0, tk.END)
            campos[chave].insert(0, valor)

        for i, (label, entry) in enumerate(campos.items()):
            tk.Label(janela_formulario, text=label + ":", bg="#5a5a5a", fg="white", font=("Arial", 12, "bold")).place(x=80, y=120 + i * 50)
            entry.place(x=300, y=120 + i * 50)

        if produto.get("imagem"):
            try:
                img = tk.PhotoImage(file=produto["imagem"])
                label_img = tk.Label(janela_formulario, image=img, bg="#5a5a5a")
                label_img.image = img
                label_img.place(x=550, y=120)
            except Exception:
                pass

        mensagem = tk.Label(janela_formulario, text="Produto editado com sucesso!", bg="#5a5a5a", fg="#5a5a5a", font=("Arial", 12, "bold"))
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

            # atualiza o dicionário do produto
            produto.update({
                "nome": nome,
                "quantidade": qtd,
                "validade": validade,
                "adicao": adicao,
                "fornecedor": fornecedor
            })

            # salva no JSON
            self.estoque.salvar_produtos()

            mensagem.config(text="Produto editado com sucesso!", fg="lime")

            janela_formulario.destroy()
            self.destroy()

            EditarProdutoWindow(self.parent, self.estoque, self.read_produto)

            if self.read_produto:
                try:
                    self.read_produto.atualizar_resultados()
                except Exception:
                    pass

        tk.Button(janela_formulario, text="Confirmar", bg="limegreen", fg="white", font=("Arial", 14, "bold"), cursor='hand2', command=confirmar_edicao).place(x=500, y=430)
        BotaoVoltar(janela_formulario, text="VOLTAR", bg='#1A73E8', fg='white', font=("Arial", 14, "bold")).place(x=660, y=430)
>>>>>>> Stashed changes
