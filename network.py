from layer import Layer
import numpy as np

def relu(x):
    return np.maximum(0, x)

class Network:
    def __init__(self, layer_sizes):
        # layer_sizes e.g. [2, 3, 4, 1]
        self.layers = [
            Layer(n_neurons=layer_sizes[i+1], n_inputs=layer_sizes[i])
            for i in range(len(layer_sizes) - 1)
        ]

    def forward(self, inputs):
        for i, layer in enumerate(self.layers):
            inputs = layer.forward(inputs)
            if i < len(self.layers) - 1:
                inputs = relu(inputs)
        return inputs

    def backward(self, d_output, learning_rate=0.01):
        for layer in reversed(self.layers):
            d_output = layer.backward(d_output, learning_rate)

    def train(self, inputs, targets, learning_rate=0.001):
        predictions = self.forward(inputs)
        loss = mse_loss(predictions, targets)
        d_output = 2 * (predictions - targets)
        self.backward(d_output, learning_rate)
        return loss



def mse_loss(predictions,targets):
    return np.mean((predictions - targets)**2)


    