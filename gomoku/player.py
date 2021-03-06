import numpy as np

from common.exception import ValidationError
from common.env import get_env

class Player():

    def __init__(self, name, color):

        if color not in ['B', 'W']:
            raise ValidationError('Invalid color')

        self.name = name
        self.color = color
        self.player_init()

    def player_init(self):
        num_grids = get_env('NUM_GRIDS')
        self.map_my_pieces = np.zeros((num_grids, num_grids))
        self.map_prev_move = np.zeros((num_grids, num_grids))
    
    def set_game(self, game):
        self.game = game

    def place(self, r, c):
        res = self.game.place(r, c, self.color)
        self.record_place(r, c)
        return res

    def record_place(self, r, c):
        self.map_my_pieces[r][c] = 1
        num_grids = get_env('NUM_GRIDS')
        self.map_prev_move = np.zeros((num_grids, num_grids))
        self.map_prev_move[r][c] = 1