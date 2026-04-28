# from cryptography.fernet import Fernet
# def gerar_chave():
#     chave = Fernet.generate_key()
#     with open("chave.key", "wb") as chave_arquivo:
#         chave_arquivo.write(chave)
# def carregar_chave():
#     with open("chave.key", "rb") as chave_arquivo:
#         chave = chave_arquivo.read()
#     return chave    
# def criptografar_mensagem(mensagem):
#     chave = carregar_chave()
#     f = Fernet(chave)
#     mensagem_criptografada = f.encrypt(mensagem.encode())
#     return mensagem_criptografada