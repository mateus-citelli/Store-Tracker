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