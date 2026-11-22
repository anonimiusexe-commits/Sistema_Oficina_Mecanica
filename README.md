# Sistema de Oficina Mecânica

Sistema de linha de comando desenvolvido em Python e integrado ao MySQL para cadastrar clientes e seus veículos.

## Funcionalidades

- Cadastro de clientes.
- Validação dos dígitos verificadores do CPF.
- Cadastro de veículos.
- Validação de placas nos formatos antigo e Mercosul.
- Validação do ano do veículo.
- Associação de cada veículo a um cliente cadastrado.

## Estrutura do projeto

```text
Sistema_Oficina/
├── main.py
├── banco.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── oficina/
    ├── __init__.py
    ├── conexao.py
    ├── validacoes.py
    ├── clientes.py
    ├── veiculos.py
    └── menu.py
```

## Requisitos

- Python 3.10 ou superior.
- MySQL Server.
- pip.

## Configuração

1. Clone ou baixe este repositório.
2. Abra o terminal na pasta do projeto.
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Importe o arquivo `banco.sql` no MySQL Workbench ou pelo terminal.
5. Crie uma cópia de `.env.example` com o nome `.env`.
6. Edite o `.env` e informe os dados da sua conexão MySQL.
7. Execute o sistema:

   ```bash
   python main.py
   ```

## Segurança

O arquivo `.env` contém credenciais locais e está listado no `.gitignore`. Não publique esse arquivo. O `.env.example` serve apenas como modelo, sem uma senha real.

## Observação sobre o banco

O arquivo `banco.sql` cria as tabelas `clientes` e `veiculos` com os nomes de colunas esperados pelo código. Se você já possui tabelas com estrutura diferente, confira a estrutura antes de importar o script.
