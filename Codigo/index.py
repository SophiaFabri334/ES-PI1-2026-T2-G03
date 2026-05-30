# =============================================================================
# SISTEMA DE VOTACAO DIGITAL - LAD.Py
# Arquivo principal do sistema
# =============================================================================

import consultas as consultas  # Modulo de conexao e queries do banco de dados
import util as util           # Modulo de funcoes utilitarias (validacao, logs, etc.)
import seguranca as seguranca # Modulo de criptografia conforme pedido no projeto
# =============================================================================

# MENU PRINCIPAL
# Loop principal do sistema - executa ate o usuario escolher sair (opcao 3)
# =============================================================================
def menu_votacao_iniciada():
    """"
        Funcao de de menu de votacao iniciada -> feita para melhor organização do código
        Args:
            None
        
        Returns:
            None
    """
    opcaoVotacaoIniciado = -1
    while opcaoVotacaoIniciado != 0:

        #--------------------------------------------------------------------
        # RF002.03.01 - Menu Principal
        #--------------------   ------------------------------------------------
        
        print("-----------VOTACAO INICIADA-------")
        print("1 - Votar")
        print("2 - Fechar sistema de votação")
        print("----------------------------------")
        
        try:
            opcaoVotacaoIniciado = int(input("Selecione uma opcao: "))
        except:
            print("Digite um numero valido!")
            input("Digite ENTER para tentar novamente")
            opcaoVotacaoIniciado = -1
        print("----------------------------------\n")
        
        #--------------------------------------------------------
        # RF002.01.06 - Votação
        #--------------------------------------------------------
        
        if opcaoVotacaoIniciado == 1:
            util.limpar_tela()
            print("=== VOTAR ===\n")
            eleitor_valido = False

            while not eleitor_valido:
                titulo = input("Digite o título de Eleitor: ")
                cpf_4  = input("Digite os 4 primeiros dígitos do CPF: ")
                chave  = input("Digite a chave de acesso: ")
                
                if not consultas.verifica_eleitor(titulo, cpf_4, chave, 0):
                    print("\nErro: Eleitor invalido! Verifique os dados e tente novamente\n")
                    util.registrar_log_tentativa_acesso_negado("Validação de eleitor falhou")
                    continue
                
                if consultas.verifica_javotou(titulo, cpf_4, chave):
                    print("\nErro: Eleitor invalido! Esse eleitor já votou nessa eleição\n")
                    util.registrar_log_voto_duplo()
                    continue
            
                eleitor_valido = True

            util.limpar_tela()
            confirma_candidato = False 
            while not confirma_candidato:
                numero_candidato  = input("Digite o número do candidato que deseja votar: ")
                id_candidato = None
                numero = 0

                resultado = consultas.retorna_candidato(numero_candidato)
                if not resultado:
                    print("Candidato não encontrado - Seu voto está selecionado como NULO")
                else:
                    util.limpar_tela()
                    print("=== CANDIDATO SELECIONADO: ===\n")
                    print("Nome:", resultado[1])
                    print("Numero:", resultado[2])
                    print("Partido:", resultado[3])
                    id_candidato = resultado[0]
                    numero = resultado[2]
                

                # Perguntar se quer votar nesse candidato
                is_candidato_conf_input = input("Você tem certeza que quer votar nesse candidato? (S/N): ").strip().upper()

                if is_candidato_conf_input not in ['S', 'N']:
                    print("Digite apenas S ou N.")
                    continue

                if is_candidato_conf_input == 'N':
                    print("\nVoto cancelado.\n")
                    continue

                confirma_candidato = True

            protocolo = consultas.inserir_voto(id_candidato,numero,titulo,cpf_4,chave)
            
            if protocolo:
                print("\nVOTO CONFIRMADO!")
                print("PROTOCOLO:", protocolo)
                input("Pressione ENTER para continuar")
                util.limpar_tela()
                util.registrar_log_voto_sucesso()

        # ---------------------------------------------------------
        # RF002.01.07 - Encerrar sistema de votação
        # ---------------------------------------------------------
        
        elif opcaoVotacaoIniciado == 2:
            util.limpar_tela()
            util.limpar_tela()
            print("=== FECHAR SISTEMA DE VOTAÇÃO ===\n")
            mesario_valido = False
            # ---------------------------------------------------------
            # RF002.01.01, RF002.01.02, RF002.01.03, RF002.01.04, 
            # RF002.01.05 e RF002.01.06 - Abertura do Sistema e Zerézima
            # ---------------------------------------------------------
            while not mesario_valido:
                titulo = input("Digite o título de Eleitor: ")
                cpf_4  = input("Digite os 4 primeiros dígitos do CPF: ")
                chave  = input("Digite a chave de acesso: ")
                
                if not consultas.verifica_eleitor(titulo, cpf_4, chave, 1):
                    print("\nErro: Mesario invalido! Verifique os dados e tente novamente\n")
                    util.registrar_log_tentativa_acesso_negado("Validação de mesário falhou")
                    continue

                mesario_valido = True
                
            #-----------------------------------------------------------------
            # RF002.02.02 - Exibição dos Protocolos de Votação
            #------------------------------------------------------------------

            # Perguntar se deseja encerrar a votação
            is_enc_votacao = input("Você tem certeza que quer encerrar essa votação? (S/N): ").strip().upper()

            if is_enc_votacao not in ['S', 'N']:
                print("Digite apenas S ou N.")
                continue

            if is_enc_votacao == 'N':
                print("\nCancelando encerramento de votação.\n")
                opcaoVotacaoIniciado = -1
                continue
            else:
                util.limpar_tela()
                chave_valida = False
                while not chave_valida:
                    chave_acesso  = input("Digite a chave de acesso novamente para confirmação: ")
                    
                    if not consultas.verifica_eleitor(titulo, cpf_4, chave_acesso, 1):
                        print("\nErro: Chave inválida! Verifique tente novamente\n")
                        util.registrar_log_tentativa_acesso_negado("Chave de acesso inválida para encerramento")
                        continue

                    chave_valida = True

                print("\nEncerrando votação...")
                if consultas.fechar_urna():
                    print("VOTAÇÃO ENCERRADA COM SUCESSO!")
                    util.registrar_log_encerramento()
                    input("Pressione ENTER para continuar")
                    return
                else:
                    print("Erro ao encerrar votação.")
        else:
            print("=== OPÇÃO INVÁLIDA ===\n")
            input("Digite ENTER para tentar novamente")
            util.limpar_tela()

