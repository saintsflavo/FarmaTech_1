from conexao import conectar

carrinho = []

def listar_produtos():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id_produto, nome_produto, preco_produto, quantidade_produto
    FROM tbl_produtos
    WHERE quantidade_produto > 0
    """)

    produtos = cursor.fetchall()

    print("\n     ===== PRODUTOS DISPONÍVEIS =====\n")

    if not produtos:
        print("Nenhum produto encontrado!")

    else:
        for p in produtos:
            print(f"ID: {p[0]} | {p[1]} | R$ {p[2]} | Estoque: {p[3]}")

    cursor.close()
    conexao.close()


def pesquisar_produto():

    nome = input("Digite o nome do produto: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_produto, nome_produto, preco_produto, quantidade_produto
    FROM tbl_produtos
    WHERE nome_produto LIKE %s
    """

    cursor.execute(sql, (f"%{nome}%",))

    produtos = cursor.fetchall()

    print("\n=== RESULTADO DA PESQUISA ===")

    if produtos:
        for p in produtos:
            print(f"ID: {p[0]} | {p[1]} | R$ {p[2]} | Estoque: {p[3]}")
    else:
        print("Nenhum produto encontrado.")

    cursor.close()
    conexao.close()


def adicionar_carrinho():
    listar_produtos()
    print("")
    while True:

        try:
            id_produto = int(input("Digite o ID do produto: "))

            if id_produto <= 0:
                print("Digite um ID válido!")
            else:
                break

        except ValueError:
            print("Digite um ID válido!")

    while True:

        try:
            quantidade = int(input("Quantidade desejada: "))

            if quantidade <= 0:
                print("Insira uma quantidade válida!")
            else:
                break

        except ValueError:
            print("Digite uma quantidade válida!")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id_produto, nome_produto, preco_produto, quantidade_produto
    FROM tbl_produtos
    WHERE id_produto = %s
    """, (id_produto,))

    produto = cursor.fetchone()

    if not produto:

        print("❌ Produto não encontrado.")

        cursor.close()
        conexao.close()
        return

    # verifica quanto já tem no carrinho

    quantidade_no_carrinho = 0

    for item in carrinho:

        if item[0] == id_produto:
            quantidade_no_carrinho += item[3]

    estoque_disponivel = produto[3] - quantidade_no_carrinho

    # verifica estoque real disponível

    if quantidade > estoque_disponivel:

        print("\n❌ Estoque insuficiente.")
        print(f"Disponível: {estoque_disponivel} unidade(s).")

    else:

        preco = float(produto[2])
        subtotal = preco * quantidade

        carrinho.append((
            produto[0],
            produto[1],
            preco,
            quantidade,
            subtotal
        ))

        print(f"\n🛒 '{produto[1]}' foi adicionado ao carrinho!")

    cursor.close()
    conexao.close()


def ver_carrinho():

    print("\n====== CARRINHO ======")

    total = 0

    if not carrinho:
        print("Carrinho vazio.")
        return

    for item in carrinho:

        print(f"""
ID Produto: {item[0]}
Produto: {item[1]}
Quantidade: {item[3]}
Subtotal: R$ {item[4]:.2f}
------------------------
""")

        total += item[4]

    print(f"TOTAL: R$ {total:.2f}")


def remover_item_carrinho():

    if not carrinho:
        print("Carrinho vazio!")
        return

    ver_carrinho()

    while True:

        try:
            id_produto = int(input("\nDigite o ID do produto que deseja remover: "))
            break

        except ValueError:
            print("Digite um ID válido!")

    for item in carrinho:

        if item[0] == id_produto:
            carrinho.remove(item)

            print("✔ Produto removido do carrinho!")
            return

    print("❌ Produto não encontrado no carrinho.")


def finalizar_compra():

    conexao = conectar()
    cursor = conexao.cursor()

    print("\n    === FINALIZAR COMPRA ===")

    if not carrinho:
        print("Carrinho vazio!")

        cursor.close()
        conexao.close()
        return

    total = 0

    print("\nItens da compra:")

    for item in carrinho:
        print(f"- {item[1]} | {item[3]}x | R$ {item[4]:.2f}")
        total += item[4]

    print(f"\nTOTAL DA COMPRA: R$ {total:.2f}")

    print("\nFormas de pagamento:")
    print("1 - Dinheiro")
    print("2 - Cartão (Crédito/Débito)")
    print("3 - Pix")
    print("0 - Retornar")
    print("")
    opcao = input("Escolha a forma de pagamento: ")

    if opcao == "1":
        forma = "Dinheiro"

    elif opcao == "2":
        forma = "Cartão (Crédito/Débito)"

    elif opcao == "3":
        forma = "Pix"

    elif opcao == "0":
        print("\n↩ Voltando ao menu...")
        cursor.close()
        conexao.close()

        return ("continuar")

    else:
        print("Opção inválida!")

        cursor.close()
        conexao.close()
        return

    sql = """
    INSERT INTO tbl_vendas (total_venda, forma_pagamento)
    VALUES (%s, %s)
    """

    cursor.execute(sql, (total, forma))

    id_venda = cursor.lastrowid

    for item in carrinho:

        id_produto = item[0]
        quantidade = item[3]
        subtotal = item[4]

        sql = """
        INSERT INTO tbl_vendas_produtos
        (id_venda, id_produto, quantidade_produto, subtotal_produto)
        VALUES (%s, %s, %s, %s)
        """

        valores = (
            id_venda,
            id_produto,
            quantidade,
            subtotal
        )

        cursor.execute(sql, valores)

        sql_update = """
        UPDATE tbl_produtos
        SET quantidade_produto = quantidade_produto - %s
        WHERE id_produto = %s
        """

        cursor.execute(sql_update, (quantidade, id_produto))

    conexao.commit()

    print("\n✔ Compra finalizada com sucesso!\n")
    print(f"Pagamento: {forma}")
    print(f"Total pago: R$ {total:.2f}")

    carrinho.clear()

    cursor.close()
    conexao.close()

    print("\n====================================")

    resposta = input("Deseja comprar com a FarmaTech novamente? (s/n): ").lower()

    if resposta == "s":

        print("\n✔ Redirecionando para o menu...")
        return "continuar"

    else:

        print("\n👋 Obrigado por comprar na FarmaTech!")
        return "sair"


def menu_cliente(usuario):

    while True:

        print("\n========================")
        print("     ÁREA DO CLIENTE")
        print("========================")
        print("")
        print(f"Bem-vindo(a), {usuario}!")
        print("")
        print("1 - Listar produtos")
        print("2 - Pesquisar produto")
        print("3 - Adicionar ao carrinho")
        print("4 - Ver carrinho")
        print("5 - Remover item do carrinho")
        print("6 - Finalizar compra")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            listar_produtos()

        elif opcao == "2":
            pesquisar_produto()

        elif opcao == "3":
            adicionar_carrinho()

        elif opcao == "4":
            ver_carrinho()

        elif opcao == "5":
            remover_item_carrinho()

        elif opcao == "6":

            resultado = finalizar_compra()

            if resultado == "sair":
                break

        elif opcao == "0":

            print("Saindo do sistema do cliente...")
            break

        else:
            print("❌ Opção inválida")
            resultado = finalizar_compra()
            
