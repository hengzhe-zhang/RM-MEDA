import matplotlib.pylab as plt
from pygmo import *
from pygmo.core import problems, population, algorithm

from RMMEDA import rm_meda

prob = problems.zdt(1)  # creating a problem here we used zdt1
# prob = problems.dtlz(3)
# prob = problem.kur()
# prob = problem.fon()
# prob = problem.cec2009(1)
# prob = problem.cassini_1(objectives=2)
pop = population(prob, 20)
alg = algorithm(rm_meda(gen=100, K=5))
pop = alg.evolve(pop)
ax = plot_non_dominated_fronts(pop.get_f())
plt.show()
