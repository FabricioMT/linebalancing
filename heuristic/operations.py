from heuristic.data_types import *
import copy
import numpy as np

def pin_job(job:Task,machine:Machine, job_list:list[Task]):
    if machine.slots != 0:
        machine.add_job(job)
        job.assign_machine(machine)
        job_list.remove(job)
    else:
        return print(f'Machine {machine.key} Slots {machine.slots} !')

class Create_init_solution(Data):

    def __init__(self, params: Data):
        super().__init__(params.machines, params.task, params.precedences)
        self.seed = None
        task = params.task
        machines = params.machines
        precedences = params.precedences
        self._create_solution(machines,task,precedences)
        
    
    def restart(self):
        self.__init__(self)

    def _create_solution(self, machines: list[Machine], jobs :list[Task],precendence_list):
        aux_job_list = jobs.copy()
        aux_machines = TaskListClass(machines.copy())

        DivMod = divmod(len(jobs),len(machines))

        div,resto = DivMod[0],DivMod[1]

        for mch in aux_machines: 
            mch.slots = div
            if aux_machines.is_last(mch):
                mch.slots = div+resto            
        
        for machine in aux_machines:
            for task in precendence_list.values():
                pred,succ = task[0],task[1]

                if succ.pred not in aux_job_list:
                    for job in succ.pred:
                        if job.machine is None:
                            if job.pred not in aux_job_list:
                                for i in job.pred:
                                    if i.machine is None:
                                        pin_job(i,machine,aux_job_list)
                            pin_job(job,machine,aux_job_list)
        
                if machine.slots == 0: break

                if succ.succ == []:         
                    for job in succ.pred:                       
                        if job.machine is None:
                            if job.pred not in aux_job_list:
                                for i in job.pred:
                                    if i.machine is None:
                                        pin_job(i,machine,aux_job_list)                   
                            pin_job(job,machine,aux_job_list)
                        else:
                            if succ not in aux_job_list: break
                            pin_job(succ,machine,aux_job_list)  


class Operation:

    def __init__(
        self,
        machine: Machine,
        job: Task,
        release=None,
    ) -> None:
        self.machine = machine
        self.job = job
        self.code = machine, job
        self.duration = job.cost
        self.release = release
        self.tail = None
        self.critical = False
    
    def __repr__(self) -> str:
        return str(self.__dict__)

class Graph(Data):

    def __init__(self, Data:Data):
        super().__init__(Data.machines, Data.task, Data.precedences)
        self.M = {machine.key: machine for machine in self.machines}
        self.seq = [i for i in self.precedences.values()]
        self.O = {}  
        self.C = None
        self.neighborhood = []

    def precede_job(self, machine, job):
        last_job = self.M[machine].jobs.prev(job)
        if last_job is not None:
            return self.O[machine, last_job]
        else:
            prev_machine = TaskListClass(self.M.keys()).prev(machine)
            if prev_machine is not None:
                last_job_prev_machine = self.M[prev_machine].jobs[-1]
                return self.O[prev_machine, last_job_prev_machine]
            else:
                return None

    def follow_job(self, machine, job):
        next_job = self.M[machine].jobs.next(job)
        if next_job is not None:
            return self.O[machine, next_job]
        else:
            # Se não houver tarefa seguinte na mesma máquina, verifique na máquina seguinte
            next_machine = TaskListClass(self.M.keys()).next(machine)
            if next_machine is not None:
                first_job_next_machine = self.M[next_machine].jobs[0]
                return self.O[next_machine, first_job_next_machine]
            else:
                return None

    def precede_machine(self, machine, job):
        list_machine = TaskListClass(self.M)
        last_machine = list_machine.prev(machine)
        if last_machine is not None:
            last_job = self.M.get(last_machine).jobs[-1]
            return self.O[last_machine, last_job]
        else:
            return None

    def follow_machine(self, machine, job):
        list_machine = TaskListClass(self.M)
        follow_machine = list_machine.next(machine)
        if follow_machine is not None:
            next_job = self.M.get(follow_machine).jobs[0]
            return self.O[follow_machine, next_job]
        else:
            return None
        
    def copy(self):
        return copy.deepcopy(self)
    
class Neighborhood:

    def __init__(self, graph: Graph):
        self.graph = graph
        self.moves = []

    def reset_moves(self):
        # Resetar a lista de movimentos
        self.moves = []
 
    def generate_swap_moves(self):
        # Gerar todos os movimentos de troca possíveis entre máquinas diferentes
        for machine_from in self.graph.M.keys():
            for task_from in self.graph.M[machine_from].jobs:
                for machine_to in self.graph.M.keys():
                    if machine_from != machine_to:  # Certificar-se de que as máquinas são diferentes
                        for task_to in self.graph.M[machine_to].jobs:
                            
                            move = machine_from, task_from,machine_to, task_to
                            self.moves.append(move)

    def get_neighbors(self):
        # Retornar a lista de vizinhos (movimentos) gerados
        self.generate_swap_moves()
        
        return self.moves

