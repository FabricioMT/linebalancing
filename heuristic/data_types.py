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
    def item(self,x): return self[x]

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

class Operation:
    
    def __init__(
        self,
        machine: Any,
        job: Any,
        release=None,
    ) -> None:
        self.machine = machine
        self.job = job     
        self.duration = job.cost
        self.release = release
        #self.tail = None
        #self.critical = False
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def reset_release(self, release):
        self.release = release

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

class Graph(Data):
    def __init__(self, params: Data):
        """Graph structure to job-shop problem

        Parameters
        ----------
        params : JobShopParams
            Parameters that define the problem
        """
        super().__init__(params.machines, params.task, params.precedences)
        
        self.M = params.machines
        self.O = {}
        self.V = []
        self._start_operations()
    def restart(self):
        self.__init__(self)
    

    def _start_operations(self):
        for key,m in enumerate(self.machines):
            for key_j,j in enumerate(m.jobs):
                pass
                #print(j.cost)
                #self.O[key, j] = Operation(m, j, 0.0)    
            
                
    def precede_job(self, machine, operation):
        """Returns the operation belonging to job processed just before (machine, job)

        Parameters
        ----------
        machine : Any
            Machine key
        
        job : Any
            Job key

        Returns
        -------
        Operation
        """
        
        task1, pred1 = operation[0]
        task2, pred2 = operation[1]
        last_machine = task1[0].machine
        if last_machine is not None:
            return pred1
        else:
            machine
            return None
        
    
    def follow_job(self, machine, job):
        """Returns the operation belonging to job processed right after (machine, job)

        Parameters
        ----------
        machine : Any
            Machine key
        
        job : Any
            Job key

        Returns
        -------
        Operation
        """
        next_machine = self.seq[job].next(machine)
        if next_machine is not None:
            return self.O[next_machine, job]
        else:
            return None
    
    def precede_machine(self, machine, job):
        """Returns the operation processed on machine just before (machine, job)

        Parameters
        ----------
        machine : Any
            Machine key
        
        job : Any
            Job key

        Returns
        -------
        Operation
        """
        last_job = self.M[machine].jobs.prev(job)
        if last_job is not None:
            return self.O[machine, last_job]
        else:
            return None
    
    def follow_machine(self, machine, job):
        """Returns the operation processed on machine right after (machine, job)

        Parameters
        ----------
        machine : Any
            Machine key
        
        job : Any
            Job key

        Returns
        -------
        Operation
        """
        last_job = self.M[machine].jobs.next(job)
        if last_job is not None:
            return self.O[machine, last_job]
        else:
            return None
    
    def copy(self):
        return copy.deepcopy(self)
    
    @property
    def order(self):
        releases = np.array([o.release for o in self.O.values()])
        unordered = np.array([o.job for o in self.O.values()])
        seq = np.argsort(releases)
        order = unordered[seq]
        return order
    
    @property
    def pheno(self):
        pheno = []
        for m in self.M.values():
            pheno = pheno + m.task
        return np.array(pheno)
    
    @property
    def signature(self):
        return hash(str(self.order))
    
    # def plot(self, horizontal=True, figsize=[7, 3], dpi=100, colors=None):
    #     if horizontal:
    #         self._plot_horizontal(figsize=figsize, dpi=dpi, colors=colors)
    #     else:
    #         self._plot_vertical(figsize=figsize, dpi=dpi, colors=colors)

    # def _plot_vertical(self, figsize=[7, 3], dpi=100, colors=None):
        
    #     if colors is None:
    #         colors = self.colors
        
    #     fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    #     for i, j in enumerate(self.task):
    #         machines, starts, spans = self._get_elements(j)
            
    #         if i >= len(colors):
    #             i = i % len(colors)
            
    #         color = colors[i]
    #         ax.bar(machines, spans, bottom=starts, label=f"Job {j}", color=color)

    #     ax.set_xticks(self.machines)
    #     ax.set_xlabel("Machine")
    #     ax.set_ylabel("Time")
    #     ax.legend(loc='upper left', bbox_to_anchor=(1, 1.03))
    #     fig.tight_layout()
    #     plt.show()

    # def _plot_horizontal(self, figsize=[7, 3], dpi=100, colors=None):
        
    #     colors = self._get_colors(colors)
        
    #     fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    #     for i, j in enumerate(self.task):
    #         machines, starts, spans = self._get_elements(j)
            
    #         if i >= len(colors):
    #             i = i % len(colors)
            
    #         color = colors[i]
    #         ax.barh(machines, spans, left=starts, label=f"Job {j}", color=color)

    #     ax.set_yticks(self.machines)
    #     ax.set_xlabel("Time")
    #     ax.set_ylabel("Machine")
    #     ax.legend(loc='upper left', bbox_to_anchor=(1, 1.03))
    #     fig.tight_layout()
    #     plt.show()
    
    # def _get_colors(self, colors):
    #     if colors is None:
    #         colors = self.colors
    #     return colors
    
    # def _get_elements(self, j):
    #     print('j',j)
    #     machines = self.machines
    #     starts = [self.O[m, j].release for m in self.machines]
    #     spans = [self.O[m, j].duration for m in self.machines]
    #     return machines, starts, spans

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
        precedence = TaskListClass()
        TaskDiv =  int(len(preced)/len(machines))

        for m in machines:    
            while len(aux_job) >= 1:
                rand_job = random.choice(aux_job)      
                aux_suces = rand_job.succ.copy()

                if rand_job.pred == []:
                    #print(f'Tarefa {rand_job.task_id}: Custo = {rand_job.cost} Pred = {[pred.task_id for pred in rand_job.pred]} Suces = {[succ.task_id for succ in rand_job.succ]}')
                    m.add_job(rand_job)
                    rand_job.assign_machine(m)
                    precedence.append(rand_job)
                    aux_job.remove(rand_job)
                    break
                
                # if rand_job.succ == []:
                #     m.add_job(rand_job)
                #     rand_job.assign_machine(m)
                #     precedence.append(rand_job)
                #     aux_job.remove(rand_job)
                #     break

                if rand_job.pred in aux_job:
                    break
                else:
                    m.add_job(rand_job)
                    rand_job.assign_machine(m)
                    precedence.append(rand_job)
                    aux_job.remove(rand_job)
                    #print(jobs)
                    #print(f'Tarefa {rand_job.task_id}: Custo = {rand_job.cost} Pred = {[pred.task_id for pred in rand_job.pred]} Suces = {[succ.task_id for succ in rand_job.succ]}')
                if len(m.jobs) == TaskDiv:
                    break
        return precedence
    

