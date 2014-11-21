from random import choice, randint, sample, shuffle, random
from time import asctime as time
from sys import argv

def random_individual(size):
    return [randint(0, 1) for i in range(size)]

def fitness(individual):
    return sum(individual)

def select_parents(population):
    parents = []
    for i in range(10):
        sample_parents = sample(population, 3)
        fit_parents = [(fitness(parent), parent) for parent in sample_parents]
        fit_parents.sort(reverse = True)
        parents.append(fit_parents[0][1])
    return parents

def get_parent_pairs(parents):
    pairs = []
    shuffle(parents)
    for i in xrange(0, len(parents), 2):
        pairs.append([parents[i], parents[i + 1]])
    return pairs

def crossover(pair):
    i = randint(0, len(pair[0]) - 1)
    j = randint(0, len(pair[0]) - 1)
    if i < j:
        return [pair[0][:i] + pair[1][i:j] + pair[0][j:], pair[1][:i] + pair[0][i:j] + pair[1][j:]]
    else:
        return [pair[0][:j] + pair[1][j:i] + pair[0][i:], pair[1][:j] + pair[0][j:i] + pair[1][i:]]

def get_offsprings(pairs, cp):
    offsprings = []
    while len(offsprings) < POPULATION_SIZE:
        for p in pairs:
            r = random()
            if r < cp:
                offsprings.append(crossover(p))
            else:
                offsprings.append(p)
    return offsprings

def mutate(individual, mr):
    i = 0
    for b in individual:
        r = random()
        if r < mr:
            if b == 1:
                individual[i] = 0
            else:
                individual[i] = 1
        i += 1
    return individual

def get_mutation(offsprings, mr):
    mutated = []
    for o in offsprings:
        mutated.append(mutate(o[0], mr))
        mutated.append(mutate(o[1], mr))
    return mutated

if __name__ == '__main__':
    INDIVIDUAL_SIZE = 64
    POPULATION_SIZE = 50
    CROSSOVER_PROBABLITY = 0.5
    MUTATION_RATE = 0.05
    MAX_GENERATIONS = 200

    if len(argv) < 2:
        ITERATIONS = 50
    else:
        ITERATIONS = int(argv[1])

    OPTIMAL = [1] * INDIVIDUAL_SIZE
    f = open("result.txt", "w")
    f.write("GA log")
    f.close()
    result = []
    for j in range(ITERATIONS):
        POPULATION = [random_individual(INDIVIDUAL_SIZE) for i in range(POPULATION_SIZE)]
        parents = select_parents(POPULATION)
        i = 0
        while ( (i != MAX_GENERATIONS) and (parents[0] != OPTIMAL)):
            pairs = get_parent_pairs(parents)
            offsprings = get_offsprings(pairs, CROSSOVER_PROBABLITY)
            mutated = get_mutation(offsprings, MUTATION_RATE)
            fit_parents = [(fitness(o), o) for o in mutated]
            fit_parents.sort(reverse = True)
            parents = [p[1] for p in fit_parents][:10]
            for p in parents:
                print p
            print "==================== {0} =================".format(i)
            i += 1
        if parents[0] == OPTIMAL:
            f = open("result.txt", "a")
            f.write("\nGeneration number where we reached success: {0} \n Iteration {1}\n".format(i, j))
            f.close()
            result.append([i, j])
    maximum = max(result, key=lambda r:result[0])
    minimum = min(result, key=lambda r:result[0])
    average = 0
    for r in result:
        average += result[0]
    average = average / len(result)
    f = open("result.txt", "a")
    f.write("\nMaximum generation reached: {0} \n Minimum generation reached: {1} \n Average generation reached {2}\n".format(maximum, minimum, average)
