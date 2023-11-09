import numpy as np

def CrossoverOperator(parent1,parent2):
    parent1 = np.array(parent1)
    parent2 = np.array(parent2)

    offspring = (-1)*np.ones(len(parent1)).astype(int)

    offspring[0] = parent1[0]
    stop_condition = int(parent2[0])

    while True:
        indexing = np.where(parent1==stop_condition)
        index = indexing[0]
        offspring[index] = parent1[parent1==stop_condition]
        stop_condition = parent2[parent1==stop_condition]
        indexing = (np.where(parent1==stop_condition))
        index = indexing[0]
        
        if offspring[index] != -1:
            break
    
    for i in range(len(offspring)):
        if offspring[i] == -1:
            offspring[i] = parent2[i]
    
    return offspring
