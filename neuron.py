from random import random
import numpy as np

class Neuron:
    def __init__(self):
        #random number for now
        self.weights = np.random.randn()
        self.bias = np.random.randn()
    
    def forward(self, inputs):
        self.inputs = inputs
        return self.weights * inputs + self.bias
    
    def backward(self,target,learning_rate = 0.01):
        output = self.forward(self.inputs)
        d_weight = 2 * (output - target) * self.inputs
        d_bias = 2 * (output - target)
        self.weights -= learning_rate * d_weight
        self.bias -= learning_rate * d_bias