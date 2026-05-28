from datetime import datetime
# from cryptography.fernet import Fernet
import random
import string
import os # Limpa a tela do terminal

def limpar_tela():
    if os.name == 'nt':
        os.system('cls') # limpar tela do windows
    else:
        os.system('clear && printf "\e[3J"')
        os.system('clear') # limpar tela do mac/linux

 
def salvar_log(texto):
    """
    Salva log com timestamp no formato [YYYY-MM-DD HH:MM:SS] conforme RF002.02.01.02
    
    Args:
        texto (str): Descrição da ocorrência a ser registrada
    
    Returns:
        None
    """
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open("historico.txt", "a", encoding="utf-8") as arq:
        arq.write(f"{timestamp} {texto}\n")

def limpar_log():
    """
    Limpa log ao fechar o sistema de votação
    Returns:
        None
    """

    with open("historico.txt", "w", encoding="utf-8") as arq:
        pass

def validar_cpf(cpf):
    """
    Valida CPF matematicamente conforme Anexo B do documento.
    Rejeita CPFs com todos os dígitos iguais.
    
    Args:
        cpf (str): CPF com apenas números (11 dígitos)
    
    Returns:
        bool: True se CPF é válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verifica o primeiro dígito
    if int(cpf[9]) != digito1:
        return False
    
    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica o segundo dígito
    if int(cpf[10]) != digito2:
        return False
    
    return True

def validar_titulo(titulo):
    """
    Valida Título de Eleitor matematicamente conforme Anexo A do documento.
    Valida 12 dígitos: 8 sequenciais + 2 de UF + 2 verificadores.
    
    Args:
        titulo (str): Título de eleitor com apenas números (12 dígitos)
    
    Returns:
        bool: True se título é válido, False caso contrário
    """
    titulo = ''.join(filter(str.isdigit, str(titulo)))

    if len(titulo) != 12:
        return False

    sequencial = titulo[:8]
    uf = titulo[8:10]
    dv_informado = titulo[10:]

    pesos1 = [2, 3, 4, 5, 6, 7, 8, 9]

    soma1 = 0
    for i in range(8):
        soma1 += int(sequencial[i]) * pesos1[i]

    resto1 = soma1 % 11

    if resto1 == 10:
        dv1 = 0
    else:
        dv1 = resto1
    if uf in ["01", "02"] and dv1 == 0:
        dv1 = 1

    soma2 = (
        int(uf[0]) * 7 +
        int(uf[1]) * 8 +
        dv1 * 9
    )

    resto2 = soma2 % 11

    if resto2 == 10:
        dv2 = 0
    else:
        dv2 = resto2

    if uf in ["01", "02"] and dv2 == 0:
        dv2 = 1

    dv_calculado = f"{dv1}{dv2}"

    return dv_calculado == dv_informado


def gerar_chave_acesso(nome):
    """
    Gera chave de acesso única para o eleitor conforme especificação.
    Formato: 2 primeiras letras do primeiro nome + 1ª letra do segundo nome + 4 dígitos aleatórios
    Exemplo: André Silva → ANS4821
    
    Args:
        nome (str): Nome completo do eleitor
    
    Returns:
        str: Chave de acesso gerada (antes da criptografia)
    """
    partes = nome.strip().split()
    primeiro_nome = partes[0]
    segundo_nome = partes[1]

    parte1 = primeiro_nome[:2].lower()
    parte2 = segundo_nome[0].lower()

    numeros = ''.join(random.choices(string.digits, k=4))

    return parte1 + parte2 + numeros


def exibir_logs():
    """
    Exibe o conteúdo do arquivo de logs conforme RF002.02.01.08
    Lê e exibe todas as ocorrências registradas no arquivo historico.txt
    
    Args:
        None
    
    Returns:
        None
    """
    try:
        with open("historico.txt", "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            if conteudo:
                print("\n" + "="*60)
                print("LOGS DE OCORRÊNCIAS DO SISTEMA")
                print("="*60)
                print(conteudo)
                print("="*60 + "\n")
            else:
                print("\nNenhum log registrado ainda.\n")
    except FileNotFoundError:
        print("\nArquivo de logs não encontrado.\n")
    except Exception as e:
        print(f"\nErro ao exibir logs: {str(e)}\n")


def registrar_log_abertura():
    """
    Registra log de abertura da votação conforme RF002.02.01.03
    Mensagem: "ABERTURA: Votação iniciada com sucesso. Total de votos zerado."
    
    Args:
        None
    
    Returns:
        None
    """
    mensagem = "ABERTURA: Votação iniciada com sucesso. Total de votos zerado."
    salvar_log(mensagem)


def registrar_log_tentativa_acesso_negado(motivo=""):
    """
    Registra tentativa de acesso negado conforme RF002.02.01.04
    Mensagem: "ALERTA: Tentativa de acesso negado"
    
    Args:
        motivo (str, optional): Motivo do acesso negado (validação mesário ou eleitor)
    
    Returns:
        None
    """
    mensagem = f"ALERTA: Tentativa de acesso negado{' - ' + motivo if motivo else ''}"
    salvar_log(mensagem)


def registrar_log_voto_duplo():
    """
    Registra tentativa de voto duplo conforme RF002.02.01.05
    Mensagem: "ALERTA: Tentativa de voto duplo"
    
    Args:
        None
    
    Returns:
        None
    """
    mensagem = "ALERTA: Tentativa de voto duplo"
    salvar_log(mensagem)


def registrar_log_voto_sucesso():
    """
    Registra sucesso de votação conforme RF002.02.01.06
    Mensagem: "SUCESSO: Voto realizado com sucesso"
    
    Args:
        None
    
    Returns:
        None
    """
    mensagem = "SUCESSO: Voto realizado com sucesso"
    salvar_log(mensagem)


def registrar_log_encerramento():
    """
    Registra encerramento da votação conforme RF002.02.01.07
    Mensagem: "ENCERRAMENTO: Votação finalizada com sucesso."
    
    Args:
        None
    
    Returns:
        None
    """
    mensagem = "ENCERRAMENTO: Votação finalizada com sucesso."
    salvar_log(mensagem)


def gerar_protocolo(numero_candidato):
    """
    Gera protocolo de votação no formato: V + 2 letras + ano + número candidato (2 dígitos) + 5 dígitos aleatórios
    Exemplo: VRT269950134
    
    Args:
        numero_candidato (int/str): Número do candidato votado
    
    Returns:
        str: Protocolo gerado (antes da criptografia)
    """
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    ano = datetime.now().strftime("%y")
    numero_candidato = str(numero_candidato).zfill(2)
    numeros_aleatorios = ''.join(random.choices(string.digits, k=5))
    protocolo = f"V{letras}{ano}{numero_candidato}{numeros_aleatorios}"
    return protocolo


def exibir_protocolos_auditoria(protocolos):
    """
    Exibe protocolos de votação de forma formatada para auditoria conforme RF002.02.02.
    
    Args:
        protocolos (list): Lista de protocolos a exibir
    
    Returns:
        None
    """
    if not protocolos:
        print("\nNenhum protocolo registrado ainda.\n")
        return
    
    print("\n" + "="*60)
    print("PROTOCOLOS DE VOTAÇÃO - AUDITORIA")
    print("="*60)
    print(f"Total de protocolos: {len(protocolos)}\n")
    
    for i, protocolo in enumerate(protocolos, 1):
        print(f"{i:3d}. {protocolo}")
    
    print("\n" + "="*60)
    print("Protocolos em ordem alfabética para verificação")
    print("="*60 + "\n")

