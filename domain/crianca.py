from dataclasses import dataclass

@dataclass(frozen=True)
class Crianca:
    id: int
    nome: str
    idade: int
    responsavel: str
