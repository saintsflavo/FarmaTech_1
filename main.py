from bd import conectar
from login import fazer_login

usuario_logado = fazer_login()
conexao = conectar()

cursor = conexao.cursor()

print("Sistema FarmaTech iniciado!")

cursor.close()
conexao.close()

from crud_produtos import (
    cadastrar_produto,
    listar_produtos,
    atualizar_produto,
    deletar_produto
)


while True:

     print("\n===== FARMATECH =====")
     print("")
     print("1 - Cadastrar produto")
     print("2 - Listar produtos")
     print("3 - Atualizar produto")
     print("4 - Deletar produto")
     print("5 - Sair")
     print("")
     opcao = input("Escolha uma opção: ")

     if opcao == "1":
         cadastrar_produto()

     elif opcao == "2":
         listar_produtos()

     elif opcao == "3":
         atualizar_produto()

     elif opcao == "4":
         deletar_produto()

     elif opcao == "5":
         print("Sistema encerrado!")
         break

     else:
         print("Opção inválida!")