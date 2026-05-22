from conexao import conectar

def criar_produto():

    nome = input("Nome do produto: ")
    
    while True:
        try:
            preco = float(input("Preço: "))
            break
        except ValueError:
            print("Digite um valor válido!")
    while True:
        try:
            quantidade = int(input("Quantidade: "))
            break
        except ValueError:
            print("Digite uma quantia válida!")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_produtos (nome_produto, preco_produto, quantidade_produto)
    VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (nome, preco, quantidade))
    conexao.commit()

    cursor.close()
    conexao.close()
    print("")
    print("✔ Produto criado com sucesso!")


def listar_produtos():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tbl_produtos")
    produtos = cursor.fetchall()

    print("\n        ======= PRODUTOS =======")
    print("")
    for p in produtos:
        print(f"ID: {p[0]} | {p[1]} | R$ {p[2]} | Estoque: {p[3]}")

    cursor.close()
    conexao.close()


def atualizar_produto():

    id_produto = input("ID do produto: ")

    nome = input("Novo nome: ")
    
    while True:
        try:
            preco = float(input("Novo preço: "))
            break
        except ValueError:
            print("Digite um preço válido!")

    while True:
        try:
            quantidade = int(input("Nova quantidade: "))
            break
        except ValueError:
            print("Digite uma quantidade válida!")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_produtos
    SET nome_produto=%s, preco_produto=%s, quantidade_produto=%s
    WHERE id_produto=%s
    """

    cursor.execute(sql, (nome, preco, quantidade, id_produto))
    conexao.commit()

    cursor.close()
    conexao.close()
    print("")
    print("✔ Produto atualizado!")


def deletar_produto():

    id_produto = input("ID do produto para deletar: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM tbl_produtos WHERE id_produto=%s"

    cursor.execute(sql, (id_produto,))
    conexao.commit()

    cursor.close()
    conexao.close()
    print("")
    print("✔ Produto removido!")

def relatorio_vendas():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*), SUM(total_venda) FROM tbl_vendas")
    resultado = cursor.fetchone()

    total_vendas = resultado[0] or 0
    valor_total = resultado[1] or 0

    print("\n====== RELATÓRIO DE VENDAS ======")
    print("")
    print(f"Total de compras: {total_vendas}")
    print(f"Valor total arrecadado: R$ {valor_total:.2f}")

    cursor.close()
    conexao.close()


def menu_admin(usuario):

    while True:

        print("\n========================")
        print("      PAINEL ADMIN")
        print("========================")
        print("")
        print("1 - Criar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Deletar produto")
        print("5 - Relatório de vendas")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            criar_produto()

        elif opcao == "2":
            listar_produtos()

        elif opcao == "3":
            atualizar_produto()

        elif opcao == "4":
            deletar_produto()

        elif opcao == "5":
            relatorio_vendas()

        elif opcao == "0":
            print("Saindo do admin...")
            break

        else:
            print("Opção inválida!")