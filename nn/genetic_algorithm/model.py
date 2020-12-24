import numpy as np
import copy

from common.exception import ModelError
from nn.genetic_algorithm.layers import GAInput, GADense, GAOutput
from nn.model import SequentialModel

class GAModel():

    def __init__(self, population):
        self.layers_blueprint = []
        self.forest = []
        self.population = population

    def add(self, layer):
        self.layers_blueprint.append(layer)

    def new_model(self):
        ga_model = GASequentialModel()

        # Make a copy of all the models and layers
        layers = copy.deepcopy(self.layers_blueprint)

        for layer in layers:
            ga_model.add(layer)

        ga_model.compile()

        return ga_model
    
    def new_population(self):
        for _ in range(self.population):
            self.forest.append(self.new_model())

    def simulate(self, func, keep_rate = 0.9, mutate_rate = 0.01, params = ()):
        for idx, gas_model in enumerate(self.forest):
            print('Simulating: {}/{}'.format(idx + 1, self.population), end = '\r')
            func(gas_model, params)

        # Sort by reward in descending order
        self.sort_forest()
        
        print('\nMin {}, max {}'.format(self.forest[-1].reward, self.forest[0].reward))

        # Abandon ones with low score
        keep_idx = int(self.population * keep_rate)
        for idx in reversed(range(keep_idx, self.population)):
            del self.forest[idx]
        
        probs = [model.reward for model in self.forest]
        probs = probs / np.sum(probs)

        # Crossover
        for _ in range(self.population - keep_idx):
            choice = np.random.choice(self.forest[0:keep_idx], 2, p = probs)
            p1 = choice[0]
            p2 = choice[1]
            ofspr = copy.deepcopy(p1)

            # Crossover
            for layer_old, layer_new in zip(p2.layers, ofspr.layers):
                # Crossover p2's W and b to the offspring
                mate_W = copy.deepcopy(layer_old.W)
                mate_b = copy.deepcopy(layer_old.b)
                layer_new.crossover(mate_W = mate_W, mate_b = mate_b)

                # Mutate
                layer_new.mutate(mutate_rate)

            self.forest.append(ofspr)

        assert len(self.forest) == self.population
    
    def sort_forest(self):
        self.forest.sort(key = lambda model:model.reward, reverse = True)


class GASequentialModel(SequentialModel):

    def __init__(self):
        super().__init__()
        self.reward = 0

    def set_reward(self, reward):
        self.reward = reward

    