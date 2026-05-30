import numpy as np
import re
#expressões regulares em inglês 
#----------------------------------------------------------------------------------------------
#                                     (RNF 005) 
#----------------------------------------------------------------------------------------------
# Matriz 2x2 fixa para garantir que o sistema sempre gere a MESMA chave para o MESMO título
CHAVE_MESTRA = np.array([[3, 3], [2, 5]])

# def validar_cpf(cpf):
#     cpf = re.sub(r'\D', '', str(cpf))
#     return len(cpf) == 11
#     # Valida e ve se o cpf existe e tem o num certo (ex: se tiver 9, vai dar erro)

def criptografar(texto):
    """Lógica da Cifra de Hill: Título -> Letras Criptografadas
        Args:
        texto (str): texto a ser encriptografado
    
        Returns:
            texto já criptografado
    """
    texto_limpo = re.sub(r'\D', '', str(texto))
    
    if len(texto_limpo) % 2 != 0:
        texto_limpo += "0"
    
    # Converte os números para as letras
    texto_limpo = "".join([chr(int(n) + ord('A')) for n in texto_limpo])
    
    # encriptação 
    numeros = [ord(char) - ord('A') for char in texto_limpo]
    resultado = ""
    for i in range(0, len(numeros), 2):
        bloco = np.array(numeros[i:i+2])
        encriptado = np.dot(CHAVE_MESTRA, bloco) % 26
        resultado += "".join(chr(int(num) + ord('A')) for num in encriptado)
    return resultado

# Descriptografia 
def descriptografar(texto_criptografado):
    """
    Lógica inversa da Cifra de Hill
    Args:
        texto (str): Texto já criptografado
    
    Returns:
        Texto descriptografado
    """
  
    det = int(np.round(np.linalg.det(CHAVE_MESTRA))) % 26
    if len(texto_criptografado) % 2 != 0:
        texto_criptografado += "A"
    # Inverso multiplicativo do determinante módulo 26
    det_inv = pow(det, -1, 26)
    
    # Matriz invertida (a,b,c,d = d,c,b,a)
    adj = np.array([
        [CHAVE_MESTRA[1, 1], -CHAVE_MESTRA[0, 1]],
        [-CHAVE_MESTRA[1, 0], CHAVE_MESTRA[0, 0]]
    ])
    chave_inversa = (det_inv * adj) % 26
    
    # Converter as letras de volta para números base (0 a 25)
    numeros = [ord(char) - ord('A') for char in texto_criptografado]
    resultado = ""
    
    # Descriptografia em blocos de 2
    for i in range(0, len(numeros), 2):
        bloco = np.array(numeros[i:i+2])
        
        # Multiplica o bloco pela matriz inversa e aplica o módulo
        descriptografado = np.dot(chave_inversa, bloco) % 26
        
        # Junta os números recuperados (convertendo os inteiros de volta para string)
        resultado += "".join(str(int(num)) for num in descriptografado)
        
    # remove o 0 que adiciona no final da descriptografia
    if resultado.endswith("0"):
        resultado = resultado[:-1]
    return resultado
