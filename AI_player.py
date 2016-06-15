"""AI for Chess."""

from Pieces import Move
import random

def AI_choose_move(board, player, depth):
    """Returns the best next move determined using a backtracking algorithm.

    Parameters
    ----------
    board : board
        Current board of the game.

    player : string
        "white" or "black", the color of the AI pieces.

    depth : integer
        How many moves ahead the algorithm should consider.

    Returns
    -------
    move : move
        One of the moves tied as the best, as determined by the algorithm.
    """
    if depth == 0:
        return Move()

    candidates = construct_candidates(board, player)
    if len(candidates) == 0:
        return Move()

    for candidate in candidates:
        current_score = board.score
        board.make_move(candidate)
        score_change = board.score - current_score
        other_player = "black" if player == "white" else "white"

        next_move = AI_choose_move(board, other_player, depth - 1)

        candidate.score_change = score_change + (next_move.score_change*(3/4))
        board.unmake_move(candidate)

    if player == "white":
        possible_best_move = max(candidates, key=lambda x: x.score_change)
    else:
        possible_best_move = min(candidates, key=lambda x: x.score_change)

    best_score = possible_best_move.score_change

    # Filter out moves not tied for the best score change
    candidates = [candidate for candidate in candidates if candidate.score_change == best_score]

    # Return a random move from the set of moves tied for the best score_change
    move = random.choice(candidates)
    return move

def construct_candidates(board, player):
    """Returns a list of valid moves for the player.

    Parameters
    ----------
    board : board
        Current board of the game.

    player : string
        "white" or "black", the color of the AI pieces.

    Returns
    -------
    candidate_moves : list
        List of valid moves for the player.
    """
    candidate_moves = []
    for piece in board.pieces[player]:
        for move in piece.get_moves():
            candidate_moves.append(move)
    return candidate_moves

def AI_make_move(board, player, depth):
    """Returns a list of valid moves for the player.

    Parameters
    ----------
    board : board
        Current board of the game.

    player : string
        "white" or "black", the color of the AI pieces.

    Returns
    -------
    candidate_moves : list
        List of valid moves for the player.
    """
    move = AI_choose_move(board, player, depth)
    print("%s is moving %s to position %s for %s" %
          (player.capitalize(), move.origin_piece.summary, move.destination, move.score_change))
    board.make_move(move)
