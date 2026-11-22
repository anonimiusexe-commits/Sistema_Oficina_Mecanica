
from oficina.validacoes import validar_ano, validar_placa


def cadastrar_veiculo(conexao):
    print("\n===== CADASTRO DE VEÍCULOS =====")

    cursor = conexao.cursor()

    try:
        cursor.execute(
            "SELECT id_clientes, nome FROM clientes ORDER BY nome"
        )
        clientes = cursor.fetchall()

        if not clientes:
            print("Cadastre um cliente primeiro!")
            return

        print("\nClientes disponíveis:")
        for cliente in clientes:
            print(f"ID: {cliente[0]} | Nome: {cliente[1]}")

        id_clientes = input("\nID do cliente: ").strip()

        try:
            id_clientes = int(id_clientes)
        except ValueError:
            raise ValueError("O ID do cliente deve ser um número inteiro!")

        ids_disponiveis = [cliente[0] for cliente in clientes]

        if id_clientes not in ids_disponiveis:
            raise ValueError("Esse ID de cliente não está na lista!")

        placa = validar_placa(input("Placa: "))
        modelo = input("Modelo: ").strip()
        ano = validar_ano(input("Ano: "))
        problema = input("Problema: ").strip()

        if not modelo or not problema:
            raise ValueError("Preencha todos os campos!")

        sql = """
            INSERT INTO veiculos
                (placa, modelo, ano, problema, id_clientes)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (placa, modelo, ano, problema, id_clientes)

        cursor.execute(sql, valores)
        conexao.commit()

        print("\nVeículo cadastrado com sucesso!")
        print("ID do veículo:", cursor.lastrowid)

    finally:
        cursor.close()


def consultar_veiculos(conexao):
    print("\n===== VEÍCULOS CADASTRADOS =====")

    cursor = conexao.cursor()

    try:
        sql = """
            SELECT
                v.id_veiculos,
                v.placa,
                v.modelo,
                v.ano,
                v.problema,
                c.nome
            FROM veiculos v
            INNER JOIN clientes c
                ON v.id_clientes = c.id_clientes
            ORDER BY v.id_veiculos
        """

        cursor.execute(sql)
        veiculos = cursor.fetchall()

        if not veiculos:
            print("Nenhum veículo cadastrado!")
            return

        for veiculo in veiculos:
            print("\n------------------------------")
            print(f"ID: {veiculo[0]}")
            print(f"Placa: {veiculo[1]}")
            print(f"Modelo: {veiculo[2]}")
            print(f"Ano: {veiculo[3]}")
            print(f"Problema: {veiculo[4]}")
            print(f"Cliente: {veiculo[5]}")

    finally:
        cursor.close()


def atualizar_veiculo(conexao):
    print("\n===== ATUALIZAR VEÍCULO =====")

    cursor = conexao.cursor()

    try:
        id_veiculo = input("ID do veículo: ").strip()

        if not id_veiculo.isdigit():
            raise ValueError("Digite um ID válido!")

        id_veiculo = int(id_veiculo)

        cursor.execute(
            "SELECT id_veiculos FROM veiculos WHERE id_veiculos = %s",
            (id_veiculo,)
        )

        if not cursor.fetchone():
            print("Veículo não encontrado!")
            return

        placa = validar_placa(input("Nova placa: "))
        modelo = input("Novo modelo: ").strip()
        ano = validar_ano(input("Novo ano: "))
        problema = input("Novo problema: ").strip()

        if not modelo or not problema:
            raise ValueError("Preencha todos os campos!")

        sql = """
            UPDATE veiculos
            SET placa = %s, modelo = %s, ano = %s, problema = %s
            WHERE id_veiculos = %s
        """

        valores = (placa, modelo, ano, problema, id_veiculo)

        cursor.execute(sql, valores)
        conexao.commit()

        print("Veículo atualizado com sucesso!")

    finally:
        cursor.close()


def excluir_veiculo(conexao):
    print("\n===== EXCLUIR VEÍCULO =====")

    cursor = conexao.cursor()

    try:
        id_veiculo = input("ID do veículo que deseja excluir: ").strip()

        if not id_veiculo.isdigit():
            raise ValueError("Digite um ID válido!")

        id_veiculo = int(id_veiculo)

        cursor.execute(
            "SELECT id_veiculos, modelo FROM veiculos WHERE id_veiculos = %s",
            (id_veiculo,)
        )

        veiculo = cursor.fetchone()

        if not veiculo:
            print("Veículo não encontrado!")
            return

        print(f"Veículo encontrado: {veiculo[1]}")

        confirmacao = input(
            "Tem certeza que deseja excluir? (s/n): "
        ).strip().lower()

        if confirmacao == "s":
            cursor.execute(
                "DELETE FROM veiculos WHERE id_veiculos = %s",
                (id_veiculo,)
            )

            conexao.commit()
            print("Veículo excluído com sucesso!")

        else:
            print("Exclusão cancelada!")

    finally:
        cursor.close()
