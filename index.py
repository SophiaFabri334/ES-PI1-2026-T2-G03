# =============================================================================
# SISTEMA DE VOTACAO DIGITAL - LAD.Py
# Arquivo principal do sistema
# =============================================================================

import Codigo.consultas as consultas  # Modulo de conexao e queries do banco de dados
import Codigo.util as util       # Modulo de funcoes utilitarias (validacao, logs, etc.)

# =============================================================================
# FUNCOES AUXILIARES
# =============================================================================

def verificar_cpf_existe(cpf):
    """
    Verifica se o CPF ja existe no banco de dados.
    Busca nas tabelas 'usuarios' e 'mesarios' para evitar duplicidade.
    
    Parametros:
        cpf (str): CPF a ser verificado (apenas numeros)
    
    Retorna:
        bool: True se CPF ja existe, False caso contrario
    """
    try:
        # Busca na tabela de usuarios (eleitores comuns)
        consultas.cursor.execute("SELECT cpf FROM usuarios WHERE cpf = %s", (cpf,))
        if consultas.cursor.fetchone():
            return True
        
        # Busca na tabela de mesarios
        consultas.cursor.execute("SELECT cpf FROM mesarios WHERE cpf = %s", (cpf,))
        if consultas.cursor.fetchone():
            return True
        
        return False
    except:
        return False

# =============================================================================
# MENU PRINCIPAL
# Loop principal do sistema - executa ate o usuario escolher sair (opcao 3)
# =============================================================================

