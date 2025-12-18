# Objetivo 

Este projeto utiliza o framework FastAPI para criar uma interface de extração de dados públicos de saúde. O sistema consulta APIs externas, processa os dados e retorna JSONs organizados. 
O sistema é dividido em dois fluxos principais:

Busca de Médicos (CFM): Localiza médicos por nome, estado e especialidade.

Busca de Profissionais (CNES): Localiza o quadro de funcionários de um hospital, exigindo um fluxo de descoberta de ID (via CNPJ ou Nome) antes da extração final.

# Estrutura visual do projeto 

projeto_api_saude

│

├── main.py                       # Ponto de entrada (Roda o servidor)

├── models.py                     # Schemas de validação (Pydantic)

├── body.py                       # Funções auxiliares e dicionários
│

├── routers/                      # Pasta para organizar as rotas

│   ├── router_busca_medica.py    # Lógica de busca no CFM

│   └── router_cnes_profissionais.py # Lógica de busca no CNES
│

├── outputs/                      # (Opcional) Onde os arquivos .json são salvos

│   ├── medicos_mt.json

│   └── profissionais_123_pag1.json
│

└── requirements.txt              # Bibliotecas usadas (fastapi, requests, etc.)

# Arquivos 

## Arquivo models.py

Define o "contrato" de dados do sistema. Todas as classes herdam de BaseModel (Pydantic) para garantir validação automática.

Campos Opcionais: Definidos com valores padrão (ex: str = "") ou Optional.

Campos Obrigatórios: Classes como FiltroCNPJ e FiltroNome não possuem valores padrão, tornando o envio do dado obrigatório para a requisição ocorrer.

## Arquivo router_busca_medica.py

Contém a rota POST que interage com a API pública do CFM.

Entrada: Recebe o payLoad validado pelo Pydantic.

Transformação: Utiliza a função body_medico (do arquivo body.py) para converter os dados limpos no formato complexo exigido pelo site do CFM.

Execução:

Configura Headers e Cookies.

Realiza a requisição (requests.post) dentro de um bloco try/except para tratamento de erros.

Saída: Se sucesso (200), processa a resposta, salva um backup local e retorna o JSON. Se falha, retorna o erro tratado.

## Arquivo router_cnes_profissionais.py

Este módulo é responsável pelo fluxo de estabelecimentos (DataSUS) e possui três rotas distintas:

Configuração Global: Possui a função consultar_estabelecimentos que centraliza Headers e Cookies para evitar bloqueios de segurança (WAF).

Rota 1: Busca ID por CNPJ:

Higieniza a entrada (remove pontos e traços).

Trata a resposta da API (que pode vir como lista ou dicionário).

Filtra os resultados para garantir o match exato do CNPJ e retorna o ID.

Rota 2: Busca ID por Nome:

Converte a entrada para MAIÚSCULO (padrão do banco de dados).

Itera sobre os resultados para extrair ID e dados relevantes.

Rota 3: Baixar Profissionais:

Utiliza o ID obtido anteriormente.

Baixa a lista completa de ativos.

Gera uma lista otimizada (apenas dados relevantes) e calcula metadados da pesquisa (total encontrado, paginação).

## Arquivo body.py

Arquivo de suporte que mantém as rotas limpas.

Funções de Payload: body_medico e body_profissionais montam a estrutura JSON exata para envio às APIs externas.

Tradução (De/Para): Contém dicionários que traduzem termos amigáveis (ex: "Cardiologia") para os códigos internos dos sites governamentais.

## Arquivo main.py

O maestro da aplicação.

Cria a instância app = FastAPI().

Importa e inclui os roteadores (app.include_router) para expor os endpoints no servidor local.