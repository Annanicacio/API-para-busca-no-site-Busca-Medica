from fastapi import FastAPI
from app.routers.v1 import router_busca_medica, router_cnes_profissionais

app = FastAPI(title="API de Extração de Dados - Saúde")

# Incluindo as rotas que criamos nos outros arquivos
app.include_router(router_busca_medica.router, tags=["CFM - Busca Médica"])
app.include_router(router_cnes_profissionais.router, tags=["CNES - Profissionais"])

@app.get("/")
def home():
    return {"mensagem": "API rodando! Acesse /docs para testar."}
