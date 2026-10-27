import pygame

from .board import Board
from .constants import COLS, RED, ROWS, WHITE


class Game:
    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.selected = None
        self.turn = RED
        self.valid_moves = {}

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()

    def winner(self):
        if self.board.red_left <= 0:
            return WHITE
        if self.board.white_left <= 0:
            return RED
        if not self._has_moves(self.turn):
            return WHITE if self.turn == RED else RED
        return None

    def select(self, row, col):
        if not (0 <= row < ROWS and 0 <= col < COLS):
            return False

        if self.selected is not None and (row, col) in self.valid_moves:
            return self._move(row, col)

        piece = self.board.board[row][col]
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece)
            return bool(self.valid_moves)

        self.selected = None
        self.valid_moves = {}
        return False

    def get_valid_moves(self, piece):
        captures = self._captures_for(piece)
        if captures:
            return captures

        has_capture = any(
            self._captures_for(other)
            for row in self.board.board
            for other in row
            if other != 0 and other.color == self.turn
        )
        if has_capture:
            return {}

        moves = {}
        for row_delta, col_delta in self._directions(piece):
            row, col = piece.row + row_delta, piece.col + col_delta
            if self._inside_board(row, col) and self.board.board[row][col] == 0:
                moves[(row, col)] = []
        return moves

    def _move(self, row, col):
        piece = self.selected
        if piece is None:
            return False

        captured = self.valid_moves[(row, col)]
        old_row = piece.row
        old_col = piece.col
        piece.move(row, col)
        self.board.board[old_row][old_col] = 0
        self.board.board[row][col] = piece
        self._remove(captured)

        became_king = not piece.king and (
            (piece.color == RED and row == 0)
            or (piece.color == WHITE and row == ROWS - 1)
        )
        if became_king:
            piece.make_king()
            if piece.color == RED:
                self.board.red_kings += 1
            else:
                self.board.white_kings += 1

        follow_up_captures = {} if became_king else self._captures_for(piece)
        if captured and follow_up_captures:
            self.selected = piece
            self.valid_moves = follow_up_captures
        else:
            self.selected = None
            self.valid_moves = {}
            self.change_turn()
        return True

    def _captures_for(self, piece):
        captures = {}
        for row_delta, col_delta in self._directions(piece):
            middle_row = piece.row + row_delta
            middle_col = piece.col + col_delta
            target_row = piece.row + row_delta * 2
            target_col = piece.col + col_delta * 2
            if not self._inside_board(target_row, target_col):
                continue

            middle = self.board.board[middle_row][middle_col]
            if (middle != 0 and middle.color != piece.color
                    and self.board.board[target_row][target_col] == 0):
                captures[(target_row, target_col)] = [middle]
        return captures

    def _directions(self, piece):
        directions = []
        if piece.color == RED or piece.king:
            directions.extend(((-1, -1), (-1, 1)))
        if piece.color == WHITE or piece.king:
            directions.extend(((1, -1), (1, 1)))
        return directions

    def _has_moves(self, color):
        for row in self.board.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    if self._captures_for(piece) or self._simple_moves_for(piece):
                        return True
        return False

    def _simple_moves_for(self, piece):
        for row_delta, col_delta in self._directions(piece):
            row, col = piece.row + row_delta, piece.col + col_delta
            if self._inside_board(row, col) and self.board.board[row][col] == 0:
                return True
        return False

    def _remove(self, pieces):
        for piece in pieces:
            self.board.board[piece.row][piece.col] = 0
            if piece.color == RED:
                self.board.red_left -= 1
                if piece.king:
                    self.board.red_kings -= 1
            else:
                self.board.white_left -= 1
                if piece.king:
                    self.board.white_kings -= 1

    @staticmethod
    def _inside_board(row, col):
        return 0 <= row < ROWS and 0 <= col < COLS

    def change_turn(self):
        self.turn = WHITE if self.turn == RED else RED
