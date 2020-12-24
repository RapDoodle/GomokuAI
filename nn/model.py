import numpy as np

from common.exception import ModelError
from nn.layers import Input, Dense, Output
from nn.genetic_algorithm.layers import GAInput, GADense, GAOutput

class SequentialModel():

    def __init__(self):
        """The initialization of the neural network"""
        self.input_layer = None
        self.output_layer = None
        self.layers = []
        self.compiled = False

    def model_init(self):
        """Initialize the weights of the neural network"""

        # Must be compiled before initializing
        if not self.compiled:
            raise ModelError("not compiled model")

    def compile(self):
        """Compile the model. The structure is not editable anymore"""
        if self.input_layer is None or len(self.layers) <= 0:
            raise ModelError('not enough layers to form a neural network')

        if not isinstance(self.input_layer, Input):
            raise ModelError('the first layer of the model must be of type Input')

        if not isinstance(self.layers[-1], Output):
            if not isinstance(self.layers[-1], GAOutput):
                raise ModelError('the last layer of the model must be of type Output')

        self.compiled = True

        n_layers = len(self.layers)

        try:
            for idx in range(n_layers):
                if idx == 0:
                    # The input layer
                    continue
                elif idx == 1:
                    self.input_layer.init(self.layers[idx])
                    self.layers[idx].init(prev_layer = self.input_layer)
                else:
                    self.layers[idx - 1].set_next_layer(self.layers[idx])
                    self.layers[idx].init(prev_layer = self.layers[idx - 1])
                    if idx + 1 == n_layers:
                        self.output_layer = self.layers[idx]
        except:
            self.compiled = False
            raise ModelError('unable to compile')

    def add(self, layer):
        if self.input_layer is None:
            self.input_layer = layer

        self.layers.append(layer)
    
    def predict(self, X):
        return self.input_layer.forward(X)

    def fit(self, X_train, y_train, learning_rate = 0.1):
        self.predict(X_train)
        self.output_layer.backward(y_train)
        self.output_layer.update_weights(learning_rate = learning_rate)
        
    def summary(self):
        print('========== NEURAL NETWORK SUMMARY ==========')
        if not self.compiled:
            print('The model is not compiled')
            return
        
        curr_layer = self.input_layer
        print('  Type\t\tUnits\tUse bias')
        while curr_layer is not None:
            if isinstance(curr_layer, GAOutput):
                type = 'GAOutput'
            elif isinstance(curr_layer, GAInput):
                type = 'GAInput'
            elif isinstance(curr_layer, GADense):
                type = 'GADense'
            elif isinstance(curr_layer, Output):
                type = 'Output'
            elif isinstance(curr_layer, Input):
                type = 'Input'
            elif isinstance(curr_layer, Dense):
                type = 'Dense'
            print('  {} layer\t{}\t{}'.format(type, curr_layer.units, str(curr_layer.use_bias)))
            curr_layer = curr_layer.next_layer
            
        print('============================================')