from pydantic import BaseModel
from typing import Optional  

class BuscaMedica(BaseModel):
    # Aceita string OU None. Se não enviar nada, vira None.
    nome: Optional[str] = None  
    uf: Optional[str] = None
    espec_med: Optional[str] = None
    quantidade: int = 10

class BuscaProfissional(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    sus: Optional[str] = None
    vinculacao: Optional[str] = None
    tipo: Optional[str] = None
    quantidade: int = 10

class FiltroCNPJ(BaseModel):
    cnpj: str # obrigatorio

class FiltroNome(BaseModel):
    nome_hospital: str # obrigatorio 

class FiltroProfissionais(BaseModel):
    id_cnes: str        
    nome_medico: Optional[str] = None 
    sus: Optional[str] = None          
    pagina: int = 1          
    itens_por_pagina: int = 50