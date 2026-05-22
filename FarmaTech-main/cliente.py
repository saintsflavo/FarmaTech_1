from conexao import conectar

def listar_produtos():
    conexao = conectar()
    
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id_produto, nome_produto, preco_produto, quantidade_produto FROM tbl_produtos")
    
    produtos = cursor.fetchall()

    print("\n       === PRODUTOS DISPONÍVEIS ===")
    print("")

    for p in produtos:
        print(f"ID: {p[0]} | {p[1]} | R$ {p[2]} | Estoque: {p[3]}")

    cursor.close()
    conexao.close()

def pesquisar_produto():

    nome = input("Digite o nome do produto: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT id_produto, nome_produto, preco_produto, quantidade_produto FROM tbl_produtos WHERE nome_produto LIKE %s"
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

carrinho = []


def adicionar_carrinho():

    id_produto = input("Digite o ID do produto: ")
    quantidade = int(input("Quantidade desejada: "))
    
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

    if quantidade > produto[3]:
        print("")
        print("❌ Estoque insuficiente.")
        print(f"Disponível: {produto[3]} unidade(s).")

    else:
        try:
            preco = float(produto[2])
            subtotal = preco * quantidade
        except Exception:
            preco = 0.0

        carrinho.append((
            produto[0],  # id
            produto[1],  # nome
            preco,       # preço unitário
            quantidade,
            subtotal
        ))

        print(f"\n🛒 '{produto[1]}' foi adicionado ao carrinho!")

    cursor.close()
    conexao.close()


def ver_carrinho():

    print("\n====== CARRINHO ======")
    print("")
    total = 0

    if not carrinho:
        print("Carrinho vazio.")
        return

    for item in carrinho:
        print(f"{item[1]} | {item[3]}x | R$ {item[4]:.2f}")
        total += item[4]

    print(f"\nTOTAL: R$ {total:.2f}")

def finalizar_compra():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n    === FINALIZAR COMPRA ===")

    if not carrinho:
        print("Carrinho vazio!")
        return

    total = 0

    print("\nItens da compra:")
    for item in carrinho:
        print(f"- {item[1]} | {item[3]}x | R$ {item[4]:.2f}")
        total += item[4]

    print(f"\nTOTAL DA COMPRA: R$ {total:.2f}")

    print("\nFormas de pagamento:")
    print("1 - Dinheiro")
    print("2 - Cartão de crédito")
    print("3 - Pix")

    opcao = input("Escolha a forma de pagamento: ")

    if opcao == "1":
        forma = "Dinheiro"
    elif opcao == "2":
        forma = "Cartão de crédito"
    elif opcao == "3":
        forma = "Pix"
    else:
        print("Forma inválida!")
        return

    print(f"\n✔ Compra finalizada com sucesso!")
    print("")
    print(f"Pagamento: {forma}")
    print(f"Total pago: R$ {total:.2f}")

    sql = """
INSERT INTO tbl_vendas (total_venda, forma_pagamento)
VALUES (%s, %s)
"""

    cursor.execute(sql, (total, forma))

    for item in carrinho:

        id_produto = item[0]

        sql = """
        UPDATE tbl_produtos
        SET quantidade_produto = quantidade_produto - %s
        WHERE id_produto = %s
        """

        quantidade = item[3]

        cursor.execute(sql, (quantidade, id_produto))
    
    conexao.commit()
    carrinho.clear()

    print("\n====================================")
    resposta = input("Deseja comprar com a FarmaTech novamente? (s/n): ").lower()

    if resposta == "s":
        print("\n✔ Redirecionando para o menu...")
        return "continuar"

    else:
        print("\n👋 Obrigado por comprar na FarmaTech!")
        return "sair"
    
    cursor.close()
    conexao.close()

def menu_cliente(usuario):

    while True:

        print("\n========================")
        print(f"     ÁREA DO CLIENTE")
        print("========================")
        print("")
        print(f"Bem-vindo(a), {usuario}!")
        print("")
        print("1 - Listar produtos")
        print("2 - Pesquisar produto")
        print("3 - Adicionar ao carrinho")
        print("4 - Ver carrinho")
        print("5 - Finalizar compra")
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
            resultado = finalizar_compra()

            if resultado == "sair":
                break

        elif opcao == "0":
            print("Saindo do sistema do cliente...")
            break

        else:
            print("❌ Opção inválida")