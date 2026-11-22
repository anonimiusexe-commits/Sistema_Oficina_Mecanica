import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def conectar():
    """Abre e retorna uma conexão com o banco de dados MySQL."""
    configuracao = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "oficina"),
    }

    return mysql.connector.connect(**configuracao)
