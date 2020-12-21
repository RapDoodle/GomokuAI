import pygame
import numpy as np

from common.exception import AlreadyPlacedExcpetion, ValidationError
from common.env import get_env

class GameBoard():

    def __init__(self, game = None):

        self.game = game

        # Font
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)

        # Color scheme
        self.background_color = (255, 206, 115)
        self.grid_color = (0, 0, 0)

        self.window_width = get_env('MARGIN') * 2 + (get_env('NUM_GRIDS') - 1) * get_env('GRID_LEN')
        self.window_height = self.window_width

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('./gomoku/fonts/times.ttf', 24)
        self.running = True

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
    
    def render_piece(self, r, c, piece_color, render_count = False, count_color = None, count = None):
        # Draw the piece
        x = get_env('MARGIN') + c * get_env('GRID_LEN')
        y = get_env('MARGIN') + r * get_env('GRID_LEN')
        r = get_env('GRID_LEN') // 2

        pygame.draw.circle(self.screen, piece_color, [x, y], r)
        
        step_num = self.font.render(str(count), False, count_color)
        box_x = step_num.get_rect().width
        box_y = step_num.get_rect().height

        self.screen.blit(step_num, (x - box_x // 2 + 1, y - box_y // 2))
        pygame.display.update()

    def click_handler(self, event):
        if self.game is not None:
            r = round((event.pos[1] - get_env('MARGIN')) / get_env('GRID_LEN'))
            c = round((event.pos[0] - get_env('MARGIN')) / get_env('GRID_LEN'))
            self.game.click(r, c)

    def spin(self):
        while self.running:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # A left click
                        self.click_handler(event)
                elif event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game is not None:
                        if event.key == pygame.K_r:
                            self.game.restart()
                        elif event.key == pygame.K_s:
                            self.game.save()
                        elif event.key == pygame.K_l:
                            self.game.load()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def set_title(self, msg):
        pygame.display.set_caption('Gomoku AI [' + msg + ']')

if __name__ == '__main__':
    game_board = GameBoard()
    game_board.spin()