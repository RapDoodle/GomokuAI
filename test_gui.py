from gomoku.gomoku import Gomoku
from gomoku.player import Player

gomoku = Gomoku()
player1 = Player('Player 1', 'B')
player2 = Player('Player 2', 'W')
gomoku.start(player1, player2)