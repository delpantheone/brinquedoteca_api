from pydantic import BaseModel

class CriancaBase(BaseModel):
    nome: str
    idade: int
    responsavel: str

class CriancaCreate(CriancaBase):
    pass

class CriancaOut(CriancaBase):
    id: int
