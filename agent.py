import numpy as np
from collections import deque
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


class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        batch = [self.buffer[i] for i in indices]
        states, actions, rewards, next_states, dones = zip(*batch)
        return np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(dones)

    def __len__(self):
        return len(self.buffer)


class Agent:
    def __init__(self, batch_size=32):
        self.network = Network([STATE_SIZE, 64, 64, ACTION_SIZE])
        self.epsilon = 1.0
        self.batch_size = batch_size
        self.replay_buffer = ReplayBuffer()

    def act(self, state_vector):
        q_values = self.network.forward(state_vector)
        return choose_action(q_values, self.epsilon)

    def train(self, state, action, reward, next_state, done, gamma=0.95):
        self.replay_buffer.push(state, action, reward, next_state, done)

        if len(self.replay_buffer) < self.batch_size:
            return

        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)

        for i in range(self.batch_size):
            r = np.clip(rewards[i], -1.0, 1.0)
            q_values = self.network.forward(states[i])
            target = q_values.copy()

            if dones[i]:
                target[actions[i]] = r
            else:
                q_next = self.network.forward(next_states[i])
                target[actions[i]] = r + gamma * np.max(q_next)

            self.network.train(states[i], target)


def choose_action(q_values, epsilon=0.1):
    if np.random.rand() < epsilon:
        return np.random.randint(len(q_values))  # random
    return int(np.argmax(q_values))              # greedy
