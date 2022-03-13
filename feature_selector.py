import numpy as np
import pygmo as pg
from matplotlib import pyplot as plt
from pygmo.core import *

from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor

"""
Feature selection tool based on MOEA algorithms
"""


class FeatureSelectionProblem:

    def __init__(self, X, y, model) -> None:
        super().__init__()
        self.X = X
        self.y = y
        self.dim = X.shape[1]
        self.model: RandomForestRegressor = model

    # Define objectives
    def fitness(self, x):
        x = np.round(x)
        if x.sum() == 0:
            return [1, 1]
        f1 = np.sum(x)
        f2 = -1 * cross_val_score(self.model, self.X[:, x.astype(bool)], self.y)
        return [f1, np.mean(f2)]

    # Return number of objectives
    def get_nobj(self):
        return 2

    # Return bounds of decision variables
    def get_bounds(self):
        return ([0] * self.dim, [1] * self.dim)

    # Return function name
    def get_name(self):
        return "Feature Selection Problem"


class MOEASelector(SelectFromModel):
    def fit(self, X, y=None, **kwargs):
        self.problem = pg.problem(FeatureSelectionProblem(X, y, self.estimator))
        generation = 5
        pop = population(self.problem, 20)
        alg = algorithm(nsga2(gen=generation, cr=0.9, m=1 / 30, eta_c=20, eta_m=20, seed=20))
        pop = alg.evolve(pop)
        self.pf = pop.get_x()[non_dominated_front_2d(pop.get_f())]
        self.ps = pop.get_f()[non_dominated_front_2d(pop.get_f())]
        return pop


if __name__ == '__main__':
    dt = DecisionTreeRegressor()
    x, y = load_boston(return_X_y=True)
    selector = MOEASelector(dt)
    pop = selector.fit(x, y)

    obj = pop.get_f()[non_dominated_front_2d(pop.get_f())]
    obj[:, 0] = np.round(obj[:, 0])
    plt.scatter(obj[:, 0], -1 * obj[:, 1])
    plt.xlabel('Number of features')
    plt.ylabel('$R^2$ Score')
    plt.show()
