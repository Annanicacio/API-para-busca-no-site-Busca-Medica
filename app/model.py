from pydantic import BaseModel


class BuscaMedica(BaseModel):
    nome: str
    uf: str
    espec_med: str
    quantidade: int = 10