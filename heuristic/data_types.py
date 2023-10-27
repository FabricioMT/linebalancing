from typing import Any, Union
import numpy as np
import copy
import random
from collections import UserList
from itertools import *
from queue import PriorityQueue

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
        if job.machine is None:
            self.jobs.append(job)
            job.assign_machine(self.key)
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

        
    aux_pred = set(task.pred)
    aux_succ = set(task.succ)
    aux_list_jobs = set(list_jobs)

    outlist = aux_pred - aux_list_jobs
    in_list = aux_succ - aux_list_jobs

    print('outlist',outlist)
    print('in_list',in_list)
    
    if task.pred:
        for i in task.pred:
            if i.machine is None:
                return i
    
    if task.succ:
        for i in task.succ:
            if i.machine is None:
                for x in i.pred:
                    if x.machine is None:
                        return x
                return i
            
    #return task
        

def pin_job(job:Task,machine:Machine, job_list:list[Task],DivMod):
    div,resto = DivMod[0],DivMod[1]
    if len(machine.jobs) < div:
        if job.machine is None:
            machine.add_job(job)
            job_list.remove(job)

def intersection(task_pred_list:list[Task],aux_job:list[Task]):
    aux_tasklist= set(task_pred_list)
    aux_job_list= set(aux_job)
    result = aux_tasklist.intersection(aux_job_list)
    print('result',result)

class DataRandomParams(Data):

    def __init__(self, params: Data):
        super().__init__(params.machines, params.task, params.precedences)
        self.seed = None
        task = params.task
        machines = params.machines
        precedences = params.precedences
        self.seq = self._create_solution(machines,task,precedences)
    
    def restart(self):
        self.__init__(self)

    def _create_solution(self, machines: list[Machine], jobs :list[Task],preced):
        random.seed(self.seed)
        aux_job_list = jobs.copy()
        aux_machines = TaskListClass(machines.copy())


        DivMod = divmod(len(preced),len(machines))

        div,resto = DivMod[0],DivMod[1]
        
        
        for machine in aux_machines:
            for key,task in preced.items():             
                pred,succ = task[0],task[1]



                if succ.pred not in aux_job_list:  
                    for job in succ.pred:
                        if job.machine is None:
                            pin_job(job,machine,aux_job_list,DivMod)

                if pred.succ == []:
                    print('pred.succ',pred.succ)
                    for job in pred.pred:
                        if job.machine is None:
                            pin_job(job,machine,aux_job_list,DivMod)
           
                if succ.succ == []:  
                    for job in succ.pred:
                        if job.machine is None:
                            pin_job(job,machine,aux_job_list,DivMod)


                if len(machine.jobs) >= div:
                        break
                

        while len(aux_job_list) is not 0:
            for job in aux_job_list:
                machine.add_job(job)
                aux_job_list.remove(job)

        print(div,resto)
        print(machine)
        print(aux_job_list)



                




                    
                    


                    


                
    
                    
                
                
    

