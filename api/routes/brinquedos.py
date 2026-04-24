from fastapi import APIRouter, status, HTTPException
from schemas.brinquedo import BrinquedoCreate, BrinquedoOut
from services.brinquedoteca_service import (
    ErrosValidacao,
    cadastrar_brinquedo,
    obter_brinquedo,
    listar_brinquedos,
)

router = APIRouter(prefix="/brinquedos", tags=["brinquedos"])

@router.post("", response_model=BrinquedoOut, status_code=status.HTTP_201_CREATED)
def cadastrar_brinquedo_route(data: BrinquedoCreate):
    return cadastrar_brinquedo(**data.model_dump())

@router.get("/brinquedo/{brinquedo_id}", response_model=BrinquedoOut)
def obter_brinquedo_route(brinquedo_id: int):
    try:
        return obter_brinquedo(brinquedo_id)
    except ErrosValidacao as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.messages)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

@router.get("", response_model=list[BrinquedoOut])
def listar_brinquedos_route():
    return listar_brinquedos()
