import psycopg2

dados = [
    {"codigo": 1, "nome": "Feijão", "preco": 10},
    {"codigo": 2, "nome": "Arroz", "preco": 20},
    {"codigo": 3, "nome": "Macarrão", "preco": 15},
    {"codigo": 4, "nome": "Tilápia", "preco": 17.5},
    {"codigo": 5, "nome": "Peixe Espada", "preco": 11.24},
    {"codigo": 6, "nome": "Camarão", "preco": 10},
    {"codigo": 7, "nome": "Coca Cola", "preco": 7},
    {"codigo": 8, "nome": "Pipoca", "preco": 2},
    {"codigo": 9, "nome": "Milho", "preco": 9},
    {"codigo": 10, "nome": "Ervilha", "preco": 40},
    {"codigo": 11, "nome": "Bolo de Chocolate", "preco": 70},
    {"codigo": 12, "nome": "Bolo de Morango", "preco": 23.67},
    {"codigo": 13, "nome": "Biscoito de Povilho", "preco": 10.48},
    {"codigo": 14, "nome": "Lasanha", "preco": 10},
    {"codigo": 15, "nome": "Salsicha", "preco": 11},
    {"codigo": 16, "nome": "Linguiça", "preco": 15},
    {"codigo": 17, "nome": "Picanha", "preco": 18},
    {"codigo": 18, "nome": "Queijo", "preco": 39},
    {"codigo": 19, "nome": "Presunto", "preco": 80},
    {"codigo": 20, "nome": "Requeijão", "preco": 90}
]

connection = psycopg2.connect(
    database="postgres", user="postgres", password="postgree", host="127.0.0.1", port="5432")
cursor = connection.cursor()

for produto_atual in dados:
    cursor.execute(
        """INSERT INTO produto (codigo, nome, preco, preco_reajuste) VALUES (%s, %s, %s, %s);""", (produto_atual["codigo"], produto_atual['nome'], produto_atual['preco'], (float(produto_atual['preco']) * 0.1) + float(produto_atual['preco'])))
    connection.commit()
