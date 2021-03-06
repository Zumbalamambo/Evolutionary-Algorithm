import numpy as np
import matplotlib.pyplot as plt

DNA_SIZE = 10            # DNA length
POP_SIZE = 100           # population size
CROSS_RATE = 0.8         # mating probability (DNA crossover)
MUTATION_RATE = 0.003    # mutation probability
N_GENERATIONS = 200
X_BOUND = [0, 5]         # x upper and lower bounds

F = lambda x: np.sin(10*x)*x + np.cos(2*x)*x     # to find the maximum of this function

# find non-zero fitness for selection
get_fitness = lambda pred: pred + 1e-3 - np.min(pred)

# convert binary DNA to decimal and normalize it to a range(0, 5)
translateDNA = lambda pop: pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / (2**DNA_SIZE-1) * X_BOUND[1]


def select(pop, fitness):    # nature selection wrt pop's fitness
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True, p=fitness/fitness.sum())
    return pop[idx]


def crossover(parent, pop_copy):     # mating process (genes crossover)
    if np.random.uniform(0, 1) < CROSS_RATE:
        i_ = np.random.choice(np.arange(POP_SIZE), size=1, replace=False)  # select another individual from pop
        cross_points = np.random.randint(0, 2, DNA_SIZE).astype(np.bool)  # choose a crossover points
        parent[cross_points] = pop[i_, cross_points]  # mating and produce one child
    return parent


def mutate(child):
    for point in range(DNA_SIZE):
        if np.random.uniform(0, 1) < MUTATION_RATE:
            child[point] = 1 if child[point] == 0 else 0
    return child


pop = np.random.randint(0, 2, (1, DNA_SIZE)).repeat(POP_SIZE, axis=0)  # initialize the pop DNA

plt.ion()       # something about plotting
x = np.linspace(*X_BOUND, 200)

for _ in range(N_GENERATIONS):
    F_values = F(translateDNA(pop))    # compute function value by extracting DNA

    # something about plotting
    plt.cla()
    plt.scatter(translateDNA(pop), F_values, s=200, lw=0, c='red', alpha=0.5); plt.plot(x, F(x))
    plt.pause(0.05)

    # evolution
    fitness = get_fitness(F_values)
    pop = select(pop, fitness)
    pop_copy = pop.copy()
    for parent in pop:
        child = crossover(parent, pop_copy)
        child = mutate(child)
        parent[:] = child       # parent is replaced its child

plt.ioff(); plt.show()