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
    texto = re.sub(r'\D', '', str(texto))
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


# def exibir_menu():
#     while True:
#         print("\n" + "="*30)
#         print(" SISTEMA DE VOTAÇÃO HILL ")
#         print("="*30)
#         print("1. Cadastrar Novo Eleitor")
#         print("2. Simular Login de Eleitor")
#         print("0. Sair")
        
#         opcao = input("\nEscolha uma opção: ")

#         if opcao == '1':
#             nome = input("Nome do Eleitor: ")
#             cpf = input("CPF: ")
#             titulo = input("Título de Eleitor: ")

#             if validar_cpf(cpf):
#                 # Gerando a chave usando Numpy e Cifra de Hill
#                 chave = gerar_chave_acesso(titulo)
                
#                 print("\n" + "-"*30)
#                 print(f"CADASTRADO COM SUCESSO!")
#                 print(f"Eleitor: {nome}")
#                 print(f"Chave de Acesso Gerada: {chave}")
#                 print("-"*30)
#                 print("> Salve esta chave! Você precisará dela para votar.")
#             else:
#                 print("\n[ERRO] CPF inválido. Tente novamente.")

#         elif opcao == '2':
#             print("\n--- TESTE DE LOGIN ---")
#             tit_teste = input("Digite o Título: ")
#             chave_teste = input("Digite a Chave recebida (letras): ").upper()

#             # gera a chave de novo para comparar
#             if chave_teste == gerar_chave_acesso(tit_teste):
#                 print("\n[ACESSO LIBERADO] A Cifra de Hill validou sua identidade!")
#             else:
#                 print("\n[ACESSO NEGADO] Chave ou Título incorretos.")

#         elif opcao == '0':
#             print("Saindo do sistema...")
#             break
#         else:
#             print("Opção inválida.")

# if __name__ == "__main__":
#     exibir_menu()