def boletim_urna():
    #--------------------------------------------------------------------------------
    # RF002.02, RF002.03, RF003.01 - Menus de Resultados e Auditoria
    #--------------------------------------------------------------------------------
    """
        Exibe o Boletim de Urna com contagem de votos por candidato em ordem alfabética
        e ao final declara o vencedor da eleição.

        Args:
            None
        
        Returns:
            None
    
    """
    # Imprime cabeçalho formatado do boletim de urna
    util.limpar_tela()
    print("=== BOLETIM DE URNA - RESULTADO DA VOTAÇÃO ===\n")
    
    # Chama função do módulo consultas para obter todos os candidatos com seus votos
    resultados = consultas.obter_resultados_por_candidato()
    
    # Verifica se há resultados; se não houver votos, exibe mensagem e sai da função
    if len(resultados) == 0: 
        print("Nenhum voto registrado ainda.")
        return 
    
    # Calcula o total de votos somando pela lista de candidatos 
    total_votos = 0
    for r in resultados:
        total_votos = total_votos + r[4] 
    
    # Exibe o total de votos registrados
    print("Total de votos: ", total_votos)
    
    # Imprime sobre cada candidato e exibe seus dados 
    for r in resultados: 
        print("="*30)
        print("Candidato: " , r[2])
        print("Número: " , r[1])
        print("Partido: " , r[3])
        print("Votos: " , r[4])

    print("\n\n")
    print("-"*70)
    # Itera sobre cada resultado de candidato para exibir seus dados em ordem alfabética
    for resultado in resultados:
        # Extrai os dados do candidato: número (índice 1), nome (2), partido (3) e votos (4)
        numero, nome, partido, votos = resultado[1], resultado[2], resultado[3], resultado[4]
        
        # Imprime a linha da tabela com formatação adequada (alinhamento e espaçamento)
        print(f"{numero:<5} {nome:<40} {partido:<15} {votos:<8}")
    
    # Imprime linha de separação e total de votos na rodapé
    print("-"*70)
    print(f"{'TOTAL DE VOTOS':<5} {'':<40} {'':<10} {total_votos:<8}")
    print("="*70)
    votos_nulos = consultas.obter_votos_nulos()
    print("Votos nulos:", votos_nulos)
    print("="*70)
    # Chama função do módulo consultas para obter o candidato com maior número de votos
    vencedor = consultas.obter_vencedor()
    
    # Verifica se há algum vencedor (se não há votos, retorna None)
    if vencedor:
        # Desempacota os dados do vencedor: número, nome, partido e quantidade de votos
        numero_venc, nome_venc, partido_venc, votos_venc = vencedor
        
        # Exibe linha em branco para separação visual
        print()
        
        # Exibe as informações do candidato vencedor com formatação clara
        print("="*70)
        print("DECLARAÇÃO DE VENCEDOR")
        print("="*70)
        print(f"\nCANDIDATO VENCEDOR:")
        print(f"Nome: {nome_venc}")
        print(f"Número: {numero_venc}")
        print(f"Partido: {partido_venc}")
        print(f"Total de votos obtidos: {votos_venc}")
        print("\n" + "="*70 + "\n")
    
    # Registra esta operação nos logs do sistema para auditoria
    util.salvar_log("RESULTADO - Boletim de Urna consultado")
    input("Digite ENTER para voltar ao menu de resultados")
    util.limpar_tela()
    #-------------------------------------------------------------------
    # RF002.02.01.08 e RF002.02.02 - Exibição de Dados na Auditoria
    #-------------------------------------------------------------------

def declaracao_vencedor():
    """
    Exibe a declaração do vencedor da votação.
    Nota: Esta informação também é exibida ao final do Boletim de Urna.
    """

    print("=== DECLARAÇÃO DO VENCEDOR ===\n")
    # Imprime cabeçalho formatado da declaração de vencedor
    
    # Chama função do módulo consultas para obter o candidato com maior número de votos
    vencedor = consultas.obter_vencedor()
    
    # Verifica se há algum vencedor (se não há votos, retorna None)
    if vencedor is None: 
        print("Nenhum voto foi registrado ainda.")
        return 
    
    # Desempacota os dados do vencedor: número, nome, partido e quantidade de votos
    numero, nome, partido, votos = vencedor
    
    # Exibe as informações do candidato vencedor 
    print("Vencedor: " , vencedor[1])
    print("Numero: " , vencedor[0])
    print("Partido: " , vencedor[2])
    print("Votos: " , vencedor[3]) 
    print("----------------------------------\n")
    
    # Registra esta operação nos logs do sistema para auditoria
    util.salvar_log("RESULTADO - Declaração de Vencedor consultada")

def estatistica_comparecimento(): 
    """
        Exibe estatísticas de comparecimento dos eleitores.
        Args:
            None
        
        Returns:
            None
    """
    # Imprime cabeçalho formatado da estatística de comparecimento
    util.limpar_tela()
    print("=== ESTATÍSTICA DE COMPARECIMENTO ===")
    
    # Chama função do módulo consultas para obter dados de comparecimento dos eleitores
    stats = consultas.obter_estatistica_comparecimento()
    
    # Verifica se os dados foram carregados corretamente
    if not stats:
        print("\nErro ao carregar estatísticas.\n")
        return
    
    # Extrai os dados do dicionário retornado: total, votaram, não votaram e percentual
    total = stats['total_eleitores']
    votaram = stats['eleitores_votaram']
    nao_votaram = stats['nao_votaram']
    percentual = stats['percentual']
    
    # Exibe quantidade absoluta de eleitores aptos
    print(f"\nTotal de eleitores aptos: {total}")
    
    # Exibe quantidade absoluta de pessoas que votaram
    print(f"Quantidade de pessoas que votaram: {votaram}")
    
    # Exibe quantidade de eleitores que não votaram
    print(f"Eleitores que não votaram: {nao_votaram}")
    
    # Exibe o percentual de comparecimento em relação ao total de eleitores aptos
    print(f"Percentual de comparecimento: {percentual:.2f}%")
    
    print("\n" + "="*50 + "\n")
    
    # Registra esta operação nos logs do sistema para auditoria
    util.salvar_log("RESULTADO!! - Estatística de Comparecimento consultada")
    input("Pressione ENTER para voltar ao menu de resultados")
    util.limpar_tela()

def votos_por_partido():
    """
        Exibe contagem de votos agrupados por partido.
        Mostra a somatória de votos recebidos por cada legenda partidária.
        Args:
            None
        
        Returns:
            None
    """
    # Imprime cabeçalho formatado da análise de votos por partido
    util.limpar_tela()
    print("=== VOTOS POR PARTIDO ===\n")    
    # Chama função do módulo consultas para obter votos agrupados por partido
    partidos = consultas.obter_votos_por_partido()
    
    # Verifica se há dados de partidos; se não há votos, exibe mensagem e sai da função 
    if len(partidos) == 0: 
        print("Nenhum voto foi registrado ainda.")
        return 
    
    
    # Calcula o total de votos somando a lista de partidos
    total_votos = 0 
    for p in partidos: 
        total_votos = total_votos + p[1]
    

    # Exibe o total de votos registrados
    print("Total de Votos: " , total_votos)
    print("\n-------------------------------------------------")
    # Imprime sobre cada partido para exibir sua quantidade de votos; p[0]= nome do partido , p[1]= quantidade de votos
    for p in partidos: 
        print(f"Partido: {p[0]:<15}  Votos: {p[1]:<10}" )
        print("-------------------------------------------------")
   
    # Registra esta operação nos logs do sistema para auditoria
    util.salvar_log("RESULTADO!! - Votos por Partido consultados")
    input("Pressione ENTER para voltar ao menu de resultados")
    util.limpar_tela()

