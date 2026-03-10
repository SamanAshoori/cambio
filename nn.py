import numpy as np
#my first neuron
class Neuron:
    def __init__(self):
        #random number for now
        self.weights = np.random.randn()
        self.bias = np.random.randn()
    
    def forward(self, inputs):
        return self.weights * inputs + self.bias
    
class Layer:
    def __init__(self,n_neurons,n_inputs):
        self.weights = np.random.randn(n_neurons,n_inputs)
        self.biases = np.random.randn(n_neurons,)
        
    def forward(self,inputs):
        return relu(np.dot(self.weights,inputs) + self.biases)
    
def relu(x):
    return np.maximum(0,x)


def mse_loss(predictions,targets):
    return np.mean((predictions - targets)**2)


    
if __name__ == "__main__":
    layer1 = Layer(3,2)
    layer2 = Layer(4,3)
    x = np.array([0.5, 0.3])
    out1 = layer1.forward(x)
    out2 = layer2.forward(out1)
    print(out2)
    
predictions = np.array([1.0, 2.0, 3.0])
targets     = np.array([1.0, 2.0, 3.0])
print(mse_loss(predictions, targets))

predictions = np.array([2.0, 0.0])
targets     = np.array([0.0, 2.0])
print(mse_loss(predictions, targets))
print(relu(np.array([-2.0, -0.5, 0.0, 1.0, 3.0])))


