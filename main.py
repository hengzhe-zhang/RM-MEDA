import matplotlib.pylab as plt
from pygmo import plot_non_dominated_fronts
from pygmo.core import population, problems

from RMMEDA import *

prob = problems.zdt(1)  # creating a problem here we used zdt1
# prob = problems.dtlz(3)
# prob = problem.kur()
# prob = problem.fon()
# prob = problem.cec2009(1)
# prob = problem.cassini_1(objectives=2)
pop = population(prob, 20)

alg = rm_meda(gen=100, K=5)
pop = alg.evolve(pop)
# prob.plot(pop)
ax = plot_non_dominated_fronts(pop.get_f())
plt.show()
