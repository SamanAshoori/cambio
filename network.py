from layer import Layer
import numpy as np
    
class Network:
    def __init__(self, layer_sizes):
        # layer_sizes e.g. [2, 3, 4, 1]
        self.layers = [
            Layer(n_neurons=layer_sizes[i+1], n_inputs=layer_sizes[i])
            for i in range(len(layer_sizes) - 1)
        ]

    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs

    def backward(self, d_output, learning_rate=0.01):
        for layer in reversed(self.layers):
            d_output = layer.backward(d_output, learning_rate)

    def train(self, inputs, targets, learning_rate=0.01):
        predictions = self.forward(inputs)
        loss = mse_loss(predictions, targets)
        d_output = 2 * (predictions - targets)
        self.backward(d_output, learning_rate)
        return loss



def mse_loss(predictions,targets):
    return np.mean((predictions - targets)**2)


    
if __name__ == "__main__":
    net = Network([2, 3, 4, 1])
x = np.array([0.5, 0.3])
target = np.array([2.0])

for epoch in range(100):
    loss = net.train(x, target)
    if epoch % 10 == 0:
        print(f"epoch {epoch}: loss={loss:.4f}")
    