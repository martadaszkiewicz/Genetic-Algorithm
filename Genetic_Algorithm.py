import numpy as np
import matplotlib.pyplot as plt
import time
from genetic_algorithm_functions import Create_Initial_Population, Calculate_Cost, Select_Parents, Crossover_Operator, Mutation_Operator

def Genetic_Algorithm(x, y, P, n, p_m):
    last_index = len(x)-1
    start_time = time.process_time()

    Initial_Population = Create_Initial_Population(x,P)
    for i in range(1000):
        
        vector_of_costs, Initial_Population_with_Costs = Calculate_Cost(Initial_Population, x, y)
        
        Selected_Parents = Select_Parents(Initial_Population_with_Costs, n)
        
        Offsprings = Crossover_Operator(Selected_Parents,n,P)
        
        Offsprings_with_Mutation = Mutation_Operator(p_m, Offsprings)
        
        Final_Population = np.copy(Initial_Population)
        Final_Population_of_all = np.concatenate((Final_Population, Offsprings_with_Mutation), axis=1)
        

        vector_of_final_costs, Final_Population_with_Costs = Calculate_Cost(Final_Population_of_all, x, y)

        # sorting the sequences by the costs (distances)
        Final_Population_to_read = np.copy(Final_Population_with_Costs[:, Final_Population_with_Costs[last_index+1, :].argsort()])
        
        Initial_Population = np.copy(Final_Population_to_read[:last_index+1, :P])

    end_time = time.process_time()
    
    return np.around(Final_Population_to_read[last_index+1, 0],7), Final_Population_to_read[:last_index+1, 0].astype(int), end_time-start_time


# cost, sequence, time_to_process = Genetic_Algorithm(x, y, P, n, p_m)

