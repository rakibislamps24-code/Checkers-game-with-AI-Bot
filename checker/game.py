import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checker.board import Board

# Coordinate the current turn, player selections, legal moves, and board display.
class Game:
    # Set up a new game and associate it with the Pygame window.
    def __init__(self, win):
        self._init()
        self.win = win
    
    # Redraw the board and legal-move indicators, then refresh the window.
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    # Reset the board, current player, selection, and cached legal moves.
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    # Return the winner reported by the board, or None if play can continue.
    def winner(self):
        return self.board.winner(self.turn)

    # Start a fresh game using the same game window.
    def reset(self):
        self._init()

    # Select a piece belonging to the current player or attempt a legal move.
    # If a selected move fails, allow the clicked square to be selected instead.
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    # Move the selected piece to a cached legal destination and remove captures.
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    # Draw a blue marker on each destination in the supplied legal-move map.
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    # Clear cached moves and switch control to the other player.
    def change_turn(self):
        self.selected = None
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
    #***********************return the current game board**************************************
    def get_board(self):
        return self.board
    #***********************return the current game board after ai move**************************************
    def ai_move(self, board):
        self.board = board
        self.change_turn()