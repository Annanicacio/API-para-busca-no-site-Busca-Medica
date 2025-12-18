from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from app.models.model import BuscaMedica
from app.body import body_medico
import requests
import json


router = APIRouter()

@router.post("/baixar-medicos", response_class=PlainTextResponse)
def buscar_medicos_mt(payLoad: BuscaMedica):
    """
    Realiza uma busca de médicos no portal do CFM (Conselho Federal de Medicina) com base nos filtros fornecidos.

    Esta rota atua como um cliente HTTP que repassa a consulta para a API pública do CFM,
    utilizando headers e cookies específicos para emular uma sessão de navegador válida.
    
    Além de retornar os dados na resposta, a função salva uma cópia local dos resultados.

    Args:
        payLoad (BuscaMedica): Objeto Pydantic contendo os critérios de pesquisa:
            - nome (str): Nome do médico (parcial ou completo).
            - uf (str): Sigla do estado (ex: "MT").
            - espec_med (str): Especialidade médica.
            - quantidade (int): Quantidade de registros a retornar (paginação).

    Returns:
        str: Uma string contendo o JSON formatado (pretty-print) retornado pelo CFM.
             Em caso de falha, retorna uma mensagem de erro (status code ou exceção).

    Side Effects:
        - Cria ou sobrescreve um arquivo local chamado 'medicos_mt.json' com o resultado da busca.
    """
   

    url_alvo = "https://portal.cfm.org.br/api_rest_php/api/v2/medicos/buscar_medicos"

    cookies = {
    '_fbp': 'fb.2.1765483774391.584124195940232557',
    '_gid': 'GA1.3.10975152.1765917266',
    '_gat_gtag_UA_17854308_1': '1',
    '_ga_P7Y8CBXPB2': 'GS2.1.s1765921494$o7$g1$t1765921495$j59$l0$h0',
    '_ga': 'GA1.1.1069647552.1765483775',
}

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://portal.cfm.org.br',
        'Referer': 'https://portal.cfm.org.br/busca-medicos',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': '_fbp=fb.2.1765483774391.584124195940232557; _gid=GA1.3.10975152.1765917266; _gat_gtag_UA_17854308_1=1; _ga_P7Y8CBXPB2=GS2.1.s1765921494$o7$g1$t1765921495$j59$l0$h0; _ga=GA1.1.1069647552.1765483775',
    }


    payload_data = body_medico(
        payLoad.uf,
        payLoad.nome,
        payLoad.espec_med,
        payLoad.quantidade,
    )

    try:
        response = requests.post(
            url_alvo,
            headers=headers,
            cookies=cookies,
            json=payload_data, # O Python converte para JSON automaticamente
            timeout=15 
        )

        if response.status_code == 200:
            dados = response.json() 

            # Salva backup local
            with open("medicos_mt.json", "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)

            # Retorna TEXTO na tela
            return json.dumps(dados, indent=4, ensure_ascii=False)
        else:
            return f"Erro CFM {response.status_code}:\n{response.text}"

    except Exception as e:
        return f"Erro Interno: {str(e)}"