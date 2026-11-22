from oficina.conexao import conectar
from oficina.menu import executar_menu


def main():
    conexao = None

    try:
        conexao = conectar()
        print("Conexão realizada com sucesso!")
        executar_menu(conexao)

    except Exception as erro:
        print(f"Não foi possível iniciar o sistema: {erro}")

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()
            print("Conexão encerrada.")


if __name__ == "__main__":
    main()
