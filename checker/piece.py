from .constants import SQUARE_SIZE, GREY, CROWN
import pygame

# Represent one checker, including its position, color, king status, and drawing.
class Piece:
    PADDING = 15
    OUTLINE = 2

    # Create a checker at the given board square and calculate its screen position.
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    # Convert the board row and column into the pixel center of this checker.
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    # Mark this checker as a king so it can move in both directions.
    def make_king(self):
        self.king = True
    
    # Draw the checker and, for kings, center the crown image on it.
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    # Update the board coordinates and recalculate the screen position.
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    # Provide the piece's color as its readable representation.
    def __repr__(self):
        return str(self.color)