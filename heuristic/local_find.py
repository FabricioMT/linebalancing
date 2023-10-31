from heuristic.operations import *
from heuristic.data_types import *


def find_swaps(grafo:Graph):
    swaps = []
    for key,machine in grafo.M.items():
        last_critical = False
        last_job = None
        for job in machine.jobs:
            if grafo.O[key,job]:
                if last_critical:
                    swaps.append((machine.key, last_job, job))
                last_critical = True
            else:
                last_critical = False
            last_job = job
    return swaps


def calc_cost(swap: tuple, graph: Graph):

    # Label operations of swap
    a = graph.O[swap[0], swap[1]]
    b = graph.O[swap[0], swap[2]]
    
    # Find previous and following operations
    PJa = graph.precede_job(*a.code)
    PMa = graph.precede_machine(*a.code)
    SJa = graph.follow_job(*a.code)
    SMa = graph.follow_machine(*a.code)
    
    PJb = graph.precede_job(*b.code)
    PMb = graph.precede_machine(*b.code)
    SJb = graph.follow_job(*b.code)
    SMb = graph.follow_machine(*b.code)
    
    # Calc equation terms for preceding
    if PMa is None:
        PMa_term = 0.0
    else:
        PMa_term = PMa.release + PMa.duration
    if PJb is None:
        PJb_term = 0.0
    else:
        PJb_term = PJb.release + PJb.duration
    if PJa is None:
        PJa_term = 0.0
    else:
        PJa_term = PJa.release + PJa.duration
    
    # Calc equation terms for next
    if SMa is None:
        q_SMa = 0.0
    else:
        q_SMa = SMa.tail
    if SMb is None:
        q_SMb = 0.0
    else:
        q_SMb = SMb.tail
    if SJa is None:
        q_SJa = 0.0
    else:
        q_SJa = SJa.tail
    if SJb is None:
        q_SJb = 0.0
    else:
        q_SJb = SJb.tail
    
    # New releases
    rb_new = max(PMa_term, PJb_term)
    ra_new = max(rb_new + b.duration, PJa_term)
    
    # New tails
    qa_new = max(q_SMb, q_SJa) + a.duration
    qb_new = max(qa_new, q_SJb) + b.duration
    
    # New makespan
    C_new = max(rb_new + qb_new, ra_new + qa_new)
    
    return C_new

def find_best_move(graph: Graph):

    # Save current solution
    C_best = graph.C
    best_move = None
    swaps = find_swaps(graph)
    
    # Iterate over swaps
    if swaps is not None:
        for swap in swaps:
            C_swap = calc_cost(swap, graph)
            if C_swap < C_best:
                best_move = swap
                C_best = C_swap
    
    return best_move

def busca_local(data:Data,max_steps=1000):
    initSol = Create_init_solution(data)
    FO = calculate_makespan(initSol.machines)
    
    aux_init_machines = initSol.machines.copy()
    aux_init_jobs = initSol.task.copy()

    G = Graph(initSol)
    print('len(G.O)')

    swaps = find_swaps(G)
    #print(swaps)
    #find_best_move(G)
    #print(G.O)

