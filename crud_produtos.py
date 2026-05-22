from bd import conectar

def cadastrar_produto():

    nome = input("Nome do produto: ")
    descricao = input("Descrição: ")
    
    while True:
        try:
            preco = float(input("Preço: "))
            break
        except ValueError:
            print("Digite um preço válido!")
    while True:
        try:
            estoque = int(input("Estoque: "))
            break
        except ValueError:
            print("Digite uma quantidade válida!")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_produtos
    (nome_produto, descricao_produto, preco_produto, estoque_produto)
    VALUES (%s, %s, %s, %s)
    """

    valores = (nome, descricao, preco, estoque)

    cursor.execute(sql, valores)

    conexao.commit()

    print("Produto cadastrado com sucesso!")

    cursor.close()
    conexao.close()


def listar_produtos():

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT * FROM tbl_produtos"

    cursor.execute(sql)

    resultados = cursor.fetchall()

    if len(resultados) == 0:
        print("\n Nenhum produto encontrado!")
    
    else:
        
        for produto in resultados:
            print(f"""
ID: {produto[0]}
Nome: {produto[1]}
Descrição: {produto[2]}
Preço: R${produto[3]}
Estoque: {produto[4]}
-------------------------
    """)
    
    cursor.close()
    conexao.close()

def atualizar_produto():

    id_produto = int(input("Digite o ID do produto: "))
    novo_nome = input("Novo nome: ")
    nova_descricao = input("Nova descrição: ")
    
    while True:
        try:
            novo_preco = float(input("Novo preço: "))
            break
        except ValueError:
            print("Digite um preço válido!")

    while True:
        try:
            novo_estoque = int(input("Novo estoque: "))
            break
        except ValueError:
            print("Digite uma quantidade válida!")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_produtos
    SET
        nome_produto = %s,
        descricao_produto = %s,
        preco_produto = %s,
        estoque_produto = %s
    WHERE id_produto = %s
    """

    valores = (
        novo_nome,
        nova_descricao,
        novo_preco,
        novo_estoque,
        id_produto
    )

    cursor.execute(sql, valores)

    conexao.commit()

    print("\n Produto atualizado com sucesso!")

    cursor.close()
    conexao.close()

def deletar_produto():

    id_produto = int(input("Digite o ID do produto que deseja deletar: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM tbl_produtos WHERE id_produto = %s"

    valores = (id_produto,)

    cursor.execute(sql, valores)

    conexao.commit()

    if cursor.rowcount > 0:
        print("Produto deletado com sucesso!")
    else:
        print("Produto não encontrado!")

    cursor.close()
    conexao.close()