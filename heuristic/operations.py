from heuristic.data_types import *
from heuristic.data_types import Machine, Task
import copy

def pin_job(job:Task,machine:Machine, job_list:list[Task]):
    if machine.slots != 0:
        machine.add_job(job)
        job_list.remove(job)

def calculate_makespan(machines:list[Machine]):
    return max([machine.total_cost for machine in machines])

class Create_init_solution(Data):

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
                            pin_job(job,machine,aux_job_list)
                            
                if succ.succ == []:             
                    for job in succ.pred:
                        if job.machine is None:                     
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
    
    def reset_release(self, release):
        self.release = release

class Graph(Data):

    def __init__(self, Data:Data):
        super().__init__(Data.machines, Data.task, Data.precedences)
        self.M = {machine.key: machine for machine in self.machines}
        print(self.M)
        self.O = {}
        self._start()
        self.C = max([machine.total_cost for machine in self.machines])
        self.precedences = TaskListClass(self.O.keys())
        self.task = TaskListClass(Data.task)
            

    def _start(self):
        for key, machine in self.M.items():     
            for job in machine.jobs:
                self.O[key,job] = Operation(machine.key, job, release=0.0)

    def precede_job(self, machine, job):
        print('job',job)
        print('machine',machine)
        last_machine = self.task[job.task_id].prev
        print(last_machine)
        if last_machine is not None:
            return self.O[last_machine, job]
        else:
            return None
    
    def follow_job(self, machine, job):

        next_machine = self.task[job.task_id].machine
        if next_machine is not None:
            return self.O[next_machine, job]
        else:
            return None
    
    def precede_machine(self, machine, job):

        last_job = self.M[machine].jobs.prev(job)
        if last_job is not None:
            return self.O[machine, last_job]
        else:
            return None
    
    def follow_machine(self, machine, job):

        last_job = self.M[machine].jobs.next(job)
        if last_job is not None:
            return self.O[machine, last_job]
        else:
            return None
    
    def copy(self):
        return copy.deepcopy(self)
    