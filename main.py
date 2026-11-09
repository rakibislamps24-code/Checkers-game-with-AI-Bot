# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checker.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checker.game import Game
from checker.minimax.algorithm import minimax

FPS = 60
dp = 3

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Convert the mouse's pixel coordinates into the board's row and column.
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Run the Pygame event loop, process player clicks, and refresh the game display.
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(),dp, WHITE, game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

main()