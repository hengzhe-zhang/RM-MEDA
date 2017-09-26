import numpy as np
from LocalPCA_v0 import *

def RMMEDA_operator(PopDec,K,M):
#    K = Global.ParameterSet(5);
#    PopDec = Population.decs;
    N,D  = PopDec.shape
#    M      = Global.M;
    
    ## Modeling
    Model,probability = LocalPCA(PopDec,M,K)

    ## Reproduction
    OffspringDec = np.zeros((N,D))
    # Generate new trial solutions one by one
    for i in np.arange(N):
        # Select one cluster by Roulette-wheel selection
        k = (np.where(np.random.rand()<=probability))[0][0]
        # Generate one offspring
        if not len(Model[k]['eVector'])==0:
            lower = Model[k]['a'] - 0.25*(Model[k]['b']-Model[k]['a'])
            upper = Model[k]['b'] + 0.25*(Model[k]['b']-Model[k]['a'])
            trial = np.random.uniform(1,M-1)*(upper-lower) + lower
            sigma = np.sum(np.abs(Model[k]['eValue'][M-1:D]))/(D-M+1)
            OffspringDec[i,:] = Model[k]['mean'] + trial*Model[k]['eVector'][:,:M-1].conj().transpose() + np.random.randn(1,D)*np.sqrt(sigma)
        else:
            OffspringDec[i,:] = Model[k]['mean'] + np.random.randn(1,D)

    
#    Offspring = INDIVIDUAL(OffspringDec);

    return OffspringDec
    
print RMMEDA_operator(PopDec,K,M)
