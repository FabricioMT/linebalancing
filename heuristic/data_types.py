from typing import Any, Union
import numpy as np
import copy
import random
from collections import UserList

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
    

 
class TaskListClass(UserList):

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

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]
    
    def append(self, __object) -> None:
        if __object not in self:
            super().append(__object)
        else:
            pass
    
    def __len__(self) -> int:
        return super().__len__()

    
    # def __iter__(self):
    #     for i in range(self.__getitem__()):
    #         yield 'Task: %d' % (i+1)
    
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

def find_next_task(list_jobs:Task,task:Task,candidate_succ:UserList):
    print('find_next_task')
    print(list_jobs)
    print('candidate_succ',candidate_succ)
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

    if task.machine != None:
        if task.succ[0] == []:
            return task
        return task.succ[0]
            
    if outlist:
        for i in outlist:
            if i.machine is None:
                return i
            return task
    
    if in_list:
        for i in in_list:
            if i.machine is None:
                return i
            return task.succ[0]
    return list_jobs[0]

def pin_job(job:Task,machine:Machine, job_list:list[Task]):
    machine.add_job(job)
    job.assign_machine(machine)
    job_list.remove(job)
    return job

def machine_check(machine:Machine, TaskDiv:int):
    print('machine_check Machine',machine)
    machine_jobs = set(machine.jobs)
    machine_jobs_pred = set()
    machine_jobs_succ = set()

    for job in machine_jobs:
        for i in job.pred:
           machine_jobs_pred.add(i) 
        for i in job.succ:
           machine_jobs_succ.add(i)

    mjs = machine_jobs_succ - machine_jobs
    mjp = machine_jobs_pred - machine_jobs

    print('machine_jobs_pred',mjp)
    print('machine_jobs_succ',mjs)

    if len(machine.jobs) >= TaskDiv:
        return mjs

    
        





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
        x =1 
        aux_job = jobs.copy()
        #print(aux_job)
        #print(job)     
        TaskDiv =  int(len(jobs)/len(machines))
        removidas = [UserList]
        candidate_succ = UserList
        
        while len(aux_job) >= 1:
            job = aux_job[0]     
            #print(f'Tarefa {job.task_id}: Custo = {job.cost} Pred = {[pred.task_id for pred in job.pred]} Suces = {[succ.task_id for succ in job.succ]}')
            for m in machines:

                if job.pred == []:
                    realised_job = pin_job(job,m,aux_job)
                    job = job.succ[0]


                if job.succ == []:
                    for tasks in job.pred:
                        if tasks.machine is None:
                            job = tasks
                    realised_job = pin_job(job,m,aux_job)
                    job = job.succ[0]
                
                candidate_succ = machine_check(m,TaskDiv)
                
                job = find_next_task(aux_job,job,candidate_succ) 
                print('next job',job)
                
                
                if job in candidate_succ:
                    realised_job = pin_job(job,m,aux_job)


                if len(m.jobs) != TaskDiv: break
                
    
                    
                
                
    

