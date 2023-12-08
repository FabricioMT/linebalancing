from heuristic.operations import *
from heuristic.data_types import *
import random


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

def find_best_move(graph: Graph):
    graph.neighborhood = Neighborhood(graph)
    swaps = graph.neighborhood.get_neighbors()
    
    best_moves = []
    #printdata()
    for move in swaps:
        if troca_valida(graph,move,graph.seq):
            best_moves.append(move)

    return best_moves

def sucessores_indiretos(task, precedencias):
    sucessores = set()

    def buscar_sucessores(task_atual):
        for pred, succ in precedencias:
            if pred == task_atual:
                sucessores.add(succ)
                buscar_sucessores(succ)

    buscar_sucessores(task)
    return sucessores

def reorganizar_tarefas_e_sucessores(graph, machine_key, task_with_successor):
    # Encontrar a máquina
    machine = graph.M[machine_key]
    # Verificar se a máquina foi encontrada
    if machine:
        # Encontrar a tarefa com o sucessor
        task = task_with_successor
        # Verificar se a tarefa foi encontrada
        if task:
            # Encontrar os sucessores indiretos da tarefa
            #predecessores = predecessores_indiretos(task,graph.seq)
            sucessores = sucessores_indiretos(task, graph.seq)
           
            # Remover a tarefa e seus sucessores da posição atual
            tasks_to_remove = [t for t in machine.jobs if t in sucessores]
            #print('tasks_to_remove',tasks_to_remove)
            for t in tasks_to_remove:
                machine.jobs.remove(t)

            # Adicionar a tarefa e seus sucessores ao final da lista
            machine.jobs.extend(tasks_to_remove)

def apply_move(graph: Graph, move) -> Graph:

    machine_from, task_from,machine_to, task_to = move

    machine1 = graph.M[machine_from]
    machine2 = graph.M[machine_to]

    p = predecessores_indiretos(task_from,graph.seq)
    s = sucessores_indiretos(task_from,graph.seq)
    # print(task_from)
    # print(p)
    # print(s)
    p2 = predecessores_indiretos(task_to,graph.seq)
    s2 = sucessores_indiretos(task_from,graph.seq)
    # print(task_to)
    # print(p2)
    # print(s2)
    machine1.swap_jobs(task_from,task_to,machine2)
    machine2.swap_jobs(task_to,task_from,machine1)
    reorganizar_tarefas_e_sucessores(graph,machine_to,task_from)
    reorganizar_tarefas_e_sucessores(graph,machine_from,task_to)

    

    return graph

def _local_search_step(graph, copy=False):
    
    # Define new graph
    if copy:
        new_graph = graph.copy()
    else:
        new_graph = graph 
    # Obtain best move

    best_moves = find_best_move(new_graph)
    C_best = graph.C
    move = random.choice(best_moves)
    print('move',move)
    if move is not None:
        new_graph = apply_move(new_graph,move)

        #C_swap = calculate_makespan(new_graph.machines)

    #new_graph = apply_move(new_graph,best_move)

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


