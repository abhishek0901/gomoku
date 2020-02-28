import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np


# Input Structure -> (2 X width X height)
# Output -> Pi (1,width X height), Value (Winning Percentage)

def set_learning_rate(optimizer, lr):
    """Sets the learning rate to the given value"""
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr

class NeuralNetModel(nn.Module):
    def __init__(self, board_width, board_height):
        super(NeuralNetModel, self).__init__()

        self.board_height = board_height
        self.board_width = board_width

        # ---------------------------------------------------#
        #				Conv. Block Declaration				#
        # ---------------------------------------------------#
        self.conv1 = nn.Conv2d(2, 32, kernel_size=3, padding=1)
        self.conv1_bn = nn.BatchNorm2d(32)

        # ---------------------------------------------------#
        #				Res. Block Declaration				#
        # ---------------------------------------------------#

        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.conv2_bn = nn.BatchNorm2d(32)

        self.conv3 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.conv3_bn = nn.BatchNorm2d(32)

        # ---------------------------------------------------#
        #				Policy Block Declaration			#
        # ---------------------------------------------------#
        self.conv4 = nn.Conv2d(32, 2, kernel_size=1, padding=0)
        self.conv4_bn = nn.BatchNorm2d(2)

        self.prob_fc1 = nn.Linear(2 * self.board_width * self.board_height, self.board_width * self.board_height)

        # ---------------------------------------------------#
        #				Value Block Declaration				#
        # ---------------------------------------------------#
        self.conv5 = nn.Conv2d(32, 1, kernel_size=1, padding=0)
        self.conv5_bn = nn.BatchNorm2d(1)

        self.val_fc1 = nn.Linear(1 * self.board_width * self.board_height, 32)
        self.val_fc2 = nn.Linear(32, 1)

    def forward(self, input_state):
        # ---------------------------------------------------#
        #				Conv. Block Implementation			#
        # ---------------------------------------------------#
        x = self.conv1(input_state)
        x = self.conv1_bn(x)
        x = F.relu(x)

        # ---------------------------------------------------#
        #				Res. Block Implementation			#
        # ---------------------------------------------------#
        res_net_skip = x
        x = self.conv2(x)
        x = self.conv2_bn(x)
        x = F.relu(x)

        x = self.conv3(x)
        x = self.conv3_bn(x)
        x = x + res_net_skip
        x = F.relu(x)

        # ---------------------------------------------------#
        #				Policy Block Implementation			#
        # ---------------------------------------------------#
        y = self.conv4(x)
        y = self.conv4_bn(y)
        y = F.relu(y)
        y = y.view(-1, 2 * self.board_width * self.board_height)
        y = self.prob_fc1(y)
        y = F.softmax(y, dim=1)

        # ---------------------------------------------------#
        #				Value Block Implementation			#
        # ---------------------------------------------------#
        z = self.conv5(x)
        z = self.conv5_bn(z)
        z = F.relu(z)

        z = z.view(-1, 1 * self.board_width * self.board_height)
        z = self.val_fc1(z)
        z = F.relu(z)
        z = self.val_fc2(z)
        z = torch.tanh(z)

        return y, z


class PolicyValueNet():

    def __init__(self, board_width, board_height, model_file=None):
        self.board_height = board_height
        self.board_width = board_width
        self.l2_constant = 1e-4

        self.neural_net = NeuralNetModel(self.board_width, self.board_height)
        self.optimizer = optim.Adam(self.neural_net.parameters(), weight_decay=self.l2_constant)

        if model_file:
            network_parameters = torch.load(model_file)
            self.neural_net.load_state_dict(network_parameters)

    def get_move(self, current_board):
        # Convert board into 2 * width * height Tensor Variable
        current_board_tensor = Variable(torch.FloatTensor([current_board]))
        log_action_probabilities, value = self.neural_net(current_board_tensor)
        action_probs = log_action_probabilities.data.numpy()

        return action_probs, value

    def train_step(self, board_list, action_probs_list, value_list, lr, epochs=1, temperature=1):
        board_list_tensor = Variable(torch.FloatTensor(board_list))
        action_probs_list_tensor = Variable(torch.FloatTensor(action_probs_list))
        value_list_tensor = Variable(torch.FloatTensor(value_list))

        for epoch in range(epochs):
            print("Epoch........... : ", epoch, end=' ')
            self.optimizer.zero_grad()
            set_learning_rate(self.optimizer, lr)

            # Forward
            log_action_probabilities, value = self.neural_net(board_list_tensor)

            # print(value.size(),value_list_tensor.size(),action_probs_list_tensor.size(),log_action_probabilities.size())

            log_action_probabilities = torch.log(log_action_probabilities)

            value_loss = (value.view(-1) - value_list_tensor) ** 2
            policy_loss = -torch.sum(
                (action_probs_list_tensor ** temperature) * log_action_probabilities, dim=1)

            # print(value_loss.size(),policy_loss.size())
            loss = torch.sqrt(torch.mean(value_loss.T + policy_loss))
            loss.backward(retain_graph=True)
            print("Loss : ", loss.item())
            self.optimizer.step()

        return (loss.item(), torch.mean(value_loss).item(), torch.mean(policy_loss).item())

    def get_policy_param(self):
        return self.neural_net.state_dict()

    def save_model(self, model_file):
        torch.save(self.get_policy_param(), model_file)