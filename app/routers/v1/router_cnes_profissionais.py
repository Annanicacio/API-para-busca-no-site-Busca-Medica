from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from app.models.model import FiltroCNPJ, FiltroNome, FiltroProfissionais
import requests
import json
import re
import math


router = APIRouter()

BASE_URL = "https://cnes.datasus.gov.br"


COOKIES_CNES = {
    "TS0142589a": "0121427f932176b550f1e22001d6d259329648a122033953375a4f76f42789923539547014077b8395da873e4446ad18da97dae842",
}

HEADERS_BASE = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Referer": "https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp?search=44595700000141",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
}

TIMEOUT = 60


def consultar_estabelecimentos(params: dict) -> list:
    """
    Função auxiliar que centraliza as requisições HTTP para a API de busca do CNES.

    Esta função configura os Headers e Cookies necessários para imitar um navegador,
    evitando bloqueios de segurança (WAF) do site do DataSUS.

    Args:
        params (dict): Dicionário com os parâmetros de busca.
                       Ex: {'cnpj': '...'} ou {'search': '...', 'page': 0}.

    Returns:
        list: Uma lista de dicionários contendo os estabelecimentos encontrados.
              Retorna uma lista vazia [] em caso de erro de conexão,
              status diferente de 200 ou falha no parse do JSON.
    """
    url = f"{BASE_URL}/services/estabelecimentos"
    headers = HEADERS_BASE.copy()
    headers["Referer"] = f"{BASE_URL}/pages/estabelecimentos/consulta.jsp"

    try:
        response = requests.get(
            url, headers=headers, params=params, cookies=COOKIES_CNES, timeout=TIMEOUT
        )

        if response.status_code == 200:
            dados = response.json()
            if isinstance(dados, list):
                return dados
            elif isinstance(dados, dict):
                return dados.get("content", [])
            return []
        else:
            print(
                f"--- [ERRO API] Status: {response.status_code} // Body: {response.text[:100]} // {response.url}"
            )
            return []
    except Exception as e:
        print("ERRO CONEXÃO:", e)
        return []


@router.get("/buscar-id-por-cnpj", response_class=PlainTextResponse)
def buscar_id_por_cnpj(filtros: FiltroCNPJ = Depends()):
    """
    Localiza o ID CNES de um estabelecimento de saúde utilizando o CNPJ como chave de busca.

    A função realiza a higienização do CNPJ (removendo pontuação), consulta a API de estabelecimentos
    e filtra os resultados para garantir uma correspondência exata.

    Args:
        filtros (FiltroCNPJ): Parâmetros de consulta injetados via Query String.
            - cnpj (str): O CNPJ do hospital (com ou sem pontuação).

    Returns:
        str: Uma string JSON formatada.
            - Sucesso: Retorna um objeto com `STATUS: ENCONTRADO`, `id_cnes`, `nome_fantasia`, etc.
            - Erro de API: Retorna o status code e o texto de erro da API externa.
            - Lista Vazia: Retorna um erro específico sugerindo a renovação do cookie (TS0142589a).
            - Não Encontrado: Retorna a lista original caso o CNPJ não conste nela.

    Raises:
        Exception: Captura erros internos de conexão ou lógica e retorna um JSON com a chave "erro_interno".
    """
    cnpj_limpo = re.sub(r"\D", "", filtros.cnpj)

    url = f"{BASE_URL}/services/estabelecimentos"
    params = {"cnpj": cnpj_limpo}

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS_BASE,
            cookies=COOKIES_CNES,
            timeout=TIMEOUT,
        )

        if response.status_code != 200:
            return json.dumps(
                {
                    "erro": f"API retornou status {response.status_code}",
                    "detalhe": response.text,
                },
                indent=4,
            )

        dados = response.json()
        lista_resultados = []
        if isinstance(dados, list):
            lista_resultados = dados
        elif isinstance(dados, dict):
            lista_resultados = dados.get("content", [])

        if not lista_resultados:
            return json.dumps(
                {
                    "erro": "A busca foi feita com sucesso (200 OK), mas a lista veio vazia.",
                    "dica": "Cookie vencido. Atualize o TS0142589a.",
                },
                indent=4,
                ensure_ascii=False,
            )

        for hospital in lista_resultados:
            cnpj_site = re.sub(r"\D", "", str(hospital.get("cnpj", "")))
            if cnpj_site == cnpj_limpo:
                retorno = {
                    "STATUS": "ENCONTRADO",
                    "id_cnes": hospital.get("cnes"),
                    "nome_fantasia": hospital.get("noFantasia"),
                    "municipio": hospital.get("noMunicipio"),
                    "uf": hospital.get("uf"),
                }
                return json.dumps(retorno, indent=4, ensure_ascii=False)

        return json.dumps(
            {
                "lista_retornada": lista_resultados,
            },
            indent=4,
            ensure_ascii=False,
        )

    except Exception as e:
        return json.dumps({"erro_interno": str(e)}, indent=4)


