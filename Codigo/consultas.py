import mysql.connector
from datetime import datetime
import util as util
import seguranca as seguranca 
"""
Módulo de conexão e consultas com banco de dados MySQL
Responsável por todas as operações CRUD e autenticação
"""

conexao = mysql.connector.connect(
    host =  "localhost",
    user = "root",
    password = "puc1234",
    database = "sistema_eleicao"
)

cursor = conexao.cursor()

def confirmar_limpar():
    conexao.commit()
    print("\n" * 100) 

def inserir_candidatos(numero, nome, partido):
    """
    Insere um novo candidato no banco de dados conforme RF001.09.
    
    Args:
        numero (int): Número único de votação do candidato
        nome (str): Nome completo do candidato
        partido (str): Sigla ou nome do partido
    
    Returns:
        int: ID do candidato inserido ou None em caso de erro
    """
    try:
        sql = "INSERT INTO candidatos (numero, nome_candidato, partido) VALUES (%s, %s, %s)"
        valores = (numero, nome, partido)
        cursor.execute(sql, valores)
        conexao.commit()
        id_candidato = cursor.lastrowid
        print("Candidato cadastrado com ID: ", id_candidato)
        return id_candidato
    except Exception as e:
        print(f"Erro ao cadastrar candidato: {str(e)}")
        return None

