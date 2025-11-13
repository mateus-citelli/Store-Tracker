import tkinter as tk
import json
import os
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



class ListaProdutos:            
    def __init__(self, frame, produtos, selecionado):
        self.frame = frame
        self.produtos = produtos
        self.selecionado = selecionado  # variável que guarda o código selecionado

        # Aqui já cria os radiobuttons e labels diretamente
    def exibir_radiobuttonsElabels(self):   
        for i, (codigo, produto) in enumerate(self.produtos.items(), start=1):
            rb = tk.Radiobutton(self.frame, variable=self.selecionado, value=codigo, bg="#4d4d4d", activebackground="#4d4d4d", highlightthickness=0)
            rb.grid(row=i, column=0, padx=(5,15))

            tk.Label(self.frame, text=codigo, bg="#4d4d4d", fg="white", font=("Arial", 11)).grid(row=i, column=1)
            tk.Label(self.frame, text=produto["nome"], bg="#4d4d4d", fg="white", font=("Arial", 11)).grid(row=i, column=2)
            tk.Label(self.frame, text=produto["adicao"], bg="#4d4d4d", fg="white", font=("Arial", 11)).grid(row=i, column=3)



class CriarJanela(tk.Toplevel):  #A classe herda tudo da Toplevel, ou seja, a classe filha (CriarJanela) ganha todos os métodos e atributos da classe pai (tk.Toplevel).
    def __init__(self, parent, width, height, title, bg):
        super().__init__(parent) #super() chama o construtor da classe pai (tk.Toplevel) para que a nova janela seja de fato um Toplevel. Passamos parent para que essa janela saiba qual é a janela pai.
        self.parent = parent
        self.parent.withdraw()
        self.geometry(f"{width}x{height}")
        self.title(title)
        self.config(bg=bg)

    def fechar(self):
        """Fecha a janela e devolve a janela pai, se houver"""
        self.destroy()
        self.parent.deiconify()



class BotaoVoltar(tk.Button):
    """Botão genérico de 'Voltar' que fecha a janela atual e reabre a anterior."""
    def __init__(self, master, text="Voltar", **kwargs):
        """
        master: onde o botão será exibido (geralmente a própria janela)
        texto: texto do botão
        kwargs: opções adicionais (bg, fg, font, etc.)
        """
        super().__init__(
            master,
            text=text,
            command=self.voltar,
            cursor="hand2",
            **kwargs
        )

    def voltar(self):
        """Fecha a janela atual (que é o master) e reabre a anterior."""
        janela = self.master  # o master é a própria janela onde o botão foi criado

        if hasattr(janela, "fechar"):
            janela.fechar()
        else:
            janela.destroy()

class Login: #Para encapsular a senha do usuário
    def __init__(self):
        self.__senha = None  # atributo privado

    def set_senha(self, senha):
        """Define a senha (por exemplo, após o usuário digitar)."""
        self.__senha = senha

    def get_senha(self):
        return self.__senha



class Estoque:

    def __init__(self, armazem="produtos.json"):
        self.armazem = armazem
        self.produtos = self.carregar_produtos()

    def carregar_produtos(self):
        """Carrega o arquivo JSON; retorna {} se não existir ou estiver vazio."""
        if os.path.exists(self.armazem):
            try:
                with open(self.armazem, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def salvar_produtos(self):
        """Salva o dicionário 'produtos' no arquivo JSON."""
        with open(self.armazem, "w", encoding="utf-8") as f:
            json.dump(self.produtos, f, indent=4, ensure_ascii=False)

    def adicionar_produto(self, codigo, nome, quantidade, validade, adicao, fornecedor, imagem="sem_imagem.png"):
        """Adiciona um produto ao estoque e salva no JSON."""
        self.produtos[codigo] = {
            "nome": nome,
            "quantidade": quantidade,
            "validade": validade,
            "adicao": adicao,
            "fornecedor": fornecedor,
            "imagem": imagem
        }
        self.salvar_produtos()
        print(f"'{nome}' foi adicionado ao estoque.")

    def remover_produto(self, codigo):
        """Remove um produto pelo código, se existir."""
        if codigo in self.produtos:
            del self.produtos[codigo]
            self.salvar_produtos()
            return True
        return False

    def editar_produto(self, codigo, **kwargs):
        """Edita os dados de um produto existente."""
        if codigo in self.produtos:
            self.produtos[codigo].update(kwargs)
            self.salvar_produtos()
            return True
        return False

    def buscar_produtos(self, termo, campos=None):
        """Retorna lista de tuplas (codigo, produto) filtrando pelo termo nos campos informados."""
        termo = termo.lower()
        campos = campos or ["nome", "quantidade", "validade", "adicao", "fornecedor"]
        resultados = []
        for codigo, produto in self.produtos.items():
            for campo in campos:
                valor = codigo if campo == "codigo" else produto.get(campo, "")
                if termo in str(valor).lower():
                    resultados.append((codigo, produto))
                    break
        return resultados