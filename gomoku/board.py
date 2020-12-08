import pygame
import numpy as np

from common.exception import AlreadyPlacedExcpetion, ValidationError
from common.env import get_env

class GameBoard():

    def __init__(self, player1, player2):

        # Setting players
        self.player1 = player1
        self.player2 = player2

        player1.set_board(self)
        player2.set_board(self)

        # Turn
        self.turn = 1
        self.end = False

        # Color scheme
        self.background_color = (255, 206, 115)
        self.grid_color = (0, 0, 0)

        self.window_width = get_env('MARGIN') * 2 + (get_env('NUM_GRIDS') - 1) * get_env('GRID_LEN')
        self.window_height = self.window_width

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.message('Turn: Black')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('./gomoku/fonts/times.ttf', 24)
        self.running = True

        # Grids
        self.grids = np.zeros((get_env('NUM_GRIDS'), get_env('NUM_GRIDS')), dtype=str)

        # Draw the board
        self.draw_board()

    def draw_board(self):
        x1 = 0
        y1 = 0
        x2 = self.window_width
        y2 = self.window_height
        pygame.draw.rect(self.screen, self.background_color,[x1 , y1, x2, y2], 0)
        
        for idx in range(get_env('NUM_GRIDS')):
            # Vertical line
            x1 = get_env('MARGIN') + idx * get_env('GRID_LEN')
            y1 = get_env('MARGIN')
            x2 = x1
            y2 = self.window_height - get_env('MARGIN')
            pygame.draw.line(self.screen, self.grid_color, [x1, y1], [x2, y2], 1)

            # Horizontal line
            x1 = get_env('MARGIN')
            y1 = get_env('MARGIN') + idx * get_env('GRID_LEN')
            x2 = self.window_height - get_env('MARGIN')
            y2 = y1
            pygame.draw.line(self.screen, self.grid_color, [x1, y1], [x2, y2], 1)

        pygame.display.update()
    
    def place(self, r, c, color):
        if color not in ['B', 'W']:
            raise ValidationError('Invalid color')
        
        if r < 0 or r > get_env('NUM_GRIDS') - 1:
            raise ValidationError('Invalid row number')

        if c < 0 or c > get_env('NUM_GRIDS') - 1:
            raise ValidationError('Invalid column number')

        if (self.grids[r][c] == ''):
            self.grids[r][c] = color
        else:
            raise AlreadyPlacedExcpetion()
        
        # Draw the piece
        x = get_env('MARGIN') + c * get_env('GRID_LEN')
        y = get_env('MARGIN') + r * get_env('GRID_LEN')
        r = get_env('GRID_LEN') // 2
        piece_color = (255, 255, 255) if color == 'W' else (0, 0, 0)
        pygame.draw.circle(self.screen, piece_color, [x, y], r)
        pygame.display.update()

    def click_handler(self, event):
        if not self.end:
            r = round((event.pos[1] - get_env('MARGIN')) / get_env('GRID_LEN'))
            c = round((event.pos[0] - get_env('MARGIN')) / get_env('GRID_LEN'))

            try:
                if self.turn == 1:
                    self.player1.place(r, c)
                    self.turn = 2
                    if(self.win_check(r, c, 'B')):
                        self.message('Black Won!')
                    else:
                        self.message('Turn: White')
                else:
                    self.player2.place(r, c)
                    self.turn = 1
                    if(self.win_check(r, c, 'W')):
                        self.message('White Won!')
                    else:
                        self.message('Turn: Black')
            except AlreadyPlacedExcpetion:
                pass
            except ValidationError:
                pass
    
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

    def spin(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # A left click
                        self.click_handler(event)
            self.clock.tick(60)

        pygame.quit()

    def message(self, msg):
        pygame.display.set_caption('Gomoku AI [' + msg + ']')

if __name__ == '__main__':
    game_board = GameBoard()
    game_board.spin()