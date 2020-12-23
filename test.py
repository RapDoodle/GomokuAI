"""For testing only"""

from nn.model import SequentialModel
from nn.layers import Input, Dense, Output
import common.constant as const
from gomoku.player import Player
from gomoku.gomoku import Gomoku
from common.exception import AlreadyPlacedExcpetion

import numpy as np
import pandas as pd

import nn.math as m

model = SequentialModel()
num_input_units = 15 * 15 * 3
num_output_units = 15 * 15
model.add(Input(num_input_units))
model.add(Dense(512, activation = 'tanh', use_bias = True))
model.add(Dense(512, activation = 'tanh', use_bias = True))
model.add(Dense(384, activation = 'tanh', use_bias = True))
model.add(Dense(256, activation = 'tanh', use_bias = True))
model.add(Dense(225, activation = 'relu', use_bias = True))
model.add(Output(num_output_units, activation = 'softmax', use_bias = True))
model.compile()
model.summary()

gomoku = Gomoku()
player1 = Player('Player 1', 'B')
player2 = Player('Player 2', 'W')
gomoku.start(player1, player2, render = False)


max_turn = 30000

for iteration in range(1, 10000):

    gomoku.restart()
    turn = 'B'
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

        y_pred = model.predict(X)
        pos = y_pred.argmax()
        # if pos == 0:
        #     print(y_pred)
        #     break
        r = pos // 15
        c = pos % 15
        y = None
        try:
            result = curr_player.place(r, c)
            if result == const.PLACE_SUCCESS:
                turn = opponent_player.color
                success = success + 1
            elif result == const.PLACE_WIN:
                y = curr_player.map_prev_move.reshape((225, 1))
                model.fit(X, y, learning_rate = 0.01)
                break
            else:
                print('???')
        except AlreadyPlacedExcpetion:
            y = curr_player.map_prev_move.reshape((225, 1)) * -1
            model.fit(X, y, learning_rate = 0.01)
        
        if y is not None and i % 20 == 0:
            loss = np.sum(np.square(y_pred - y))
            peek = y_pred[0]
            print('{}/{} Step: {} Current attempt: ({}, {}) Loss: {} Peek: {}'.format(i, max_turn, success, r, c, loss, peek), end = '\r')

    gomoku.save()