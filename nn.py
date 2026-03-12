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
        self.inputs = inputs
        return relu(np.dot(self.weights,inputs) + self.biases)
    
    def backward(self,d_output,learning_rate=0.01):
        d_weight = np.outer(d_output,self.inputs)
        d_bias = d_output
        self.weights -= learning_rate * d_weight
        self.biases -= learning_rate * d_bias
        return np.dot(d_output,self.weights)
    
def relu(x):
    return np.maximum(0,x)


def mse_loss(predictions,targets):
    return np.mean((predictions - targets)**2)


    
if __name__ == "__main__":
    layer1 = Layer(n_neurons=3, n_inputs=2)
    layer2 = Layer(n_neurons=1, n_inputs=3)

    x = np.array([0.5, 0.3])
    target = np.array([2.0])

    for epoch in range(100):
        # forward
        out1 = layer1.forward(x)
        out2 = layer2.forward(out1)

        # loss
        loss = mse_loss(out2, target)

        # backward
        d_output = 2 * (out2 - target)
        d_hidden = layer2.backward(d_output)
        layer1.backward(d_hidden)

        if epoch % 10 == 0:
            print(f"epoch {epoch}: loss={loss:.6f}")
    