import tkinter as tk

import crud as crud


class PrincipalBD:
    def __init__(self, win):
        self.objBD = crud.AppBD()

        self.lbCodigo = tk.Label(win, text="Código do Produto:")
        self.lbNome = tk.Label(win, text="Nome do Produto:")
        self.lbPreco = tk.Label(win, text="Preço do Produto:")
        self.lbPrecoReajuste = tk.Label(
            win, text="Preço acrescido em 10%:")
        self.lbMensagemOperacao = tk.Label(win, text="")

        self.txtCodigo = tk.Entry(bd=3)
        self.txtNome = tk.Entry()
        self.txtPreco = tk.Entry()
        self.txtPrecoReajusteValor = tk.Entry(state='readonly')

        self.btnCadastrar = tk.Button(
            win, text="Cadastrar", command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(
            win, text="Atualizar", command=self.fAtualizarProduto)
        self.btnExcluir = tk.Button(
            win, text="Excluir", command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(
            win, text="Limpar", command=self.fLimparTela)
        self.btnBuscar = tk.Button(
            win, text="Buscar", command=self.fBuscarProduto)

        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)

        self.lbNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)

        self.lbPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)

        self.lbPrecoReajuste.place(x=100, y=200)
        self.txtPrecoReajusteValor.place(x=250, y=200)

        self.btnCadastrar.place(x=100, y=250)
        self.btnAtualizar.place(x=200, y=250)
        self.btnExcluir.place(x=300, y=250)
        self.btnLimpar.place(x=400, y=250)
        self.btnBuscar.place(x=500, y=250)

        self.lbMensagemOperacao.place(x=70, y=300)

    def alterarMensagemOperacao(self, msgOperacao):
        self.lbMensagemOperacao.configure(text=msgOperacao)

    def fBuscarProduto(self):
        try:
            codigo, nome, preco = self.fLerCampos()
            record = self.objBD.buscarProduto(codigo)
            codigo = record[0]
            nome = record[1]
            preco = record[2]
            preco_reajuste = record[3]
            self.fLimparTela()
            self.alterarMensagemOperacao(
                f"Produto encontrado na base: {record}")
            self.txtCodigo.insert(0, codigo)
            self.txtNome.insert(0, nome)
            self.txtPreco.insert(
                0, preco[3:].replace('.', '').replace(',', '.'))
            self.txtPrecoReajusteValor.config(state='normal')
            self.txtPrecoReajusteValor.insert(
                0, preco_reajuste[3:].replace('.', '').replace(',', '.'))
            self.txtPrecoReajusteValor.config(state='readonly')
        except Exception as error:
            self.alterarMensagemOperacao(f"Falha ao buscar produto: {error}")

    def fCadastrarProduto(self):
        try:
            codigo, nome, preco = self.fLerCampos()
            record = self.objBD.inserirDados(codigo, nome, preco)
            preco_reajuste = record[3]
            # self.fLimparTela()
            self.alterarMensagemOperacao(
                f"Cadastro realizado com sucesso! {record}")
            self.txtPrecoReajusteValor.config(state='normal')
            self.txtPrecoReajusteValor.delete(0, tk.END)
            self.txtPrecoReajusteValor.insert(
                0, preco_reajuste[3:].replace(',', '.'))
            self.txtPrecoReajusteValor.config(state='readonly')
        except Exception as error:
            self.alterarMensagemOperacao(f"Falha ao cadastrar: {error}")

    def fAtualizarProduto(self):
        try:
            codigo, nome, preco = self.fLerCampos()
            record = self.objBD.atualizarDados(codigo, nome, preco)
            preco_reajuste = record[3]
            # self.fLimparTela()
            self.alterarMensagemOperacao(
                f"Produto atualizado com sucesso! {record}")
            self.txtPrecoReajusteValor.config(state='normal')
            self.txtPrecoReajusteValor.delete(0, tk.END)
            self.txtPrecoReajusteValor.insert(
                0, preco_reajuste[3:].replace('.', '').replace(',', '.'))
            self.txtPrecoReajusteValor.config(state='readonly')
        except Exception as error:
            self.alterarMensagemOperacao(f"Falha ao atualizar: {error}")
            print("Não foi possível fazer a atualização.")

    def fExcluirProduto(self):
        try:
            codigo, nome, preco = self.fLerCampos()
            self.objBD.excluirDados(codigo)
            self.fLimparTela()
            self.alterarMensagemOperacao("Produto excluído com sucesso!")
            print("Produto Excluído com Sucesso!")
        except Exception as error:
            self.alterarMensagemOperacao(f"Falha ao excluir: {error}")
            print("Não foi possível fazer a exclusão do produto.")

    def fLimparTela(self):
        try:
            self.txtCodigo.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtPreco.delete(0, tk.END)
            self.txtPrecoReajusteValor.config(state='normal')
            self.txtPrecoReajusteValor.delete(0, tk.END)
            self.txtPrecoReajusteValor.config(state='readonly')
            self.lbMensagemOperacao["text"] = ""
        except Exception as error:
            self.alterarMensagemOperacao(f"Falha ao limpar: {error}")
            print("Não foi possível limpar os campos.")

    def fLerCampos(self):
        try:
            codigo = int(self.txtCodigo.get())
            nome = (self.txtNome.get()).strip().capitalize()
            preco = None
            if (self.txtPreco.get() != ""):
                preco = float(self.txtPreco.get())
        except Exception as error:
            self.alterarMensagemOperacao(
                f"Não foi possível ler os dados: {error}")
        return codigo, nome, preco


janela = tk.Tk()
principal = PrincipalBD(janela)
janela.title("Bem vindo a Tela de Cadastro - Gomes Mercados")
janela.geometry("600x500")
janela.mainloop()