def verificar_numero_candidato_existe(numero):
    """
    Verifica se o número do candidato já existe no banco de dados conforme RF001.10.
    
    Args:
        numero (int): Número de votação a ser verificado
    
    Returns:
        bool: True se número já existe, False caso contrário
    """
    try:
        cursor.execute("SELECT 1 FROM candidatos WHERE numero = %s LIMIT 1", (numero,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar número do candidato: {str(e)}")
        return False

def buscar_candidato_por_numero(numero):
    """
    Busca um candidato pelo número conforme RF001.13.
    
    Args:
        numero (int): Número de votação do candidato
    
    Returns:
        tuple: Tupla com dados do candidato ou None se não encontrado
    """
    try:
        cursor.execute(
            "SELECT id_candidato, numero, nome_candidato, partido FROM candidatos WHERE numero = %s",
            (numero,)
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar candidato: {str(e)}")
        return None

def buscar_candidatos_todos():
    """
    Busca todos os candidatos cadastrados conforme RF001.14.
    
    Args:
        None
    
    Returns:
        list: Lista de tuplas com dados de todos os candidatos
    """
    try:
        cursor.execute("SELECT id_candidato, numero, nome_candidato, partido FROM candidatos ORDER BY nome_candidato")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar candidatos: {str(e)}")
        return []

def atualizar_candidato(numero_antigo, numero_novo, nome, partido):
    """
    Atualiza informações de um candidato conforme RF001.11.
    Permite editar número (com validação de unicidade), nome e partido.
    
    Args:
        numero_antigo (int): Número anterior do candidato
        numero_novo (int): Novo número de votação
        nome (str): Novo nome do candidato
        partido (str): Novo partido do candidato
    
    Returns:
        bool: True se atualização foi bem-sucedida, False caso contrário
    """
    try:
        sql = "UPDATE candidatos SET numero = %s, nome_candidato = %s, partido = %s WHERE numero = %s"
        cursor.execute(sql, (numero_novo, nome, partido, numero_antigo))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar candidato: {str(e)}")
        return False

def remover_candidato(numero):
    """
    Remove um candidato do banco de dados conforme RF001.12.
    
    Args:
        numero (int): Número de votação do candidato a remover
    
    Returns:
        bool: True se remoção foi bem-sucedida, False caso contrário
    """
    try:
        cursor.execute("DELETE FROM candidatos WHERE numero = %s", (numero,))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao remover candidato: {str(e)}")
        return False


def inserir_eleitores(titulo_eleitor, cpf, nome, senha, ja_votou, mesario):
    """
    Insere um novo eleitor no banco de dados conforme RF001.01.
    
    Args:
        titulo_eleitor (str): Título de eleitor validado (12 dígitos)
        cpf (str): CPF validado (11 dígitos)
        nome (str): Nome completo do eleitor
        senha (str): Chave de acesso gerada
        ja_votou (int): Status de votação (None ou 1)
        mesario (int): Indica se é mesário (0 ou 1)
    
    Returns:
        None
    """
    sql = "INSERT INTO eleitores (titulo_eleitor, cpf, nome_completo, senha, ja_votou, mesario) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (titulo_eleitor, cpf, nome, senha, ja_votou, mesario)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Eleitor cadastrado com ID: ", cursor.lastrowid)
    
def inserir_voto(id_candidato, numero_candidato, titulo, cpf, chave):
    """
    Insere um voto no banco de dados conforme RF002.01.06.07.
    Gera protocolo único e criptografado (RNF005).
    
    Args:
        id_candidato (int): ID do candidato votado
        numero_candidato (int): Número do candidato
        titulo (str): Título do eleitor (para rastreabilidade)
        cpf (str): Primeiros 4 dígitos do CPF (para rastreabilidade)
        chave (str): Chave de acesso do eleitor
    
    Returns:
        str: Protocolo de votação gerado ou None em caso de erro
    """
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
def busca_eleitores():
    """
    Busca e retorna todos os eleitores cadastrados conforme RF001.08.
    
    Args:
        None
    
    Returns:
        list: Lista de tuplas com dados de todos os eleitores
    """
    sql = "SELECT E.id_eleitor, E.titulo_eleitor, E.cpf, E.nome_completo, E.ja_votou, E.mesario FROM ELEITORES E ORDER BY E.id_eleitor"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

def filtra_eleitores(pesquisa):
    """
    Busca eleitores por título, nome ou CPF conforme RF001.07.
    
    Args:
        pesquisa (str): Termo de busca (título, nome ou CPF)
    
    Returns:
        list: Lista de tuplas com eleitores encontrados
    """
    sql = "SELECT E.id_eleitor, E.titulo_eleitor, E.cpf, E.nome_completo, E.ja_votou, E.mesario FROM ELEITORES E WHERE E.titulo_eleitor LIKE %s OR E.nome_completo LIKE %s OR E.cpf LIKE %s ORDER BY E.id_eleitor"
    
    valor = f"%{pesquisa}%"
    valores = (seguranca.criptografar(valor), valor, seguranca.criptografar(valor))

    cursor.execute(sql, valores)
    resultado = cursor.fetchall()
    
    return resultado

def remover_eleitor(cpf):
    """
    Remove um eleitor do banco de dados conforme RF001.06.
    
    Args:
        cpf (str): CPF do eleitor a remover
    
    Returns:
        None
    """
    cursor.execute("DELETE FROM eleitores WHERE cpf = %s", (seguranca.criptografar(cpf),))
    conexao.commit()

def verificar_cpf_existe(cpf):
    """
    Verifica se o CPF já existe no banco de dados conforme RF001.03.
    
    Args:
        cpf (str): CPF a ser verificado (apenas números)
    
    Returns:
        bool: True se CPF já existe, False caso contrário
    """
    try:
        cursor.execute("SELECT 1 FROM eleitores WHERE cpf = %s LIMIT 1", (seguranca.criptografar(cpf),))
        return cursor.fetchone() is not None

    except Exception as e:
        print("Erro ao verificar CPF:", e)
        return False
    
def verificar_titulo_existe(titulo):
    """
    Verifica se o título de eleitor já existe no banco de dados conforme RF001.03.
    
    Args:
        titulo (str): Título de eleitor a ser verificado
    
    Returns:
        bool: True se título já existe, False caso contrário
    """
    try:
        cursor.execute("SELECT 1 FROM eleitores WHERE titulo_eleitor = %s LIMIT 1", (titulo,))
        return cursor.fetchone() is not None

    except Exception as e:
        print("Erro ao verificar titulo de eleitor:", e)
        return False
    
def verifica_eleitor(titulo, cpf_4, chave, tipo):
    """
    Verifica se eleitor/mesário existe e tem credenciais válidas conforme RF002.01.01 e RF002.01.06.01.
    
    Args:
        titulo (str): Título de eleitor
        cpf_4 (str): Primeiros 4 dígitos do CPF
        chave (str): Chave de acesso do eleitor
        tipo (int): 0 para eleitor comum, 1 para mesário
    
    Returns:
        bool: True se credenciais são válidas, False caso contrário
    """
    try:
        sql = "SELECT nome_completo, mesario FROM eleitores WHERE titulo_eleitor=%s AND LEFT(cpf,4)=%s AND senha=%s "
        if tipo == 1:
            sql += " AND COALESCE(mesario,0) = 1"
        cursor.execute(sql, (titulo, seguranca.criptografar(cpf_4), seguranca.criptografar(chave)))
        return cursor.fetchone() is not None
    except Exception as e:
        print("Erro ao verificar se o mesario existe no banco:", e)
        return False

def verifica_javotou(titulo, cpf_4, chave):
    """
    Verifica se eleitor já votou conforme RF002.01.06.02.
    
    Args:
        titulo (str): Título de eleitor
        cpf_4 (str): Primeiros 4 dígitos do CPF
        chave (str): Chave de acesso do eleitor
    
    Returns:
        bool: True se eleitor já votou, False caso contrário
    """
    try:
        sql = "SELECT ja_votou FROM eleitores WHERE titulo_eleitor=%s AND LEFT(cpf,4)=%s AND senha=%s"
        cursor.execute(sql, (titulo, seguranca.criptografar(cpf_4), seguranca.criptografar(chave)))
        resultado = cursor.fetchone()

        if resultado is None:
            return False

        ja_votou = resultado[0]

        if ja_votou is None:
            return False

        return bool(ja_votou)
    except Exception as e:
        print("Erro ao verificar se o mesario existe no banco:", e)
        return False
    
def limpa_votos():
    """
    Executa a Zerézima conforme RF002.01.04-05.
    Limpa todos os votos anteriores e exibe lista de candidatos com zero votos.
    
    Args:
        None
    
    Returns:
        None
    """
    print("Iniciando zerézima")
    cursor.execute("DELETE FROM votos") 
    conexao.commit() 
    print("Todos os votos anteriores foram apagados ")
    lista_candidatos()

    
def lista_candidatos():
    """
    Lista todos os candidatos com suas contagens de votos atuais.
    Utilizado na Zerézima para garantir que todos têm zero votos.
    
    Args:
        None
    
    Returns:
        None
    """
    print("Todos os candidatos estão com 0 votos:")
    cursor.execute("select count(v.id_voto) votos, c.id_candidato, c.numero, c.nome_candidato, c.partido from candidatos c left join votos v on v.id_candidato = c.id_candidato group by c.id_candidato, c.numero, c.nome_candidato, c.partido")
    
    for c in cursor:
        print(f"Candidato: {c[3]} | Número: {c[2]} | Votos: {c[0]}")

    print("\nZerézima concluída.")

def retorna_candidato(numero):
    """
    Busca um candidato pelo número conforme RF002.01.06.05.
    
    Args:
        numero (int/str): Número do candidato
    
    Returns:
        tuple: Tupla com dados do candidato ou None se não encontrado
    """
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
    Atualiza o status do eleitor para "Já votou" conforme RF002.01.06.08.
    
    Args:
        titulo (str): Título de eleitor
        cpf_4 (str): Primeiros 4 dígitos do CPF
        chave (str): Chave de acesso do eleitor
    
    Returns:
        bool: True se atualização foi bem-sucedida, False caso contrário
    """
    try:
        sql = "UPDATE eleitores SET ja_votou = 1 WHERE titulo_eleitor=%s AND left(cpf,4)=%s AND senha=%s"
        cursor.execute(sql, (titulo, seguranca.criptografar(cpf_4), seguranca.criptografar(chave)))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao atualizar eleitor:", e)
        return False
    
def limpa_javotou():
    """
    Limpa o status "Já votou" de todos os eleitores após encerramento da votação.
    
    Args:
        None
    
    Returns:
        bool: True se limpeza foi bem-sucedida, False caso contrário
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
    """
    Verifica se a urna está aberta conforme RF002.01.
    
    Args:
        None
    
    Returns:
        bool: True se urna está aberta, False caso contrário
    """
    cursor.execute("SELECT aberta FROM urna WHERE id = 1")
    resultado = cursor.fetchone()

    if resultado is None:
        return False

    return resultado[0] == 1

def abrir_urna():
    """
    Abre a urna e registra data/hora de abertura conforme RF002.01.01.
    
    Args:
        None
    
    Returns:
        None
    """
    sql = "UPDATE urna SET aberta = 1, data_abertura = %s, data_fechamento = NULL WHERE id = 1"
    cursor.execute(sql, (datetime.now(),))
    conexao.commit()

def fechar_urna():
    """
    Fecha a urna e registra data/hora de fechamento conforme RF002.01.07.06.
    
    Args:
        None
    
    Returns:
        bool: True se fechamento foi bem-sucedido, False caso contrário
    """
    try:
        sql = "UPDATE urna SET aberta = 0, data_fechamento = %s WHERE id = 1"
        cursor.execute(sql, (datetime.now(),))
        conexao.commit()
        limpa_javotou()
        return True
    except Exception as e:
        return False

def listar_protocolos_votacao():
    """
    Retorna lista de todos os protocolos de votação gerados conforme RF002.02.02.
    Ordena em ordem alfabética para auditoria.
    
    Args:
        None
    
    Returns:
        list: Lista de protocolos em ordem alfabética, ou lista vazia se nenhum
    """
    try:
        sql = "SELECT protocolo FROM votos ORDER BY protocolo ASC"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        
        if not resultado:
            return []
        
        protocolos = [protocolo[0] for protocolo in resultado]
        return protocolos
    
    except Exception as e:
        print(f"Erro ao listar protocolos: {str(e)}")
        return []

def obter_resultados_por_candidato():
    """
    Retorna contagem de votos por candidato para Boletim de Urna.
    
    Args:
        None
    
    Returns:
        list: Lista de tuplas (id, número, nome, partido, votos)
    """
    try:
        # Query SQL que faz LEFT JOIN entre candidatos e votos
        # Agrupa por candidato e conta o número de votos para cada um
        # Ordena em ordem alfabética pelo nome do candidato
        sql = """
        SELECT 
            c.id_candidato, 
            c.numero, 
            c.nome_candidato, 
            c.partido,
            COUNT(v.id_voto) as votos
        FROM candidatos c
        LEFT JOIN votos v ON v.id_candidato = c.id_candidato
        GROUP BY c.id_candidato, c.numero, c.nome_candidato, c.partido
        ORDER BY c.nome_candidato ASC
        """
        # Executa a query
        cursor.execute(sql)
        # Retorna todas as linhas do resultado
        return cursor.fetchall()
    except Exception as e:
        # Se ocorrer erro na consulta, exibe mensagem e retorna lista vazia
        print(f"Erro ao obter resultados: {str(e)}")
        return []

def obter_vencedor():
    """
    Retorna candidato com maior número de votos (vencedor).
    
    Args:
        None
    
    Returns:
        tuple: Tupla (número, nome, partido, votos) do vencedor ou None
    """
    try:
        # Query SQL que seleciona o candidato com mais votos
        # Agrupa por candidato e conta votos
        # Ordena por votos (descendente) e limita a 1 resultado (o vencedor)
        sql = """
        SELECT 
            c.numero, 
            c.nome_candidato, 
            c.partido,
            COUNT(v.id_voto) as votos
        FROM candidatos c
        LEFT JOIN votos v ON v.id_candidato = c.id_candidato
        GROUP BY c.id_candidato, c.numero, c.nome_candidato, c.partido
        ORDER BY votos DESC
        LIMIT 1
        """
        # Executa a query
        cursor.execute(sql)
        # Retorna apenas a primeira linha (o vencedor)
        return cursor.fetchone()
    except Exception as e:
        # Se ocorrer erro na consulta, exibe mensagem e retorna None
        print(f"Erro ao obter vencedor: {str(e)}")
        return None

def obter_estatistica_comparecimento():
    """
    Retorna estatísticas de eleitores que votaram vs total de eleitores.
    
    Args:
        None
    
    Returns:
        dict: Dicionário com total_eleitores, eleitores_votaram, nao_votaram, percentual
    """
    try:
        # Query 1: Conta total de eleitores (excluindo mesários que é mesario = 0)
        sql_total = "SELECT COUNT(*) FROM eleitores WHERE mesario = 0"
        
        # Query 2: Conta quantos eleitores já votaram (ja_votou = 1)
        sql_votaram = "SELECT COUNT(*) FROM eleitores WHERE mesario = 0 AND ja_votou = 1"
        
        # Executa primeira query e obtém o total de eleitores
        cursor.execute(sql_total)
        total = cursor.fetchone()[0]
        
        # Executa segunda query e obtém quantos votaram
        cursor.execute(sql_votaram)
        votaram = cursor.fetchone()[0]
        
        # Calcula quantos NÃO votaram (total - votaram)
        nao_votaram = total - votaram
        
        # Calcula o percentual de comparecimento (se há eleitores)
        percentual = (votaram / total * 100) if total > 0 else 0
        
        # Retorna um dicionário com todos os dados calculados
        return {
            'total_eleitores': total,
            'eleitores_votaram': votaram,
            'nao_votaram': nao_votaram,
            'percentual': percentual
        }
    except Exception as e:
        # Se ocorrer erro na consulta, exibe mensagem e retorna dicionário vazio
        print(f"Erro ao obter estatística: {str(e)}")
        return {}

def obter_votos_por_partido():
    """
    Retorna contagem de votos agrupados por partido.
    
    Args:
        None
    
    Returns:
        list: Lista de tuplas (partido, votos)
    """
    try:
        # Query SQL que agrupa votos por partido
        # Conta quantos votos cada partido recebeu através de seus candidatos
        # Ordena por quantidade de votos (descendente)
        sql = """
        SELECT 
            c.partido,
            COUNT(v.id_voto) as votos
        FROM candidatos c
        LEFT JOIN votos v ON v.id_candidato = c.id_candidato
        GROUP BY c.partido
        ORDER BY votos DESC
        """
        # Executa a query
        cursor.execute(sql)
        # Retorna todas as linhas do resultado (cada partida com seus votos)
        return cursor.fetchall()
    except Exception as e:
        # Se ocorrer erro na consulta, exibe mensagem e retorna lista vazia
        print(f"Erro ao obter votos por partido: {str(e)}")
        return []