def validacao_integridade(): 
    """
        Exibe validação de integridade dos votos registrados.
        Compara o total de votos na urna com a quantidade de eleitores
        que possuem o status "Já Votou".
        Args:
            None
        
        Returns:
            None
    """
    # Imprime cabeçalho formatado da validação de integridade
    util.limpar_tela()
    print("=== VALIDAÇÃO DE INTEGRIDADE DOS VOTOS ===\n")
    
    # Chama função do módulo consultas para obter dados de validação de integridade
    validacao = consultas.validacao_integridade_votos()
    
    # Verifica se os dados foram carregados corretamente
    if not validacao:
        print("\nErro ao carregar dados de integridade.\n")
        return
    
    # Extrai os dados do dicionário retornado pela função de validação
    total_votos = validacao['total_votos']
    eleitores_ja_votou = validacao['eleitores_ja_votou']
    eleitores_nao_votaram = validacao['eleitores_nao_votaram']
    total_eleitores = validacao['total_eleitores']
    diferenca = validacao['diferenca']
    integridade_ok = validacao['integridade_ok']
    
    # Seção 1: Exibe dados da urna
    print(f"\nDADOS DA URNA:")
    print(f"Total de votos registrados: {total_votos}")
    
    # Seção 2: Exibe dados dos eleitores
    print(f"\nDADOS DOS ELEITORES:")
    print(f"Total de eleitores aptos: {total_eleitores}")
    print(f"Eleitores com status 'Já Votou': {eleitores_ja_votou}")
    print(f"Eleitores que não votaram: {eleitores_nao_votaram}")
    
    # Seção 3: Exibe comparação entre votos e eleitores que votaram
    print(f"\nCOMPARAÇÃO:")
    print(f"Votos registrados na urna: {total_votos}")
    print(f"Eleitores com 'Já Votou': {eleitores_ja_votou}")
    print(f"Diferença: {diferenca}")
    
    # Seção 4: Exibe o status de integridade com símbolos visuais
    print(f"\nSTATUS DE INTEGRIDADE:")
    if integridade_ok:
        # Se total de votos = eleitores que votaram, integridade está OK
        print("✓ INTEGRIDADE CONFIRMADA")
        print("  Os dados estão íntegros:")
        print(f"  • Total de votos ({total_votos}) = Eleitores com 'Já Votou' ({eleitores_ja_votou})")
    else:
        # Se há discrepância, exibe alerta
        print("✗ ALERTA - Inconsistência Detectada!")
        print(f"  Existe uma diferença de {diferenca} registro(s)")
        print(f"  • Total de votos ({total_votos}) ≠ Eleitores com 'Já Votou' ({eleitores_ja_votou})")
    
    print("\n" + "="*70 + "\n")
    
    # Registra esta operação nos logs do sistema para auditoria
    util.salvar_log("RESULTADO!! - Validação de Integridade consultada")

    input("Pressione ENTER para voltar ao menu de resultados")
    util.limpar_tela()
                                
