import numpy as np
import re
#expressões regulares em inglês 

# Matriz 2x2 fixa para garantir que o sistema sempre gere a mesma chave para o mesmo título
CHAVE_MESTRA = np.array([[3, 3], [2, 5]])

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', str(cpf))
    return len(cpf) == 11

def criptografar(texto):
    """Lógica da Cifra de Hill: Título -> Letras Criptografadas"""
    texto_limpo = re.sub(r'\D', '', str(texto))
    
    if len(texto_limpo) % 2 != 0:
        texto_limpo += "0"
    
    # Converte números para letras
    texto_limpo = "".join([chr(int(n) + ord('A')) for n in texto_limpo])
    
    # encriptação 
    numeros = [ord(char) - ord('A') for char in texto_limpo]
    resultado = ""
    for i in range(0, len(numeros), 2):
        bloco = np.array(numeros[i:i+2])
        encriptado = np.dot(CHAVE_MESTRA, bloco) % 26
        resultado += "".join(chr(int(num) + ord('A')) for num in encriptado)
    return resultado