import numpy as np

from common.exception import ValidationError
from common.env import get_env

class Player():

    def __init__(self, name, color):

        if color not in ['B', 'W']:
            raise ValidationError('Invalid color')

        self.name = name
        self.color = color
        num_grids = get_env('NUM_GRIDS')
        self.map_my_pieces = np.zeros((num_grids, num_grids))
        self.map_prev_move = np.zeros((num_grids, num_grids))
    
    def set_board(self, board):
        self.board = board

    def place(self, r, c):
        self.board.place(r, c, self.color)
        self.map_my_pieces[r][c] = 1
        num_grids = get_env('NUM_GRIDS')
        self.map_prev_move = np.zeros((num_grids, num_grids))
        self.map_prev_move[r][c] = 1