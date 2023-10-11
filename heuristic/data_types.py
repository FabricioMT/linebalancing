from typing import Any, Union
import numpy as np
import copy
import random

class Task:
    def __init__(self, task_id):
        self.task_id = int(task_id)
        self.pred = []
        self.succ = []
        self.machine = None
        self.cost = 0

    def add_predecessor(self, predecessor):
        self.pred.append(predecessor)

    def add_successor(self, successor):
        self.succ.append(successor)

    def assign_machine(self, machine):
        self.machine = machine
        
    
    def assign_cost(self, cost: int):
        self.cost = cost
    
    def __repr__(self) -> str:
        return str(self.task_id)
 
class TaskListClass(list):

    def prev(self, x):
        if self.is_first(x):
            return None
        else:
            i = self.index(x)
            return self[i - 1]
    
    def next(self, x):
        if self.is_last(x):
            return None
        else:
            i = self.index(x)
            return self[i + 1]
    
    def is_first(self, x):
        return x == self[0]
    
    def is_last(self, x):
        return x == self[-1]
    
    def swap(self, x, y):
        i = self.index(x)
        j = self.index(y)
        self[i] = y
        self[j] = x
    
    def append(self, __object) -> None:
        if __object not in self:
            super().append(__object)
        else:
            pass

class Machine:
    
    def __init__(
        self,
        key,
        jobs=None,
    ) -> None:
        if jobs is None:
            jobs = TaskListClass()
        self.key = key
        self.jobs = jobs
        self.total_cost = 0
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def add_job(self, job):
        self.jobs.append(job)
        self.total_cost = self.total_cost + job.cost

class Data:
    def __init__(self, machines: list[Machine], jobs: list[Task], seq: dict):

        self.machines = machines
        self.task = jobs
        self.precedences = seq

class DataRandomParams(Data):

    def __init__(self, params: Data):
        super().__init__(params.machines, params.task, params.precedences)
        self.seed = None
        task = params.task
        machines = params.machines
        precedences = params.precedences
        self.seq = self._random_sequences(machines,task,precedences)
        

    def restart(self):
        self.__init__(self)

    def _random_sequences(self, machines: Machine, jobs :list[Task],preced):
        random.seed(self.seed)

        aux_job = jobs.copy()
        #print(preced)     
        TaskDiv =  int(len(jobs)/len(machines))

        for m in machines:
            while len(aux_job) >= 1:
                rand_job = random.choice(aux_job)  
                aux_suces = rand_job.succ.copy()

                if rand_job.pred == []:
                    #print(f'Tarefa {rand_job.task_id}: Custo = {rand_job.cost} Pred = {[pred.task_id for pred in rand_job.pred]} Suces = {[succ.task_id for succ in rand_job.succ]}')
                    m.add_job(rand_job)
                    rand_job.assign_machine(m)
                    aux_job.remove(rand_job)
                    break
                
                if rand_job.pred in aux_job:
                    break
                else:
                    m.add_job(rand_job)
                    rand_job.assign_machine(m)
                    aux_job.remove(rand_job)
                    #print(jobs)
                    #print(f'Tarefa {rand_job.task_id}: Custo = {rand_job.cost} Pred = {[pred.task_id for pred in rand_job.pred]} Suces = {[succ.task_id for succ in rand_job.succ]}')          
                
                if len(m.jobs) == TaskDiv:        
                    break
                
                
    

