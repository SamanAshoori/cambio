
import numpy as np


class Layer:
    def __init__(self,n_neurons,n_inputs):
        self.weights = np.random.randn(n_neurons, n_inputs) * np.sqrt(2 / n_inputs)
        self.biases = np.zeros(n_neurons)
        
    def forward(self,inputs):
        self.inputs = inputs
        return np.dot(self.weights,inputs) + self.biases
    
    def backward(self,d_output,learning_rate=0.01):
        d_output = np.clip(d_output, -1.0, 1.0)
        d_weight = np.outer(d_output,self.inputs)
        d_bias = d_output
        self.weights -= learning_rate * d_weight
        self.biases -= learning_rate * d_bias
        return np.dot(d_output,self.weights)
    
    