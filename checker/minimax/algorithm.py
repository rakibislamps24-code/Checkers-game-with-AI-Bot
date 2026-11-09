from copy import deepcopy
from ..constants import RED, WHITE
#***************Code for minimax***************
def minimax(position, depth, max_player, game):
    turn = WHITE if max_player else RED
    if depth == 0 or position.winner(turn) is not None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):#it will look all the possible moves for the white player or max player
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):#it will look all the possible moves for the red player or min player
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move

    #min player


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board, color, game):
    moves = []

#for each piece in the board of that color get all the valid moves
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        #for each valid move add it to the list
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)#make a copy of the board
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves