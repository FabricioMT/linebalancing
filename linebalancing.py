import sys
from timeit import default_timer as timer
from datetime import timedelta
from os import listdir
from heuristic.data_types import *
from heuristic.local_find import *
from heuristic.grasp import *
import csv


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

def write_reports(results_3, results_5, results_11):
    # Crie um objeto de arquivo CSV
    with open('relatorio.csv', 'w', newline='') as csvfile:
        # Crie um escritor CSV
        writer = csv.writer(csvfile, delimiter=';')

        # Escreva os cabeçalhos do relatório
        writer.writerow(['Numero de Maquinas', 'Melhor FO', 'FO Media', 'Desvio (%)', 'Tempo Melhor (seg.)', 'Tempo Medio (seg.)'])
        i = [3,5,11]
        # Itere sobre os resultados de cada relatório e escreva-os no arquivo CSV
        for results in [results_3, results_5, results_11]:
            writer.writerow([i.pop(0), results[0]['Melhor FO'], results[0]['FO Media'], results[0]['Desvio (%)'], results[0]['Tempo Melhor (seg.)'], results[0]['Tempo Medio (seg.)']])

def printdata(Data: Data):
    
    #print('Maquinas:',Data.machines)
    #for task in graph.task: print(f'Tarefa {task.task_id}: Custo = {task.cost} Pred = {[pred.task_id for pred in task.pred]} Suces = {[succ.task_id for succ in task.succ]}')
    print('\n')
    #print('pair_cost:',Data.pair_cost.items())
    for machine in Data.machines: print(f'Maquina: [{machine.key}] Tarefas Atendidas: {machine.jobs}\nCusto total da Maquina: {machine.total_cost}')
    print('\n')
    print('Maior FO:',calculate_makespan(Data.machines))

    
if __name__ == '__main__':

    start = timer()
    tempo_corrido = timedelta(seconds=start)
    inputs, n_machine = readArgs()

    data3 = assign_data(inputs,3)
    grasp3 = GRASP(data3)
    results3 = grasp3.execute(0.1)
    printdata(grasp3.data)

    data5 = assign_data(inputs,5)
    grasp5 = GRASP(data5)
    results5 = grasp5.execute(0.1)
    printdata(grasp5.data)

    data11 = assign_data(inputs,11)
    grasp11 = GRASP(data11)
    results11 = grasp11.execute(0.1)
    printdata(grasp11.data)

    write_reports(results3, results5, results11)

    end = timer()
    timing = timedelta(seconds=end-start)
  
    print(f"\n Tempo de Execução: {timing.microseconds} Micro Seconds\n")

