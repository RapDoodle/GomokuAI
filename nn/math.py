import numpy as np

def sigmoid(X):
    return 1 / (1 + np.exp(-X))

def relu(X):
    return np.maximum(0, X)

def tanh(X):
    return np.tanh(X)

def linear(X):
    return X

def softmax(X):
    e_X = np.exp(X)
    return e_X / np.sum(e_X)