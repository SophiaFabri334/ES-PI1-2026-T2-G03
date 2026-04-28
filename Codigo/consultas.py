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
    valores = (id_candidato,)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Voto cadastrado com ID: ", cursor.lastrowid)

# busca de eleitores 
def busca_eleitores():
    cursor = conexao.cursor()
    sql = "SELECT E.id_eleitor, E.titulo_eleitor, E.cpf, E.nome_completo, E.ja_votou, E.mesario FROM ELEITORES E ORDER BY E.id_eleitor"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado

# busca de eleitores por pesquisa
def filtra_eleitores(pesquisa):
    cursor = conexao.cursor()
    
    sql = "SELECT E.id_eleitor, E.titulo_eleitor, E.cpf, E.nome_completo, E.ja_votou, E.mesario FROM ELEITORES E WHERE E.titulo_eleitor LIKE %s OR E.nome_completo LIKE %s OR E.cpf LIKE %s ORDER BY E.id_eleitor"
    
    valor = f"%{pesquisa}%"
    valores = (valor, valor, valor)

    cursor.execute(sql, valores)
    resultado = cursor.fetchall()
    cursor.close()
    
    return resultado

#remover eleitor
def remover_eleitor(cpf):
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM eleitores WHERE cpf = %s", (cpf,))
    conexao.commit()
    cursor.close()

def verificar_cpf_existe(cpf):
    """
    Verifica se o CPF ja existe no banco de dados.
    Busca nas tabelas 'eleitores' para evitar duplicidade.
    
    Parametros:
        cpf (str): CPF a ser verificado (apenas numeros)
    
    Retorna:
        bool: True se CPF ja existe, False caso contrario
    """
    try:
        # Busca na tabela de usuarios (eleitores comuns)
        cursor.execute("SELECT 1 FROM eleitores WHERE cpf = %s LIMIT 1", (cpf,))
        return cursor.fetchone() is not None

    except Exception as e:
        print("Erro ao verificar CPF:", e)
        return False