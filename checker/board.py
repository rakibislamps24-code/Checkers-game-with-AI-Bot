import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

# Store the checkers grid and implement board setup, drawing, and move rules.
class Board:
    # Create the initial grid and initialize remaining-piece and king counts.
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    # Fill the background and draw the alternating playable squares.
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # ***************Calculate and return the heuristic value of the board state.*******************
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    #************************Return all pieces of a given color available on the board.******************
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    # Move a piece to another square and crown it when it reaches the far edge.
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # Promote only when a regular piece reaches its far edge.
        if not piece.king and (
            (piece.color == WHITE and row == ROWS - 1)
            or (piece.color == RED and row == 0)
        ):
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    # Return the piece (or empty-square marker) at the given grid coordinates.
    def get_piece(self, row, col):
        return self.board[row][col]

    # Populate the grid with pieces on the playable squares of the starting rows.
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    # Draw the squares first, then draw every piece currently on the board.
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    # Remove captured pieces from the grid and update the appropriate piece count.
    def remove(self, pieces):
        for piece in pieces:
            if piece == 0:
                continue

            self.board[piece.row][piece.col] = 0
            if piece.color == RED:
                self.red_left -= 1
                if piece.king:
                    self.red_kings -= 1
            else:
                self.white_left -= 1
                if piece.king:
                    self.white_kings -= 1
    
    # Determine the winner from piece counts and the current player's mobility.
    def winner(self, turn=None):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        if turn == RED and not any(
            self.get_valid_moves(piece) for piece in self.get_all_pieces(RED)
        ):
            return WHITE
        if turn == WHITE and not any(
            self.get_valid_moves(piece) for piece in self.get_all_pieces(WHITE)
        ):
            return RED
        
        return None 

    # Collect legal diagonal destinations, including available capture sequences.
    # Kings are checked in both vertical directions; regular pieces move forward.
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    # Scan diagonally left for moves and recursively explore further captures.
    # Each returned map key is a destination; its value lists pieces to capture.
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    # Scan diagonally right for moves and recursively explore further captures.
    # Each returned map key is a destination; its value lists pieces to capture.
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves