
import mysql.connector
from getpass import getpass
from datetime import datetime
import re


# ===================================
# VALIDAÇÕES
# ===================================

def validar_cpf(cpf):
    cpf = re.sub(r"\D", "", cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValueError("CPF inválido!")

    for tamanho in [9, 10]:
        soma = 0

        for i in range(tamanho):
            soma += int(cpf[i]) * (tamanho + 1 - i)

        digito = (soma * 10) % 11

        if digito == 10:
            digito = 0

        if digito != int(cpf[tamanho]):
            raise ValueError("CPF inválido!")

    return cpf


def validar_placa(placa):
    placa = placa.upper().replace("-", "").replace(" ", "")

    antigo = r"[A-Z]{3}[0-9]{4}"
    mercosul = r"[A-Z]{3}[0-9][A-Z][0-9]{2}"

    if not (re.fullmatch(antigo, placa)
            or re.fullmatch(mercosul, placa)):
        raise ValueError("Placa inválida!")

    return placa


def validar_ano(ano):
    ano = int(ano)
    ano_atual = datetime.now().year

    if ano < 1900 or ano > ano_atual:
        raise ValueError("Ano inválido!")

    return ano


# ===================================
# CADASTRO DE CLIENTES
# ===================================

def cadastrar_cliente(conexao):

    print("\n===== CADASTRO DE CLIENTES =====")

    nome = input("Nome: ").strip()
    cpf = validar_cpf(input("CPF: "))
    email = input("Email: ").strip()
    telefone = input("Telefone: ").strip()

    if not nome or not email or not telefone:
        raise ValueError("Preencha todos os campos!")

    cursor = conexao.cursor()

    try:
        sql = """
            INSERT INTO clientes
            (nome, cpf, email, telefone)
            VALUES (%s, %s, %s, %s)
        """

        valores = (nome, cpf, email, telefone)

        cursor.execute(sql, valores)
        conexao.commit()

        print("\nCliente cadastrado com sucesso!")
        print("ID do cliente:", cursor.lastrowid)

    finally:
        cursor.close()


# ===================================
# CADASTRO DE VEÍCULOS
# ===================================

def cadastrar_veiculo(conexao):

    print("\n===== CADASTRO DE VEÍCULOS =====")

    cursor = conexao.cursor()

    try:
        # Mostrar clientes cadastrados
        cursor.execute(
            "SELECT id_clientes, nome FROM clientes"
        )

        clientes = cursor.fetchall()

        if not clientes:
            print("Cadastre um cliente primeiro!")
            return

        print("\nClientes disponíveis:")

        for cliente in clientes:
            print(f"ID: {cliente[0]} | Nome: {cliente[1]}")

        # Dados do veículo
        id_clientes = int(input("\nID do cliente: "))
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

        valores = (
            placa,
            modelo,
            ano,
            problema,
            id_clientes
        )

        cursor.execute(sql, valores)
        conexao.commit()

        print("\nVeículo cadastrado com sucesso!")
        print("ID do veículo:", cursor.lastrowid)

    finally:
        cursor.close()


# ===================================
# MENU PRINCIPAL
# ===================================

def menu(conexao):

    while True:

        print("\n===== SISTEMA OFICINA MECÂNICA =====")
        print("1 - Cadastrar cliente")
        print("2 - Cadastrar veículo")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        try:
            if opcao == "1":
                cadastrar_cliente(conexao)

            elif opcao == "2":
                cadastrar_veiculo(conexao)

            elif opcao == "0":
                print("Sistema encerrado!")
                break

            else:
                print("Opção inválida!")

        except ValueError as erro:
            print("Erro de validação:", erro)

        except mysql.connector.Error as erro:
            conexao.rollback()
            print("Erro no MySQL:", erro)


# ===================================
# CONEXÃO COM O MYSQL
# ===================================

def main():

    conexao = None

    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password=getpass("Senha do MySQL: "),
            database="oficina"
        )

        if conexao.is_connected():
            print("Conexão realizada com sucesso!")
            menu(conexao)

    except mysql.connector.Error as erro:
        print("Erro de conexão:", erro)

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()
            print("Conexão encerrada.")


if __name__ == "__main__":
    main()
