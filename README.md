# 💻 ProjetoIntegrador

# 👩​ ​Integrantes do Grupo​

| ----- Nome ------ |
| Anne Vieira       |
| Cecília Rufatto   |
| Gabriela Tomie    |
| Sophia Dalla      |
| Sophia Fabri      |

------------------------------------------------------------------------------------------------------------------------------------------

# 🗳️ Sobre o Projeto

Este projeto consiste em um Sistema de Eleições Eletrônicas completo, desenvolvido em Python com persistência de dados em MySQL. A aplicação foi projetada para simular com precisão e segurança o fluxo de um pleito eleitoral, desde a configuração inicial até a divulgação final dos resultados, garantindo a integridade e o sigilo de cada voto.

O sistema conta com uma interface baseada em menus e submenus intuitivos, guiados por um mapa de navegação fluído que direciona o usuário pelas etapas corretas da votação. Para garantir uma experiência de uso profissional e organizada, o programa utiliza um recurso de limpeza automática de tela, mantendo o terminal sempre limpo e facilitando a leitura das informações a cada transição de menu.

------------------------------------------------------------------------------------------------------------------------------------------

# 🔐 Segurança, Validação e Auditoria

A segurança é a espinha dorsal da aplicação. O fluxo é protegido por uma chave de acesso restrita, permitindo um controle rigoroso sobre a abertura e o encerramento da votação. Para garantir o preceito de "um eleitor, um voto", o sistema possui um mecanismo estrito de controle de voto único, validando a identidade do cidadão por meio da validação do título de eleitor. Além disso, toda a base de dados conta com criptografia para proteger informações sensíveis e uma camada de validação de integridade, assegurando que os dados não foram corrompidos ou alterados. Para fins de transparência, o sistema dispõe de um módulo de auditoria, permitindo verificar a conformidade de todo o processo.

------------------------------------------------------------------------------------------------------------------------------------------

# 👥 Gestão de Usuários e Candidatos

O gerenciamento do ecossistema eleitoral é feito de ponta a ponta. O sistema oferece um CRUD completo para a administração de votantes, permitindo cadastrar, editar, listar e deletar eleitores. Paralelamente, a gestão e cadastro de candidatos são estruturados para vincular corretamente os concorrentes aos seus respectivos cargos e legendas.

------------------------------------------------------------------------------------------------------------------------------------------

# 📝 O Processo de Votação e Apuração

No momento da realização do voto, o eleitor pode escolher seu candidato ou optar explicitamente pelo voto nulo. Durante o pleito, o administrador tem acesso à listagem de votantes em tempo real. Após o encerramento da sessão, o sistema executa a apuração de resultados de forma automatizada, gerando o boletim de urna (documento oficial que consolida os dados daquela seção) e emitindo a declaração de vencedor.

------------------------------------------------------------------------------------------------------------------------------------------

# 📊 Relatórios e Estatísticas

Por fim, o sistema entrega uma visão analítica detalhada sobre o encerramento da eleição. É possível consultar o resultado dos votos gerais, avaliar o desempenho político por meio do relatório de votos por partido e mensurar o engajamento do eleitorado através da estatística de comparecimento (indicando o índice de abstenção e presença).

------------------------------------------------------------------------------------------------------------------------------------------

# 🚀 Tecnologias Utilizadas

* Linguagem: Python
* Banco de Dados: MySQL
* Segurança: Criptografia de dados (Cifra Hills).
