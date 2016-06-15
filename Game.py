"""Game object for chess; runs a game if called from command line."""

from Board import Board
from Pieces import Move
from AI_player import AI_make_move


class Game:
    """Chess game object.

    Parameters
    ----------
    white : str
        "user" or "AI", indicating whether the white
        pieces will be played by a user or by an AI.
    white_depth : int
        For an AI player playing for white, indicates the number of moves
        ahead to calculate when choosing moves; None for user players.
    black : str
        "user" or "AI", indicating whether the black
        pieces will be played by a user or by an AI.
    black_depth : int
        For an AI player playing for black, indicates the number of moves
        ahead to calculate when choosing moves; None for user players.

    Attributes
    ----------
    players : dict
        Dictionary specifying the type of player for each color:
            ("user", None) for users;
            ("AI", depth) for AIs.
    turn : int
        The current turn.
    board : board
        The Board object for the game.

    Methods
    ----------
    print_board()
        Prints the board.
    get_user_move()
        Obtains a move from the user.
    is_valid_move(move)
        Checks if the move is a valid move.
    make_user_move(player)
        Retrieves a valid move from the user and makes the move.
    do_turn(player)
        Performs a turn in the game for the given player.
    play_game()
        Plays a game.
    """

    def __init__(self, white, white_depth, black, black_depth):
        """Initialize a Game object."""
        self.players = {"white": (white, white_depth),
                        "black": (black, black_depth)
                        }
        self.turn = 0
        self.board = Board()

    def print_board(self):
        """Print the board."""
        self.board.print_grid()

    def get_user_move(self):
        """Obtain a move from the user.

        Returns
        -------
        origin_x : int
            The x position of the piece being moved.
        origin_y : int
            The y position of the piece being moved.
        target_x : int
            The x position of the location to which the piece is being moved.
        target_y : int
            The y position of the location to which the piece is being moved.
        """
        try:
            origin_x = int(input("STARTING X position: "))
            origin_y = int(input("STARTING Y position: "))

            target_x = int(input("ENDING X position: "))
            target_y = int(input("ENDING Y position: "))
        except ValueError:
            print("Not a valid input\n")
            origin_x, origin_y, target_x, target_y = self.get_user_move()

        return origin_x, origin_y, target_x, target_y

    def is_valid_move(self, move):
        """Check if the move is a valid move.

        Parameters
        ----------
        move : move
            The move object to be checked if valid.

        Returns
        -------
        is_valid : bool
            True if the move is valid.
        """
        move_summaries = [piece_move.summary
                          for piece_move in move.origin_piece.get_moves()]
        if move.summary in move_summaries:
            return True
        return False

    def make_user_move(self, player):
        """Retrive a valid move from the user and make the move.

        Parameters
        ----------
        player : str
            The player making the move.
        """
        valid_move = False

        while valid_move is False:

            origin_x, origin_y, target_x, target_y = self.get_user_move()

            if self.board._inbounds((origin_x, origin_y)) is False:
                print("Starting position was out of bounds")
                continue

            if self.board._inbounds((target_x, target_y)) is False:
                print("Ending position was out of bounds")
                continue

            origin_piece = self.board.grid[origin_y][origin_x]
            target_piece = self.board.grid[target_y][target_x]

            if origin_piece == 'empty':
                print("Piece is empty")
                continue

            if origin_piece.player != player:
                print("You can't move the other player's piece")
                continue

            user_move = Move((origin_x, origin_y), origin_piece, (target_x, target_y), target_piece)

            if self.is_valid_move(user_move) is False:
                print("Move was not valid")
            else:
                valid_move = True

        self.board.make_move(user_move)

    def do_turn(self, player):
        """Perform a turn in the game for the given player.

        Parameters
        ----------
        player : str
            The player making the move.

        Returns
        -------
        white_check : bool
            True if player white is in check.
        black_check : bool
            True if player black is in check.
        white_won : bool
            True if player white won.
        black_won : bool
            True if player black won.
        """
        white_check = False
        black_check = False
        white_won = False
        black_won = False

        print()
        # Make move
        if self.players[player][0] == "user":
            self.make_user_move(player)
        else:
            AI_make_move(self.board, player, self.players[player][1])
        self.print_board()

        # Check if a player is in check.
        if self.board.check_check("white"):
            white_check = True
            print("PLAYER WHITE IS IN CHECK!")
        if self.board.check_check("black"):
            black_check = True
            print("PLAYER BLACK IS IN CHECK!")

        # Check if a player won.
        if self.board.check_won("white"):
            white_won = True
            print("PLAYER WHITE WON! Score:", self.board.score)
        if self.board.check_won("black"):
            black_won = True
            print("PLAYER BLACK WON! Score:", self.board.score)

        # If neither player won, print board stats
        if white_won is False and black_won is False:
            other_player = "white" if player == "black" else "black"
            print("%s's turn, Turn" % other_player.capitalize(), self.turn + 1,
                  ', Score', self.board.score,
                  ', Pieces', self.board.num_pieces, '...')

        # Increment turn count if player black just moved.
        if player == "black":
            self.turn += 1

        return white_check, black_check, white_won, black_won

    def play_game(self):
        """Play a game.

        Returns
        -------
        white_won : bool
            True if player white won.
        black_won : bool
            True if player black won.
        """
        self.print_board()
        for turn in range(10000):
            white_check, black_check, white_won, black_won = self.do_turn("white")
            if white_won or black_won:
                break
            white_check, black_check, white_won, black_won = self.do_turn("black")
            if white_won or black_won:
                break

        return white_won, black_won


def initialize_players():
    """Retrieve from the user info about the players needed to create a Game.

    Returns
    -------
    white : str
        "user" or "AI", indicating whether the white
        pieces will be played by a user or by an AI.
    white_depth : int
        For an AI player playing for white, indicates the number of moves
        ahead to calculate when choosing moves; None for user players.
    black : str
        "user" or "AI", indicating whether the black
        pieces will be played by a user or by an AI.
    black_depth : int
        For an AI player playing for black, indicates the number of moves
        ahead to calculate when choosing moves; None for user players.
    """
    white = input("Would you like player white to be an AI (a) or a user (u)?: ")
    while white not in ['u', 'a']:
        print("Input must be either (u) or (a)")
        white = input("Would you like player white to be an AI (a) or a user (u)?: ")

    white = "user" if white == 'u' else 'AI'
    if white == 'AI':
        white_depth = int(input("with a depth parameter of...?: "))
    else:
        white_depth = None

    black = input("Would you like player black to be an AI (a) or a user (u)?: ")
    while black not in ['u', 'a']:
        print("Input must be either (u) or (a)")
        black = input("Would you like player black to be an AI (a) or a user (u)?: ")

    black = "user" if black == 'u' else 'AI'
    if black == 'AI':
        black_depth = int(input("with a depth parameter of...?: "))
    else:
        black_depth = None

    return white, white_depth, black, black_depth


if __name__ == "__main__":
    Game(*initialize_players()).play_game()