opcao = 0 
while opcao != 3: 
    print("----------------------------------")
    print("1 - Gerenciamento")
    print("2 - Votacao")
    print("3 - Sair")
    print("----------------------------------")
    
    # Tratamento de excecao para entrada invalida
    try:
        opcao = int(input("Selecione uma opcao: "))
    except:
        print("Digite um numero valido!")
        opcao = 0
    print("----------------------------------\n")

    # =================================================================
    # MODULO DE GERENCIAMENTO (RF001)
    # Controle administrativo de eleitores e candidatos
    # =================================================================
    if opcao == 1:
        print("Opcao de gerenciamento selecionado\n")
        util.salvar_log("Opcao de gerenciamento selecionado")

        opcaoGerenciamento = -1
        while opcaoGerenciamento != 0:
            print("-----------GERENCIAMENTO-----------")
            print("1 - Cadastrar Eleitor")
            print("2 - Editar Eleitor")
            print("3 - Remover Eleitor")
            print("4 - Buscar Eleitor")
            print("5 - Listar Eleitores")
            print("6 - Gerenciar Candidatos")
            print("0 - Voltar ao menu principal")
            print("----------------------------------")
            
            try:
                opcaoGerenciamento = int(input("Selecione uma opcao: "))
            except:
                print("Digite um numero valido!")
                opcaoGerenciamento = -1
            print("----------------------------------\n")

            # ---------------------------------------------------------
            # CADASTRAR ELEITOR (RF001.01 a RF001.04)
            # Solicita dados, valida CPF, verifica duplicidade,
            # gera chave de acesso e salva no banco
            # ---------------------------------------------------------
            if opcaoGerenciamento == 1:
                print("=== CADASTRO DE ELEITOR ===\n")
                util.salvar_log("GERENCIAMENTO - Cadastrar Eleitor")
                
                # RF001.01 - Solicitar nome completo
                nome = input("Digite o nome completo: ").strip()
                if not nome:
                    print("\nErro: Nome nao pode estar vazio!\n")
                    continue
                
                # RF001.01 - Solicitar CPF
                cpf = input("Digite o CPF (apenas numeros): ").strip()
                cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres nao numericos
                
                # RF001.02 - Validar CPF matematicamente
                if not util.validar_cpf(cpf):
                    print("\nErro: CPF invalido! Verifique os digitos.\n")
                    util.salvar_log("ERRO - CPF invalido informado")
                    continue
                
                # RF001.03 - Verificar duplicidade de CPF
                if verificar_cpf_existe(cpf):
                    print("\nErro: CPF ja cadastrado no sistema!\n")
                    util.salvar_log("ERRO - Tentativa de cadastro com CPF duplicado")
                    continue
                
                # RF001.01 - Perguntar se e mesario
                is_mesario_input = input("O eleitor e mesario? (S/N): ").strip().upper()
                is_mesario = is_mesario_input == 'S'
                
                # RF001.04 - Gerar chave de acesso exclusiva
                chave_acesso = util.gerar_chave_acesso()
                
                # Inserir no banco de dados
                try:
                    if is_mesario:
                        # Cadastra na tabela de mesarios
                        consultas.inserir_mesarios(cpf, nome, chave_acesso)
                        util.salvar_log("SUCESSO - Mesario cadastrado: " + nome)
                    else:
                        # Cadastra na tabela de usuarios (eleitores)
                        consultas.inserir_usuarios(cpf, nome, chave_acesso, None, False)
                        util.salvar_log("SUCESSO - Eleitor cadastrado: " + nome)
                    
                    # Exibir confirmacao e chave de acesso
                    print("\n" + "="*40)
                    print("CADASTRO REALIZADO COM SUCESSO!")
                    print("="*40)
                    print("Nome: " + nome)
                    print("CPF: " + cpf)
                    print("Tipo: " + ("Mesario" if is_mesario else "Eleitor"))
                    print("\nCHAVE DE ACESSO: " + chave_acesso)
                    print("\nATENCAO: Guarde esta chave!")
                    print("Ela sera necessaria para votar.")
                    print("="*40 + "\n")
                    
                except Exception as e:
                    print("\nErro ao cadastrar: " + str(e) + "\n")
                    util.salvar_log("ERRO - Falha ao cadastrar eleitor: " + str(e))
            
            # ---------------------------------------------------------
            # EDITAR ELEITOR (RF001.05)
            # Busca por CPF, exibe dados atuais e permite alteracao
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 2:
                print("=== EDITAR ELEITOR ===\n")
                util.salvar_log("GERENCIAMENTO - Editar Eleitor")
                
                # Solicitar CPF para busca
                cpf_busca = input("Digite o CPF do eleitor a editar: ").strip()
                cpf_busca = ''.join(filter(str.isdigit, cpf_busca))
                
                # Validar formato do CPF
                if len(cpf_busca) != 11:
                    print("\nErro: CPF deve ter 11 digitos!\n")
                    continue
                
                # Variaveis para armazenar resultado da busca
                eleitor_encontrado = None
                tipo_eleitor = None
                
                try:
                    # Buscar na tabela de usuarios
                    consultas.cursor.execute(
                        "SELECT cpf, nome_completo, senha FROM usuarios WHERE cpf = %s", 
                        (cpf_busca,)
                    )
                    resultado = consultas.cursor.fetchone()
                    
                    if resultado:
                        eleitor_encontrado = resultado
                        tipo_eleitor = "usuario"
                    else:
                        # Se nao encontrou em usuarios, buscar em mesarios
                        consultas.cursor.execute(
                            "SELECT cpf, nome_completo, senha FROM mesarios WHERE cpf = %s", 
                            (cpf_busca,)
                        )
                        resultado = consultas.cursor.fetchone()
                        if resultado:
                            eleitor_encontrado = resultado
                            tipo_eleitor = "mesario"
                            
                except Exception as e:
                    print("\nErro ao buscar: " + str(e) + "\n")
                    continue
                
                # Verificar se eleitor foi encontrado
                if not eleitor_encontrado:
                    print("\nEleitor nao encontrado!\n")
                    util.salvar_log("ERRO - Eleitor nao encontrado para edicao: " + cpf_busca)
                    continue
                
                # Exibir dados atuais do eleitor
                print("\n" + "="*40)
                print("DADOS ATUAIS:")
                print("="*40)
                print("CPF: " + eleitor_encontrado[0])
                print("Nome: " + eleitor_encontrado[1])
                print("Tipo: " + ("Mesario" if tipo_eleitor == "mesario" else "Eleitor"))
                print("="*40)
                
                # Menu de opcoes de edicao
                print("\nO que deseja editar?")
                print("1 - Nome")
                print("0 - Cancelar")
                
                try:
                    opcao_edicao = int(input("Opcao: "))
                except:
                    print("\nOpcao invalida!\n")
                    continue
                
                if opcao_edicao == 0:
                    print("\nEdicao cancelada.\n")
                    continue
                elif opcao_edicao == 1:
                    # Editar nome
                    novo_nome = input("Digite o novo nome: ").strip()
                    if not novo_nome:
                        print("\nErro: Nome nao pode estar vazio!\n")
                        continue
                    
                    # Executar UPDATE no banco de dados
                    try:
                        if tipo_eleitor == "usuario":
                            consultas.cursor.execute(
                                "UPDATE usuarios SET nome_completo = %s, login = %s WHERE cpf = %s",
                                (novo_nome, novo_nome + cpf_busca, cpf_busca)
                            )
                        else:
                            consultas.cursor.execute(
                                "UPDATE mesarios SET nome_completo = %s, login = %s WHERE cpf = %s",
                                (novo_nome, novo_nome + cpf_busca, cpf_busca)
                            )
                        
                        # Confirmar transacao
                        consultas.conexao.commit()
                        
                        # Exibir confirmacao
                        print("\n" + "="*40)
                        print("ELEITOR ATUALIZADO COM SUCESSO!")
                        print("="*40)
                        print("Nome anterior: " + eleitor_encontrado[1])
                        print("Nome novo: " + novo_nome)
                        print("="*40 + "\n")
                        
                        util.salvar_log("SUCESSO - Eleitor editado: " + cpf_busca)
                        
                    except Exception as e:
                        print("\nErro ao atualizar: " + str(e) + "\n")
                        util.salvar_log("ERRO - Falha ao editar eleitor: " + str(e))
                else:
                    print("\nOpcao invalida!\n")
            
            # ---------------------------------------------------------
            # REMOVER ELEITOR (RF001.06) - A implementar
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 3:
                print("Entrou em Gerenciamento -> Remover Eleitor\n")
                util.salvar_log("GERENCIAMENTO - Remover Eleitor")
            
            # ---------------------------------------------------------
            # BUSCAR ELEITOR (RF001.07) - A implementar
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 4:
                print("Entrou em Gerenciamento -> Buscar Eleitor\n")
                util.salvar_log("GERENCIAMENTO - Buscar Eleitor")
            
            # ---------------------------------------------------------
            # LISTAR ELEITORES (RF001.08) - A implementar
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 5:
                print("Entrou em Gerenciamento -> Listar Eleitores\n")
                util.salvar_log("GERENCIAMENTO - Listar Eleitores")
            
            # ---------------------------------------------------------
            # GERENCIAR CANDIDATOS (RF001.09 a RF001.14) - Opcional
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 6:
                print("Entrou em Gerenciamento -> Gerenciar Candidatos\n")
                util.salvar_log("GERENCIAMENTO - Gerenciar Candidatos")
            
            # Voltar ao menu principal
            elif opcaoGerenciamento == 0:
                print("Voltando ao menu principal...\n")
                util.salvar_log("GERENCIAMENTO - Voltar ao menu principal")
            
            # Opcao invalida
            else:
                print("Gerenciamento -> Opcao invalida\n")
                util.salvar_log("Gerenciamento -> Opcao invalida")
    
    # =================================================================
    # MODULO DE VOTACAO (RF002)
    # Processamento do processo eleitoral
    # =================================================================
    elif opcao == 2:
        print("Opcao de votacao selecionado\n")
        util.salvar_log("Opcao de votacao selecionado")
        
        opcaoVotacao = -1
        while opcaoVotacao != 0:
            print("-----------VOTACAO-----------")
            print("1 - Abrir sistema de votacao")
            print("2 - Resultados")
            print("3 - Auditoria")
            print("0 - Sair")
            print("----------------------------------")
            
            try:
                opcaoVotacao = int(input("Selecione uma opcao: "))
            except:
                print("Digite um numero valido!")
                opcaoVotacao = -1
            print("----------------------------------\n")

            # ---------------------------------------------------------
            # ABRIR SISTEMA DE VOTACAO (RF002.01) - A implementar
            # ---------------------------------------------------------
            if opcaoVotacao == 1:
                print("Entrou em Votacao -> Abrir sistema de votacao\n")
                util.salvar_log("VOTACAO - Abrir sistema de votacao")
            
            # ---------------------------------------------------------
            # RESULTADOS DA VOTACAO (RF002.03)
            # Submenu com opcoes de relatorios
            # ---------------------------------------------------------
            elif opcaoVotacao == 2:
                print("Entrou em Votacao -> Resultados\n")
                util.salvar_log("VOTACAO - Resultados")
            
                opcaoVotacaoResultados = -1
                while opcaoVotacaoResultados != 0:
                    print("-----------VOTACAO RESULTADOS-----------")
                    print("1 - Boletim de urna")
                    print("2 - Estatistica")
                    print("3 - Votos por partido")
                    print("4 - Validacao integridade")
                    print("0 - Voltar")
                    print("----------------------------------")
                    
                    try:
                        opcaoVotacaoResultados = int(input("Selecione uma opcao: "))
                    except:
                        print("Digite um numero valido!")
                        opcaoVotacaoResultados = -1
                    print("----------------------------------\n")

                    # RF002.03.02 - Boletim de urna
                    if opcaoVotacaoResultados == 1:
                        print("Entrou em Votacao Resultados -> Boletim de urna\n")
                        util.salvar_log("VOTACAO RESULTADOS - Boletim de urna")
                    
                    # RF002.03.04 - Estatistica de comparecimento
                    elif opcaoVotacaoResultados == 2:
                        print("Entrou em Votacao Resultados -> Estatistica\n")
                        util.salvar_log("VOTACAO RESULTADOS - Estatistica")
                    
                    # RF002.03.05 - Votos por partido
                    elif opcaoVotacaoResultados == 3:
                        print("Entrou em Votacao Resultados -> Votos por partido\n")
                        util.salvar_log("VOTACAO RESULTADOS - Votos por partido")
                    
                    # RF002.03.06 - Validacao de integridade
                    elif opcaoVotacaoResultados == 4:
                        print("Entrou em Votacao Resultados -> Validacao integridade\n")
                        util.salvar_log("VOTACAO RESULTADOS - Validacao integridade")
                    
                    elif opcaoVotacaoResultados == 0:
                        print("Voltando...\n")
                        util.salvar_log("VOTACAO RESULTADOS - Voltar")
                    
                    else:
                        print("Votacao -> Resultados -> Opcao invalida\n")
                        util.salvar_log("Votacao -> Resultados -> Opcao invalida")
            
            # ---------------------------------------------------------
            # AUDITORIA DA VOTACAO (RF002.02)
            # Logs e protocolos para fiscalizacao
            # ---------------------------------------------------------
            elif opcaoVotacao == 3:
                print("Entrou em Votacao -> Auditoria\n")
                util.salvar_log("VOTACAO - Auditoria")

                opcaoVotacaoAuditoria = -1
                while opcaoVotacaoAuditoria != 0:
                    print("-----------VOTACAO AUDITORIA-----------")
                    print("1 - Logs Ocorrencia")
                    print("2 - Protocolos")
                    print("0 - Voltar")
                    print("----------------------------------")
                    
                    try:
                        opcaoVotacaoAuditoria = int(input("Selecione uma opcao: "))
                    except:
                        print("Digite um numero valido!")
                        opcaoVotacaoAuditoria = -1
                    print("----------------------------------\n")

                    # RF002.02.01 - Logs de ocorrencias
                    if opcaoVotacaoAuditoria == 1:
                        print("Entrou em Votacao Auditoria -> Logs Ocorrencia\n")
                        util.salvar_log("VOTACAO AUDITORIA - Logs Ocorrencia")
                    
                    # RF002.02.02 - Protocolos de votacao
                    elif opcaoVotacaoAuditoria == 2:
                        print("Entrou em Votacao Auditoria -> Protocolos\n")
                        util.salvar_log("VOTACAO AUDITORIA - Protocolos")
                    
                    elif opcaoVotacaoAuditoria == 0:
                        print("Voltando...\n")
                        util.salvar_log("VOTACAO AUDITORIA - Voltar")
                    
                    else:
                        print("Votacao -> Auditoria -> Opcao invalida\n")
                        util.salvar_log("Votacao -> Auditoria -> Opcao invalida")

            elif opcaoVotacao == 0:
                print("Saindo do modulo de votacao...\n")
                util.salvar_log("VOTACAO - Sair")
            
            else:
                print("Votacao -> Opcao invalida\n")
                util.salvar_log("Votacao -> Opcao invalida")
    
    # =================================================================
    # SAIR DO SISTEMA
    # =================================================================
    elif opcao == 3:
        print("Saindo do programa\n")
        util.salvar_log("MENU INICIAL - Saindo do programa")
    
    # Opcao invalida no menu principal
    else:
        print("Opcao invalida\n")
        util.salvar_log("MENU INICIAL - Opcao invalida")