opcao = 0 
while opcao != 3: 
    util.limpar_tela()
    print("LAD.Py - Sistema de votação digital")
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
        input("Digite ENTER para tentar novamente")
        opcao = 0
    print("----------------------------------\n")

    # =================================================================
    # MODULO DE GERENCIAMENTO (RF001)
    # Controle administrativo de eleitores e candidatos
    # =================================================================
    if opcao == 1:
        opcaoGerenciamento = -1

        #--------------------------------------------------------------------------------------------
        # RF001.09, RF001.10, RF001.11, RF001.12, RF001.13 e RF001.14 - Gerenciamento de Candidatos
        #--------------------------------------------------------------------------------------------
        
        while opcaoGerenciamento != 0:
            util.limpar_tela()
            print("-----------GERENCIAMENTO-----------")
            print("1 - Cadastrar Eleitor")
            print("2 - Editar Eleitor")
            print("3 - Remover Eleitor")
            print("4 - Buscar Eleitor")
            print("5 - Listar Eleitores")
            print("6 - Gerenciamento de Candidatos")
            print("0 - Voltar ao menu principal")
            print("----------------------------------")
            
            try:
                opcaoGerenciamento = int(input("Selecione uma opcao: "))
            except:
                print("Digite um numero valido!")
                input("Digite ENTER para tentar novamente")
                opcaoGerenciamento = -1
            print("----------------------------------\n")

            # ---------------------------------------------------------
            # CADASTRAR ELEITOR (RF001.01 a RF001.04)
            # Solicita dados, valida CPF, verifica duplicidade,
            # gera chave de acesso e salva no banco
            # ---------------------------------------------------------
            if opcaoGerenciamento == 1:
                cadastrar_eleitor_novamente = "S"
                while cadastrar_eleitor_novamente == "S":
                    util.limpar_tela()
                    print("=== CADASTRO DE ELEITOR ===\n")
                    
                    # RF001.01 - Solicitar nome completo
                    nome_valido = False 
                    while not nome_valido:
                        nome = input("Digite o nome completo: ")

                        partes = nome.strip().split()
                        if len(partes) < 2:
                            print("\nErro: Digite o nome e o sobrenome\n")
                            util.salvar_log("ERRO - Tentativa de cadastro sem nome e sobrenome")
                            nome_valido = False
                            continue

                        nome_valido = True
                    
                    
                    cpf_valido = False 
                    while not cpf_valido :
                        # RF001.01 - Solicitar CPF
                        cpf = input("Digite o CPF (apenas numeros): ").strip()

                        cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres nao numericos
                        # RF001.02 - Validar CPF matematicamente
                        if not util.validar_cpf(cpf):
                            print("\nErro: CPF invalido! Verifique os digitos. Digite um cpf válido\n")
                            util.salvar_log("ERRO - CPF invalido informado")
                            continue
                        
                        # RF001.03 - Verificar duplicidade de CPF
                        if consultas.verificar_cpf_existe(cpf):
                            print("\nErro: CPF ja cadastrado no sistema! Digite um cpf válido\n")
                            util.salvar_log("ERRO - Tentativa de cadastro com CPF duplicado")
                            continue

                        cpf_valido = True

                    titulo_valido = False 
                    while not titulo_valido:
                        # RF001.01 - Solicitar Título de Eleitor
                        titulo = input("Digite o Título de Eleitor (apenas numeros): ").strip()
                        titulo = ''.join(filter(str.isdigit, titulo))  # Remove caracteres nao numericos

                        # RF001.02 - Validar titulo matematicamente
                        if not util.validar_titulo(titulo):
                            print("\nErro: Titulo inválido! Verifique os digitos e digite novamente!\n")
                            util.salvar_log("ERRO - Titulo de eleitor invalido informado")
                            continue

                        # RF001.03 - Verificar duplicidade de titulo
                        if consultas.verificar_titulo_existe(titulo):
                            print("\nErro: titulo de eleitor ja cadastrado no sistema! Digite um titulo de eleitor válido\n")
                            util.salvar_log("ERRO - Tentativa de cadastro com Titulo de eleitor duplicado")
                            continue

                        titulo_valido = True

                    resp_mesario = False 
                    while not resp_mesario:
                        # RF001.01 - Perguntar se e mesario
                        is_mesario_input = input("O eleitor e mesario? (S/N): ").strip().upper()
                        is_mesario = is_mesario_input == 'S'

                        if is_mesario_input not in ['S', 'N']:
                            print("Digite apenas S ou N, tente novamente.")
                            continue

                        resp_mesario = True

                    # RF001.04 - Gerar chave de acesso exclusiva
                    chave_acesso = util.gerar_chave_acesso(nome)
                    
                    # Inserir no banco de dados
                    try:
                        mesario = 1 if is_mesario else 0

                        # Cadastra na tabela de eleitores
                        consultas.inserir_eleitores(titulo, seguranca.criptografar(cpf), nome, seguranca.criptografar(chave_acesso), None, mesario)
                    
                        util.salvar_log("SUCESSO - Eleitor cadastrado: " + nome)
                        util.limpar_tela()
                        # Exibir confirmacao e chave de acesso
                        print("\n" + "="*40)
                        print("CADASTRO REALIZADO COM SUCESSO!")
                        print("="*40)
                        print("Nome: " + nome)
                        print("CPF: " + cpf)
                        print("Título de Eleitor: " + titulo)
                        print("Tipo: " + ("Mesario" if is_mesario else "Eleitor"))
                        print("\nCHAVE DE ACESSO: " + chave_acesso)
                        print("\nATENCAO: Guarde esta chave!")
                        print("Ela sera necessaria para votar.")
                        print("="*40 + "\n")
                        
                    except Exception as e:
                        print("\nErro ao cadastrar: " + str(e) + "\n")
                        util.salvar_log("ERRO - Falha ao cadastrar eleitor: " + str(e))
                        
                    cadastrar_eleitor_novamente = ""
                    while cadastrar_eleitor_novamente not in ['S', 'N']:
                        cadastrar_eleitor_novamente = input("Você deseja cadastrar um novo eleitor? (S/N): ").strip().upper()
                        if cadastrar_eleitor_novamente not in ['S', 'N']:
                            print("Digite apenas S ou N.")
                            continue

                        if cadastrar_eleitor_novamente != 'S':
                            break
            
            # ---------------------------------------------------------
            # EDITAR ELEITOR (RF001.05)
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 2:
                editar_eleitor_novamente = "S"

                while editar_eleitor_novamente == "S":
                    util.limpar_tela()
                    print("=== EDITAR ELEITOR ===\n")

                    cpf_busca = input("Digite o CPF do eleitor a editar: ").strip()
                    cpf_busca = ''.join(filter(str.isdigit, cpf_busca))

                    # VALIDAR CPF
                    if len(cpf_busca) != 11:
                        print("\nErro: CPF deve ter 11 dígitos!\n")

                        tentar_novamente = ""
                        while tentar_novamente not in ["S", "N"]:
                            tentar_novamente = input("Deseja tentar novamente? (S/N): ").strip().upper()
                            if tentar_novamente not in ["S", "N"]:
                                print("\nErro: digite apenas S ou N!\n")
                            
                        if tentar_novamente == "S":
                            continue
                        else:
                            break

                    cpf_criptografado = seguranca.criptografar(cpf_busca)

                    eleitor_encontrado = None
                    eleitor_mesario = "Não"

                    try:
                        consultas.cursor.execute(
                            """
                            SELECT cpf, nome_completo, titulo_eleitor,
                                mesario, senha
                            FROM eleitores
                            WHERE cpf = %s
                            """,
                            (cpf_criptografado,)
                        )

                        eleitor_encontrado = consultas.cursor.fetchone()

                    except Exception as e:
                        print("\nErro ao buscar eleitor:", str(e), "\n")

                    # ELEITOR NÃO ENCONTRADO
                    if not eleitor_encontrado:
                        print("\nEleitor não encontrado!\n")
                        util.salvar_log("ERRO - Eleitor nao encontrado para edicao: "+ cpf_busca)

                        tentar_novamente = ""
                        while tentar_novamente not in ["S", "N"]:
                            tentar_novamente = input("Deseja tentar novamente? (S/N): ").strip().upper()
                            if tentar_novamente not in ["S", "N"]:
                                print("\nErro: digite apenas S ou N!\n")
                            
                        if tentar_novamente == "S":
                            continue
                        else:
                            break

                    # DEFINIR SE É MESÁRIO
                    if eleitor_encontrado[3]:
                        eleitor_mesario = "Sim"

                    while True:
                        util.limpar_tela()

                        # DADOS ATUAIS
                        print("=" * 40)
                        print("DADOS ATUAIS")
                        print("=" * 40)
                        print("CPF:", eleitor_encontrado[0])
                        print("Nome:", eleitor_encontrado[1])
                        print("Título:", eleitor_encontrado[2])
                        print("Mesário:", eleitor_mesario)
                        print("=" * 40)

                        # MENU
                        print("\nO que deseja fazer?")
                        print("1 - Editar nome")
                        print("2 - Voltar")
                        print("0 - Cancelar edição")

                        try:
                            opcao_edicao = int(input("Opção: "))
                        except:
                            print("=== OPÇÃO INVÁLIDA ===\n")
                            input("Digite ENTER para tentar novamente")
                            continue

                        # CANCELAR EDIÇÃO
                        if opcao_edicao == 0:
                            editar_eleitor_novamente = "N"
                            break

                        # VOLTAR PARA DIGITAR CPF
                        elif opcao_edicao == 2:
                            break

                        # EDITAR NOME
                        elif opcao_edicao == 1:
                            novo_nome = input("Digite o novo nome: ").strip()
                            if not novo_nome:
                                print("\nErro: Nome não pode estar vazio!\n")
                                input("Pressione ENTER para continuar...")
                                continue

                            try:
                                consultas.cursor.execute(
                                    """
                                    UPDATE eleitores
                                    SET nome_completo = %s
                                    WHERE cpf = %s
                                    """,
                                    (novo_nome, cpf_criptografado)
                                )

                                consultas.conexao.commit()

                                util.limpar_tela()

                                print("=" * 40)
                                print("ELEITOR ATUALIZADO COM SUCESSO!")
                                print("=" * 40)
                                print("Nome anterior:",
                                    eleitor_encontrado[1])
                                print("Nome novo:", novo_nome)
                                print("=" * 40)

                                util.salvar_log("SUCESSO - Eleitor editado: "+ cpf_busca)

                            except Exception as e:
                                print("\nErro ao atualizar:", str(e))
                                util.salvar_log("ERRO - Falha ao editar eleitor: "+ str(e))

                            continuar = ""
                            while continuar not in ["S", "N"]:
                                continuar = input("\nDeseja editar outro eleitor? (S/N): ").strip().upper()
                                if continuar not in ["S", "N"]:
                                    print("\nErro: digite apenas S ou N!\n")
                            if continuar == "S":
                                break
                            else:
                                editar_eleitor_novamente = "N"
                                break

                        else:
                            print("\nOpção inválida!\n")
                            input("Pressione ENTER para continuar...")
            # ---------------------------------------------------------
            # REMOVER ELEITOR (RF001.06) 
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 3:
                conf_remove_eleitor = "S"
                while conf_remove_eleitor == "S":
                    util.limpar_tela()
                    print("=== REMOVER ELEITOR ===\n")
                    
                    # Solicitar CPF para busca
                    cpf_busca = input("Digite o CPF do eleitor a remover: ").strip()
                    cpf_busca = ''.join(filter(str.isdigit, cpf_busca))
                
                    # Validar formato do CPF
                    if len(cpf_busca) != 11:
                        print("\nErro: CPF deve ter 11 digitos!\n")
                        input("Pressione Enter para continuar")
                        continue
                    cpf_busca = seguranca.criptografar(cpf_busca)
                    # Variaveis para armazenar resultado da busca
                    eleitor_encontrado = None   
                    try:
                        # Buscar na tabela de eelitores
                        consultas.cursor.execute(
                            "SELECT cpf, nome_completo, mesario FROM eleitores WHERE cpf = %s", 
                            (cpf_busca,)
                        )
                        eleitor_encontrado = consultas.cursor.fetchone()
                                
                    except Exception as e:
                        print ("\nErro ao buscar: " + str(e) + "\n")
                        util.salvar_log("ERRO - Falha ao buscar eleitor para remocao: " + str(e))
                        continue
                    
                    # Verificar se eleitor foi encontrado
                    if not eleitor_encontrado:
                        print("\nEleitor nao encontrado!\n")
                        util.salvar_log("ERRO - Eleitor nao encontrado para remocao: " + cpf_busca)
                        input("Pressione Enter para continuar")

                        continue
                    util.limpar_tela()
                    # Exibir dados do eleitor a remover
                    print("\n" + "="*40)
                    print("DADOS DO ELEITOR A REMOVER:")
                    print("="*40)
                    print("CPF: " + eleitor_encontrado[0])
                    print("Nome: " + eleitor_encontrado[1])
                    print("Mesario: " + ("Sim" if eleitor_encontrado[2] else "Não"))
                    print("="*40)
                    
                    # Solicitar confirmacao
                    confirmacao = input("\nTem certeza que deseja remover este eleitor? (S/N): ").strip().upper()
                    
                    if confirmacao != 'S':
                        print("\nRemocao cancelada.\n")
                        util.salvar_log("GERENCIAMENTO - Remocao de eleitor cancelada: " + cpf_busca)

                        conf_remove_eleitor = ""
                        while conf_remove_eleitor not in ["S", "N"]:
                            conf_remove_eleitor = input("\nDeseja remover outro eleitor? (S/N): ").strip().upper()
                            if conf_remove_eleitor not in ["S", "N"]:
                                print("\nErro: digite apenas S ou N!\n")

                        if conf_remove_eleitor != "S":
                            break

                        continue
                    
                    # Executar DELETE no banco de dados
                    try:
                        consultas.remover_eleitor(cpf_busca)
                        util.limpar_tela()
                        # Exibir confirmacao
                        print("\n" + "="*40)
                        print("ELEITOR REMOVIDO COM SUCESSO!")
                        print("="*40)
                        print("CPF: " + eleitor_encontrado[0])
                        print("Nome: " + eleitor_encontrado[1])
                        print("="*40 + "\n")
                        
                        util.salvar_log("SUCESSO - Eleitor removido: " + cpf_busca + " (" + eleitor_encontrado[1] + ")")
                        
                    except Exception as e:
                        print("\nErro ao remover: " + str(e) + "\n")
                        util.salvar_log("ERRO - Falha ao remover eleitor: " + str(e))

                    conf_remove_eleitor = ""
                    while conf_remove_eleitor not in ["S", "N"]:
                        conf_remove_eleitor = input("\nDeseja remover outro eleitor? (S/N): ").strip().upper()
                        if conf_remove_eleitor not in ["S", "N"]:
                            print("\nErro: digite apenas S ou N!\n")
                    
                    if conf_remove_eleitor != "S":
                        break
            
            # ---------------------------------------------------------
            # BUSCAR ELEITOR (RF001.07) 
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 4:
                buscar_novamente = 'S'
                while buscar_novamente == 'S':
                    util.limpar_tela()
                    print("=== BUSCAR ELEITOR ===\n")

                    pesquisa = input("Pesquisa: ").strip()
                    try:
                        util.limpar_tela()
                        resultado = consultas.filtra_eleitores(pesquisa)
                        if not resultado:
                            print("\nNenhum eleitor encontrado.\n")
                        else:
                            print("\n\n=== ELEITORES ===")
                            for res in resultado:
                                print("="*40)
                                print(f"ID: {res[0]}")
                                print(f"Titulo de Eleitor: {res[1]}")
                                print(f"CPF: {res[2]}")
                                print(f"Nome: {res[3]}")
                                print(f"Ja votou: {'Não' if res[4] == None else 'Sim'}")
                                print(f"Mesario: {'Sim' if res[5] == 1 else 'Não'}")
                                print("="*40 + "\n")

                        buscar_novamente = ""
                        while buscar_novamente not in ["S", "N"]:
                            buscar_novamente = input("Você deseja fazer uma nova busca? (S/N): ").strip().upper()
                            if buscar_novamente not in ["S", "N"]:
                                print("\nErro: digite apenas S ou N!\n")
                        
                        if buscar_novamente != 'S':
                            break

                    except Exception as e:
                        print("\nErro ao buscar eleitores: " + str(e) + "\n")
                        util.salvar_log("ERRO - Falha ao buscar eleitores: " + str(e))
                        break                
            # ---------------------------------------------------------
            # LISTAR ELEITORES (RF001.08) 
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 5:
                listar_novamente = 'S'
                while listar_novamente == 'S':
                    util.limpar_tela()
                    resultado = consultas.busca_eleitores()
                    if not resultado:
                        print("\nNenhum eleitor encontrado.")
                    else:
                        print("\n\n=== CANDIDATOS ===")
                        print("="*120)
                        print(f"{'ID':<5} {'Nome':<50} {'Título de Eleitor':<20} {'CPF':<20} {'Já votou':<10} {'Mesário':<10}")
                        print("="*120)
                        for res in resultado:
                            print(f"{res[0]:<5} {res[3]:<50} {res[1]:<20} {res[2]:<20} {'Não' if res[4] == None else 'Sim':<10} {'Sim' if res[5] == 1 else 'Não':<10}")
                        print("="*120 + "\n")
                    listar_novamente = ""
                    while listar_novamente not in ["S", "N"]:
                        listar_novamente = input("Você deseja listar novamente? (S/N): ").strip().upper()
                        if listar_novamente not in ["S", "N"]:
                            print("\nErro: digite apenas S ou N!\n")
                    if listar_novamente != 'S':
                        break

            # ---------------------------------------------------------
            # CADASTRAR CANDIDATOS (RF001.09 a RF001.14) - Opcional
            # ---------------------------------------------------------
            elif opcaoGerenciamento == 6:
                opcaoCandidatos = -1
                while opcaoCandidatos != 0:
                    util.limpar_tela()
                    print("-----------GERENCIAMENTO CANDIDATOS-----------")
                    print("1 - Cadastrar Candidato")
                    print("2 - Editar Candidato")
                    print("3 - Remover Candidato")
                    print("4 - Buscar Candidato")
                    print("5 - Listar Candidatos")
                    print("0 - Voltar")
                    print("----------------------------------------------")
                    
                    try:
                        opcaoCandidatos = int(input("Selecione uma opcao: "))
                    except:
                        print("Digite um numero valido!")
                        opcaoCandidatos = -1
                    print("----------------------------------\n")

                    # -------------------------------------------------
                    # CADASTRAR CANDIDATO (RF001.09)
                    # -------------------------------------------------
                    if opcaoCandidatos == 1:
                        cadastrar_novamente = 'S'
                        while cadastrar_novamente == 'S':
                            util.limpar_tela()
                            print("=== CADASTRO DE CANDIDATO ===\n")
                            util.salvar_log("GERENCIAMENTO CANDIDATOS - Cadastrar")
                            
                            numero_valido = False
                            while not numero_valido:
                                try:
                                    numero = int(input("Digite o número de votação: "))
                                    
                                    if consultas.verificar_numero_candidato_existe(numero):
                                        print("\nErro: Número de candidato já cadastrado! Digite outro número\n")
                                        util.salvar_log("ERRO - Tentativa de cadastro com número duplicado")
                                        continue
                                    
                                    numero_valido = True
                                except ValueError:
                                    print("\nErro: Digite um número inteiro válido\n")
                            
                            nome_valido = False
                            while not nome_valido:
                                nome = input("Digite o nome do candidato: ").strip()
                                
                                if len(nome) < 3:
                                    print("\nErro: Nome deve ter pelo menos 3 caracteres\n")
                                    continue
                                
                                nome_valido = True

                            partido_valido = False
                            while not partido_valido:
                                partido = input("Digite o partido/legenda: ").strip()
                                
                                if not partido:
                                    print("Digite um partido válido!")
                                    partido_valido = False
                                    continue 

                                partido_valido = True
                                try:
                                    id_candidato = consultas.inserir_candidatos(numero, nome, partido)
                                    util.limpar_tela()
                                    if id_candidato:
                                        print("\n" + "="*40)
                                        print("CANDIDATO CADASTRADO COM SUCESSO!")
                                        print("="*40)
                                        print("Número: " + str(numero))
                                        print("Nome: " + nome)
                                        print("Partido: " + partido)
                                        print("="*40 + "\n")
                                        util.salvar_log(f"SUCESSO - Candidato cadastrado: {nome} (Nº {numero})")
                                    else:
                                        print("\nErro ao cadastrar candidato\n")

                                    cadastrar_novamente = ""
                                    while cadastrar_novamente not in ["S", "N"]:
                                        cadastrar_novamente = input("Você deseja cadastrar um novo candidato? (S/N): ").strip().upper()
                                        if cadastrar_novamente not in ["S", "N"]:
                                            print("\nErro: digite apenas S ou N!\n")                                    
                                    if cadastrar_novamente != 'S':
                                        break
                                except Exception as e:
                                    print(f"\nErro ao cadastrar: {str(e)}\n")
                                    util.salvar_log(f"ERRO - Falha ao cadastrar candidato: {str(e)}")
                    
                    # -------------------------------------------------
                    # EDITAR CANDIDATO (RF001.11)
                    # -------------------------------------------------
                    elif opcaoCandidatos == 2:
                        editar_novamente = 'S'
                        while editar_novamente == 'S':
                            util.limpar_tela()
                            print("=== EDITAR CANDIDATO ===\n")
                            util.salvar_log("GERENCIAMENTO CANDIDATOS - Editar")
                            
                            try:
                                numero_busca = int(input("Digite o número do candidato a editar: "))
                                
                                candidato = consultas.buscar_candidato_por_numero(numero_busca)
                                
                                if not candidato:
                                    print("\nCandidato não encontrado!\n")
                                    util.salvar_log(f"ERRO - Candidato não encontrado: {numero_busca}")
                                    
                                    editar_novamente = ""
                                    while editar_novamente not in ["S", "N"]:
                                        editar_novamente = input("Você deseja editar outro candidato? (S/N): ").strip().upper()
                                        if editar_novamente not in ["S", "N"]:
                                            print("\nErro: digite apenas S ou N!\n")
                                    if editar_novamente != 'S':
                                        break
                                    continue
                                
                                id_cand, numero, nome, partido = candidato
                                util.limpar_tela()
                                print("\n" + "="*40)
                                print("DADOS ATUAIS:")
                                print("="*40)
                                print("Número: " + str(numero))
                                print("Nome: " + nome)
                                print("Partido: " + partido)
                                print("="*40 + "\n")
                                
                                print("O que deseja editar?")
                                print("1 - Número")
                                print("2 - Nome")
                                print("3 - Partido")
                                print("4 - Alterar Candidato")
                                print("0 - Cancelar Edição")
                                
                                try:
                                    opcao_edicao = int(input("\n Selecione a opção desejada: "))
                                except:
                                    print("=== OPÇÃO INVÁLIDA ===\n")
                                    input("Digite ENTER para tentar novamente")

                                util.limpar_tela()
                                if opcao_edicao == 4:
                                    continue
                                elif opcao_edicao == 1:
                                    numero_novo_valido = False
                                    while not numero_novo_valido:
                                        try:
                                            numero_novo = int(input("Digite o novo número: "))
                                            
                                            if numero_novo != numero and consultas.verificar_numero_candidato_existe(numero_novo):
                                                print("\nErro: Este número já existe! Digite outro\n")
                                                continue
                                            
                                            numero_novo_valido = True
                                        except ValueError:
                                            print("\nErro: Digite um número inteiro válido\n")

                                    util.limpar_tela()
                                    if consultas.atualizar_candidato(numero, numero_novo, nome, partido):
                                        print("\n" + "="*40)
                                        print("CANDIDATO ATUALIZADO COM SUCESSO!")
                                        print("="*40)
                                        print("Número anterior: " + str(numero))
                                        print("Número novo: " + str(numero_novo))
                                        print("="*40 + "\n")
                                        util.salvar_log(f"SUCESSO - Candidato editado: número {numero} → {numero_novo}")
                                    else:
                                        print("\nErro ao atualizar candidato\n")
                                
                                elif opcao_edicao == 2:
                                    nome_novo_valido = False
                                    while not nome_novo_valido:
                                        nome_novo = input("Digite o novo nome: ").strip()
                                        if not nome_novo:
                                            print("\nErro: Nome não pode estar vazio!\n")
                                            continue
                                        
                                        if consultas.atualizar_candidato(numero, numero, nome_novo, partido):
                                            print("\n" + "="*40)
                                            print("CANDIDATO ATUALIZADO COM SUCESSO!")
                                            print("="*40)
                                            print("Nome anterior: " + nome)
                                            print("Nome novo: " + nome_novo)
                                            print("="*40 + "\n")
                                            util.salvar_log(f"SUCESSO - Candidato editado: {nome} → {nome_novo}")
                                        else:
                                            print("\nErro ao atualizar candidato\n")

                                        nome_novo_valido = True
                                
                                elif opcao_edicao == 3:
                                    partido_valido = False
                                    while not partido_valido:
                                        partido_novo = input("Digite o novo partido: ").strip()
                                        if not partido_novo:
                                            print("Digite um partido válido!")
                                            continue

                                        partido_valido = True
                                        if consultas.atualizar_candidato(numero, numero, nome, partido_novo):
                                            print("\n" + "="*40)
                                            print("CANDIDATO ATUALIZADO COM SUCESSO!")
                                            print("="*40)
                                            print("Partido anterior: " + partido)
                                            print("Partido novo: " + partido_novo)
                                            print("="*40 + "\n")
                                            util.salvar_log(f"SUCESSO - Candidato editado: partido {partido} → {partido_novo}")
                                        else:
                                            print("\nErro ao atualizar candidato\n")
                                elif opcao_edicao == 0:
                                    print("\nEdição cancelada.\n")
                                    break
                                else:
                                    try:
                                        opcao_edicao = int(input("\n Selecione a opção desejada: "))
                                    except:
                                        print("=== OPÇÃO INVÁLIDA ===\n")
                                        input("Digite ENTER para tentar novamente")
                                        continue

                               
                            except ValueError:
                                print("\nErro: Digite um número válido!\n")
                            except Exception as e:
                                print(f"\nErro: {str(e)}\n")
                                util.salvar_log(f"ERRO - Falha ao editar candidato: {str(e)}")

                            editar_novamente = ""
                            while editar_novamente not in ["S", "N"]:
                                editar_novamente = input("Você deseja editar outro candidato? (S/N): ").strip().upper()
                                if editar_novamente not in ["S", "N"]:
                                    print("\nErro: digite apenas S ou N!\n")
                            if editar_novamente != 'S':
                                break
                    
                    # -------------------------------------------------
                    # REMOVER CANDIDATO (RF001.12)
                    # -------------------------------------------------
                    elif opcaoCandidatos == 3:
                        remover_novamente = "S"

                        while remover_novamente == "S":
                            util.limpar_tela()
                            print("=== REMOVER CANDIDATO ===\n")
                            util.salvar_log("GERENCIAMENTO CANDIDATOS - Remover")

                            try:
                                numero_busca = int(input("Digite o número do candidato a remover: "))
                                candidato = consultas.buscar_candidato_por_numero(numero_busca)
                                if not candidato:
                                    print("\nCandidato não encontrado!\n")
                                    util.salvar_log(f"ERRO - Candidato não encontrado para remoção: {numero_busca}")

                                else:
                                    id_cand, numero, nome, partido = candidato
                                    util.limpar_tela()
                                    print("\n" + "="*40)
                                    print("DADOS DO CANDIDATO A REMOVER:")
                                    print("="*40)
                                    print("Número: " + str(numero))
                                    print("Nome: " + nome)
                                    print("Partido: " + partido)
                                    print("="*40 + "\n")

                                    confirmacao = input("Tem certeza que deseja remover este candidato? (S/N): ").strip().upper()
                                    if confirmacao == 'S':
                                        util.limpar_tela()
                                        if consultas.remover_candidato(numero):
                                            print("\n" + "="*40)
                                            print("CANDIDATO REMOVIDO COM SUCESSO!")
                                            print("="*40)
                                            print("Número: " + str(numero))
                                            print("Nome: " + nome)
                                            print("="*40 + "\n")

                                            util.salvar_log(f"SUCESSO - Candidato removido: {nome} (Nº {numero})")

                                        else:
                                            print("\nErro ao remover candidato\n")

                                    else:
                                        print("\nRemoção cancelada.\n")
                                        util.salvar_log(f"GERENCIAMENTO CANDIDATOS - Remoção cancelada: {numero}")

                            except ValueError:
                                print("\nErro: Digite um número válido!\n")

                            except Exception as e:
                                print(f"\nErro: {str(e)}\n")
                                util.salvar_log(f"ERRO - Falha ao remover candidato: {str(e)}")

                            remover_novamente = ""
                            while editar_novamente not in ["S", "N"]:
                                remover_novamente = input("Você deseja remover outro candidato? (S/N): ").strip().upper()
                                if remover_novamente not in ["S", "N"]:
                                    print("\nErro: digite apenas S ou N!\n")
                            if remover_novamente != 'S':
                                break
                    # -------------------------------------------------
                    # BUSCAR CANDIDATO (RF001.13)
                    # -------------------------------------------------
                    elif opcaoCandidatos == 4:
                        buscar_novamente = "S"
                        while buscar_novamente == "S":
                            util.limpar_tela()
                            print("=== BUSCAR CANDIDATO ===\n")
                            util.salvar_log("GERENCIAMENTO CANDIDATOS - Buscar")
                            
                            try:
                                numero_busca = int(input("Digite o número do candidato: "))
                                
                                candidato = consultas.buscar_candidato_por_numero(numero_busca)
                                
                                if not candidato:
                                    print("\nCandidato não encontrado!\n")
                                else:
                                    id_cand, numero, nome, partido = candidato
                                    print("\n" + "="*40)
                                    print("CANDIDATO ENCONTRADO:")
                                    print("="*40)
                                    print("Número: " + str(numero))
                                    print("Nome: " + nome)
                                    print("Partido: " + partido)
                                    print("="*40 + "\n")
                            
                            except ValueError:
                                print("\nErro: Digite um número válido!\n")
                            except Exception as e:
                                print(f"\nErro: {str(e)}\n")

                            buscar_novamente = ""
                            while buscar_novamente not in ["S", "N"]:
                                buscar_novamente = input("Você deseja buscar outro candidato? (S/N): ").strip().upper()
                                if buscar_novamente not in ["S", "N"]:
                                    print("\nErro: digite apenas S ou N!\n")
                            if buscar_novamente != 'S':
                                break
                    # -------------------------------------------------
                    # LISTAR CANDIDATOS (RF001.14)
                    # -------------------------------------------------
                    elif opcaoCandidatos == 5:
                        listar_candidato_novamente = "S"
                        while listar_candidato_novamente == "S":
                            util.limpar_tela()
                            util.salvar_log("GERENCIAMENTO CANDIDATOS - Listar")
                            try:
                                candidatos = consultas.buscar_candidatos_todos()
                                
                                if not candidatos:
                                    print("Nenhum candidato cadastrado.\n")
                                else:
                                    print("\n\n=== CANDIDATOS ===")
                                    print("="*60)
                                    print(f"{'Nº':<5} {'Nome':<30} {'Partido':<20}")
                                    print("="*60)
                                    for cand in candidatos:
                                        id_cand, numero, nome, partido = cand
                                        print(f"{numero:<5} {nome:<30} {partido:<20}")
                                    print("="*60 + "\n")
                            
                            except Exception as e:
                                print(f"\nErro ao listar candidatos: {str(e)}\n")

                            listar_candidato_novamente = ""
                            while listar_candidato_novamente not in ["S", "N"]:
                                listar_candidato_novamente = input("Você deseja listar os candidatos novamente? (S/N): ").strip().upper()
                                if listar_candidato_novamente not in ["S", "N"]:
                                    print("\nErro: digite apenas S ou N!\n")
                            if listar_candidato_novamente != 'S':
                                break
                    
                    elif opcaoCandidatos == 0:
                        print("Voltando ao menu de gerenciamento...\n")
                    
                    else:
                        print("=== OPÇÃO INVÁLIDA ===\n")
                        input("Digite ENTER para tentar novamente")
                        util.salvar_log("GERENCIAMENTO CANDIDATOS - ERRO: Opção inválida")
            
            # Voltar ao menu principal
            elif opcaoGerenciamento == 0:
                print("Voltando ao menu principal...\n")
            
            # Opcao invalida
            else:
                util.salvar_log("Gerenciamento -> ERRO: Opcao invalida do menu")
                print("=== OPÇÃO INVÁLIDA ===\n")
                input("Digite ENTER para tentar novamente")
    
    # =================================================================
    # MODULO DE VOTACAO (RF002)
    # Processamento do processo eleitoral
    # =================================================================
    
    elif opcao == 2:
        util.limpar_tela()
        if consultas.urna_aberta():
            print("========== VOTAÇÃO ========\n")
            print("=== URNA JÁ ESTÁ ABERTA ===\n")
            menu_votacao_iniciada()

            util.salvar_log("VOTACAO - Urna ja aberta")
        else:
            opcaoVotacao = -1
            while opcaoVotacao != 0:
                print("-----------VOTACAO-----------")
                print("1 - Abrir sistema de votacao")
                print("2 - Resultados da Votação")
                print("3 - Auditoria da votação")
                print("0 - Sair")
                print("-----------------------------")
                
                try:
                    opcaoVotacao = int(input("Selecione uma opcao: "))
                except:
                    print("Digite um numero valido!")
                    opcaoVotacao = -1
                print("----------------------------------\n")

                # ---------------------------------------------------------
                # ABRIR SISTEMA DE VOTACAO (RF002.01) 
                # ---------------------------------------------------------
                
                if opcaoVotacao == 1:
                    util.limpar_tela()
                    print("=== ABRIR SISTEMA DE VOTAÇÃO ===\n")
                    mesario_valido = False
                    while not mesario_valido:
                        titulo = input("Digite o título de Eleitor: ")
                        cpf_4  = input("Digite os 4 primeiros dígitos do CPF: ")
                        chave  = input("Digite a chave de acesso: ")
                        
                        if not consultas.verifica_eleitor(titulo, cpf_4, chave, 1):
                            print("\nErro: Mesario invalido! Verifique os dados e tente novamente\n")
                            util.registrar_log_tentativa_acesso_negado("Validação de mesário falhou")
                            continue

                        mesario_valido = True

                    print("\nMesário validado com sucesso!\n")
                    print("\nExecutando a Zerézima...\n")
                    consultas.limpa_votos()
                    consultas.abrir_urna()
                    util.registrar_log_abertura()
                    input("Pressione ENTER para continuar")
                    util.limpar_tela()
                    menu_votacao_iniciada()
                    print("----------------------------------\n")

                elif opcaoVotacao == 2:
                    util.limpar_tela()
                    opcaoResultados = 1
                    while opcaoResultados != 0:
                        print("------------RESULTADOS-----------")
                        print("1 - Boletim de Urna")
                        print("2 - Declaração de Vencedor")
                        print("3 - Estatística de Comparecimento")
                        print("4 - Votos por Partido")
                        print("5 - Validação de Integridade")
                        print("0 - Voltar")
                        print("---------------------------------")


                        opcaoResultados = int(input("Selecione uma opção: "))

                        if opcaoResultados == 1: 
                            boletim_urna()

                        elif opcaoResultados == 2: 
                            util.limpar_tela()
                            declaracao_vencedor()
                            input("Pressione ENTER para voltar ao menu de resultados")
                            util.limpar_tela()

                        elif opcaoResultados == 3: 
                            estatistica_comparecimento()

                        elif opcaoResultados == 4: 
                            votos_por_partido()

                        elif opcaoResultados == 5: 
                            validacao_integridade()

                        elif opcaoResultados == 0: 
                            util.limpar_tela()

                        else: 
                            util.salvar_log("VOTACAO - Resultado - ERRO: Selecionado opção inválida do menu")
                            print("\n=== OPÇÃO INVÁLIDA ===\n")
                            input("Digite ENTER para tentar novamente")
                            util.limpar_tela()

                
                # ---------------------------------------------------------
                # AUDITORIA DA VOTACAO (RF002.02)
                # ---------------------------------------------------------
                
                elif opcaoVotacao == 3:
                    util.limpar_tela()
                    opcaoVotacaoAuditoria = -1
                    while opcaoVotacaoAuditoria != 0:
                        print("-----------VOTACAO AUDITORIA----------")
                        print("1 - Exibição de Logs de Ocorrências")
                        print("2 - Exibição dos Protocolos de Votação")
                        print("0 - Voltar")
                        print("--------------------------------------")
                        
                        try:
                            opcaoVotacaoAuditoria = int(input("Selecione uma opcao: "))
                        except:
                            print("Digite um numero valido!")
                            opcaoVotacaoAuditoria = -1
                        print("----------------------------------\n")

                        util.limpar_tela()
                        # RF002.02.01 - Logs de ocorrencias
                        if opcaoVotacaoAuditoria == 1:
                            print("=== EXIBIÇÃO DE LOGS DE OCORRÊNCIAS ===\n")
                            util.exibir_logs()
                            util.salvar_log("AUDITORIA - Exibição de Logs de Ocorrências")
                
                        # -------------------------------------------------------------------------------- 
                            # RF002.02.02 - Exibição dos Protocolos de Votação de votacao
                        # --------------------------------------------------------------------------------

                        elif opcaoVotacaoAuditoria == 2:
                            print("=== EXIBIÇÃO DOS PROTOCOLOS DE VOTAÇÃO ===\n")
                            util.salvar_log("AUDITORIA - Exibição dos Protocolos de Votação")
                            
                            protocolos = consultas.listar_protocolos_votacao()
                            
                            if not protocolos:
                                print("Nenhum protocolo registrado ainda.\n")
                            else:
                                print("="*60)
                                print("PROTOCOLOS DE VOTAÇÃO GERADOS")
                                print("="*60)
                                print(f"Total de protocolos: {len(protocolos)}\n")
                                
                                for i, protocolo in enumerate(protocolos, 1):
                                    print(f"{i}. {protocolo}")
                                
                                print("\n" + "="*60)
                                print("Obs: Protocolos em ordem alfabética para auditoria")
                                print("="*60 + "\n")
                        
                        elif opcaoVotacaoAuditoria == 0:
                            print("Voltando...\n")
                        
                        else:
                            print("=== OPÇÃO INVÁLIDA ===\n")
                            input("Digite ENTER para tentar novamente")
                            util.salvar_log("Votacao -> Auditoria -> ERRO: Opcao invalida do menuß")

                elif opcaoVotacao == 0:
                    print("Saindo do modulo de votacao...\n")
                    util.salvar_log("VOTACAO - Sair")
                
                else:
                    print("=== OPÇÃO INVÁLIDA ===\n")
                    input("Digite ENTER para tentar novamente")
                    util.salvar_log("Votacao -> Opcao invalida")
    
    # =================================================================
    # SAIR DO SISTEMA
    # =================================================================
    elif opcao == 3:
        util.limpar_tela()
        util.limpar_log()         
        print("=== PROGRAMA FINALIZADO ===\n")
    # Opcao invalida no menu principal
    else:
        print("=== OPÇÃO INVÁLIDA ===\n")
        input("Digite ENTER para tentar novamente")

