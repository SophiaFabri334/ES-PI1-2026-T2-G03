import numpy as np

# Cifra de Hill - Implementação em Python 
#numpy é uma biblioteca poderosa para manipulação de matrizes, 
# o que é necessário para a Cifra de Hill, 
# que se baseia em operações matriciais para 
# encriptar e decriptar mensagens.

def is_invertible(matrix):
    # Matri"X" e não matri"Z" porque está em inglês, 
    # e é mais comum usar "matri"x" para se referir a 
    # matrizes em geral.

    """Verifica se a matriz é válida para a Cifra de Hill."""
    if matrix.shape[0] != matrix.shape[1]:
        return False
    
    det = int(np.round(np.linalg.det(matrix))) 
    # Arredonda para evitar erros
    
    # Para ser funcional na decriptação: det != 0 
    # Não pode ser divisível por 2 ou 13 (2x13=26)

    return det != 0 and det % 2 != 0 and det % 13 != 0

def generate_safe_key(size):
    """Gera uma matriz aleatória que garantidamente funciona."""
    while True:
        key = np.random.randint(1, 10, (size, size))
        if is_invertible(key):
            return key

def encrypt(plaintext, key):
    """Encripta o texto usando a cifra de Hill."""
    plaintext = plaintext.upper().replace(" ", "")
     # Remove espaços

    numbers = [ord(char) - ord('A') for char in plaintext if char.isalpha()]
    
    while len(numbers) % key.shape[0] != 0:
        numbers.append(0) 
        # Adiciona 'A' como preenchimento
    
    ciphertext = []
    for i in range(0, len(numbers), key.shape[0]):
        block = np.array(numbers[i:i+key.shape[0]])
        encrypted_block = (np.dot(key, block) % 26).astype(int)
        ciphertext.extend(encrypted_block)
    
    return ''.join(chr(num + ord('A')) for num in ciphertext)







# --- EXEMPLO DE USO ---
#tamanho_da_chave = 2 # Matriz 2x2
#minha_chave = generate_safe_key(tamanho_da_chave)
#texto = "HELLO"
#texto_encriptado = encrypt(texto, minha_chave)
#print(f"Chave Gerada:\n{minha_chave}")
#print(f"Texto Original: {texto}")
#print(f"Texto Criptografado: {texto_encriptado}")
