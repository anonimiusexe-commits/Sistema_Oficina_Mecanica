import mysql.connector

from oficina.clientes import cadastrar_cliente
from oficina.veiculos import cadastrar_veiculo, consultar_veiculos, atualizar_veiculo, excluir_veiculo

def executar_menu(conexao):
    while True:
        print("\n===== SISTEMA OFICINA MECÂNICA =====")
        print("1 - Cadastrar cliente")
        print("2 - Cadastrar veículo")
        print("3 - Consultar veículos")
        print("4 - Atualizar veículo")
        print("5 - Excluir veículo")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar_cliente(conexao)

            elif opcao == "2":
                cadastrar_veiculo(conexao)

            elif opcao == "3":
                consultar_veiculos(conexao)

                resposta = input("\nDeseja cadastrar outro veículo? (s/n): ").strip().lower()

                if resposta == "s":
                    cadastrar_veiculo(conexao)
            elif opcao == "4":
                atualizar_veiculo(conexao)

            elif opcao == "5":
                excluir_veiculo(conexao)

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
