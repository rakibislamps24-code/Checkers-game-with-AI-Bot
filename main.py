# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checker.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from checker.game import Game
from checker.minimax.algorithm import minimax

FPS = 60
DEPTH = 3

# Convert the mouse's pixel coordinates into the board's row and column.
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Run the Pygame event loop, process player clicks, and refresh the game display.
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    run = True
    clock = pygame.time.Clock()
    game = Game(win)

    while run:
        clock.tick(FPS)

        winner = game.winner()
        if winner is not None:
            print(winner)
            break

        # *********AI-r turn-e WHITE-r jonno depth-limited Alpha-Beta Minimax chalai.******* 
        if game.turn == WHITE:
            _, new_board = minimax(game.get_board(), DEPTH, True, game)
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()