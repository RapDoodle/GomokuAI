import time
import numpy as np
import pandas as pd
import pygame

from common.exception import AlreadyPlacedExcpetion, ValidationError
from gomoku.board import GameBoard
from gomoku.player import Player
from common.env import get_env
from gomoku.message_box import info_message_box

class Gomoku():

    def __init__(self):
        # Grids
        self.grids = np.zeros((get_env('NUM_GRIDS'), get_env('NUM_GRIDS')), dtype=str)

        self.player1 = None
        self.player2 = None
        self.log = []
    
    def start(self, player1, player2):
        self.board = GameBoard(game = self)

        # Setting players
        self.player1 = player1
        self.player2 = player2

        player1.set_board(self)
        player2.set_board(self)

        self.game_init()

        self.board.spin()

    def restart(self):
        self.game_init()
        self.player1.player_init()
        self.player2.player_init()
        self.log = []
        self.board.draw_board()

    def game_init(self):
        self.grids = np.zeros((get_env('NUM_GRIDS'), get_env('NUM_GRIDS')), dtype=str)

        self.board.draw_board()

        # Turn
        self.turn = 1
        self.end = False
        self.count = 1

    def place(self, r, c, turn_check = None):
        if turn_check is not None:
            if (self.turn == 1 and turn_check == 'W') or (self.turn == 2 and turn_check == 'B'):
                raise ValidationError('Turn check failed')
            elif turn_check not in ['W', 'B']:
                raise ValidationError('Invaid turn identifier')
        
        if r < 0 or r > get_env('NUM_GRIDS') - 1:
            raise ValidationError('Invalid row number')

        if c < 0 or c > get_env('NUM_GRIDS') - 1:
            raise ValidationError('Invalid column number')
        
        if self.turn == 1:
            color = 'B'
        else:
            color = 'W'

        if (self.grids[r][c] == ''):
            self.grids[r][c] = color
        else:
            raise AlreadyPlacedExcpetion()

        piece_color = (255, 255, 255) if color == 'W' else (0, 0, 0)
        count_color = (0, 0, 0) if color == 'W' else (255, 255, 255)

        self.board.render_piece(r, c, piece_color = piece_color, 
            render_count = True, count = self.count, count_color = count_color)
        
        self.log.append((r, c, color, self.count))
        self.count = self.count + 1

    def click(self, r, c, ignore_message = False, verify_color = None):
        if not self.end:
            if verify_color is not None:
                if (self.turn == 1 and verify_color == 'W') or (self.turn == 2 and verify_color == 'B'):
                    raise ValidationError('Incorrect color in log')

            try:
                if self.turn == 1:
                    self.player1.place(r, c)
                    self.turn = 2
                    if self.win_check(r, c, 'B'):
                        if ignore_message:
                            self.board.set_title('Black Won!')
                        else:
                            info_message_box('Black Won!')
                    else:
                        self.board.set_title('Turn: White')
                else:
                    self.player2.place(r, c)
                    self.turn = 1
                    if self.win_check(r, c, 'W'):
                        if ignore_message:
                            self.board.set_title('White Won!')
                        else: 
                            info_message_box('White Won!')
                    else:
                        self.board.set_title('Turn: Black')
            except AlreadyPlacedExcpetion:
                print('Already placed.')
                # pass
            except ValidationError:
                print('Validation error')
                # pass

    def win_check(self, r, c, color):
        ns_dir_count = self.get_continuous_count(r, c, 1, 0, color)
        ws_dir_count = self.get_continuous_count(r, c, 0, 1, color)
        nw_se_dir_count = self.get_continuous_count(r, c, 1, 1, color)
        ne_sw_dir_count = self.get_continuous_count(r, c, 1, -1, color)
        
        if (ns_dir_count >= 5 or ws_dir_count >= 5 or 
            nw_se_dir_count >= 5 or ne_sw_dir_count >= 5):
            self.end = True
            return True
        
        return False

    def get_continuous_count(self, r, c, dr, dc, color):
        if color not in ['B', 'W']:
            raise ValidationError('Invalid color')
        
        if self.grids[r][c] != color:
            return 0

        count = 1
        d1_end = False
        d2_end = False

        d1_curr_r = r
        d1_curr_c = c

        d2_curr_r = r
        d2_curr_c = c

        while not d1_end or not d2_end:

            d1_curr_r = d1_curr_r + dr
            d1_curr_c = d1_curr_c + dc

            d2_curr_r = d2_curr_r - dr
            d2_curr_c = d2_curr_c - dc

            if d1_curr_r < 0 or d1_curr_r > get_env('NUM_GRIDS') - 1:
                d1_end = True
            if d1_curr_c < 0 or d1_curr_c > get_env('NUM_GRIDS') - 1:
                d1_end = True
            if d2_curr_r < 0 or d2_curr_r > get_env('NUM_GRIDS') - 1:
                d2_end = True
            if d2_curr_c < 0 or d2_curr_c > get_env('NUM_GRIDS') - 1:
                d2_end = True
            
            if not d1_end:
                if self.grids[d1_curr_r][d1_curr_c] == color:
                    count = count + 1
                else:
                    d1_end = True
            if not d2_end:
                if self.grids[d2_curr_r][d2_curr_c] == color:
                    count = count + 1
                else:
                    d2_end = True
            
        return count
        
    def save(self):
        df = pd.DataFrame(self.log, columns = ['row', 'column', 'color', 'step']) 
        df.to_csv('./test.csv', index = False)

    def load(self):
        self.game_init()

        df = pd.read_csv('./test.csv')
        for idx, row in df.iterrows():
            self.click(row['row'], row['column'], ignore_message = True, verify_color = row['color'])
            pygame.time.wait(100)
            pygame.event.pump()

