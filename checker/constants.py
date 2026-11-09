import pygame

#size of board and square
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

#Board-er jonn ivory ar forest-green palette.
LIGHT_SQUARE = (238, 232, 213)
DARK_SQUARE = (46, 64, 59)
BACKGROUND = (24, 35, 34)

#RED human player, WHITE AI;
RED = (176, 55, 72)
WHITE = (247, 244, 230)
BLUE = (72, 174, 151)
GREY = (35, 43, 42)

CROWN = pygame.transform.scale(pygame.image.load('assets/assets/crown.png'), (44, 25))
