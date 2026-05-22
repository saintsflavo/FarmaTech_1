import mysql.connector

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='FarmaTech'
        )

        return conexao

    except mysql.connector.Error as erro:
        print(f'Erro ao conectar ao banco: {erro}')
        return None

if conectar():
    print('Conectado com suceso! ')