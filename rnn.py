# Recurrent Neural Network

import random

import numpy as np
import cv2
import torch
from torch import nn

from visualizer.visualizer import *


class DataFormatter:
    """
    From the data format obtained, organize it to the format required by model.

    Choose training, validating, and testing data sets
    """

    def __init__(self, data):
        """
        input and output can be in any format

        :param data: {'input': input data, 'output': output data}
        """
        self.data = data
        self.test_input_data = None
        self.test_output_data = None
        self.validity_input_data = None
        self.validity_output_data = None
        self.train_input_data = None
        self.train_output_data = None

    def format_data(self, manual_input=None):
        """
        Format data to
        1. input array
        2. output array
        """
        input_text = self.data if not manual_input else manual_input
        # Join all the sentences together and extract the unique characters from the combined sentences
        self.chars = set(''.join(input_text))

        # Creating a dictionary that maps integers to the characters
        self.int2char = dict(enumerate(self.chars))

        # Creating another dictionary that maps characters to integers
        self.char2int = {char: ind for ind, char in self.int2char.items()}

        # Finding the length of the longest string in our data
        maxlen = len(max(input_text, key=len))

        # Padding

        # A simple loop that loops through the list of sentences and adds a ' ' whitespace until the length of
        # the sentence matches the length of the longest sentence
        for i in range(len(input_text)):
            while len(input_text[i]) < maxlen:
                input_text[i] += ' '

        # Creating lists that will hold our input and target sequences
        input_seq = []
        target_seq = []

        for i in range(len(input_text)):
            # Remove last character for input sequence
            input_seq.append(input_text[i][:-1])

            # Remove first character for target sequence
            target_seq.append(input_text[i][1:])
            print("Input Sequence: {}\nTarget Sequence: {}".format(input_seq[i], target_seq[i]))

        for i in range(len(text)):
            input_seq[i] = [self.char2int[character] for character in input_seq[i]]
            target_seq[i] = [self.char2int[character] for character in target_seq[i]]

        self.dict_size = len(self.char2int)
        self.seq_len = maxlen - 1
        self.batch_size = len(text)

        input_seq = self.one_hot_encode(input_seq, self.dict_size, self.seq_len, self.batch_size)

        input_seq = torch.from_numpy(input_seq)
        target_seq = torch.Tensor(target_seq)

        return input_seq, target_seq

    def one_hot_encode(self, sequence, dict_size, seq_len, batch_size):
        # Creating a multi-dimensional array of zeros with the desired output shape
        features = np.zeros((batch_size, seq_len, dict_size), dtype=np.float32)

        # Replacing the 0 at the relevant character index with a 1 to represent that character
        for i in range(batch_size):
            for u in range(seq_len):
                features[i, u, sequence[i][u]] = 1
        return features

    def get_train_validity_test_data(self, train_percentage=80, validity_percentage=0):
        """

        :return:
            1. test_input_data
            2. test_output_data
        """

        num_inputs = self.input_data.shape[1]
        num_train_inputs = int(train_percentage / 100 * num_inputs)
        num_validity_inputs = int(validity_percentage / 100 * num_inputs)

        random_select_rows = random.sample(range(0, num_inputs), num_inputs)

        self.train_input_data = np.array([self.input_data[index] for index in random_select_rows[:num_train_inputs]])
        self.train_output_data = np.array([self.output_data[index] for index in random_select_rows[:num_train_inputs]])

        self.validity_input_data = np.array(
            [
                self.input_data[index]
                for index in random_select_rows[num_train_inputs:(num_train_inputs + num_validity_inputs)]
            ]
        )
        self.validity_output_data = np.array(
            [
                self.output_data[index]
                for index in random_select_rows[num_train_inputs:(num_train_inputs + num_validity_inputs)]
            ]
        )

        self.test_input_data = np.array(
            [
                self.input_data[index]
                for index in random_select_rows[(num_train_inputs + num_validity_inputs):]
            ]
        )

        self.test_output_data = np.array(
            [
                self.output_data[index]
                for index in random_select_rows[(num_train_inputs + num_validity_inputs):]
            ]
        )


