import mysql.connector
from datetime import datetime
import util as util       # Modulo de funcoes utilitarias (validacao, logs, etc.)
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
    sql = "INSERT INTO candidatos (numero, nome_candidato, partido) VALUES (%s, %s, %s)"
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
def inserir_voto(id_candidato, numero_candidato, titulo, cpf, chave):
    try:
        protocolo = util.gerar_protocolo(numero_candidato)
        sql = "INSERT INTO votos (id_candidato, data_hora, protocolo) VALUES (%s, %s, %s)"

        valores = (id_candidato, datetime.now(), protocolo)
        cursor.execute(sql, valores)
        conexao.commit()
        print("Voto cadastrado com sucesso:", cursor.lastrowid)
        atualiza_eleitor(titulo, cpf, chave)
        return protocolo
    except Exception as e:
        print("Erro ao cadastrar voto:", e)
        return None
    
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
    
def verificar_titulo_existe(titulo):
    """
    Verifica se o titulo de eleitor ja existe no banco de dados.
    """
    try:
        # Busca na tabela de usuarios (eleitores comuns)
        cursor.execute("SELECT 1 FROM eleitores WHERE titulo_eleitor = %s LIMIT 1", (titulo,))
        return cursor.fetchone() is not None

    except Exception as e:
        print("Erro ao verificar titulo de eleitor:", e)
        return False
    
# verifica eleitor - tipo = 1 ? mesario : eleitor
def verifica_eleitor(titulo, cpf_4, chave, tipo):
    """
        Verifica se o mesario/eleitor existe no banco. 
    """
    try:
        sql = "SELECT nome_completo, mesario FROM eleitores WHERE titulo_eleitor=%s AND LEFT(cpf,4)=%s AND senha=%s "
        if tipo == 1:
            sql += " AND COALESCE(mesario,0) = 1"
        cursor.execute(sql, (titulo, cpf_4, chave))
        return cursor.fetchone() is not None
    except Exception as e:
        print("Erro ao verificar se o mesario existe no banco:", e)
        return False

# verifica eleitor - tipo = 1 ? mesario : eleitor
def verifica_javotou(titulo, cpf_4, chave):
    """
        Retorna true se der erro ou se o usuario ja votou
    """
    try:
        sql = "SELECT ja_votou FROM eleitores WHERE titulo_eleitor=%s AND LEFT(cpf,4)=%s AND senha=%s"
        cursor.execute(sql, (titulo, cpf_4, chave))
        resultado = cursor.fetchone()

        if resultado is None:
            return False

        ja_votou = resultado[0]

        # trata None
        if ja_votou is None:
            return False

        return bool(ja_votou)
    except Exception as e:
        print("Erro ao verificar se o mesario existe no banco:", e)
        return False
    
#limpa votos
def limpa_votos():
    print("Iniciando zerézima")
    cursor.execute("DELETE FROM votos") 
    conexao.commit() 
    print("Todos os votos anteriores foram apagados ")
    lista_candidatos()

    
# lista candidatos
def lista_candidatos():
    print("Todos os candidatos estão com 0 votos:")
    cursor.execute("select count(v.id_voto) votos, c.id_candidato, c.numero, c.nome_candidato, c.partido from candidatos c left join votos v on v.id_candidato = c.id_candidato group by c.id_candidato, c.numero, c.nome_candidato, c.partido")
    
    for c in cursor:
        print(f"Candidato: {c[3]} | Número: {c[2]} | Votos: {c[0]}")

    print("\nZerézima concluída.")

# busca o candidato selecionado para votação
def retorna_candidato(numero):
    try:
        cursor.execute("select c.id_candidato, c.nome_candidato, c.numero, c.partido from candidatos c where c.numero =%s", (numero,))

        candidato = cursor.fetchone()

        if candidato is None:
            print("\nCandidato não encontrado!\n")
            return None

        return candidato

    except Exception as e:
        print("Erro ao buscar candidato:", e)
        return None
    
def atualiza_eleitor(titulo, cpf_4, chave):
    """
        Atualiza o campo ja_votou para 1
    """

    try:
        sql = "UPDATE eleitores SET ja_votou = 1 WHERE titulo_eleitor=%s AND left(cpf,4)=%s AND senha=%s"
        cursor.execute(sql, (titulo, cpf_4, chave))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao atualizar eleitor:", e)
        return False
    
def limpa_javotou():
    """
        Limpa o campo de todos os eleitores que estão como já votou
    """

    try:
        sql = "UPDATE eleitores SET ja_votou = 0"
        cursor.execute(sql)
        conexao.commit()

        return True
    except Exception as e:
        print("Erro ao limpar ja votou dos eleitores:", e)
        return False
    
def urna_aberta():
    cursor.execute("SELECT aberta FROM urna WHERE id = 1")
    resultado = cursor.fetchone()

    if resultado is None:
        return False

    return resultado[0] == 1

def abrir_urna():
    sql = "UPDATE urna SET aberta = 1, data_abertura = %s, data_fechamento = NULL WHERE id = 1"

    cursor.execute(sql, (datetime.now(),))
    conexao.commit()

def fechar_urna():
    try:
        sql = "UPDATE urna SET aberta = 0, data_fechamento = %s WHERE id = 1"

        cursor.execute(sql, (datetime.now(),))
        conexao.commit()

        limpa_javotou()

        return True
    except Exception as e:
        return False