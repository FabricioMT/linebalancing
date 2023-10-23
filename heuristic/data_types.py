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
    
    def __len__(self) -> int:
        return super().__len__()
    


class Machine:
    
    def __init__(self, key,jobs=None) -> None:
        if jobs is None: jobs = TaskListClass()
        self.key = key
        self.jobs = jobs
        self.total_cost = 0
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def add_job(self, job):
        self.jobs.append(job)
        self.total_cost = self.total_cost + job.cost
        print(f'Job: {job.task_id} assign in Machine: {self.key}')
    
    def __len__(self) -> int:
        return super().__len__()


class Data:
    def __init__(self, machines: list[Machine], jobs: list[Task], seq: dict):

        self.machines = machines
        self.task = jobs
        self.precedences = seq

def find_next_task(list_jobs:Task,task:Task):
    print('find_next_task')
    print(list_jobs)
    print('current task',task)
    print('task machine',task.machine)
    print(task.pred)
    print(task.succ)
    x = 1
    task.pred = set(task.pred)
    list_jobs = set(list_jobs)
    if task.pred not in list_jobs:
        
        for job in task.pred:
            task_pred_mch = job.machine
        task_pred_mch.add_job(task)
        task.assign_machine(task_pred_mch)
        list_jobs.remove(task)
        return list_jobs[0]
    else:
        for jobs in task.pred:
            if jobs.machine is None:
                return jobs
        



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
        #print(aux_job)
        #print(job)     
        TaskDiv =  int(len(jobs)/len(machines))
        
        while len(aux_job) >= 1:
            job = aux_job[0]     
            #print(f'Tarefa {job.task_id}: Custo = {job.cost} Pred = {[pred.task_id for pred in job.pred]} Suces = {[succ.task_id for succ in job.succ]}')
            for m in machines:
                if job.pred == []:
                    m.add_job(job)
                    job.assign_machine(m)
                    aux_job.remove(job)
                    job = job.succ[0]  

                if job.succ == []:
                    for tasks in job.pred:
                        if tasks.machine is None:
                            job = tasks
                    m.add_job(job)
                    job.assign_machine(m)
                    aux_job.remove(job)
                    job = job.succ[0]
    
                ret = find_next_task(aux_job,job) 
                print('next job',ret)
                job = ret
        
                if len(m.jobs) != TaskDiv:
                    m.add_job(job)
                    job.assign_machine(m)
                    aux_job.remove(job)
                else: break
    
                    
                
                
    

