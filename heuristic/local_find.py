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

def troca_valida(graph: Graph, move:list[Operation,Operation],sequence):
    operation1, operation2 = move
    maquina1 = operation1.machine
    maquina2 = operation2.machine
    # Verifica se as tarefas estão em máquinas diferentes
    if maquina1 == maquina2:
        return False
    tarefa1_predecessores = operation1.predecessores_indiretos
    tarefa2_predecessores = operation2.predecessores_indiretos
    # Verifica se a troca quebra as precedências
    if operation2.job in tarefa1_predecessores or operation1.job in tarefa2_predecessores: 
        return False
    
    if sequence.index(operation1.job) == 0 or sequence.index(operation2.job) == 0: return False

    # if predecessores_alocados_corretamente(operation1.job,maquina2):
    #     return

    for task in tarefa1_predecessores:
        if task.machine.key > maquina2.key:
            return False

    for task in tarefa2_predecessores:
        if task.machine.key > maquina1.key:
            return False

    #print(sequence)

    # print('operation2.job)',operation2.job)
    # print('sequence.index(operation2.job)',sequence.index(operation2.job))
    # if tarefa1_predecessores.difference(maquina2.jobs):
    #     # print('operation1.job',operation1.job)
    #     # print('tarefa1_predecessores',tarefa1_predecessores)
    #     # print('maquina2.jobs',maquina2.jobs)
    #     # print(tarefa1_predecessores.difference(maquina2.jobs))
    #     return False
 
    # if tarefa2_predecessores.difference(maquina1.jobs):
    #     return False

    return True

def reorganizar_tarefas_e_sucessores(graph, machine_key, task_with_successor):
    # Encontrar a máquina
    machine = machine_key
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

def reorganizar_tarefas_e_predecessores(graph, machine_key, task_with_successor):
    # Encontrar a máquina
    machine = machine_key
    # Verificar se a máquina foi encontrada
    if machine:
        # Encontrar a tarefa com o sucessor
        task = task_with_successor
        # Verificar se a tarefa foi encontrada
        if task:
            # Encontrar os sucessores indiretos da tarefa
            predecessores = predecessores_indiretos(task,graph.seq)
            #print('predecessores',predecessores)
            #sucessores = sucessores_indiretos(task, graph.seq)
            # Remover a tarefa e seus sucessores da posição atual
            tasks_to_remove = [t for t in machine.jobs if t in predecessores]
            #print('tasks_to_remove',tasks_to_remove)
            for t in tasks_to_remove:
                machine.jobs.remove(t)

            # Adicionar a tarefa e seus sucessores ao final da lista
            machine.jobs.extend(tasks_to_remove)

def apply_move(graph: Graph, move:list[Operation,Operation]) -> Graph:

    operation1, operation2 = move
    maquina1 = operation1.machine
    maquina2 = operation2.machine

    task_from = operation1.job
    task_to = operation2.job
    #print('task_from,task_to',task_from,task_to)
    maquina1.swap_jobs(task_from,task_to,maquina2)
    maquina2.swap_jobs(task_to,task_from,maquina1)

    # reorganizar_tarefas_e_sucessores(graph,maquina1,task_from)
    # reorganizar_tarefas_e_sucessores(graph,maquina2,task_to)
    #verificar_precedencias(graph.M)
    #reorganizar_tarefas_e_predecessores(graph,maquina2,task_from)
    # reorganizar_tarefas_e_predecessores(graph,maquina1,task_from)

    # reorganizar_tarefas_e_predecessores(graph,maquina2,task_to)
    # reorganizar_tarefas_e_predecessores(graph,maquina1,task_from)
    return graph

def find_best_move(graph: Graph):
    G_copy = graph
    cpoy_swaps = G_copy.moves
    C_best = calculate_makespan(G_copy.machines)
    moves = []
    best_move = None

    for move in cpoy_swaps:
        if troca_valida(G_copy,move,G_copy.sequence):
            moves.append(move)
    # Iterate over swaps
    if moves is not None:
        for swap in moves:
            if swap is not None:  
                C_swap = apply_move(G_copy,swap)
                C_swap.C = calculate_makespan(C_swap.machines)

                if C_swap.C < C_best:
                    
                    best_move = swap
                    C_best = C_swap.C
    
    return best_move

def _local_search_step(graph):
    
    new_graph = graph 
    # Obtain best move
    #printdata(new_graph)
    best_move = find_best_move(new_graph)
    #print('best_move',best_move)
    if best_move is not None:
        new_graph = apply_move(new_graph,best_move)
        new_graph.C = calculate_makespan(new_graph.machines)
    #printdata(new_graph)
    return new_graph

def calculate_makespan(machines:list[Machine]):
    return max([machine.total_cost for machine in machines])

def busca_local(data:Graph, max_steps:int):
    initSol = Graph(data)
    initSol.C = calculate_makespan(initSol.machines)
    makepan_inicial = initSol.C
    proceed = True
    k = 0
    while proceed and k < max_steps:
        S = _local_search_step(initSol)
        C_new = S.C
        if C_new < makepan_inicial:
            makepan_inicial = C_new
        else:
            proceed = False

        k = k + 1
    
    return S


