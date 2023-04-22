import os

import torch as T
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
from torch.distributions.normal import Normal


class CriticNetwork(nn.Module):
    def __init__(self, beta, input_dims, n_actions, fc_dims, chkpt_dir, fc1_dims=256, fc2_dims=256, fc3_dims=128, fc4_dims=128,
            name='critic'):
        super(CriticNetwork, self).__init__()

        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')

        self.input_dims = input_dims
        self.n_actions = n_actions

        self.name = name
        self.checkpoint_dir = chkpt_dir
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name+'_sac')

        self.fcs = []
        self.fc1 = nn.Linear(self.input_dims[0] + n_actions, fc_dims[0])
        self.fcs.append(self.fc1)

        for fc_count in range(1, len(fc_dims)):
            self.fc = nn.Linear(fc_dims[fc_count - 1], fc_dims[fc_count])
            self.fc.to(self.device)
            self.fcs.append(self.fc)

        self.q = nn.Linear(fc_dims[-1], 1)

        self.optimizer = optim.Adam(self.parameters(), lr=beta)

        self.to(self.device)

    def forward(self, state, action):
        action_value = self.fcs[0](T.cat([state, action], dim=1))
        action_value = F.relu(action_value)

        for self.fc in self.fcs[1:]:
            action_value = self.fc(action_value)
            action_value = F.relu(action_value)

        q = self.q(action_value)

        return q

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))
        self.eval()

class ValueNetwork(nn.Module):
    def __init__(self, beta, input_dims, fc_dims, chkpt_dir, name='value'):
        super(ValueNetwork, self).__init__()

        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')

        self.input_dims = input_dims
        self.name = name
        self.checkpoint_dir = chkpt_dir
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name+'_sac')

        self.fcs = []
        self.fc1 = nn.Linear(*self.input_dims, fc_dims[0])
        self.fcs.append(self.fc1)

        for fc_count in range(1, len(fc_dims)):
            self.fc = nn.Linear(fc_dims[fc_count - 1], fc_dims[fc_count])
            self.fc.to(self.device)
            self.fcs.append(self.fc)

        self.v = nn.Linear(fc_dims[-1], 1)

        self.optimizer = optim.Adam(self.parameters(), lr=beta)

        self.to(self.device)

    def forward(self, state):
        state_value = self.fcs[0](state)
        state_value = F.relu(state_value)

        for self.fc in self.fcs[1:]:
            state_value = self.fc(state_value)
            state_value = F.relu(state_value)

        v = self.v(state_value)

        return v

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))
        self.eval()

class ActorNetwork(nn.Module):
    def __init__(self, alpha, input_dims, n_actions, max_action, fc_dims, chkpt_dir, name='actor'):
        super(ActorNetwork, self).__init__()

        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')

        self.input_dims = input_dims
        self.n_actions = n_actions

        self.name = name
        self.checkpoint_dir = chkpt_dir
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name+'_sac')
        self.max_action = max_action
        self.reparam_noise = 1e-6

        self.fcs = []
        self.fc1 = nn.Linear(*self.input_dims, fc_dims[0])
        self.fcs.append(self.fc1)

        for fc_count in range(1, len(fc_dims)):
            self.fc = nn.Linear(fc_dims[fc_count - 1], fc_dims[fc_count])
            self.fc.to(self.device)
            self.fcs.append(self.fc)

        self.mu = nn.Linear(fc_dims[-1], self.n_actions)
        self.sigma = nn.Linear(fc_dims[-1], self.n_actions)

        self.optimizer = optim.Adam(self.parameters(), lr=alpha)

        self.to(self.device)

    def forward(self, state):
        prob = self.fcs[0](state)
        prob = F.relu(prob)

        for self.fc in self.fcs[1:]:
            prob = self.fc(prob)
            prob = F.relu(prob)

        mu = self.mu(prob)
        sigma = self.sigma(prob)

        sigma = T.clamp(sigma, min=self.reparam_noise, max=1)

        return mu, sigma

    def sample_normal(self, state, reparameterize=True):
        mu, sigma = self.forward(state)
        probabilities = Normal(mu, sigma)

        if reparameterize:
            actions = probabilities.rsample()
        else:
            actions = probabilities.sample()

        action = T.tanh(actions)*T.tensor(self.max_action).to(self.device)
        log_probs = probabilities.log_prob(actions)
        log_probs -= T.log(1-action.pow(2)+self.reparam_noise)
        log_probs = log_probs.sum(1, keepdim=True)

        return action, log_probs

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))
        self.eval()
