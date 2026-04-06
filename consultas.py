import mysql.connector

# conexão com o banco de dados
conexao = mysql.connector.connect(
    host =  "localhost",
    user = "root",
    password = "puc1234",
    database = "projeto_integrador"
)

cursor = conexao.cursor()

# ---- POST - inserir novo usuário ----