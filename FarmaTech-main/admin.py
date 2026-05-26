from conexao import conectar

def criar_produto():

    nome = input("Nome do produto: ")
    
    while True:
        try:
            preco = float(input("Preço: "))
            if preco <= 0:
                print("Preço inválido!")
            else:
                break
        except ValueError:
            print("Digite um valor válido!")
    while True:
        try:
            quantidade = int(input("Quantidade: "))
            if quantidade <= 0:
                print("Quantidade inválida!")
            else:
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
    
    if not produtos:
        print("Nenhum produto encontrado!")
    else:
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

            if quantidade < 0:
                print("Quantidade inválida!")
            else:
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

    id_produto = input("ID do produto para deletar: ").strip()

    if not id_produto.isdigit():
        print("ID inválido!")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        sql = "DELETE FROM tbl_produtos WHERE id_produto = %s"

        cursor.execute(sql, (int(id_produto),))
        conexao.commit()

        if cursor.rowcount == 0:
            print("Produto não encontrado!")
        else:
            print("\n✔ Produto removido!")

    except Exception as erro:
        print(f"Erro ao remover produto: {erro}")

    finally:
        cursor.close()
        conexao.close()

def relatorio_vendas():

    conexao = conectar()
    cursor = conexao.cursor()

    print("\n====== RELATÓRIO DE VENDAS ======\n")

    cursor.execute("""
    SELECT COUNT(*), SUM(total_venda)
    FROM tbl_vendas
    """)

    resultado = cursor.fetchone()

    total_vendas = resultado[0] or 0
    valor_total = resultado[1] or 0

    print(f"🛒 Total de vendas: {total_vendas}")
    print(f"💰 Faturamento total: R$ {valor_total:.2f}")


    cursor.execute("""
    SELECT p.nome_produto, SUM(vp.quantidade_produto) AS total_vendido
    FROM tbl_vendas_produtos vp
    INNER JOIN tbl_produtos p
    ON vp.id_produto = p.id_produto
    GROUP BY p.nome_produto
    ORDER BY total_vendido DESC
    LIMIT 1
    """)

    produto = cursor.fetchone()

    print("\n====== PRODUTO MAIS VENDIDO ======\n")

    if produto:
        print(f"📦 Produto: {produto[0]}")
        print(f"🔥 Quantidade vendida: {produto[1]}")
    else:
        print("Nenhuma venda registrada.")


    cursor.execute("""
    SELECT nome_produto, quantidade_produto
    FROM tbl_produtos
    WHERE quantidade_produto < 5
    """)

    estoque_baixo = cursor.fetchall()

    print("\n====== ESTOQUE BAIXO ======\n")

    if estoque_baixo:

        for produto in estoque_baixo:
            print(f"⚠ {produto[0]} | Estoque: {produto[1]}")

    else:
        print("Nenhum produto com estoque baixo.")


    cursor.execute("""
    SELECT nome_produto
    FROM tbl_produtos
    WHERE quantidade_produto = 0
    """)

    sem_estoque = cursor.fetchall()

    print("\n====== PRODUTOS SEM ESTOQUE ======\n")

    if sem_estoque:

        for produto in sem_estoque:
            print(f"❌ {produto[0]}")

    else:
        print("Nenhum produto sem estoque.")


    cursor.execute("""
    SELECT id_venda, total_venda, forma_pagamento, data_venda
    FROM tbl_vendas
    ORDER BY data_venda DESC
    """)

    vendas = cursor.fetchall()

    print("\n====== HISTÓRICO DE VENDAS ======\n")

    if vendas:

        for venda in vendas:

            print(f"""
    Venda: {venda[0]}
    Total: R$ {venda[1]:.2f}
    Pagamento: {venda[2]}
    Data: {venda[3]}
    -------------------------
    """)

    else:
        print("Nenhuma venda registrada.")   

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
        print("")
        print(f"Bem-vindo(a), {usuario}")

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