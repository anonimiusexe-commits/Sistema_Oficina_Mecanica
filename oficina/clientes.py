def cadastrar_cliente(conexao):
    print("\n===== CADASTRO DE CLIENTES =====")

    nome = input("Nome: ").strip()
    cpf = input("CPF: ").strip()
    email = input("Email: ").strip()
    telefone = input("Telefone: ").strip()

    if not nome or not cpf or not email or not telefone:
        raise ValueError("Preencha todos os campos!")

    from oficina.validacoes import validar_cpf
    cpf = validar_cpf(cpf)

    cursor = conexao.cursor()

    try:
        sql = """
            INSERT INTO clientes (nome, cpf, email, telefone)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, cpf, email, telefone))
        conexao.commit()

        print("\nCliente cadastrado com sucesso!")
        print("ID do cliente:", cursor.lastrowid)

    finally:
        cursor.close()
