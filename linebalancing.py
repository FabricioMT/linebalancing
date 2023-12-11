import sys
from timeit import default_timer as timer
from datetime import timedelta
from os import listdir
from heuristic.data_types import *
from heuristic.local_find import *
from heuristic.grasp import *

def assign_data(file_path,num_machines):
    with open(file_path, 'r') as file:
        input_data = file.readlines()

    pair_cost = {}
    num_tasks = int(input_data[0])
    precedences_sequence = {}
    task_list = [Task(i+1) for i in range(num_tasks)]
    machines = [Machine(i+1) for i in range(num_machines)]

    precedences = [tuple(map(Task, pair.split(','))) for pair in input_data[num_tasks+1:-1]]
    processing_times = list(map(int, input_data[1:num_tasks+1]))
    
    for task,time in zip(task_list,processing_times): task.assign_cost(time)
    tasks_dict = {task.task_id: task for task in task_list}
    
    for i,pair in enumerate(precedences): 
        task1,task2 = pair
        task1 = tasks_dict[task1.task_id]
        task2 = tasks_dict[task2.task_id]
        task1.add_successor(task2)
        task2.add_predecessor(task1)
        precedences_sequence[i+1] = (task1,task2)
    
    for i,tasks in precedences_sequence.items():
        tasks[0].cost = processing_times[tasks[0].task_id-1]
        tasks[1].cost = processing_times[tasks[1].task_id-1]
        pair_cost[i] = (tasks[0].cost + tasks[1].cost)

    

    return Data(machines,task_list,precedences_sequence)    

def readArgs():
    if len(sys.argv) > 1:
        arq = 0
        n_machine = int(sys.argv[2])
        file_input = listdir('./inputs/')

        if n_machine >= 1:
            pass
        else:
            print("Número de Maquinas muito baixo !")
            n_machine = 1
            print("Número de Maquinas set default = 6.")
        
        for file in file_input:
            if file == sys.argv[1]:
                arq = 'inputs/' + sys.argv[1]
        
        args = sys.argv[1:]
        print(f"Arguments count: {len(sys.argv)}")
        print(f"Arguments of the script : {args}")
        if arq == 0:
            print("Arquivo não encontrado nos Inputs ou Arquivo com nome Inválido !")
            exit(1) 
    else:
        print("Entrada de Dados Inválida !")
        exit(1)
    return arq, n_machine

def calculate_makespan(machines:list[Machine]):
    return max([machine.total_cost for machine in machines])

def printdata(Data: Data):
    #print('Maquinas:',Data.machines)
    for task in Data.task: print(f'Tarefa {task.task_id}: Custo = {task.cost} Pred = {[pred.task_id for pred in task.pred]} Suces = {[succ.task_id for succ in task.succ]}')
    print('\n')
    for machine in Data.machines: print(f'Maquina: [{machine.key}] Tarefas Atendidas: {machine.jobs}\nCusto total da Maquina: {machine.total_cost}')
    print('\n')
    print('FO:',calculate_makespan(Data.machines))
    print('\n')



if __name__ == '__main__':

    start = timer()
    tempo_corrido = timedelta(seconds=start)
    inputs, n_machine = readArgs()

    data = assign_data(inputs,n_machine)
    initSol = Create_init_solution(data)

    printdata(initSol)
    
    grasp = GRASP(initSol)
    
    #GRAP MAX TIME: EM MINUTOS
    grasp.execute(1)
    printdata(grasp.data)
    end = timer()
    timing = timedelta(seconds=end-start)
  
    print(f"\n Tempo de Execução: {timing.microseconds} Micro Seconds\n")

