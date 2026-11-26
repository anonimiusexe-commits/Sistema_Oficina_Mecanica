CREATE DATABASE IF NOT EXISTS oficina
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE oficina;

CREATE TABLE IF NOT EXISTS clientes (
    id_clientes INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS veiculos (
    id_veiculos INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(7) NOT NULL UNIQUE,
    modelo VARCHAR(100) NOT NULL,
    ano INT NOT NULL,
    problema TEXT NOT NULL,
    id_clientes INT NOT NULL,
    CONSTRAINT fk_veiculos_clientes
        FOREIGN KEY (id_clientes)
        REFERENCES clientes(id_clientes)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);