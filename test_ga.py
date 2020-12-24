from nn.genetic_algorithm.layers import GAInput, GADense, GAOutput
from nn.genetic_algorithm.model import GAModel, GASequentialModel
from gomoku.gomoku import Gomoku
from gomoku.player import Player
import numpy as np
import common.constant as const
from common.exception import AlreadyPlacedExcpetion

model = GAModel(population = 2000)

model.add(GAInput(450))
model.add(GADense(384, activation = 'tanh', use_bias = True))
model.add(GADense(256, activation = 'tanh', use_bias = True))
model.add(GAOutput(225, activation = 'softmax', use_bias = True))

model.new_population()

def cal_reward(step, win):
    return step + (win * (550 - step))

max_turn = 1000

def play_gomoku(model, params):

    gomoku = Gomoku()
    player1 = Player('Player 1', 'B')
    player2 = Player('Player 2', 'W')
    gomoku.start(player1, player2, render = False)
    
    turn = 'B'
    player1.place(7, 7)
    turn = 'W'
    step = 1
    win = 0
    # valid_click_rate = 0


    for i in range(1, max_turn):
        if turn == 'B':
            curr_player = player1
            opponent_player = player2
            
        else:
            curr_player = player2
            opponent_player = player1
        
        X = curr_player.map_my_pieces.reshape((225, 1))
        X = np.append(X, opponent_player.map_my_pieces.reshape((225, 1)), axis = 0)
        
        y_pred = model.predict(X)
        
        # pos = y_pred.argmax()
        pos = y_pred.argmax()
        r = pos // 15
        c = pos % 15
        
        try:
            result = curr_player.place(r, c)
            step = step + 1
            
            if result == const.PLACE_SUCCESS:
                turn = opponent_player.color
                
            elif result == const.PLACE_WIN:
                if curr_player.color == 'B':
                    black_win_count = black_win_count + 1
                else:
                    white_win_count = white_win_count + 1
                
                win = 1
                
        except AlreadyPlacedExcpetion:
            break
            
        # if i % 1 == 0:
        #     valid_click_rate = step / i
        #     print(' ' * 100, end = '\r')
        #     print('{}/{} Step: {} Current attempt: ({}, {}) Valid click rate: {:.2f}'.format(i, max_turn, step, r, c, valid_click_rate), end = '\r')
            
        if win:
            break
    
    model.set_reward(cal_reward(step, win))
    # print('\n', model.reward)
    # gomoku.save('{} {}'.format(t_str, iteration))

for i in range(500):
    model.simulate(play_gomoku, keep_rate=0.6, mutate_rate=0.05)