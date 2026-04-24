from pydantic import BaseModel

class BrinquedoBase(BaseModel):
    nome: str
    categoria: str
    faixa_etaria_minima: int

class BrinquedoCreate(BrinquedoBase):
    pass

class BrinquedoOut(BrinquedoBase):
    id: int
    disponivel: bool
