import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

STATES = ["S", "I"]

def get_infection_probas(states, transmissions):
    """
    - states[i] = state of i
    - transmissions = array/list of i, j, lambda_ij
    - infection_probas[i]  = 1 - prod_{j: state==I} [1 - lambda_ij]
    """
    print("states:",states)
    print("transmissions", transmissions)
#     infected = (states == 1)
#     print("infected:",infected)
    N = len(states)
    infection_probas = np.zeros(N)
 
    for i in range(N):
        rates = np.array([rate for i0,j,rate in transmissions
                            if states[i][0]==i0 and states[i][1] == 1])
        infection_probas[i] = 1 - np.prod(1 - rates)
    print("infection_probas:", infection_probas)
    return infection_probas 


def propagate(current_states, infection_probas):
    """
    - current_states[i] = state of i
    - infection_probas[i]  = proba that i get infected (if susceptible)
    - recover_probas[i] = proba that i recovers (if infected)
    """
    next_states = [[None]*2]*len(current_states)
    
    
#     next_states = np.zeros_like(current_states)
    for i in range(len(current_states)):
        if (current_states[i][1] == 0):
            infected = np.random.rand() < infection_probas[i]
            current_states[i][1] = 1 if infected else 0
#         elif (current_states[i][1] == 1):
#             recovered = np.random.rand() < recover_probas[i]
#             current_states[i][1] = 2 if recovered else 1
        else:
            current_states[i][1] = 1
    return current_states


class EpidemicModel():
    def __init__(self, initial_states):
        self.N = len(initial_states)
        self.initial_states = initial_states

    def time_evolution(self, transmissions, print_every):
        """Run the simulation where
        - recover_probas[i] = mu_i time-independent
        - transmissions[t] = list of t, i, j, lambda_ij(t)
        - states[t, i] = state of i at time t
        """
        # initialize states
        T = len(transmissions)
        print("initial_states:",self.initial_states)
        states = [[None]*self.N]*(T + 1)
#         print("state length", states)
        states[0] = self.initial_states
        # iterate over time steps
        for t in range(T):
            if (t % print_every == 0):
                print(f"t = {t} / {T}")
            infection_probas = get_infection_probas(states[t], transmissions[t])
            states[t+1] = propagate(states[t], infection_probas)
        self.states = states
#         self.probas = get_dummies(states)    
    
class run_model(EpidemicModel):
    def __init__(self, data, initial_states = None):
        self.data = data
        self.transmissions = self.generate_transmissions()
        
        if initial_states is None:
            initial_states = []
            duplicates = []
            for i in range(len(self.data)):
                if len(self.data[i]) != 0:
                    for j in range(len(self.data[i])):
                        initial_state_2 = []
                        initial_state_1 = []
                        if self.data[i][j]['other_human_id'] not in duplicates: 
                            if self.data[i][j]['human2_isinfected'] == True:
                                initial_state_2.append(self.data[i][j]['other_human_id'])
                                initial_state_2.append(1)
                                duplicates.append(self.data[i][j]['other_human_id'])
                            else:
                                initial_state_2.append(self.data[i][j]['other_human_id'])
                                initial_state_2.append(0)
                                duplicates.append(self.data[i][j]['other_human_id'])
                            initial_states.append(initial_state_2)
                        if self.data[i][j]['human_id'] not in duplicates: 
                            if self.data[i][j]['human1_isinfected'] == True:
                                initial_state_1.append(self.data[i][j]['human_id'])
                                initial_state_1.append(1)
                                duplicates.append(self.data[i][j]['human_id'])
                            else:
                                initial_state_1.append(self.data[i][j]['human_id'])
                                initial_state_1.append(0)
                                duplicates.append(self.data[i][j]['human_id'])
                            initial_states.append(initial_state_1)
        super().__init__(initial_states)

        
    def generate_transmissions(self):
        transmissions = []
        for i in range(len(self.data)):
#             print(self.data)
            tf = []
            for j in range(len(self.data[i])):
                if len(self.data[i]) != 0:
                    transmission = (self.data[i][j]['human_id'], self.data[i][j]['other_human_id'], self.data[i][j]['lambda'])
                    tf.append(transmission)
                else:
                    tf.append([])
            transmissions.append(tf)
#         print("transmission", transmissions)
        return transmissions
            
    def get_counts(self):
        st=[]
        for i in range(len(self.states)):
            st.append(self.states[i][1])
        a=0
        b=0
        for i in st:
            if i == 1:
                a+=1
            else:
                b+=1
        counts = {"S":b, "I":a}

        return pd.DataFrame(counts, index= [0])

    def run(self, print_every=1):
        print("Generating transmissions")
        self.generate_transmissions()
        print("Running simulation")
        self.time_evolution(
    self.transmissions, print_every=print_every
        )