from dataclasses import dataclass, field
from datetime import datetime
from typing import Self


@dataclass
class Datas:
    inicio: datetime
    devolucao_prevista: datetime
    devolucao_efetiva: datetime


@dataclass
class Emprestimo:
    id: int
    crianca_id: int
    brinquedo_id: int
    datas: Datas
    status: str = field(default="ativo")  # Ativo | Finalizado
    multa: float = field(default=0.0)

    def conflita_com(self, outro_emprestimo: Self) -> bool:
        if self.brinquedo_id != outro_emprestimo.brinquedo_id:
            return False
        return (
            self.datas.inicio <= outro_emprestimo.datas.devolucao_prevista
            and outro_emprestimo.datas.devolucao_prevista
            <= self.datas.devolucao_prevista
        )
    
    def calcular_multa(self, data_devolucao_efetiva: datetime) -> float:
        if data_devolucao_efetiva <= self.datas.devolucao_prevista:
            return self.multa
        # Multa de R$ 2 por dia de atraso
        dias = (data_devolucao_efetiva - self.datas.devolucao_prevista).days
        return 2 * dias
