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
        self.slots = 0
        self.total_cost = 0
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def add_job(self, job):
        if job.machine is None:
            if self.slots != 0:
                self.jobs.append(job)
                job.assign_machine(self.key)
                self.total_cost = self.total_cost + job.cost
                self.slots = self.slots - 1
                print(f'Job: {job.task_id} assign in Machine: {self.key}')
    
    def __len__(self) -> int:
        return super().__len__()

class Data:
    def __init__(self, machines: list[Machine], jobs: list[Task], precedences: dict):
        self.machines = machines
        self.task = jobs
        self.precedences = precedences
       
def pin_job(job:Task,machine:Machine, job_list:list[Task]):
    if machine.slots != 0:
        machine.add_job(job)
        job_list.remove(job)

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

    def _create_solution(self, machines: list[Machine], jobs :list[Task],precendence_list):
        random.seed(self.seed)
        aux_job_list = jobs.copy()
        aux_machines = TaskListClass(machines.copy())

        DivMod = divmod(len(jobs),len(machines))

        div,resto = DivMod[0],DivMod[1]

        for mch in aux_machines: 
            mch.slots = div
            if aux_machines.is_last(mch):
                mch.slots = div+resto            
        
        print(aux_job_list)
        for machine in aux_machines:

            for task in precendence_list.values():             
                pred,succ = task[0],task[1]

                if succ.pred not in aux_job_list:
                    for job in succ.pred:
                        if job.machine is None:
                            pin_job(job,machine,aux_job_list)
                            
                if succ.succ == []:             
                    for job in succ.pred:
                        if job.machine is None:                     
                            pin_job(job,machine,aux_job_list)
                        else:
                            if succ not in aux_job_list: break
                            pin_job(succ,machine,aux_job_list)



                




                    
                    


                    


                
    
                    
                
                
    

