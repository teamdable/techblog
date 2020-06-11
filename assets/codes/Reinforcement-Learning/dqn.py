
# Based on https://gist.github.com/Pocuston/2d61d64b6db47b3963864d84a8eb8552

# Solution of Open AI gym environment "Cartpole-v0" (https://gym.openai.com/envs/CartPole-v0) using DQN and Pytorch.
# It is is slightly modified version of Pytorch DQN tutorial from
# http://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html.
# The main difference is that it does not take rendered screen as input but it simply uses observation values from the \
# environment.

import gym
import random
import math
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# hyper parameters
EPISODES = 600  # number of episodes
EPS_START = 0.9  # e-greedy threshold start value
EPS_END = 0.01  # e-greedy threshold end value
EPS_DECAY = 200  # e-greedy threshold decay
GAMMA = 0.80  # Q-learning discount factor
LR = 0.0005  # NN optimizer learning rate
HIDDEN_LAYER = 24  # NN hidden layer size
BATCH_SIZE = 128  # Q-learning batch size


class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, transition):
        self.memory.append(transition)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class Network(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
        self.l1 = nn.Linear(4, HIDDEN_LAYER)
        self.l2 = nn.Linear(HIDDEN_LAYER, 16)
        self.l3 = nn.Linear(16, 2)

    def forward(self, x):
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = self.l3(x)
        return x

env = gym.make('CartPole-v0')

model = Network()
memory = ReplayMemory(10000)
optimizer = optim.Adam(model.parameters(), LR)
steps_done = 0
episode_durations = []


def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            return model(torch.tensor([state], dtype=torch.float)).argmax(1)
    else:
        return torch.tensor([random.randrange(2)], dtype=torch.long)


def run_episode(e, environment):
    state = environment.reset()
    steps = 0
    while True:
        steps += 1
        action = select_action(state)
        next_state, reward, done, _ = environment.step(action.item())

        # zero reward when attempt ends
        if done and steps < 200:
            reward = 0

        memory.push((torch.tensor(state, dtype=torch.float),
                     action,  # action is already a tensor
                     torch.tensor(next_state, dtype=torch.float),
                     torch.tensor([reward], dtype=torch.float)))

        learn()

        state = next_state

        if done:
            print("Episode {0} finished after {1} steps".format(e, steps))
            episode_durations.append(steps)
            break


def learn():
    if len(memory) < BATCH_SIZE:
        return

    # random transition batch is taken from experience replay memory
    transitions = memory.sample(BATCH_SIZE)
    batch_state, batch_action, batch_next_state, batch_reward = zip(*transitions)

    batch_state = torch.stack(batch_state)
    batch_action = torch.stack(batch_action)
    batch_reward = torch.stack(batch_reward)
    batch_next_state = torch.stack(batch_next_state)

    # current Q values are estimated by NN for all actions
    current_q_values = model(batch_state).gather(1, batch_action)
    # expected Q values are estimated from actions which gives maximum Q value
    with torch.no_grad():
        max_next_q_values = model(batch_next_state).max(1)[0].unsqueeze(1)
    expected_q_values = batch_reward + (GAMMA * max_next_q_values)

    # loss is measured from error between current and newly expected Q values
    loss = F.smooth_l1_loss(current_q_values, expected_q_values)

    # backpropagation of loss to NN
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


for e in range(EPISODES):
    run_episode(e, env)
    if episode_durations[-1] >= env.spec.reward_threshold:
        break

print('Complete')
env.close()
