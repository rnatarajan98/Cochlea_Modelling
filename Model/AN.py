import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# DOI: 10.1121/1.393460 · Source: PubMed
class Meddis1986:
    def __init__(self, num_neurons, samplerate):
        self.A = 5
        self.B = 160
        self.g = 1660
        self.r = 12500
        self.l = 500
        self.y = 16.6
        self.h = 10000

        self.c0 = 0
        self.q0 = 1
        
        self.num_neurons = num_neurons
        self.samplerate = samplerate
        self.dt = 1/samplerate
        
    def permeability(self, s):
        if s > -self.A:
            permeability = (self.g * (s + self.A)) / (s + self.A + self.B)
        else:
            permeability = 0
        return permeability
    
    def dq(self, q, c, k):
        dqdt = (self.y*(1-q)) + (self.r*c) - (k*q)
        return dqdt * self.dt
    
    def dc(self, q, c, k):
        dcdt = (k*q) - (self.l*c) - (self.r*c)
        return dcdt * self.dt
    
    def generate_spike_probabilities(self, signal):
        q = self.q0
        c = self.c0
        
        self.probs = []
        self.cell_levels = []
        self.cleft_levels = []
        self.permeabilities = []
        for i in range(len(signal)):
            k = self.permeability(signal[i])
            q = q + self.dq(q, c, k)
            c = c + self.dc(q, c, k)
            
            prob = self.h * c * self.dt
            
            self.permeabilities.append(k)
            self.cell_levels.append(q)
            self.cleft_levels.append(c)
            self.probs.append(prob)
            
    def simulate(self, signal):
        self.generate_spike_probabilities(signal)
        
        rands = np.random.rand(len(signal), self.num_neurons)
        self.spike_train = np.zeros(shape=(len(signal), self.num_neurons))
        
        for n in range(self.num_neurons):
            self.spike_train[rands[:,n] < self.probs, n] = 1
            
#         for i in range(len(signal)):
#             print(self.spike_train[i, :])
            
        gs = gridspec.GridSpec(5, 1,height_ratios=[2, 2, 2, 2, 2])
        
        ax_signal = plt.subplot(gs[0])
        ax_signal.plot(signal, color='k')
        ax_signal.set_xticks([])
        ax_signal.set_yticks([0])
        ax_signal.set_yticklabels(['Hair Cell Signal'])
        plt.grid(which='both', axis='y')    
        
        ax_permeability = plt.subplot(gs[1])
        ax_permeability.plot(self.permeabilities, color='k')
        ax_permeability.set_xticks([])
        ax_permeability.set_yticks([0])
        ax_permeability.set_yticklabels(['Cell Permeability'])
        plt.grid(which='both', axis='y')    
        
        ax_cell = plt.subplot(gs[2])
        ax_cell.plot(self.cell_levels, color='k')
        ax_cell.set_xticks([])
        ax_cell.set_yticks([0])
        ax_cell.set_yticklabels(['Transmitter level (cell)'])
        plt.grid(which='both', axis='y')    
        
        ax_cleft = plt.subplot(gs[3])
        ax_cleft.plot(self.cleft_levels, color='k')
        ax_cleft.set_xticks([])
        ax_cleft.set_yticks([0])
        ax_cleft.set_yticklabels(['Transmitter level (cleft)'])
        plt.grid(which='both', axis='y') 
        
        ax_probs = plt.subplot(gs[4])
        ax_probs.plot(self.probs, color='k')
        ax_probs.set_xticks([])
        ax_probs.set_yticks([0])
        ax_probs.set_yticklabels(['Probability of firing'])
        plt.grid(which='both', axis='y') 

        

            

            
            
            
        
    
    