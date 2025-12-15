from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from model import BuscaMedica
from body import body_medico
import requests
import json

app = FastAPI()

@app.post("/baixar-medicos", response_class=PlainTextResponse)
def buscar_medicos_mt(payLoad: BuscaMedica):

    url_correta = "https://portal.cfm.org.br/api_rest_php/api/v2/medicos/buscar_medicos"

    cookies = {
    '_fbp': 'fb.2.1765483774391.584124195940232557',
    '_gid': 'GA1.3.1607546004.1765822931',
    '_gat_gtag_UA_17854308_1': '1',
    '_ga_P7Y8CBXPB2': 'GS2.1.s1765822929$o4$g1$t1765822931$j58$l0$h0',
    '_ga': 'GA1.1.1069647552.1765483775',
}

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
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
        # 'Cookie': '_fbp=fb.2.1765483774391.584124195940232557; _gid=GA1.3.1607546004.1765822931; _gat_gtag_UA_17854308_1=1; _ga_P7Y8CBXPB2=GS2.1.s1765822929$o4$g1$t1765822931$j58$l0$h0; _ga=GA1.1.1069647552.1765483775',
    }

    data = '[{"useCaptchav2":true,"captcha":"0cAFcWeA4-NkVTzO_EHjVtKRCdmSgGUCIV_pavYtu6RgDADMQxBXnqTBNdGlhW2c_CfG4dR-_1OYqsJhykvJRUcvt6FfXUY4tl0ABt1ZD_FElztprbeUMkOG5VWQepWNldKgCZA5V3d8Ki23qORxyUvumbB1tpORIrHSN3Cw-YXBmXF8UJh3eYh5x_WrLZAJN2PdCe9AP8uPN9VDXYspsqdnZvw4wSmnyg4U2fcq7j2Y32r90cbiJ0lWN5yXbmYTfMq86pdO-wX-P8WgIxwldYhULiC09Ngj7-nC9VwDqxC-0bL4DrOQzRQ-fck81uae4Pj-5iDCHDAmdHb6CKi0cmZV2Jtp5yTje6wIhyduv-DR88iS1pk16CYpo08TceiFea8MUwuYyqnmWn5HIc7ajTiau2yYfE7AcFM-vvMmeU9TmWb27TCUmYraxFKITttMGHWY2yOXRelbNek9KNqcIntFXmIy8ikNSiGPHUqXxnrHqmE1I2ejh-CDjjjENq_UReh0n7w0Dq7nJHhB796ZKxjjp3eSu5Uof0K7SVRypsZZhcDSmSpG9e-BwoOminsLaszsqfm4nPjBeIUb1ixp9BLnjIl9AaNRXwxytbxCFNHm7W6vJP5Nbz3bYLD5ALd7GiOPetjJbOSeb7YfTY7ObOrnBdP2murLyUXT0rM_Of8RIGxVE6L1t-JO4F6o4iWYfp6pzrncFHo2kFByqXBr1_8mM92ifEjIkAAzOPeXL_pGhLFVv9xx1CZ-AHjBoWuMqsDuXTmWxpXf2m","medico":{"nome":"","ufMedico":"MT","crmMedico":"","municipioMedico":"","tipoInscricaoMedico":"","situacaoMedico":"","detalheSituacaoMedico":"","especialidadeMedico":"","areaAtuacaoMedico":""},"page":1,"pageNumber":1,"pageSize":10}]'

    response = requests.post(
        'https://portal.cfm.org.br/api_rest_php/api/v2/medicos/buscar_medicos',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    # Pega a LISTA pura do body.py
    data = body_medico(
        payLoad.uf,
        payLoad.nome,
        payLoad.espec_med,
        payLoad.quantidade,
    )

    try:
        # MUDANÇA IMPORTANTE AQUI: Troquei 'data=' por 'json='
        response = requests.post(
            url_correta,
            cookies=cookies,
            headers=headers,
            json=data,  # <--- O Python converte a lista em JSON automaticamente aqui
        )

        if response.status_code == 200:
            try:
                dados = response.json() 

                with open("medicos_mt.json", "w", encoding="utf-8") as arquivo:
                    json.dump(dados, arquivo, indent=4, ensure_ascii=False)

                texto_formatado = json.dumps(dados, indent=4, ensure_ascii=False)
                return texto_formatado

            except Exception as erro_json:
                return f"Deu 200, mas erro ao ler JSON: {erro_json}\nTexto recebido:\n" + response.text
        else:
            return f"Erro {response.status_code}:\n" + response.text

    except Exception as e:
        return f"Erro Interno do Python: {str(e)}"