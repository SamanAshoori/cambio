import numpy as np
#my first neuron
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
    neuron = Neuron()
    input = 0.5
    target = 2.0

    for epoch in range(1000):
        output = neuron.forward(input)
        loss = (output - target) ** 2
        neuron.backward(target)
        if epoch % 10 == 0:
            print(f"epoch {epoch}: output={output:.3f}, loss={loss:.3f}")
    
predictions = np.array([1.0, 2.0, 3.0])
targets     = np.array([1.0, 2.0, 3.0])
print(mse_loss(predictions, targets))

predictions = np.array([2.0, 0.0])
targets     = np.array([0.0, 2.0])
print(mse_loss(predictions, targets))
print(relu(np.array([-2.0, -0.5, 0.0, 1.0, 3.0])))