@router.get("/buscar-id-por-nome", response_class=PlainTextResponse)
def buscar_id_por_nome(
    filtros: FiltroNome = Depends(),
):
    """
    Pesquisa estabelecimentos de saúde pelo Nome Fantasia, permitindo filtros opcionais de localização.

    A função converte automaticamente os parâmetros para letras maiúsculas antes de enviar
    para a função auxiliar de consulta. O retorno é uma lista simplificada contendo apenas
    os identificadores e dados básicos do hospital.

    Args:
        filtros (FiltroNome): Objeto contendo o nome do hospital (obrigatório).
        uf (str | None): Sigla do estado (ex: 'SP', 'MT') para refinar a busca.
        municipio (str | None): Nome do município para refinar a busca.

    Returns:
        str: String JSON contendo uma lista de objetos. Cada objeto possui:
             - id_cnes, nome, municipio, uf, cnpj.
             Caso nenhum resultado seja encontrado, retorna um JSON de erro sugerindo verificação de cookies.
    """
    params = {"nome": filtros.nome_hospital.upper()}

    resultados = consultar_estabelecimentos(params)

    if not resultados:
        return json.dumps(
            {"erro": "Nenhum estabelecimento encontrado. Verifique o COOKIE."},
            indent=4,
            ensure_ascii=False,
        )

    lista_formatada = []
    for hosp in resultados:
        lista_formatada.append(
            {
                "id_cnes": hosp.get("cnes"),
                "nome": hosp.get("noFantasia"),
                "municipio": hosp.get("noMunicipio"),
                "uf": hosp.get("uf"),
                "cnpj": hosp.get("cnpj"),
            }
        )

    return json.dumps(lista_formatada, indent=4, ensure_ascii=False)


@router.get("/baixar-profissionais", response_class=PlainTextResponse)
def baixar_profissionais(
    filtros: FiltroProfissionais = Depends(),
    pagina: int = 1,  # <-- Novo parâmetro
    itens_por_pagina: int = 50,  # <-- Novo parâmetro (Padrão 50)
):
    """
    Obtém a lista de profissionais de um estabelecimento (ID CNES) com suporte a filtros e paginação.

    Fluxo de Execução:
    1. Acessa a API do CNES e baixa a lista completa de profissionais do hospital.
    2. Aplica filtros locais (em memória) por nome, CBO ou vínculo SUS.
    3. Realiza o fatiamento (slicing) da lista para criar a paginação.
    4. Gera metadados sobre o total de páginas e registros.

    Args:
        filtros (FiltroProfissionais): Critérios de busca. O campo `id_cnes` é obrigatório.
        pagina (int): Número da página desejada (Padrão: 1).
        itens_por_pagina (int): Quantidade de registros por página (Padrão: 50).

    Returns:
        str: JSON estruturado contendo duas chaves principais:
             - 'metadados': Informações sobre paginação (total, atual, itens).
             - 'dados': Lista dos profissionais da página atual.

    Side Effects:
        - Gera um arquivo JSON local (ex: `profissionais_123456_pag1.json`) com o resultado da requisição.
    """

    if not filtros.id_cnes:
        return "Erro: Você precisa informar o 'id_cnes'."

    url = f"{BASE_URL}/services/estabelecimentos-profissionais/{filtros.id_cnes}"
    headers = HEADERS_BASE.copy()
    headers["Referer"] = (
        f"{BASE_URL}/pages/estabelecimentos/ficha/profissionais-ativos/{filtros.id_cnes}"
    )

    try:

        response = requests.get(
            url, headers=headers, cookies=COOKIES_CNES, timeout=TIMEOUT
        )

        if response.status_code != 200:
            return f"Erro CNES ({response.status_code}): {response.text}"

        profissionais = response.json()

        # 2. Aplica Filtros (Nome, CBO, SUS)
        filtrados = []
        for prof in profissionais:
            if (
                filtros.nome_medico
                and filtros.nome_medico.upper()
                not in prof.get("nm_profissional", "").upper()
            ):
                continue
            if (
                filtros.descricao_cbo
                and filtros.descricao_cbo.upper() not in prof.get("ds_cbo", "").upper()
            ):
                continue
            if filtros.sus and filtros.sus.upper() != prof.get("st_sus", "").upper():
                continue
            filtrados.append(prof)

        ## Lógica de Paginação (Fatiamento)
        total_itens = len(filtrados)
        total_paginas = math.ceil(total_itens / itens_por_pagina)

        # Garante que a página solicitada não seja menor que 1
        pag_atual = max(1, pagina)

        # Calcula índices de corte
        inicio = (pag_atual - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina

        dados_paginados = filtrados[inicio:fim]

        # Monta a resposta estruturada
        resposta_final = {
            "metadados": {
                "total_registros_encontrados": total_itens,
                "total_paginas": total_paginas,
                "pagina_atual": pag_atual,
                "itens_por_pagina": itens_por_pagina,
                "hospital_id": filtros.id_cnes,
            },
            "dados": dados_paginados,
        }

        nome_arquivo = f"profissionais_{filtros.id_cnes}_pag{pag_atual}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(resposta_final, f, indent=4, ensure_ascii=False)

        return json.dumps(resposta_final, indent=4, ensure_ascii=False)

    except Exception as e:
        return f"Erro interno: {str(e)}"
