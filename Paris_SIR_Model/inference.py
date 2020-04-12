import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
STATES = ["S", "I"]

def get_infection_probas(probas, transmissions, mstates):
    """
    - probas[i,s] = P_s^i(t)
    - transmissions = array/list of i, j, lambda_ij
    - infection_probas[i]  = sum_j lambda_ij P_I^j(t)
    """
    N = probas.shape[0]
    infection_probas = np.zeros(N)
    print("transmissions", transmissions)
    rates= np.array([])
    for i in range(N):
        for i0, j, rate in transmissions:
            for k in range(len(transmissions)):
                if i0 == transmissions[k][0]:
                    j1 = transmissions[k][1]
                    for j2 in range(len(mstates[0])):
                        if mstates[0][j2][0] == j1:
                            rates = np.concatenate([probas[j2, 1]*rate], axis = None)
        srate = 0
        for s in range(len(rates)):
            srate += rates[s]
        infection_probas[i] = srate
    return infection_probas


def propagate(probas, infection_probas):
    """
    - probas[i,s] = P_s^i(t)
    - infection_probas[i]  = proba that i get infected (if susceptible)
    - recover_probas[i] = proba that i recovers (if infected)
    """
    next_probas = np.zeros_like(probas)
    next_probas[:, 0] = probas[:, 0]*(1 - infection_probas)
    next_probas[:, 1] = probas[:, 1]*(1) + probas[:, 0]*infection_probas
    #next_probas[:, 2] = probas[:, 2] + probas[:, 1]*recover_probas
    print("next_probas", next_probas[:, 1])
    return next_probas


class InferenceModel():
    def __init__(self, initial_probas, mstates):
        self.N = len(initial_probas)
        self.initial_probas = initial_probas
        self.mstates = mstates

    def time_evolution(self, transmissions,print_every=10):
        """Run the simulation where
        - recover_probas[i] = mu_i time-independent
        - transmissions[t] = list of t, i, j, lambda_ij(t)
        - probas[t, i, s] = state of i at time t
        """
        # initialize states
        T = len(transmissions)
        probas = np.zeros((T + 1, self.N, 2))
        probas[0] = self.initial_probas
        # iterate over time steps
        for t in range(T):
            if (t % print_every == 0):
                print(f"t = {t} / {T}")
            infection_probas = get_infection_probas(probas[t], transmissions[t], self.mstates)
            probas[t+1] = propagate(probas[t], infection_probas)
        self.probas = probas
        # print("probas", self.probas)
        self.states = probas.argmax(axis=2)
        # print("states", self.states)
        
    def get_counts(self):
        counts = self.probas.sum(axis=1)
        return pd.DataFrame(counts, columns=STATES)