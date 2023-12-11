from heuristic.operations import *
from heuristic.data_types import *
from heuristic.local_find import *
import time


class GRASP:

    def __init__(self, data):
        self.data = data
        self.best_solution = None
        self.best_cost = float('inf')

    def execute(self, max_minutes):
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < max_minutes * 60:
            solution = self.construct_solution()
            self.local_search(solution)
            cost = self.calculate_makespan(solution)

            if cost < self.best_cost:
                self.best_solution = solution
                self.best_cost = cost
            elapsed_time = time.time() - start_time

    def construct_solution(self):
        sol = Create_init_solution(self.data)
        return Graph(sol)

    def local_search(self, solution):
        Solui = busca_local(solution, max_steps=5, copy=False)
        return Solui

    def calculate_makespan(self,solution):
        return max([machine.total_cost for machine in solution.machines])
