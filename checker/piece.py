from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame

#generating coints
class Piece:
    PADDING = 15
    OUTLINE = 2
    #initialize each coint
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
    #help to stay coin middle of the square
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    #turn the coin into a king
    def make_king(self):
        self.king = True

    #draw the actual circle coin
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
    #return the color of coin object so that it can be easy to debug the code
    def __repr__(self):
        return str(self.color)