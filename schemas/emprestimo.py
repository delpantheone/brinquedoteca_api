from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class DatasEmprestimoBase(BaseModel):
    inicio: datetime = Field(description="Data e hora de início do empréstimo")
    devolucao_prevista: datetime = Field(description="Data e hora prevista para devolução")
    devolucao_efetiva: Optional[datetime] = None

class EmprestimoBase(BaseModel):
    crianca_id: int
    brinquedo_id: int
    datas: DatasEmprestimoBase

class EmprestimoCreate(EmprestimoBase):
    pass

class EmprestimoOut(EmprestimoBase):
    id: int
    status: str
    multa: float
