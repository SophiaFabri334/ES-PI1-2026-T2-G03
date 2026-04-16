import mysql.connector

# conexão com o banco de dados
conexao = mysql.connector.connect(
    host =  "localhost",
    user = "root",
    password = "puc1234",
    database = "sistema_eleicao"
)

cursor = conexao.cursor()

# inserção de dados - CANDIDATOS
def inserir_candidatos(numero, nome, partido):
    sql = "INSERT INTO candidatos (numero, nome_candidato, partido) VALUES (%s, %s, %s, %s)"
    valores = (numero, nome, partido)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Candidato cadastrado com ID: ", cursor.lastrowid)


# inserção de dados - ELEITORES 
def inserir_eleitores(titulo_eleitor, cpf, nome, senha, ja_votou, mesario):
    sql = "INSERT INTO eleitores (titulo_eleitor, cpf, nome_completo, senha, ja_votou, mesario) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (titulo_eleitor, cpf, nome, senha, ja_votou, mesario) #confirmar como salvar a senha com hash
    cursor.execute(sql, valores)
    conexao.commit()
    print("Eleitor cadastrado com ID: ", cursor.lastrowid)
    
# inserção de dados - VOTOS
def inserir_voto(id_candidato):
    sql = "INSERT INTO votos (id_candidato) VALUES (%s)"
    valores = (id_candidato)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Voto cadastrado com ID: ", cursor.lastrowid)

# busca de eleitores 
def busca_eleitores():
    sql = "SELECT E.id_eleitor, E.titulo_eleitor, E.cpf, E.nome_completo, E.ja_votou, E.mesario FROM ELEITORES E ORDER BY E.id_eleitor"
    return cursor.execute(sql)
