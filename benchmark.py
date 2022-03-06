from multiprocessing import Pool

import numpy as np
import pandas as pd
from pygmo.core import *
from sklearn.model_selection import ParameterGrid

from RMMEDA import rm_meda

pop_size = 200
problems = [1, 2]


# We declare empty arrays for storing the p-distance and mean crowding distance values for all
# the algorithms and problems over 10 runs:
def benchmark_task(parameter):
    j, algorithm_name = parameter['problem'], parameter['algorithm_name']
    # p-distance
    p_dist_nspso_cd_zdt1 = []
    # crowding distance
    mean_cd_nspso_cd_zdt1 = []
    # 1. We declare the problem (either ZDT1 or ZDT2):
    if j == 'ZDT-1':
        udp = zdt(prob_id=1)
    elif j == 'ZDT-2':
        udp = zdt(prob_id=2)
    elif j == 'ZDT-3':
        udp = zdt(prob_id=3)
    else:
        raise Exception

    generation = 100
    if algorithm_name == 'NSPSO':
        algorithm_obj = nspso(gen=generation, omega=0.001, c1=2.0, c2=2.0, chi=1.0, v_coeff=0.5,
                              leader_selection_range=100,
                              diversity_mechanism='crowding distance', memory=False, seed=20)
    elif algorithm_name == 'NSGA-II':
        algorithm_obj = nsga2(gen=generation, cr=0.9, m=1 / 30, eta_c=20, eta_m=20, seed=20)
    elif algorithm_name == 'MOEA/D':
        algorithm_obj = moead(gen=generation, CR=0.9, eta_m=20, seed=20)
    elif algorithm_name == 'RM-MEDA':
        algorithm_obj = rm_meda(gen=generation, K=5)
    elif algorithm_name == 'MACO':
        algorithm_obj = maco(gen=generation)
    else:
        raise Exception
    # algorithm_obj = rm_meda(gen=100, K=5)

    for ii in range(0, 10):
        # 2. We declare the three populations to be evolved:
        pop_1 = population(prob=udp, size=pop_size, seed=ii + 3)

        # 3. We declare the algorithms to be used: NSPSO with crowding distance, NSPSO with niche count and NSGA-II:
        algo = algorithm(algorithm_obj)
        # if not isinstance(algorithm_obj, rm_meda):
        #     algo = algorithm(algorithm_obj)
        # else:
        #     algo = algorithm_obj

        # 4. We evolve the populations for the three algorithms:
        pop_1 = algo.evolve(pop_1)

        # This returns the first (i.e., best) non-dominated front:
        nds_nspso_cd = non_dominated_front_2d(pop_1.get_f())

        # We store all the non-dominated fronts crowding distances, for all the algorithms:
        cd_nspso_cd = crowding_distance(pop_1.get_f()[nds_nspso_cd])

        # 5. We compute the p-dist and store it in a vector, for each problem and each algorithm:
        # We gather the crowding distance means:
        mean_cd_nspso_cd_zdt1.append(np.mean(cd_nspso_cd[np.isfinite(cd_nspso_cd)]))
        # And the p-distance values:
        p_dist_nspso_cd_zdt1.append(udp.p_distance(pop_1))

    return {
        'problem': j,
        'algorithm': algorithm_name,
        'p-distance': f'%.3f (%.3f)' % (np.nanmean(p_dist_nspso_cd_zdt1), np.nanstd(p_dist_nspso_cd_zdt1)),
        'crowding distance': f'%.3f (%.3f)' % (np.nanmean(mean_cd_nspso_cd_zdt1), np.nanstd(mean_cd_nspso_cd_zdt1)),
    }


# We run the algos ten times each, and we store p-distance and crowding distance
result = Pool().map(
    benchmark_task, ParameterGrid({
        'problem': ['ZDT-1', 'ZDT-2', 'ZDT-3'],
        'algorithm_name': ['NSGA-II', 'MOEA/D', 'RM-MEDA', 'NSPSO', 'MACO']
    })
)

# 6. We print the results:
df = pd.DataFrame(result)
print(pd.pivot_table(df, 'p-distance', 'problem', 'algorithm', aggfunc=lambda x: ' '.join(x)).to_markdown())
print(pd.pivot_table(df, 'crowding distance', 'problem', 'algorithm', aggfunc=lambda x: ' '.join(x)).to_markdown())
