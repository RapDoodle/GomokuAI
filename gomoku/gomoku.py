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
        self.render = False
    
    def start(self, player1, player2, render = False):
        # Setting players
        self.player1 = player1
        self.player2 = player2

        player1.set_game(self)
        player2.set_game(self)

        self.game_init()

        if render:
            self.render = True
            self.board = GameBoard(game = self)
            self.board.draw_board()
            self.board.spin()

    def restart(self):
        self.game_init()
        self.player1.player_init()
        self.player2.player_init()
        self.log = []
        if self.render:
            self.board.draw_board()

    def game_init(self):
        self.grids = np.zeros((get_env('NUM_GRIDS'), get_env('NUM_GRIDS')), dtype=str)

        # Turn
        self.turn = 'B'
        self.end = False
        self.count = 1

        if self.render:
            self.board.draw_board()

    def place(self, r, c, turn_check = None, ignore_message = False):
        if turn_check is not None:
            if turn_check not in ['W', 'B']:
                raise ValidationError('invaid turn identifier')
            elif self.turn != turn_check:
                raise ValidationError('turn check failed')
        
        if r < 0 or r > get_env('NUM_GRIDS') - 1:
            raise ValidationError('invalid row number')

        if c < 0 or c > get_env('NUM_GRIDS') - 1:
            raise ValidationError('invalid column number')
        
        if self.turn == 'B':
            curr_player = self.player1
            opponent_player = self.player2
        else:
            curr_player = self.player2
            opponent_player = self.player1

        if (self.grids[r][c] == ''):
            self.grids[r][c] = curr_player.color
        else:
            raise AlreadyPlacedExcpetion()

        curr_player.record_place(r, c)

        # If no exception occurred
        if self.win_check(r, c, curr_player.color):
            msg = curr_player.name + ' won'
            if self.render:
                if ignore_message:
                    self.board.set_title(msg)
                else:
                    info_message_box(msg)
            else:
                print(msg)
        else:
            if self.render:
                if opponent_player.color == 'B':
                    self.board.set_title('Turn: black')
                else:
                    self.board.set_title('Turn: white')
        
        if self.render:
            piece_color = (255, 255, 255) if curr_player.color == 'W' else (0, 0, 0)
            count_color = (0, 0, 0) if curr_player.color == 'W' else (255, 255, 255)

            self.board.render_piece(r, c, piece_color = piece_color, 
                render_count = True, count = self.count, count_color = count_color)
        
        self.log.append((r, c, curr_player.color, self.count))
        self.count = self.count + 1

        # Handover the turn
        self.turn = opponent_player.color
        
        return True

    def click(self, r, c, ignore_message = False, verify_color = None):
        if not self.end:
            if verify_color is not None:
                if self.turn != verify_color:
                    raise ValidationError('incorrect color in log')

            try:
                self.place(r, c, turn_check = verify_color, ignore_message = ignore_message)
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
        for _, row in df.iterrows():
            self.click(row['row'], row['column'], ignore_message = True, verify_color = row['color'])
            pygame.time.wait(100)
            pygame.event.pump()

