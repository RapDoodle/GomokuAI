"""For testing only"""

from nn.model import SequentialModel
from nn.layers import Input, Dense, Output
from gomoku.player import Player
from gomoku.gomoku import Gomoku

import numpy as np

import nn.math as m

model = SequentialModel()
num_input_units = 15 * 15 * 3
num_output_units = 15 * 15
model.add(Input(num_input_units))
model.add(Dense(512, activation = 'relu', use_bias = True))
model.add(Dense(512, activation = 'relu', use_bias = True))
model.add(Dense(384, activation = 'relu', use_bias = True))
model.add(Dense(384, activation = 'relu', use_bias = True))
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
# gomoku.start(player1, player2)

turn = 1
max_turn = 300
for i in range(max_turn):
    if turn == 1:
        curr_player = player1
        opponent_player = player2
    else:
        curr_player = player2
        opponent_player = player1
    
    X = curr_player.map_my_pieces.reshape(225, 1)
    X = np.append(X, opponent_player.map_my_pieces.reshape(225, 1), axis = 0)
    X = np.append(X, curr_player.map_prev_move.reshape(225, 1), axis = 0)
    
    break
    
    