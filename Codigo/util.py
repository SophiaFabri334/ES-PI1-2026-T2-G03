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
    # Verifica se tem 12 digitos
    if not titulo.isdigit() or len(titulo) != 12:
        return False

    nums = list(map(int, titulo))

    # Verifica o primeiro dígito verificador
    soma = sum(nums[i] * (i + 2) for i in range(8))
    dv1 = soma % 11
    if dv1 == 10:
        dv1 = 0

    # Verifica o segundo dígito verificador
    soma = sum(nums[i] * (i + 7) for i in range(8)) + dv1 * 9
    dv2 = soma % 11
    if dv2 == 10:
        dv2 = 0

    return dv1 == nums[10] and dv2 == nums[11]

def gerar_chave_acesso():
    """Gera uma chave de acesso única de 8 caracteres alfanuméricos."""
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))

# # Em um projeto real, essa chave não ficaria aqui, mas para o T2, 
# # você pode gerar uma e colar aqui como string.
# CHAVE = Fernet.generate_key() 
# cipher = Fernet(CHAVE)
 
# def criptografar(texto):
#     return cipher.encrypt(texto.encode()).decode()

# def descriptografar(texto_cifrado):
#     return cipher.decrypt(texto_cifrado.encode()).decode()