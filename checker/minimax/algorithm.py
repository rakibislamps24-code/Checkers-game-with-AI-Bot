from copy import deepcopy

from ..constants import RED, WHITE


# *******Alpha-Beta pruning-shoho Minimax diye AI-r jonno shera board khuje ber kori********* 
def minimax(position, depth, max_player, game, alpha=float("-inf"), beta=float("inf")):
    # *********Search-er dike kon player, sheta diye terminal state check kori******* 
    turn = WHITE if max_player else RED
    if depth == 0 or position.winner(turn) is not None:
        return position.evaluate(), position

    if max_player:
        # *********WHITE holo maximizing player; beshi score-er move ta beche ney.******* 
        best_score = float("-inf")
        best_board = None
        # *********Bhalo score-er board age dekhe alpha update kori, jate porer search taratari prune hoy.******* 
        moves = sorted(
            get_all_moves(position, WHITE),
            key=lambda board: board.evaluate(),
            reverse=True,
        )
        for move in moves:
            score = minimax(move, depth - 1, False, game, alpha, beta)[0]
            if score > best_score:
                best_score = score
                best_board = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_score, best_board

    # *********RED holo minimizing player; kom score-er move-ta beche ney******* 
    best_score = float("inf")
    best_board = None
    # *********Kom score-er board age dekhe beta update kori, jate porer search taratari prune hoy.*******
    moves = sorted(
        get_all_moves(position, RED),
        key=lambda board: board.evaluate(),
    )
    for move in moves:
        score = minimax(move, depth - 1, True, game, alpha, beta)[0]
        if score < best_score:
            best_score = score
            best_board = move
        beta = min(beta, best_score)
        if beta <= alpha:
            break

    return best_score, best_board


def simulate_move(piece, move, board, skip):
    # *********Original board-er copy-te move chalai, capture thakle oi piece-gulo soriye dei.******* 
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board


def get_all_moves(board, color):
    # *********Nirdishto color-er prottek piece-er legal move diye notun board state toiri kori.******* 
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # *********Deep copy chara simulation-e ashol board bodle jete pare.******* 
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)

    return moves
