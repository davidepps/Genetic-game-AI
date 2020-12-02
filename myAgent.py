from copy import deepcopy
from random import random, randrange

import numpy as np

playerName = "myAgent"
nPercepts = 75  # This is the number of percepts
nActions = 7  # This is the number of actionss


class MyCreature:
    # initialises a creature with a set of chromosomes

    def __init__(self):
        # generates a set of chromosomes randomly for a new creature
        self.chromosome = list()
        for i in range(nPercepts * nActions):
            self.chromosome.append(randrange(-100, 100, 1))

    # takes a given agent and set of precepts
    # returns a list of floats to determine which action is best
    # generates actions by multiplying a given creatures chromosomes with the pertinent
    # precepts and summing the result

    def AgentFunction(self, percepts):
        # flatten precept 2d array to make calculation easier
        perceptsFlat = percepts.flatten()
        actions = np.zeros((nActions))
        # for all actions NB 1-8 so as to not multiply by zero in later arithmetic
        # is in reality 0-7
        for i in range(1, 8):
            # same true as above
            # for all precepts
            for j in range(1, 76):
                # for a given action sum all of the 75 chromosomes for that action multiplied by the set of precepts
                actions[i - 1] += self.chromosome[j * i - 1] * perceptsFlat[j - 1]
        return actions

    # from an old generation returns a new set of creatures by performing tournament selection and cross over

def newGeneration(old_population):
    N = len(old_population)

    # Fitness for all agents
    fitness = np.zeros((N))

    # for every creature generate a fitness score
    for n, creature in enumerate(old_population):
        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies

        # more information regarding fitness function in the report but size is a product of strawb and enemy eats
        # ergo to include both as well may muddy thw waters and to win survival is key hence the double multiplier

        fitness[n] = creature.turn *  creature.size
        if creature.alive:
            fitness[n] *= 2

    new_population = list()
    # for length of old pop populate a new generation
    for n in range(N):

        # Create new creature
        new_creature = MyCreature()
        # two separate tournaments generate the 2 parents
        candidates1 = list()
        candidates2 = list()
        # chooses 10` indexes and random
        for i in range(8):
            candidate = randrange(0, N - 1)
            candidates1.append(candidate)
            candidate = randrange(0, N - 1)
            candidates2.append(candidate)

        # finds the fittest candidate in each array and mixes them to form a child
        for j in range(8):
            # define parents by thier index
            parent1 = candidates1[0]
            parent2 = candidates2[0]
            if fitness[candidates1[j]] > fitness[parent1]:
                parent1 = candidates1[j]
            if fitness[candidates2[j]] > fitness[parent2]:
                parent2 = candidates2[j]
        #split the chromosome at a random point in the list
        split = randrange(0, nPercepts * nActions)
        chromosome = list()
        # takes a random amount of the chromosomes from first then second parent by split
        for i in range(nPercepts * nActions):
            mutate = randrange(1, 10)
            # handles chance of mutation generating an entirely new chromosome[i]
            if mutate == 1:
                chromosome.append(randrange(-100, 100))
            elif i < split:
                chromosome.append(old_population[parent1].chromosome[i])
            else:
                chromosome.append(old_population[parent2].chromosome[i])
        # deepcopy() assures we copy all the information and not just a pointer
        new_creature.chromosome = deepcopy(chromosome)
        # Add the new agent to the new population
        new_population.append(new_creature)

    avg_fitness = np.mean(fitness)

    return (new_population, avg_fitness)
