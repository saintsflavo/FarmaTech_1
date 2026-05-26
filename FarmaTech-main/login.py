from conexao import conectar


def buscar_usuario(login_usuario, senha_usuario):

    conexao = conectar()
    if not conexao:
        return None

    cursor = conexao.cursor(dictionary=True)

    sql = """
    SELECT login_usuario, tipo_usuario
    FROM tbl_usuarios
    WHERE login_usuario = %s AND senha_usuario = %s
    """

    cursor.execute(sql, (login_usuario, senha_usuario))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario

def usuario_existe(login_usuario):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT login_usuario FROM tbl_usuarios WHERE login_usuario = %s"
    cursor.execute(sql, (login_usuario,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado is not None


def cadastrar_usuario():

    print("\n=== CADASTRO DE USUÁRIO ===")

    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    tipo = input("Tipo (admin/cliente): ").strip().lower()

    if not login or not senha:
        print("❌ Campos obrigatórios!")
        return None

    if tipo not in ["admin", "cliente"]:
        print("❌ Tipo inválido!")
        return None

    if usuario_existe(login):
        print("❌ Usuário já existe!")
        return None

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO tbl_usuarios (login_usuario, senha_usuario, tipo_usuario)
    VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (login, senha, tipo))
    conexao.commit()

    cursor.close()
    conexao.close()
    print("")
    print("✔ Cadastro realizado com sucesso!")

    
    return {
        "login_usuario": login,
        "tipo_usuario": tipo
    }

def tela_admin(nome_usuario):
    print('\n=================================')
    print('       MENU DO ADMINISTRADOR')
    print('=================================')
    print("")
    print(f'Bem-vindo(a), {nome_usuario}!')


def tela_cliente(nome_usuario):
    print('\n=================================')
    print('        MENU DO CLIENTE')
    print('=================================')
    print("")
    print(f'Bem-vindo(a), {nome_usuario}!')



def realizar_login():
    from cliente import menu_cliente
    from admin import menu_admin

    while True:

        print("\n========================")
        print("       FARMATECH")
        print("========================")
        print("")
        print("1 - Login")
        print("2 - Cadastrar usuário")
        print("0 - Sair")

        opcao = input("\nEscolha: ")

        
        if opcao == "1":

            login = input("Login: ").strip()
            senha = input("Senha: ").strip()

            usuario = buscar_usuario(login, senha)

            if usuario:

                if usuario["tipo_usuario"] == "admin":
                    menu_admin(usuario["login_usuario"])                
                else:
                    menu_cliente(usuario["login_usuario"])
                break 

            else:
                print("❌ Login ou senha inválidos!")

        
        elif opcao == "2":

            usuario = cadastrar_usuario()

            if usuario:

                if usuario["tipo_usuario"] == "admin":
                    menu_admin(usuario["login_usuario"])
                else:
                    menu_cliente(usuario["login_usuario"])

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("❌ Opção inválida!")
            