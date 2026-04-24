from dataclasses import dataclass, field
from domain.brinquedo import Brinquedo
from domain.crianca import Crianca
from domain.emprestimo import Emprestimo

@dataclass
class MemoryDB:
    criancas_por_id: dict[int, Crianca] = field(default_factory=dict)
    brinquedos_por_id: dict[int, Brinquedo] = field(default_factory=dict)
    emprestimos_por_id: dict[int, Emprestimo] = field(default_factory=dict)
    next_crianca_id = 1
    next_brinquedo_id = 1
    next_emprestimo_id = 1

db = MemoryDB()
