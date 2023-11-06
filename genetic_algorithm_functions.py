import numpy as np
import random
# Function returning array of P-size sequences that are created using permutation.
# x - x coordinates of cities (for defining the size); P - size of initial population.
def Create_Initial_Population(x,P):
    Initial_Population = (-1)*np.ones((len(x), P))
    for i in range(P):
        Initial_Population[:, i] = np.random.permutation(len(x))
    
    return Initial_Population


# Function for calculating the costs between the cities in the given sequences (euclidean distance).
# x - x coordinates of cities; y - y coordinates of cities.
def Calculate_Cost(Initial_Population,x,y):
    vector_of_costs = []
    last_index = len(x)-1
    for i in Initial_Population.T:
        # it is important to also calculate the distance between the first and the last city (point) 
        # (in the total cost of each sequance the return has to be included):
        cost = np.sqrt(np.power((x[int(i[0])] - x[int(i[last_index])]), 2) + np.power((y[int(i[0])] - y[int(i[last_index])]), 2))
        
        for j in range(len(i)-1):
            
            if j < len(i):
                cost = cost + np.sqrt(np.power(x[int(i[j])] - x[int(i[j + 1])], 2) + np.power(y[int(i[j])] - y[int(i[j + 1])], 2))


        vector_of_costs.append(cost)
    vector_of_costs = np.array(vector_of_costs)
    Initial_Population_with_Costs = np.copy(Initial_Population)
    
    Initial_Population_with_Costs = np.append(Initial_Population_with_Costs, [vector_of_costs], axis = 0)
    
    return vector_of_costs, Initial_Population_with_Costs


# Function for choosing the (n*100)% of obtained sequences based on the cumulative sum of probability of total costs and randomly generated threshold.
# n - coefficient for limiting the number of parents and offspring.
def Select_Parents(Initial_Population_with_Costs,n):
    last_index = len(Initial_Population_with_Costs)-1
    
    
    vector_of_costs = np.copy(Initial_Population_with_Costs[last_index,:])

    fi_costs = 1/vector_of_costs
    vector_of_probability_cost = fi_costs/np.sum(fi_costs)

    Initial_Population_with_Costs_and_Probability = np.copy(Initial_Population_with_Costs)

    Initial_Population_with_Costs_and_Probability = np.append(Initial_Population_with_Costs_and_Probability, [vector_of_probability_cost], axis = 0)

    # now it is necessary to sort the columns (sequences) by the values in the last row (probability costs)
    Initial_Population_with_Costs_and_Probability = Initial_Population_with_Costs_and_Probability[:, Initial_Population_with_Costs_and_Probability[last_index+1,:].argsort()]


    row_size, column_size = Initial_Population_with_Costs_and_Probability.shape
    Selected_Parents = (-1)*np.ones((last_index,int(n*column_size)))
    for i in range(int(n*column_size)):
        threshold = random.uniform(0,0.95) # range [0,1] caused problem with following constraints 
                                            # (because of the rounded values the sum of all probability costs was slightly smaller than 1)
        cumulative_cost = 0.0
        for j in range(column_size):
            if cumulative_cost < threshold:
                cumulative_cost = cumulative_cost + Initial_Population_with_Costs_and_Probability[last_index+1, j]
                
            else:
                Selected_Parents[:,i] = Initial_Population_with_Costs_and_Probability[:last_index, j]
                
                break

    return Selected_Parents
# Selected_Parents = Select_Parents(Initial_Population_with_Costs,n)


# Crossover operator function (repeated untill (n*P) sequences of offspring are obtained).
def Crossover_Operator(Selected_Parents,n,P):
    # The algorithm is repeated until (n*P) offsprings' sequences are obtained
    # (and because array Selected_Parents has (n*P) length there is no need to input those as arguments);
    
    row_size, column_size = Selected_Parents.shape
    Offsprings = (-1)*np.ones((row_size, column_size)) 
        
    # During each algorithm call two sequences of parents are chosen randomly from the Selected_Parents array

    for i in range(int(n*P)):
        parent_1 = Selected_Parents[:, (np.random.randint(0, (int(n*P))))].astype(int)
        parent_2 = Selected_Parents[:, (np.random.randint(0, (int(n*P))))].astype(int)
        Single_Offspring = (-1)*np.ones(row_size).astype(int)   
        
        Single_Offspring[0] = parent_1[0]
        stop_condition = int(parent_2[0])

        while True:
            indexing = np.where(parent_1==stop_condition)
            index = indexing[0]
            Single_Offspring[index] = parent_1[parent_1==stop_condition]
            [stop_condition] = parent_2[parent_1==stop_condition]
            indexing = (np.where(parent_1==stop_condition))
            index = indexing[0]
            
            if Single_Offspring[index] != -1:
                break
            
           
        for j in range(len(Single_Offspring)):
            if Single_Offspring[j] == -1:
                Single_Offspring[j] = parent_2[j]
        Offsprings[:, i] = Single_Offspring
        
    return Offsprings

# Offsprings = Crossover_Operator(Selected_Parents,n,P)



# Implementation of mutation with (p_m*100)% of accuring in the population.
def Mutation_Operator(p_m, Offsprings):
    last_index = len(Offsprings)-1
    Offsprings_with_Mutation = np.copy(Offsprings).astype(int)

    row_size, column_size = Offsprings_with_Mutation.shape

    indexing = np.random.uniform(0, column_size, int(p_m*column_size)).astype(int)
    for i in indexing:
        zm1 = random.randint(0,last_index)
        zm2 = random.randint(0,last_index)
        val1 = Offsprings_with_Mutation[zm1,i]
        val2 = Offsprings_with_Mutation[zm2,i]
        Offsprings_with_Mutation[zm1,i] = val2
        Offsprings_with_Mutation[zm2,i] = val1
    
    return Offsprings_with_Mutation
    
# Offsprings_with_Mutation = Mutation_Operator(p_m,Offsprings)


