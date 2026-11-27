# ============================================
#          IMPORTAÇÃO DE BIBLIOTECAS          
# ============================================

import os
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# ============================================
#             CONEXÃO COM O MYSQL             
# ============================================

def conectar():
    configuracao = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "oficina"),
    }

    return mysql.connector.connect(**configuracao)

# ============================================
#              VALIDAÇÃO DE DADOS             
# ============================================

def validar_cpf(cpf):
    cpf = cpf.strip().replace(".", "").replace("-", "")
    if len(cpf) != 11 or not cpf.isascii() or not cpf.isdigit():
        raise ValueError("O CPF deve ter 11 números!")
    return cpf

def validar_telefone(telefone):
    if len(telefone) != 11 or not telefone.isascii() or not telefone.isdigit():
        raise ValueError("O telefone deve conter 11 números!")
    return telefone

def validar_nome(nome):
    if not nome.replace(" ", "").isalpha():
        raise ValueError("O nome deve conter apenas letras!")
    return nome

def validar_email(email):
    if email.count("@") != 1 or " " in email:
        raise ValueError("Email inválido!")

    usuario, dominio = email.split("@")

    if not usuario or "." not in dominio:
        raise ValueError("Email inválido!")

    if dominio.startswith(".") or dominio.endswith("."):
        raise ValueError("Email inválido!")

    return email

def validar_placa(placa):
    placa = placa.upper().replace("-", "").replace(" ", "")
    if len(placa) != 7 or not placa.isascii():
        raise ValueError("Placa inválida!")
    antiga = placa[:3].isalpha() and placa[3:].isdigit()
    mercosul = (placa[:3].isalpha() and placa[3].isdigit()
                and placa[4].isalpha() and placa[5:].isdigit())
    if not antiga and not mercosul:
        raise ValueError("Placa inválida!")
    return placa

def validar_ano(ano):
    try:
        ano = int(ano)
    except (TypeError, ValueError):
        raise ValueError("Informe um ano válido!")

    ano_atual = datetime.now().year

    if ano < 1900 or ano > ano_atual:
        raise ValueError("Ano inválido!")

    return ano

# ============================================
#               CRUD DE CLIENTES              
# ============================================

def cadastrar_cliente(conexao):
    print("\n===== CADASTRO DE CLIENTES =====")

    nome = validar_nome(input("Nome: ").strip())
    cpf = input("CPF: ").strip()
    email = validar_email(input("Email: ").strip())
    telefone = validar_telefone(input("Telefone: ").strip())

    if not nome or not cpf or not email or not telefone:
        raise ValueError("Preencha todos os campos!")

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

def consultar_clientes(conexao):
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM clientes ORDER BY id_clientes")
        clientes = cursor.fetchall()
        if not clientes:
            print("Nenhum cliente cadastrado!")
        for cliente in clientes:
            print("ID:", cliente["id_clientes"], "| Nome:", cliente["nome"])
            print("CPF:", cliente["cpf"], "| Email:", cliente["email"], "| Telefone:", cliente["telefone"])
    finally:
        cursor.close()

def atualizar_cliente(conexao):
    consultar_clientes(conexao)
    id_cliente = int(input("ID do cliente: "))
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_clientes FROM clientes WHERE id_clientes = %s", (id_cliente,))
        if not cursor.fetchone():
            print("Cliente não encontrado!")
            return
        nome = validar_nome(input("Informe novo nome: ").strip())
        cpf = validar_cpf(input("Informe novo CPF: "))
        email = validar_email(input("Informe novo email: ").strip())
        telefone = validar_telefone(input("Informe novo telefone: ").strip())
        if not nome or not email or not telefone:
            raise ValueError("Preencha todos os campos!")
        sql = "UPDATE clientes SET nome = %s, cpf = %s, email = %s, telefone = %s WHERE id_clientes = %s"
        cursor.execute(sql, (nome, cpf, email, telefone, id_cliente))
        conexao.commit()
        print("Cliente atualizado com sucesso!")
    finally:
        cursor.close()

def excluir_cliente(conexao):
    consultar_clientes(conexao)
    id_cliente = int(input("ID do cliente: "))
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_clientes FROM clientes WHERE id_clientes = %s", (id_cliente,))
        if not cursor.fetchone():
            print("Cliente não encontrado!")
            return
        cursor.execute("SELECT COUNT(*) FROM veiculos WHERE id_clientes = %s", (id_cliente,))
        if cursor.fetchone()[0] > 0:
            print("Exclua os veículos desse cliente primeiro!")
            return
        if input("Confirma a exclusão? (s/n): ").strip().lower() == "s":
            cursor.execute("DELETE FROM clientes WHERE id_clientes = %s", (id_cliente,))
            conexao.commit()
            print("Cliente excluído com sucesso!")
        else:
            print("Exclusão cancelada!")
    finally:
        cursor.close()

# ============================================
#               CRUD DE VEÍCULOS              
# ============================================

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

        ids_disponiveis = []
        for cliente in clientes:
            ids_disponiveis.append(cliente[0])

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

# ============================================
#                MENU PRINCIPAL               
# ============================================

def executar_menu(conexao):
    while True:
        print("\n===== SISTEMA OFICINA MECÂNICA =====")
        print("1 - Cadastrar cliente")
        print("2 - Consultar clientes")
        print("3 - Atualizar cliente")
        print("4 - Excluir cliente")
        print("5 - Cadastrar veículo")
        print("6 - Consultar veículos")
        print("7 - Atualizar veículo")
        print("8 - Excluir veículo")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()
        try:
            if opcao == "1":
                cadastrar_cliente(conexao)
            elif opcao == "2":
                consultar_clientes(conexao)
            elif opcao == "3":
                atualizar_cliente(conexao)
            elif opcao == "4":
                excluir_cliente(conexao)
            elif opcao == "5":
                cadastrar_veiculo(conexao)
            elif opcao == "6":
                consultar_veiculos(conexao)
            elif opcao == "7":
                atualizar_veiculo(conexao)
            elif opcao == "8":
                excluir_veiculo(conexao)
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
        except ValueError as erro:
            print("Erro de validação:", erro)
        except mysql.connector.Error as erro:
            if erro.errno == 1062:
                print("CPF, email, telefone ou placa já cadastrados!")
            else:
                print("Erro no MySQL:", erro)
        finally:
            conexao.rollback()

# ============================================
#           INICIALIZAÇÃO DO SISTEMA          
# ============================================

def main():
    conexao = None

    try:
        conexao = conectar()
        print("Conexão realizada com sucesso!")
        executar_menu(conexao)

    except mysql.connector.Error as erro:
        print(f"Não foi possível iniciar o sistema: {erro}")

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()
            print("Conexão encerrada.")


if __name__ == "__main__":
    main()