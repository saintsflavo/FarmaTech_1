from bd import conectar

def fazer_login():

    login = input("Login: ")
    senha = input("Senha: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT * FROM tbl_usuarios
    WHERE login_usuario = %s
    AND senha_usuario = %s
    """

    valores = (login, senha)

    cursor.execute(sql, valores)

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if usuario:

        print("Login realizado!")

        return usuario

    else:

        print("Login inválido!")

        return None