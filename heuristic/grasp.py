from heuristic.operations import *
from heuristic.data_types import *
from heuristic.local_find import *
import time


class GRASP:

    def __init__(self, data):
        self.data = data
        self.best_solution = None
        self.best_cost = float('inf')
        self.results  = []


    def execute(self, max_minutes):
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < max_minutes * 60:
        
            solution = self.construct_solution()
            
            self.local_search(solution)
            cost = self.calculate_makespan(solution)

            if cost < self.best_cost:
                self.best_solution = solution
                self.best_cost = cost
            self.results.append(solution)

            elapsed_time = time.time() - start_time

            # Calcule a FO média e desvio
                
        fo_media = sum(solution.C for solution in self.results) / len(self.results)
        desvio = (fo_media - self.best_cost) / self.best_cost * 100
        # Atualize o relatório
        relatorio = []
        relatorio.append({
                          'Melhor FO':self.best_cost,
                               'FO Media':round(fo_media,3),
                               'Desvio (%)':round(desvio,3),
                               'Tempo Melhor (seg.)':round(elapsed_time,3),
                               'Tempo Medio (seg.)':round(elapsed_time / len(self.results),3)})
        return relatorio
    

    def construct_solution(self):
        sol = Greedy_Randomized_Construction(self.data,alpha=5,seed=2)
        return sol

    def local_search(self, solution):
        Solui = busca_local(solution, max_steps=1)
        return Solui

    def calculate_makespan(self,solution):
        return max([machine.total_cost for machine in solution.machines])
    
def increment_list(new_graph_clear):
    #print(new_graph_clear.task)
    increment_cost_list = []
    for task in new_graph_clear.task:
        increment_cost = task.cost
        task_preds = predecessores_indiretos(task,new_graph_clear.seq)
        for t in task_preds:
            increment_cost += t.cost
        increment_cost_list.append({'task': task, 'increment_cost': increment_cost})
    return increment_cost_list

def cria_LRC(alpha,increment_cost_list):
    gmin = 0
    gmax = 100
    lrc_candidates = []
    for entry in increment_cost_list:
        task = entry['task']
        increment_cost = entry['increment_cost']         
        if all(pred.machine is not None for pred in task.pred):
            if gmin <= increment_cost <= gmin + alpha * (gmax - gmin):
                lrc_candidates.append(task)
                increment_cost_list.remove(entry)
    return lrc_candidates

def Greedy_Randomized_Construction(data:Data,alpha, seed):
    new_solution = data
    random.seed(seed)
    new_graph_clear = Graph(new_solution)
    aux_machines = TaskListClass(new_graph_clear.machines.copy())
    DivMod = divmod(len(new_graph_clear.task),len(new_graph_clear.machines))

    div,resto = DivMod[0],DivMod[1]

    for mch in aux_machines: 
        mch.slots = div
        if aux_machines.is_last(mch):
            mch.slots = div+resto

    increment_cost_list = increment_list(new_graph_clear)
    lrc_candidates = cria_LRC(alpha,increment_cost_list)

    while new_graph_clear.task:
        for machine in new_graph_clear.machines:
            while lrc_candidates:
                lrc_task = random.choice(lrc_candidates)
                pin_job(lrc_task,machine,lrc_candidates)
                new_graph_clear.task.remove(lrc_task)
                increment_cost_list = increment_list(new_graph_clear)
                lrc_candidates = cria_LRC(alpha,increment_cost_list)
                if machine.slots == 0: break
            
    return new_graph_clear