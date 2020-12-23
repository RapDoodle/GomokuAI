import numpy as np
import pandas as pd
import keras
import tensorflow as tf
from datetime import datetime
from keras.models import Sequential
from keras.layers import Dropout, Dense, Conv2D, MaxPooling2D, Flatten

import common.constant as const
from gomoku.player import Player
from gomoku.gomoku import Gomoku
from common.exception import AlreadyPlacedExcpetion

gomoku = Gomoku()
player1 = Player('Player 1', 'B')
player2 = Player('Player 2', 'W')
gomoku.start(player1, player2, render = False)

# Initialising the ANN
model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))

model.add(Flatten())

model.add(Dense(512, activation='relu'))

model.add(Dense(256, activation='relu'))

model.add(Dense(units = 225, kernel_initializer = 'uniform', activation = 'softmax'))

model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

df = pd.DataFrame(columns = ['iteration', 'max_step', 'black_win_rate', 'white_win_rate', 'valid_click_rate'])

now = datetime.now()
t_str = now.strftime("%Y-%m-%d %H-%M-%S")

max_iter = 10000
max_turn = 10000

black_win_count = 0
white_win_count = 0

for iteration in range(1, 10000):
    
    print('Iteration: {}/{}:'.format(iteration, max_iter))

    gomoku.restart()
    
    turn = 'B'
    player1.place(7, 7)
    turn = 'W'
    success = 0
    valid_click_rate = 0


    for i in range(1, max_turn):
        if turn == 'B':
            curr_player = player1
            opponent_player = player2
            
        else:
            curr_player = player2
            opponent_player = player1
        
        X = curr_player.map_my_pieces.reshape((1, 225))
        X = np.append(X, opponent_player.map_my_pieces.reshape((1, 225)), axis = 1)
        
        y_pred = model.predict(X)
        
        # pos = y_pred.argmax()
        pos = y_pred.argmax()
        r = pos // 15
        c = pos % 15
        
        try:
            result = curr_player.place(r, c)
            if result == const.PLACE_SUCCESS:
                turn = opponent_player.color
                success = success + 1
                
            elif result == const.PLACE_WIN:
                y_reward = curr_player.map_prev_move.reshape((1, 225))
                model.fit(X, y_reward, verbose = 0)
                
                if curr_player.color == 'B':
                    black_win_count = black_win_count + 1
                else:
                    white_win_count = white_win_count + 1
                
                break
                
        except AlreadyPlacedExcpetion:
            y_reward = curr_player.map_prev_move.reshape((1, 225)) * -1
            model.fit(X, y_reward, verbose = 0)
        
        if i % 10 == 0:
            valid_click_rate = success / i
            print(' ' * 100, end = '\r')
            print('{}/{} Step: {} Current attempt: ({}, {}) Valid click rate: {:.2f}'.format(i, max_turn, success, r, c, valid_click_rate), end = '\r')
    
    print(' ' * 100, end = '\r')
    print('{} won! Max step: {} Current attempt: ({}, {}) Valid click rate: {:.2f}'.format(curr_player.name, success, r, c, valid_click_rate))
    
    df.at[iteration - 1, 'iteration'] = iteration
    df.at[iteration - 1, 'max_step'] = success
    df.at[iteration - 1, 'black_win_rate'] = black_win_count / iteration
    df.at[iteration - 1, 'white_win_rate'] = white_win_count / iteration
    df.at[iteration - 1, 'valid_click_rate'] = valid_click_rate
    
    gomoku.save('{} {}'.format(t_str, iteration))
    
    if iteration % 1 == 0:
        df.to_csv('./statistics/{}.csv'.format(t_str))