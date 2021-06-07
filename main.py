import numpy as np
import random


popSize = 50
chromSize = 4
iteration = 100
crossoverProb = 0.9
mutationProb = 0.1

## Gen 
# 4 gen stores 4 green light ratio
population = dict()
popFitness = dict()
refs = {
    "p1":(553+533+1210+1152)/6347,
    "p2":(426+406)/6347,
    "p3":(392+282+373)/6347,
    "p4":(375+269+356)/6347,
}

for i in range(50):
    population[i] = list(np.random.dirichlet(np.ones(chromSize),size=1).flatten())



## Fitnees Function
# fittest choromosome will have a lowest fitness value 
# ref is  the  ratio of  critical  flow  ratio  to  the  total  of  critical  flow  ratio.  
# [x-ref]
def fitnessEvaluate(population):
    tempPopFitness={}
    for key, chrom in population.items():
        ft = 0
        for gen, phase in enumerate(refs.keys()):
            ft += abs(chrom[gen] - refs[phase])
        tempPopFitness[key] = ft
    return tempPopFitness

## Selection 
# Rank selection
def parentSelection():
    parents=[]
    indicies=[]
    i=0
    while i<2:
        pick = random.randint(0, len(population)-1)
        if pick not in indicies:
            indicies.append(pick)
            i=i+1

    return indicies


##Crossover 
# offspring1 = [a*parent1]+[(1-a)*parent2]
# offspring2 = [(1-a)*parent1]+[a*parent2]
# a is between 0-1
#probility 0.9
def crossoverAndMutation(parents):
    #Uniform Wheel Selection
    male = population[parents[0]]
    female = population[parents[1]]
    childs = [[],[]]
    cProb = random.random()
    if cProb <= crossoverProb:
        alpha = random.random()
        for i in range(chromSize):
            childs[0].append( (alpha * male[i]) + ((1-alpha) * female[i]) )
            childs[1].append( (alpha * female[i]) + ((1-alpha) * male[i]) )
    else:
        childs[0] = male
        childs[1] = female

    ## Mutaiton
    # probility  0.1
    for child in childs:
        for i in range(2):
            mProb = random.random()
            if mutationProb > mProb:
                mutationChromosome = list(np.random.dirichlet(np.ones(chromSize),size=1).flatten())
                alpha = random.random()
                for gen in range(chromSize):
                    childs[i][gen] = ( (alpha * mutationChromosome[gen]) + ((1-alpha) * mutationChromosome[gen]) )

    return childs


def evolve_population():
    parents = parentSelection()
    childs = crossoverAndMutation(parents)
    tempPopulation = {
        0:population[parents[0]],
        1:population[parents[1]],
        2:childs[0],
        3:childs[1],
        }
    tempPopulationFitness = fitnessEvaluate(tempPopulation)
    tempPopulationFitness = {k: v for k, v in sorted(tempPopulationFitness.items(), key=lambda item: item[1])}
    population[parents[0]] = tempPopulation[list(tempPopulationFitness.keys())[0]]
    population[parents[1]] = tempPopulation[list(tempPopulationFitness.keys())[1]]

if __name__ == "__main__":
    iters = 0
    popFitness = fitnessEvaluate(population)
    popFitness = {k: v for k, v in sorted(popFitness.items(), key=lambda item: item[1])}
    best = max(list(popFitness.values()))
    while iters < iteration:
        evolve_population()
        popFitness = fitnessEvaluate(population)
        popFitness = {k: v for k, v in sorted(popFitness.items(), key=lambda item: item[1])}
        best = max(list(popFitness.values()))
        print("{0} -> {1}".format(iters+1, best ))
        iters += 1
    
    bestPop = population[list(popFitness.keys())[0]]
    print("\n{0} -> {1}\n".format(iters, bestPop) )

## Model

## Traffic Phase and Signal
# process 120 sec
# 2 sec delay between phases(yellow signals)
# Every phase has total 40sec and yellow has 2 second
# So 38 * bestPop[phase] = green light time

print("IRL Current Signals")
ratios = [0.365,0.144,0.260,0.231]
for i in range(4):
    gls = 38*ratios[i]
    print("Phase:{0}\n-Green Light Time: {1} \n-Red Light Time: {2} \n-Yellow Light Time: {3} \n".format(i+1, gls, 38-gls, 2) )

print("Final Population Signals")
for i in range(4):
    gls = 38*bestPop[i]
    print("Phase:{0}\n-Green Light Time: {1} \n-Red Light Time: {2} \n-Yellow Light Time: {3} \n".format(i+1, gls, 38-gls, 2) )
