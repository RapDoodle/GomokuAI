from board import GameBoard
from player import Player


class Gomoku():

    def __init__(self):
        pass
    
    def start(self, player1, player2):
        self.board = GameBoard(player1, player2)
        self.board.spin()


if __name__ == '__main__':
    gomoku = Gomoku()
    player1 = Player('Player 1', 'B')
    player2 = Player('Player 2', 'W')
    gomoku.start(player1, player2)
