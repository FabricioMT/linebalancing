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
        self.slots = 0
        self.total_cost = 0
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def add_job(self, job):
        if job.machine is None:
            if self.slots != 0:
                self.jobs.append(job)
                self.total_cost = self.total_cost + job.cost
                self.slots = self.slots - 1
                #print(f'Job: {job.task_id} assign in Machine: {self.key}')
    
    def swap_jobs(self, task_a, task_b, target_machine):
            
            if task_a in self.jobs and task_b in target_machine.jobs:
                # Remover tarefas originais
                #print(task_a,task_b)
                
                self.jobs.remove(task_a)
                #print(target_machine.jobs)
                target_machine.jobs.remove(task_b)
                
                # Adicionar tarefas trocadas
                self.jobs.append(task_b)

                target_machine.jobs.append(task_a)

                # Atualizar custos e slots
                self.total_cost = sum(job.cost for job in self.jobs)
                target_machine.total_cost = sum(job.cost for job in target_machine.jobs)
    
class Data:
    def __init__(self, machines: list[Machine], jobs: list[Task], precedences: dict):
        self.machines = machines
        self.task = jobs
        self.precedences = precedences
    


