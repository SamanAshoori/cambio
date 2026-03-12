import numpy as np
from network import Network

STATE_SIZE = 19
ACTION_SIZE = 6

# Actions:
# 0 - swap drawn card with inventory slot 0
# 1 - swap drawn card with inventory slot 1
# 2 - swap drawn card with inventory slot 2
# 3 - swap drawn card with inventory slot 3
# 4 - discard drawn card
# 5 - call cambio


class Agent:
    def __init__(self):
        self.network = Network([STATE_SIZE, 64, 64, ACTION_SIZE])
        self.epsilon = 1.0  # start fully exploratory

    def act(self, state_vector):
        q_values = self.network.forward(state_vector)
        return choose_action(q_values, self.epsilon)


def choose_action(q_values, epsilon=0.1):
    if np.random.rand() < epsilon:
        return np.random.randint(len(q_values))  # random
    return int(np.argmax(q_values))              # greedy
