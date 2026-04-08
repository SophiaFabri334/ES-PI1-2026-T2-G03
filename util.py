from datetime import datetime
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

def gerar_chave_acesso():
    """Gera uma chave de acesso única de 8 caracteres alfanuméricos."""
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))