class Model(nn.Module):
    """
    1. Create model
    2. Train and validate
    3. Score calculation
    4. Test
    5. Hyper-parameter Tuning
    6. Predict
    """

    def __init__(self, data):
        super(Model, self).__init__()
        self.data_formatter = DataFormatter(data)
        self.input_seq, self.target_seq = self.data_formatter.format_data()

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("GPU is available")
        else:
            self.device = torch.device("cpu")
            print("GPU not available, CPU used")

        # Defining some parameters
        self.hidden_dim = 12  # hidden_dim
        self.n_layers = 1  # n_layers

        # Defining the layers
        # RNN Layer
        self.rnn = nn.RNN(self.data_formatter.dict_size, self.hidden_dim, self.n_layers, batch_first=True)
        # Fully connected layer
        self.fc = nn.Linear(self.hidden_dim, self.data_formatter.dict_size)

    def forward(self, x):
        batch_size = x.size(0)

        # Initializing hidden state for first input using method defined below
        hidden = self.init_hidden(batch_size)

        # Passing in the input and hidden state into the model and obtaining outputs
        out, hidden = self.rnn(x, hidden)

        # Reshaping the outputs such that it can be fit into the fully connected layer
        out = out.contiguous().view(-1, self.hidden_dim)
        out = self.fc(out)

        return out, hidden

    def init_hidden(self, batch_size):
        # This method generates the first hidden state of zeros which we'll use in the forward pass
        # We'll send the tensor holding the hidden state to the device we specified earlier as well
        hidden = torch.zeros(self.n_layers, batch_size, self.hidden_dim)
        return hidden

    def rnn_train(self, **kwargs):
        n_epochs = 100
        lr = 0.01

        # Define Loss, Optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=lr)

        # Training Run
        for epoch in range(1, n_epochs + 1):
            optimizer.zero_grad()  # Clears existing gradients from previous epoch
            self.input_seq.to(self.device)
            output, hidden = self.forward(self.input_seq)
            loss = criterion(output, self.target_seq.view(-1).long())
            loss.backward()  # Does backpropagation and calculates gradients
            optimizer.step()  # Updates the weights accordingly

            if epoch % 10 == 0:
                print('Epoch: {}/{}.............'.format(epoch, n_epochs), end=' ')
                print("Loss: {:.4f}".format(loss.item()))

    # This function takes in the model and character as arguments and returns the next character prediction and hidden state
    def predict(self, character):
        # One-hot encoding our input to fit into the model
        character = np.array([[self.data_formatter.char2int[c] for c in character]])
        character = self.data_formatter.one_hot_encode(character, self.data_formatter.dict_size, character.shape[1], 1)
        character = torch.from_numpy(character)
        character.to(self.device)

        out, hidden = self.forward(character)

        prob = nn.functional.softmax(out[-1], dim=0).data
        # Taking the class with the highest probability score from the output
        char_ind = torch.max(prob, dim=0)[1].item()

        return self.data_formatter.int2char[char_ind], hidden

    # This function takes the desired output length and input characters as arguments, returning the produced sentence
    def sample(self, out_len, start='hey'):
        self.eval()  # eval mode
        start = start.lower()
        # First off, run through the starting characters
        chars = [ch for ch in start]
        size = out_len - len(chars)
        # Now pass in the previous characters and get a new one
        for ii in range(size):
            char, h = self.predict(chars)
            chars.append(char)

        return ''.join(chars)


if __name__ == '__main__':
    text = ['hey how are you', 'good i am fine', 'have a nice day']

    model = Model(text)
    model.rnn_train()
    model.sample(15, 'good')
    viz = Visualizer.draw(model.state_dict(), 3)
    while cv2.waitKey(10) != ord('q'):
        cv2.imshow('NN', viz)
    pass
