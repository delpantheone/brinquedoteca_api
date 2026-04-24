from fastapi import APIRouter, status, HTTPException
from schemas.crianca import CriancaCreate, CriancaOut
from schemas.emprestimo import EmprestimoOut
from services.brinquedoteca_service import (
    ErrosValidacao,
    cadastrar_crianca,
    obter_crianca,
    listar_criancas,
    listar_emprestimos_por_crianca,
)

router = APIRouter(prefix="/criancas", tags=["criancas"])

@router.post("", response_model=CriancaOut, status_code=status.HTTP_201_CREATED)
def cadastrar_crianca_route(data: CriancaCreate):
    return cadastrar_crianca(**data.model_dump())

@router.get("/crianca/{crianca_id}", response_model=CriancaOut)
def obter_crianca_route(crianca_id: int):
    try:
        return obter_crianca(crianca_id)
    except ErrosValidacao as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.messages)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

@router.get("", response_model=list[CriancaOut])
def listar_criancas_route():
    return listar_criancas()

@router.get("/{crianca_id}/emprestimos", response_model=list[EmprestimoOut])
def listar_emprestimos_crianca_route(crianca_id: int):
    obter_crianca_route(crianca_id)
    return listar_emprestimos_por_crianca(crianca_id)
