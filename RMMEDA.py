#!/usr/bin/env python

import pygmo as pg
from pygmo.core import fast_non_dominated_sorting, select_best_N_mo

from Generate import *


class rm_meda():
    """
    A custom steady-state algorithm, based on the hypervolume computation.
    """

    def __init__(self, gen=20, K=5, verbose=False):
        """
        Constructs an instance of the algorithm.

        USAGE: rm_meda(gen=10, p_m=20)

        NOTE: Evolves the population using the least contributor feature.

        * gen: number of generations
        * K: the number of manifolds
        """
        # We start by calling the base constructor
        super(rm_meda, self).__init__()
        # Store the number of generations
        self.__gen = gen
        self.__K = K
        self.verbose = verbose

    def get_all_vectors_and_fitness(self, pop):
        all_elements = []
        all_fitness = []
        lnp = len(pop)
        if len(fast_non_dominated_sorting(pop.get_f())[0][0]) != lnp:
            best_idx = select_best_N_mo(pop.get_f(), lnp - len(fast_non_dominated_sorting(pop.get_f())[0][-1]))
        else:
            best_idx = fast_non_dominated_sorting(pop.get_f())[0][0]
        for i in best_idx:
            all_elements.append(pop.get_x()[i])
            all_fitness.append(pop.get_f()[i])
        return list(zip(*all_elements)), all_elements, all_fitness

    def Modeling(self, pop):
        prob = pop.problem
        dim, cont_dim, n_obj = prob.get_ncx(), prob.get_ncx() - prob.get_nix(), prob.get_nobj()
        lb, ub = prob.get_bounds()
        # We get the variables and the objective values
        varr, List, List_fitness = self.get_all_vectors_and_fitness(pop)
        # Let us store the solutions and fitness values in arrays
        self.elements_array = np.array(List)
        self.fitness_array = np.array(List_fitness)
        return RMMEDA_operator(self.elements_array, self.__K, n_obj, lb, ub)

    def evolve(self, pop):
        if len(pop) == 0:
            return pop
        lnp = len(pop)
        # Main loop of the algorithm
        for s in range(self.__gen):
            if self.verbose:
                print('Generation: ', s)
            self.genidx = s
            new_pop = self.Modeling(pop)
            for new_x in new_pop:
                try:
                    pop.push_back(new_x)
                except ValueError:  # we don't add the solution if it violates the constraints
                    pass
            temp_pop = pg.population(pop.problem, 0)
            for id in fast_non_dominated_sorting(pop.get_f())[3].argsort()[:lnp]:
                temp_pop.push_back(x=pop.get_x()[id], f=pop.get_f()[id])
            pop = temp_pop
        return pop

    def get_name(self):
        return "RM-MEDA Algorithm"
