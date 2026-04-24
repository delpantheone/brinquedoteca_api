from datetime import datetime
from typing import ValuesView
from domain.crianca import Crianca
from domain.brinquedo import Brinquedo
from domain.emprestimo import (
    Emprestimo,
    Datas,
)
from repositories.memory import db

class ErrosValidacao(Exception):
    def __init__(self, messages: list[str]):
        self.messages = messages

def cadastrar_crianca(nome: str, idade: int, responsavel: str) -> Crianca:
    nova_crianca = Crianca(db.next_crianca_id, nome, idade, responsavel)
    if nova_crianca.idade > 11:
        raise ErrosValidacao(['Idade máxima permitida para uma criança é de até 11 anos'])
    db.next_crianca_id += 1
    db.criancas_por_id[nova_crianca.id] = nova_crianca
    return nova_crianca

def obter_crianca(id: int) -> Crianca:
    if not (crianca := db.criancas_por_id.get(id)):
        raise ErrosValidacao(['Criança não encontrada'])
    return crianca

def listar_criancas() -> ValuesView[Crianca]:
    return db.criancas_por_id.values()

def cadastrar_brinquedo(nome: str, categoria: str, faixa_etaria_minima: int) -> Brinquedo:
    novo_brinquedo = Brinquedo(db.next_brinquedo_id, nome, categoria, faixa_etaria_minima)
    db.next_brinquedo_id += 1
    db.brinquedos_por_id[novo_brinquedo.id] = novo_brinquedo
    return novo_brinquedo


def obter_brinquedo(id: int) -> Brinquedo:
    if not (brinquedo := db.brinquedos_por_id.get(id)):
        raise ErrosValidacao(['Brinquedo não encontrado'])
    return brinquedo

def listar_brinquedos() -> ValuesView[Brinquedo]:
    return db.brinquedos_por_id.values()

def cadastrar_emprestimo(crianca_id: int, brinquedo_id: int, datas: Datas) -> Emprestimo:
    erros = []

    crianca = obter_crianca(crianca_id)
    brinquedo = obter_brinquedo(brinquedo_id)

    if not brinquedo.disponivel:
        erros.append('O brinquedo não está disponível para empréstimo')
    if brinquedo.faixa_etaria_minima > crianca.idade:
        erros.append('Este brinquedo não é indicado para a faixa etária desta criança')

    novo_emprestimo = Emprestimo(db.next_emprestimo_id, crianca.id, brinquedo.id, datas)
    todos_emprestimos = db.emprestimos_por_id.values()

    if crianca_bloqueada(crianca_id, todos_emprestimos):
        erros.append('Esta criança não pode fazer mais empréstimos pois possui 3 ou mais devoluções feitas com atraso')
    if atingiu_limite_emprestimos(crianca_id, todos_emprestimos):
        erros.append('Essa criança já atingiu o limite de empréstimos ativos permitidos')
    if any(e.conflita_com(novo_emprestimo) for e in todos_emprestimos):
        erros.append('Já existe um empréstimo deste brinquedo para este horário')
    
    if erros:
        raise ErrosValidacao(erros)

    db.next_emprestimo_id += 1
    db.emprestimos_por_id[novo_emprestimo.id] = novo_emprestimo
    return novo_emprestimo

def obter_emprestimo(emprestimo_id: int) -> Emprestimo:
    if not (emprestimo := db.emprestimos_por_id.get(emprestimo_id)):
        raise ErrosValidacao(['Empréstimo não localizado'])
    return emprestimo

def listar_emprestimos() -> ValuesView[Emprestimo]:
    return db.emprestimos_por_id.values()

def atingiu_limite_emprestimos(crianca_id: int, emprestimos: ValuesView[Emprestimo], limite: int = 2) -> bool:
    ativos = [e for e in emprestimos if e.crianca_id == crianca_id and e.status == "ativo"]
    return len(ativos) >= limite

def crianca_bloqueada(crianca_id: int, emprestimos: ValuesView[Emprestimo], limite: int = 3) -> bool:
    atrasos = [e for e in emprestimos if e.crianca_id == crianca_id and e.datas.devolucao_efetiva and e.datas.devolucao_efetiva > e.datas.devolucao_prevista]
    return len(atrasos) >= limite

def finalizar_emprestimo(emprestimo_id: int) -> Emprestimo:
    emprestimo = obter_emprestimo(emprestimo_id)
    
    if emprestimo.status == "finalizado":
        raise ErrosValidacao(["Este empréstimo já foi finalizado"])
    
    agora = datetime.now()
    emprestimo.datas.devolucao_efetiva = agora
    emprestimo.multa = emprestimo.calcular_multa(agora)
    emprestimo.status = "finalizado"
    
    brinquedo = obter_brinquedo(emprestimo.brinquedo_id)
    brinquedo.disponivel = True
    
    return emprestimo

def listar_emprestimos_por_crianca(crianca_id: int) -> list[Emprestimo]:
    return [e for e in db.emprestimos_por_id.values() if e.crianca_id == crianca_id]
