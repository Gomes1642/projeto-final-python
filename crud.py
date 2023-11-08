import psycopg2

global POSTGRES_CREATE_TABLE_QUERY, POSTGRES_INSERT_QUERY, POSTGRES_UPDATE_QUERY, POSTGRES_SELECT_QUERY, POSTGRES_DELETE_QUERY
POSTGRES_CREATE_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS public.produto (codigo integer NOT NULL, nome text NOT NULL, preco money NOT NULL, preco_reajuste money NOT NULL)"""
POSTGRES_INSERT_QUERY = """INSERT INTO public.produto (codigo, nome, preco, preco_reajuste) VALUES (%s, %s, %s, %s)"""
POSTGRES_UPDATE_QUERY = """UPDATE public.produto SET nome = %s, preco = %s, preco_reajuste = %s WHERE codigo = %s"""
POSTGRES_SELECT_QUERY = """SELECT * FROM public.produto WHERE codigo = %s"""
POSTGRES_DELETE_QUERY = """DELETE FROM public.produto WHERE codigo = %s"""


class AppBD:
    def __init__(self):
        self.criarTabela()

    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(
                database="postgres", user="postgres", password="postgree", host="127.0.0.1", port="5432")
        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                print(f"Falha ao se conectar ao Banco de Dados: {error}")

    def criarTabela(self):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            cursor.execute(POSTGRES_CREATE_TABLE_QUERY)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                print("Falha ao criar tabela no Banco de Dados: ", error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

    def buscarProduto(self, codigo):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            cursor.execute(POSTGRES_SELECT_QUERY, (codigo,))
            resultado_select = cursor.fetchone()
            if resultado_select is None:
                raise ValueError(
                    f"Produto com o código {codigo} não encontrado."
                )
            return resultado_select
        except ValueError:
            raise
        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                raise error
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

    def inserirDados(self, codigo, nome, preco):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            preco_reajustado = (preco * 0.1) + preco
            record_to_insert = (codigo, nome, preco, preco_reajustado)
            cursor.execute(POSTGRES_SELECT_QUERY, (codigo,))
            if cursor.fetchone():
                raise ValueError("Código já existe!")
            cursor.execute(POSTGRES_INSERT_QUERY, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro inserido com successo na tabela PRODUTO")
            cursor.execute(POSTGRES_SELECT_QUERY, (codigo,))
            return cursor.fetchone()
        except ValueError:
            raise
        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                raise error
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

    def atualizarDados(self, codigo, nome, preco):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            if (nome == '' and preco is None):
                raise ValueError("Informe algum dado para atualizar!")
            cursor.execute(POSTGRES_SELECT_QUERY, (codigo,))
            record = cursor.fetchone()
            nome_atual = record[1]
            preco_atual = record[2]
            if (nome == ''):
                nome = nome_atual
            if (preco is None):
                preco = float(preco_atual[3:].replace(
                    '.', '').replace(',', '.'))
            preco_reajuste = (preco * 0.1) + preco
            record_to_update = (nome, preco, preco_reajuste, codigo)
            cursor.execute(POSTGRES_UPDATE_QUERY, record_to_update)
            self.connection.commit()
            count = cursor.rowcount
            print(f"{count} registro(s) atualizado(s) com sucesso!")
            print("Registro Depois da Atualização ")
            cursor.execute(POSTGRES_SELECT_QUERY, (codigo,))
            record = cursor.fetchone()
            return (record)
        except ValueError:
            raise
        except (Exception, psycopg2.Error) as error:
            print("Erro na Atualização", error)
            raise
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

    def excluirDados(self, codigo):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            cursor.execute(POSTGRES_DELETE_QUERY, (codigo,))
            self.connection.commit()
            count = cursor.rowcount
            print(f"{count} registro(s) excluído(s) com sucesso!")
        except (Exception, psycopg2.Error) as error:
            print("Erro na exclusão", error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
