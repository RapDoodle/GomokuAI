"""For testing only"""

from nn.model import SequentialModel
from nn.layers import Input, Dense, Output
from gomoku.player import Player
from gomoku.gomoku import Gomoku
from common.exception import AlreadyPlacedExcpetion

import numpy as np

import nn.math as m

model = SequentialModel()
num_input_units = 15 * 15 * 3
num_output_units = 15 * 15
model.add(Input(num_input_units))
model.add(Dense(512, activation = 'relu', use_bias = True))
model.add(Dense(512, activation = 'relu', use_bias = True))
model.add(Dense(384, activation = 'relu', use_bias = True))
model.add(Dense(256, activation = 'relu', use_bias = True))
model.add(Dense(225, activation = 'relu', use_bias = True))
model.add(Output(num_output_units, activation = 'softmax', use_bias = True))
model.compile()
model.summary()
# print(model.predict(np.array([1, 2, 3, 4]).reshape(4,1)))
# print(model.predict(np.random.randn(num_input_units, 1)))
# model.fit(np.random.randn(num_input_units, 244), model.predict(np.random.randn(num_input_units, 1)))
# model.fit(np.array([1, 2, 3, 4]).reshape(4,1), np.array([1]).reshape(1,1))

gomoku = Gomoku()
player1 = Player('Player 1', 'B')
player2 = Player('Player 2', 'W')
gomoku.start(player1, player2, render = False)

turn = 'B'
max_turn = 30000
player1.place(7,7)
turn = 'W'
success = 0
for i in range(max_turn):
    if turn == 'B':
        curr_player = player1
        opponent_player = player2
    else:
        curr_player = player2
        opponent_player = player1
    
    X = curr_player.map_my_pieces.reshape((225, 1))
    X = np.append(X, opponent_player.map_my_pieces.reshape((225, 1)), axis = 0)
    X = np.append(X, curr_player.map_prev_move.reshape((225, 1)), axis = 0)

    y = model.predict(X)
    pos = y.argmax()
    r = pos // 15
    c = pos % 15

    if r == 0 and c == 0:
        print(y)

    # print(i)

    try:
        if curr_player.place(r, c):
            turn = opponent_player.color
            success = success + 1
        else:
            print('???')
    except AlreadyPlacedExcpetion:
        if i % 20 == 0:
            print('{}/{} Step: {} Current attempt: ({}, {})'.format(i, max_turn, success, r, c), end = '\r')
        y = curr_player.map_prev_move.reshape((225, 1)) * -1
        model.fit(X, y, learning_rate = 0.01)


gomoku.save()