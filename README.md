# Sistema de Oficina Mecânica

## Sobre o projeto

Sistema desenvolvido em Python e MySQL para gerenciamento de clientes e veículos de uma oficina mecânica.

O sistema permite cadastrar, consultar, atualizar e excluir informações por meio de um menu interativo no terminal.

## Funcionalidades

### Clientes

- Cadastrar clientes.
- Consultar clientes cadastrados.
- Atualizar informações.
- Excluir clientes.

### Veículos

- Cadastrar veículos.
- Consultar veículos cadastrados.
- Atualizar informações.
- Excluir veículos.
- Vincular veículos aos seus respectivos proprietários.

## Validação de dados

- Nome contendo apenas letras e espaços.
- CPF contendo 11 dígitos.
- Telefone contendo 11 dígitos.
- Verificação do formato do e-mail.
- Validação de placas antigas e Mercosul.
- Validação do ano do veículo.
- Bloqueio de informações duplicadas.
- Verificação de campos obrigatórios.

## Tecnologias utilizadas

- Python
- MySQL
- MySQL Connector
- Python-dotenv
- Git
- GitHub

## Banco de dados

O banco possui duas tabelas: clientes e veículos.

O relacionamento é de um para muitos (1:N), permitindo que um cliente tenha vários veículos, mas cada veículo pertença a apenas um cliente.

## Estrutura do projeto

- main.py — Código principal do sistema.
- banco.sql — Estrutura do banco de dados.
- requirements.txt — Bibliotecas necessárias.
- .env.example — Modelo de configuração da conexão.
- .gitignore — Arquivos ignorados pelo Git.
- README.md — Documentação do projeto.

## Como executar

1. Baixe ou clone o repositório.
2. Instale as bibliotecas utilizando o comando `pip install -r requirements.txt`.
3. Execute o arquivo banco.sql no MySQL.
4. Crie o arquivo .env utilizando o .env.example como modelo.
5. Configure os dados de conexão com o MySQL.
6. Execute o comando `python main.py`.

## Objetivo acadêmico

O projeto foi desenvolvido para aplicar os conhecimentos de programação em Python, banco de dados, CRUD, funções, listas, dicionários, tratamento de exceções e controle de versão com Git e GitHub.

## Integrantes da equipe

- Arthur Ricardo
- Elielton Nascimento
- Kevyn Emanoel