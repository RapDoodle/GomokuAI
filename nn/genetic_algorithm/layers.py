import numpy as np

from nn.layers import Input, Dense

class GAInput(Input):

    def __init__(self, units):
        super().__init__(units)

    def mutate(self, mutation_rate):
        return

    def crossover(self, mate_W, mate_b):
        return


class GADense(Dense):

    def __init__(self, units, activation, use_bias = True):
        super().__init__(units, activation, use_bias)
        self.reward = 0

    def mutate(self, mutation_rate):
        # Get the probability of mutation for each weight
        W_mutation_mask = np.random.rand(self.W.shape[0], self.W.shape[1])
        b_mutation_mask = np.random.rand(self.b.shape[0], self.b.shape[1])

        # Determine which weight to mutate
        W_mutation_mask = np.where(W_mutation_mask < mutation_rate,
                                    (np.random.rand() - 0.5) / 2, 0)
        b_mutation_mask = np.where(b_mutation_mask < mutation_rate,
                                    (np.random.rand() - 0.5) / 2, 0)
        
        # Update the weights
        self.W = self.W + W_mutation_mask
        self.b = self.b + b_mutation_mask

    def crossover(self, mate_W, mate_b):
        W_crossover_mask = np.random.rand(self.W.shape[0], self.W.shape[1])
        b_crossover_mask = np.random.rand(self.b.shape[0], self.b.shape[1])

        W_crossover_mask = np.where(W_crossover_mask >= 0.5, 1, 0)
        b_crossover_mask = np.where(b_crossover_mask >= 0.5, 1, 0)

        W_crossover_mask_invert = np.where(W_crossover_mask == 1, 0, 1)
        b_crossover_mask_invert = np.where(b_crossover_mask == 1, 0, 1)

        # Apply the invert mask on self.W and self.b
        self.W = self.W * W_crossover_mask_invert
        self.b = self.b * b_crossover_mask_invert

        # Apply the mask on mate_W and mate_b
        self.W = self.W + mate_W * W_crossover_mask
        self.b = self.b + mate_b * b_crossover_mask

class GAOutput(GADense):

    def __init__(self, units, activation, use_bias = True):
        super().__init__(units, activation, use_bias)