def body_medico(
    uf,
    nome_medico,
    espec_med,
    quantidade,
):
    
    mapa_especialidades = {
        "ACUPUNTURA": "66",
        "ADMINISTRAÇÃO EM SAÚDE": "97",
        "ADMINISTRAÇÃO HOSPITALAR": "1",
        "ALERGIA E IMUNOLOGIA": "2",
        "ALERGIA E IMUNOPATOLOGIA": "98",
        "ANATOMIA PATOLÓGICA": "84",
        "ANESTESIOLOGIA": "3",
        "ANGIOLOGIA": "4",
        "ANGIOLOGIA E CIRURGIA VASCULAR": "67",
        "BRONCOESOFAGOLOGIA": "5",
        "CANCEROLOGIA": "6",
        "CANCEROLOGIA/CANCEROLOGIA CIRÚRGICA": "80",
        "CANCEROLOGIA/CANCEROLOGIA PEDIÁTRICA": "81",
        "CARDIOLOGIA": "7",
        "CIRURGIA CARDIOVASCULAR": "8",
        "CIRURGIA DA MÃO": "10",
        "CIRURGIA DE CABEÇA E PESCOÇO": "9",
        "CIRURGIA DIGESTIVA": "99",
        "CIRURGIA DO APARELHO DIGESTIVO": "11",
        "CIRURGIA DO TRAUMA": "85",
        "CIRURGIA GASTROENTEROLÓGICA": "86",
        "CIRURGIA GERAL": "12",
        "CIRURGIA ONCOLÓGICA": "87",
        "CIRURGIA PEDIÁTRICA": "13",
        "CIRURGIA PLÁSTICA": "14",
        "CIRURGIA TORÁCICA": "15",
        "CIRURGIA TORÁXICA": "110",
        "CIRURGIA VASCULAR": "16",
        "CIRURGIA VASCULAR PERIFÉRICA": "88",
        "CITOPATOLOGIA": "17",
        "CLÍNICA MÉDICA": "68",
        "COLOPROCTOLOGIA": "69",
        "DENSITOMETRIA ÓSSEA": "260",
        "DERMATOLOGIA": "18",
        "DIAGNÓSTICO POR IMAGEM": "83",
        "DOENÇAS INFECCIOSAS E PARASITÁRIAS": "89",
        "ELETROENCEFALOGRAFIA": "19",
        "ENDOCRINOLOGIA": "70",
        "ENDOCRINOLOGIA E METABOLOGIA": "20",
        "ENDOSCOPIA": "82",
        "ENDOSCOPIA DIGESTIVA": "21",
        "ENDOSCOPIA PERORAL": "109",
        "ENDOSCOPIA PERORAL VIAS AÉREAS": "101",
        "FISIATRIA": "22",
        "FONIATRIA": "23",
        "GASTROENTEROLOGIA": "24",
        "GENÉTICA CLÍNICA": "25",
        "GENÉTICA LABORATORIAL": "108",
        "GENÉTICA MÉDICA": "71",
        "GERIATRIA": "26",
        "GERIATRIA E GERONTOLOGIA": "90",
        "GINECOLOGIA": "27",
        "GINECOLOGIA E OBSTETRÍCIA": "72",
        "HANSENOLOGIA": "28",
        "HEMATOLOGIA": "29",
        "HEMATOLOGIA E HEMOTERAPIA": "73",
        "HEMOTERAPIA": "30",
        "HEPATOLOGIA": "102",
        "HOMEOPATIA": "31",
        "IMUNOLOGIA CLÍNICA": "91",
        "INFECTOLOGIA": "32",
        "INFORMÁTICA MÉDICA": "92",
        "MASTOLOGIA": "33",
        "MEDICINA DE EMERGÊNCIA": "261",
        "MEDICINA DE FAMÍLIA E COMUNIDADE": "74",
        "MEDICINA DO ADOLESCENTE": "93",
        "MEDICINA DO ESPORTE": "103",
        "MEDICINA DO TRABALHO": "34",
        "MEDICINA DO TRÁFEGO": "35",
        "MEDICINA ESPORTIVA": "36",
        "MEDICINA FÍSICA E REABILITAÇÃO": "75",
        "MEDICINA GERAL COMUNITÁRIA": "37",
        "MEDICINA INTENSIVA": "38",
        "MEDICINA INTERNA OU CLÍNICA MÉDICA": "39",
        "MEDICINA LEGAL": "40",
        "MEDICINA LEGAL E PERÍCIA MÉDICA": "259",
        "MEDICINA NUCLEAR": "41",
        "MEDICINA PREVENTIVA E SOCIAL": "76",
        "MEDICINA SANITÁRIA": "42",
        "NEFROLOGIA": "43",
        "NEUROCIRURGIA": "44",
        "NEUROFISIOLOGIA CLÍNICA": "45",
        "NEUROLOGIA": "46",
        "NEUROLOGIA PEDIÁTRICA": "47",
        "NEUROPEDIATRIA": "94",
        "NUTRIÇÃO PARENTERAL E ENTERAL": "104",
        "NUTROLOGIA": "48",
        "OBSTETRÍCIA": "49",
        "OFTALMOLOGIA": "50",
        "ONCOLOGIA": "95",
        "ONCOLOGIA CLÍNICA": "79",
        "ORTOPEDIA E TRAUMATOLOGIA": "51",
        "OTORRINOLARINGOLOGIA": "52",
        "PATOLOGIA": "53",
        "PATOLOGIA CLÍNICA": "54",
        "PATOLOGIA CLÍNICA/MEDICINA LABORATORIAL": "77",
        "PEDIATRIA": "55",
        "PNEUMOLOGIA": "56",
        "PNEUMOLOGIA E TISIOLOGIA": "105",
        "PROCTOLOGIA": "57",
        "PSIQUIATRIA": "58",
        "PSIQUIATRIA INFANTIL": "96",
        "RADIODIAGNÓSTICO": "106",
        "RADIOLOGIA": "59",
        "RADIOLOGIA E DIAGNÓSTICO POR IMAGEM": "78",
        "RADIOTERAPIA": "60",
        "REUMATOLOGIA": "61",
        "SEXOLOGIA": "62",
        "TERAPIA INTENSIVA": "63",
        "TERAPIA INTENSIVA PEDIÁTRICA": "257",
        "TISIOLOGIA": "64",
        "TOCO-GINECOLOGIA": "258",
        "ULTRASSONOGRAFIA": "107",
        "ULTRASSONOGRAFIA EM GINECOLOGIA E OBSTETRÍCIA": "256",
        "ULTRASSONOGRAFIA GERAL": "255",
        "UROLOGIA": "65"
    }

   
    codigo_especialidade = ""
    if espec_med:
        codigo_especialidade = mapa_especialidades.get(espec_med.upper(), "")
        
    

    payload_python = [
        {
            "useCaptchav2": True,
            "captcha": "0cAFcWeA4-NkVTzO_EHjVtKRCdmSgGUCIV_pavYtu6RgDADMQxBXnqTBNdGlhW2c_CfG4dR-_1OYqsJhykvJRUcvt6FfXUY4tl0ABt1ZD_FElztprbeUMkOG5VWQepWNldKgCZA5V3d8Ki23qORxyUvumbB1tpORIrHSN3Cw-YXBmXF8UJh3eYh5x_WrLZAJN2PdCe9AP8uPN9VDXYspsqdnZvw4wSmnyg4U2fcq7j2Y32r90cbiJ0lWN5yXbmYTfMq86pdO-wX-P8WgIxwldYhULiC09Ngj7-nC9VwDqxC-0bL4DrOQzRQ-fck81uae4Pj-5iDCHDAmdHb6CKi0cmZV2Jtp5yTje6wIhyduv-DR88iS1pk16CYpo08TceiFea8MUwuYyqnmWn5HIc7ajTiau2yYfE7AcFM-vvMmeU9TmWb27TCUmYraxFKITttMGHWY2yOXRelbNek9KNqcIntFXmIy8ikNSiGPHUqXxnrHqmE1I2ejh-CDjjjENq_UReh0n7w0Dq7nJHhB796ZKxjjp3eSu5Uof0K7SVRypsZZhcDSmSpG9e-BwoOminsLaszsqfm4nPjBeIUb1ixp9BLnjIl9AaNRXwxytbxCFNHm7W6vJP5Nbz3bYLD5ALd7GiOPetjJbOSeb7YfTY7ObOrnBdP2murLyUXT0rM_Of8RIGxVE6L1t-JO4F6o4iWYfp6pzrncFHo2kFByqXBr1_8mM92ifEjIkAAzOPeXL_pGhLFVv9xx1CZ-AHjBoWuMqsDuXTmWxpXf2m", 
            "medico": {
                "nome": nome_medico,
                "ufMedico": uf,
                "especialidadeMedico": codigo_especialidade, 
                
            },
            "page": 1,
            "pageNumber": 1,
            "pageSize": quantidade,
        }
    ]

    return payload_python


def body_profissional(
    nome_hospital,
    nome,
    descricao,
    sus,
    vinculacao,
    tipo,
    quantidade,   
): 
    
   
    payload_python = [
            {
            "useCaptchav2": True,
            "captcha": "", 
            "profissional": {
                "nome_hospital": nome_hospital,
                "nome": nome,
                "descricao": descricao,
                "sus": sus,
                "vinculacao": vinculacao,
                "tipo": tipo,   
                    
                },
                "page": 1,
                "pageNumber": 1,
                "pageSize": quantidade,
                
            }
        ]
        
    return payload_python

