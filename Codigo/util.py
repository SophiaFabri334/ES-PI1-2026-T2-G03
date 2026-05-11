from datetime import datetime
# from cryptography.fernet import Fernet
import random
import string

def salvar_log(texto):
    """Salva log com timestamp no formato [YYYY-MM-DD HH:MM:SS]"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open("historico.txt", "a", encoding="utf-8") as arq:
        arq.write(f"{timestamp} {texto}\n")

def validar_cpf(cpf):
    """Valida CPF matematicamente. Retorna True se válido."""
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
    """Gera uma chave: 2 primeiras letras do primeiro nome + 1 letra do segundo nome + 4 dígitos aleatórios."""

    partes = nome.strip().split()
    primeiro_nome = partes[0]
    segundo_nome = partes[1]

    parte1 = primeiro_nome[:2].lower()
    parte2 = segundo_nome[0].lower()

    numeros = ''.join(random.choices(string.digits, k=4))

    return parte1 + parte2 + numeros


def gerar_protocolo(numero_candidato):
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    ano = datetime.now().strftime("%y")
    numero_candidato = str(numero_candidato).zfill(2)
    numeros_aleatorios = ''.join(random.choices(string.digits, k=5))
    protocolo = f"V{letras}{ano}{numero_candidato}{numeros_aleatorios}"
    return protocolo