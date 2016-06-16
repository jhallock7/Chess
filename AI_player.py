"""AI for Chess."""

from Pieces import Move
import random


def AI_choose_move(board, player, depth, attenuation=3/4):
    """Return the best next move determined using a backtracking algorithm.

    Parameters
    ----------
    board : board
        Current board of the game.
    player : str
        "white" or "black", the color of the AI pieces.
    depth : int
        How many moves ahead the algorithm should consider.
    attenuation : float
        Fraction by which to devalue the score contributions
        from predicted future moves.

    Returns
    -------
    move : move
        One of the moves tied as the best, as determined by the algorithm.

    References
    -------
    Skiena, S; "The Algorithm Design Manual".
        Section 7.1 Backtracking. (Pg 231)
    """
    if depth == 0:
        return Move()

    candidates = construct_candidates(board, player)
    if len(candidates) == 0:
        return Move()

    for candidate in candidates:
        # Store current score and make the candidate move
        current_score = board.score
        board.make_move(candidate)
        other_player = "black" if player == "white" else "white"

        # Recursively call AI_choose_move for the other player
        next_move = AI_choose_move(board, other_player, depth - 1)

        # Record relative score change due to move and unmake move
        candidate.score_change = (board.score - current_score
                                  + (next_move.score_change * attenuation))
        board.unmake_move(candidate)

    # Determine the best score change across all the candidate moves
    if player == "white":
        possible_best_move = max(candidates, key=lambda x: x.score_change)
    else:
        possible_best_move = min(candidates, key=lambda x: x.score_change)

    best_score = possible_best_move.score_change

    # Filter out moves not tied for the best score change
    candidates = [candidate
                  for candidate in candidates
                  if candidate.score_change == best_score]

    # Return a random move from the set of moves tied for the best score_change
    return random.choice(candidates)


def construct_candidates(board, player):
    """Return a list of valid moves for the player.

    Parameters
    ----------
    board : board
        Current board of the game.
    player : str
        "white" or "black", the color of the AI pieces.

    Returns
    -------
    candidate_moves : list
        List of valid moves for the player.
    """
    candidate_moves = [move
                       for piece in board.pieces[player]
                       for move in piece.get_moves()]

    return candidate_moves


def AI_make_move(board, player, depth):
    """Calculate the best possible move and make it.

    Parameters
    ----------
    board : board
        Current board of the game.
    player : str
        "white" or "black", the color of the AI pieces.
    depth : int
        How many moves ahead the algorithm should consider.
    """
    move = AI_choose_move(board, player, depth)
    print("%s is moving %s to position %s for %s" %
          (player.capitalize(), move.origin_piece.summary,
           move.destination, move.score_change))
    board.make_move(move)
