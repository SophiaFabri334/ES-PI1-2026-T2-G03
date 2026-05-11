CREATE DATABASE sistema_eleicao;
USE sistema_eleicao;
-- Tabela de Candidatos (Necessária para validar o número do voto)
CREATE TABLE candidatos (
    id_candidato INT AUTO_INCREMENT PRIMARY KEY,
    numero INT UNIQUE,
    nome_candidato VARCHAR(100) NOT NULL,
    partido VARCHAR(20) NOT NULL
);
-- Tabela de Eleitores
CREATE TABLE eleitores (
    id_eleitor INT AUTO_INCREMENT PRIMARY KEY,
    titulo_eleitor VARCHAR(12) UNIQUE NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    -- UNIQUE impede CPFs repetidos
    nome_completo VARCHAR(100) NOT NULL,
    -- UNIQUE impede logins repetidos
    senha VARCHAR(255) NOT NULL,
    -- Indica se o eleitor já votou, para controle do voto único
    ja_votou BOOLEAN DEFAULT FALSE,
    -- Indica se o eleitor tbm é um mesário
    mesario BOOLEAN DEFAULT FALSE
);
-- Tabela de votos - faz a relação dos em cada candidato
CREATE TABLE votos (
    id_voto INT AUTO_INCREMENT PRIMARY KEY,
    id_candidato INT,
    FOREIGN KEY (id_candidato) REFERENCES candidatos(id_candidato),
    data_hora datetime, 
)

CREATE TABLE urna (
    id INT PRIMARY KEY AUTO_INCREMENT,
    aberta TINYINT(1) DEFAULT 0,
    data_abertura DATETIME,
    data_fechamento DATETIME
);

INSERT INTO urna (aberta) VALUES (0);