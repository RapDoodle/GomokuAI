from gomoku.board import GameBoard
from gomoku.player import Player


class Gomoku():

    def __init__(self):
        pass
    
    def start(self, player1, player2):
        self.board = GameBoard(player1, player2)
        self.board.spin()
