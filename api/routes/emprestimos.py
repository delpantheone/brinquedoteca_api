from fastapi import APIRouter, status, HTTPException
from schemas.emprestimo import EmprestimoCreate, EmprestimoOut
from services.brinquedoteca_service import (
    ErrosValidacao,
    cadastrar_emprestimo,
    listar_emprestimos,
    obter_emprestimo,
    finalizar_emprestimo,
)

router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])

@router.post("", response_model=EmprestimoOut, status_code=status.HTTP_201_CREATED)
def cadastrar_emprestimo_route(data: EmprestimoCreate):
    try:
        return cadastrar_emprestimo(**data.model_dump())
    except ErrosValidacao as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.messages)

@router.get("", response_model=list[EmprestimoOut])
def listar_emprestimos_route():
    return listar_emprestimos()

@router.get("/{emprestimo_id}", response_model=EmprestimoOut)
def obter_emprestimo_route(emprestimo_id: int):
    try:
        return obter_emprestimo(emprestimo_id)
    except ErrosValidacao as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.messages)

@router.put("/{emprestimo_id}/devolver", response_model=EmprestimoOut)
def devolver_brinquedo_route(emprestimo_id: int):
    try:
        return finalizar_emprestimo(emprestimo_id)
    except ErrosValidacao as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.messages)
