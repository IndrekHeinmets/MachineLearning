import numpy as np


class NeuralNetwork():
    def __init__(self):
        np.random.seed(1)
        self.synaptic_weights = 2 * np.random.random((3, 1)) - 1

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def train(self, training_inputs, training_outputs, iterations):
        for i in range(iterations):
            output = self.think(training_inputs)
            error = training_outputs - output
            adjustments = np.dot(training_inputs.T, error * self.sigmoid_derivative(output))
            self.synaptic_weights += adjustments

    def think(self, inputs):
        inputs = inputs.astype(float)
        output = self.sigmoid(np.dot(inputs, self.synaptic_weights))

        return output


if __name__ == '__main__':
    neural_network = NeuralNetwork()

    print('Random synaptic weights: ')
    print(neural_network.synaptic_weights)

    train_inputs = np.array([[0, 0, 1],
                             [1, 1, 1],
                             [1, 0, 1],
                             [0, 1, 1]])

    train_outputs = np.array([[0, 1, 1, 0]]).T

    neural_network.train(train_inputs, train_outputs, 100000)

    print('Synaptic weights after training: ')
    print(neural_network.synaptic_weights)

    A = str(input('Input 1: '))
    B = str(input('Input 2: '))
    C = str(input('Input 3: '))

    print(f'New situation: Input data = {A} {B} {C}')
    print('Output data: ')
    print(neural_network.think(np.array([A, B, C])))
