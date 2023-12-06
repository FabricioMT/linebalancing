from heuristic.operations import *
from heuristic.data_types import *
from heuristic.visinhos import *
import random
def find_lower_cost(graph: Graph, machine: Machine):
    mincost = machine, min(j.cost for j in graph.M[machine].jobs)
    return mincost

def printdata(graph: Graph):
    
    #print('Maquinas:',Data.machines)
    #for task in graph.task: print(f'Tarefa {task.task_id}: Custo = {task.cost} Pred = {[pred.task_id for pred in task.pred]} Suces = {[succ.task_id for succ in task.succ]}')
    print('\n')
    #print('pair_cost:',Data.pair_cost.items())
    for machine in graph.machines: print(f'Maquina: [{machine.key}] Tarefas Atendidas: {machine.jobs}\nCusto total da Maquina: {machine.total_cost}')
    print('\n')

def predecessores_indiretos(task, precedencias):
    predecessores = set()

    def buscar_predecessores(task_atual):
        for pred, succ in precedencias:
            if succ == task_atual:
                predecessores.add(pred)
                buscar_predecessores(pred)

    buscar_predecessores(task)
    return predecessores

def troca_valida(graph, move, precedencias):
    machine_from, task_from, machine_to, task_to = move

    maquina1 = graph.M[machine_from]
    maquina2 = graph.M[machine_to]

    # Verifica se as tarefas estão em máquinas diferentes
    if maquina1 == maquina2:
        return False

    tarefa1_predecessores = predecessores_indiretos(task_from, precedencias)
    tarefa2_predecessores = predecessores_indiretos(task_to, precedencias)

    # Verifica se a troca quebra as precedências
    if task_to in tarefa1_predecessores or task_from in tarefa2_predecessores:
        return False
    
    return True

def verificar_precedencias(machines):
    for machine in machines:
        for task in machine.jobs:
            for precedencia in task.pred:
                maquina_precedencia = next((m for m, other_machine in enumerate(machines) if precedencia in [t.task_id for t in other_machine.jobs]), None)
                maquina_tarefa = machines.index(machine)
                # Verifica se a precedência é respeitada
                if maquina_precedencia is not None and maquina_precedencia > maquina_tarefa:
                    return False

    return True
# def troca_valida(graph,move, precedencias):

#     machine_from, task_from,machine_to, task_to = move

#     maquina1 = graph.M[machine_from]
#     maquina2 = graph.M[machine_to]
#     # Verifica se as tarefas estão em máquinas diferentes
#     if maquina1 == maquina2:
#         return False

#     print(precedencias)

#     tarefa1_dependencia = [pred for pred, succ in precedencias if succ == task_from]
#     tarefa2_dependencia = [pred for pred, succ in precedencias if succ == task_to]
#     print('task_from',task_from)
#     print('tarefa1_dependencia',tarefa1_dependencia)
#     print('task_to',task_to)
#     print('tarefa1_dependencia',tarefa2_dependencia)
#     # Verifica se a troca quebra a precedência da tarefa1 (tarefa1 deve ser feita após tarefa2_dependencia)
#     if tarefa1_dependencia and tarefa1_dependencia[0] == task_to:
#         return False

#     # Verifica se a troca quebra a precedência da tarefa2 (tarefa2 deve ser feita após tarefa1_dependencia)
#     if tarefa2_dependencia and tarefa2_dependencia[0] == task_from:
#         return False
    
#     return True


def find_best_move(graph: Graph):
    Copy = graph
    Copy.neighborhood = Neighborhood(Copy)
    swaps = Copy.neighborhood.get_neighbors()

    C_best = Copy.C
    best_move = []

    for move in swaps:
        if troca_valida(Copy,move,Copy.seq) and verificar_precedencias(Copy.machines):
            if move is not None:
                new_graph = apply_move(Copy,move)
                C_swap = calculate_makespan(new_graph.machines)
                if C_swap < C_best:
                    best_move = move
                    C_best = C_swap
    
    return best_move

def apply_move(graph, move):
    # Apply a random move in the neighborhood with restrictions respecting task precedences
    #print('aply move',move)
    machine_from, task_from,machine_to, task_to = move

    machine1 = graph.M[machine_from]
    machine2 = graph.M[machine_to]

    machine1.swap_jobs(task_from,task_to,machine2)
    machine2.swap_jobs(task_to,task_from,machine1)
    return graph


def _local_search_step(graph, copy=False):
    
    # Define new graph
    if copy:
        new_graph = graph.copy()
    else:
        new_graph = graph 
    # Obtain best move
    find_best_move(new_graph)

    return new_graph

def calculate_makespan(machines:list[Machine]):
    return max([machine.total_cost for machine in machines])

def busca_local(data:Data, max_steps=1000, copy=False):

    initSol = Create_init_solution(data)
    S = Graph(initSol)
    printdata(S)
    S.C = calculate_makespan(S.machines)
    makepan_inicial = S.C
    
    proceed = True
    k = 0
    
    while proceed and k < max_steps:
        
        S = _local_search_step(S, copy=copy)
        C_new = S.C
        if C_new > makepan_inicial:
            S.C = C_new
        else:
            proceed = False
        k = k + 1
    
    return S