# =============================================================================
# ENCERRAMENTO DO SISTEMA
# Exibe o historico de acoes antes de sair
# =============================================================================
print("\n" + "="*40)
print("HISTORICO DE ACOES:")
print("="*40)
with open("historico.txt", "r", encoding="utf-8") as arq:
    print(arq.read())

print("Voce saiu do projeto de votacao\n")

# Criptografia fernet
from seguranca import criptografar

# Na hora que o eleitor clica no botão:
voto_do_usuario = "Candidato 15" # Pegue isso do seu formulário
voto_protegido = criptografar(voto_do_usuario)

# Agora você salva 'voto_protegido' no banco de dados
print(f"Salvando no banco: {voto_protegido}")

cpf = input("digite o cpf: ")

#tirar tudo o que não for número 
cpf_limpo = " "
for c in cpf: 
    if c >= "0" and c <= "9":
        cpf_limpo = cpf_limpo + c 

#contar os digitos 
contador = 0 

for c in cpf_limpo:
    contador += 1 

#verificar tamanho, cpf tem 11 digitos
if contador != 11: 
    print("cpf inválido")
else: 
    soma = 0 
    for i in range(9):
        soma += int(cpf_limpo[i]) * (10 - i)

    digito1 = (soma * 10) % 11 
    if digito1 == 10: 
        digito1 = 0 

    #calcular 2 digito
    soma = 0 
    for i in range(10):
        soma += int(cpf_limpo[i]) * (11 - i)

    digito2 = (soma * 10) % 11
    if digito2 == 10: 
        digito2 = 0 

    #comparando os digitos para validar
    if digito1 == int(cpf_limpo[9]) and digito2 == int(cpf_limpo[10]): 
        print("cpf válido")
    else: 
        print("cpf inválido")

    titulo = input("digite o titulo de eleitor: ")

    #so numeros
    titulo_limpo = " "
    for c in titulo:
        if c >= "0" and c <= "9":
            titulo_limpo = titulo_limpo + c 

    #tamanho, deve ter 12 numeros 
    contador = 0 
    for c in titulo_limpo:
        contador += 1 

    if contador != 12:
        print("titulo invalido")
    else: 
        soma = 0 
        for i in range(8): 
            soma += int(titulo_limpo[i]) * (2 + i)
    
    digito1 = soma % 11
    if digito1 > 9: 
        digito1 = 0 

    #calcular 2  digito 
    soma = 0 
    for i in range(8,10):
        soma += int(titulo_limpo[i]) * (7 - i)
        
    soma += digito1 * 2

    digito2 = soma % 11 
    if digito2 > 9:
        digito2 = 0 

    #comparando digitos para validar 
    if digito1 == int(titulo_limpo[10]) and digito2 == int(titulo_limpo[11]):
        print("titulo valido")
    else: 
        print("titulo invalido") 

    
