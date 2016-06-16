"""Board object for chess."""

from Pieces import Piece


class Board():
    """Chess board object.

    Attributes
    ----------
    grid : list
        List of lists representing the board
        and containing pointers to the pieces.
    score : int
        The current score.
    num_pieces : int
        The number of pieces remaining on the board.
    kings : dict
        Dictionary containing pointers to the two kings.
    pieces : dict
        Dictionary containing pointers to the pieces
        on the board, grouped by color.

    Methods
    ----------
    _inbounds(position)
        Returns True if the position is within the bounds of the board.
    make_move(move)
        Makes the move on the board.
    unmake_move(move)
        Unmakes the move on the board.
    check_check(player)
        Returns True if the player is in check.
    check_won(player)
        Returns True if the player won.
    print_board()
        Prints the board.
    """

    def __init__(self):
        """Initialize a Board object."""
        self.grid = []
        self.score = 0
        self.num_pieces = 32
        self.kings = {}

        # List of pieces on the board
        self.pieces = {"white": [],
                       "black": []}

        # WHITE pieces
        self.pieces["white"].append(Piece(self, (0, 0), "white", "rook"))
        self.pieces["white"].append(Piece(self, (1, 0), "white", "knight"))
        self.pieces["white"].append(Piece(self, (2, 0), "white", "bishop"))
        self.pieces["white"].append(Piece(self, (3, 0), "white", "queen"))
        self.pieces["white"].append(Piece(self, (4, 0), "white", "king"))
        self.pieces["white"].append(Piece(self, (5, 0), "white", "bishop"))
        self.pieces["white"].append(Piece(self, (6, 0), "white", "knight"))
        self.pieces["white"].append(Piece(self, (7, 0), "white", "rook"))

        for col in range(8):
            self.pieces["white"].append(Piece(self, (col, 1), "white", "pawn"))

        # BLACK pieces
        for col in range(8):
            self.pieces["black"].append(Piece(self, (col, 6), "black", "pawn"))

        self.pieces["black"].append(Piece(self, (0, 7), "black", "rook"))
        self.pieces["black"].append(Piece(self, (1, 7), "black", "knight"))
        self.pieces["black"].append(Piece(self, (2, 7), "black", "bishop"))
        self.pieces["black"].append(Piece(self, (3, 7), "black", "queen"))
        self.pieces["black"].append(Piece(self, (4, 7), "black", "king"))
        self.pieces["black"].append(Piece(self, (5, 7), "black", "bishop"))
        self.pieces["black"].append(Piece(self, (6, 7), "black", "knight"))
        self.pieces["black"].append(Piece(self, (7, 7), "black", "rook"))

        # Instantiate grid
        for row in range(8):
            self.grid.append([])
            for col in range(8):
                self.grid[row].append("empty")

        # Place pieces in grid
        for piece_list in self.pieces.values():
            for piece in piece_list:
                self.grid[piece.position[1]][piece.position[0]] = piece

        # Set King pointers
        self.kings["white"] = [piece
                               for piece in self.pieces["white"]
                               if piece.piece_type == "king"]
        self.kings["black"] = [piece
                               for piece in self.pieces["black"]
                               if piece.piece_type == "king"]

    def _inbounds(self, position):
        """Return True if the position is within the bounds of the board.

        Parameters
        ----------
        position : tuple
            A position potentially on the board.

        Returns
        -------
        inbounds : bool
            True if the position is within the bounds of the board.
        """
        if position[0] < 0 or 7 < position[0]:
            return False
        if position[1] < 0 or 7 < position[1]:
            return False
        return True

    def make_move(self, move):
        """Make the move on the board.

        Parameters
        ----------
        move : move
            A move object to make on the board.
        """
        # Change grid pointers
        self.grid[move.origin[1]][move.origin[0]] = "empty"
        self.grid[move.destination[1]][move.destination[0]] = move.origin_piece

        # Change piece position attributes (no need to change in dest piece)
        move.origin_piece.position = move.destination

        # Delete dest piece from list of pieces if necessary
        if move.destination_piece != 'empty':
            player = move.destination_piece.player
            index_of_piece = self.pieces[player].index(move.destination_piece)
            del self.pieces[player][index_of_piece]
            # Change score and num_pieces
            self.score -= move.destination_piece.value
            self.num_pieces -= 1

        # Check if a pawn is reaching the last row
        if move.origin_piece.piece_type == 'pawn':
            if move.origin_piece.player == 'white' and move.destination[1] == 7:
                move.origin_piece.piece_behavior = 'queen'
                self.score += 16
                move.pawn_change = True

            if move.origin_piece.player == 'black' and move.destination[1] == 0:
                move.origin_piece.piece_behavior = 'queen'
                self.score -= 16
                move.pawn_change = True

    def unmake_move(self, move):
        """Unmake the move on the board.

        Parameters
        ----------
        move : move
            A move object to undo on the board.
        """
        # Change grid pointers
        self.grid[move.origin[1]][move.origin[0]] = move.origin_piece
        self.grid[move.destination[1]][move.destination[0]] = move.destination_piece

        if move.destination_piece != 'empty':
            # Add dest piece back to list of pieces
            self.pieces[move.destination_piece.player].append(move.destination_piece)
            # Change score and num_pieces
            self.score += move.destination_piece.value
            self.num_pieces += 1

        # Change piece position attributes (dest piece wasn't changed)
        move.origin_piece.position = move.origin

        if move.pawn_change:
            move.origin_piece.piece_behavior = 'pawn'
            if move.origin_piece.player == 'white':
                self.score -= 16
            else:
                self.score += 16
            move.pawn_change = False

    def check_check(self, player):
        """Return True if the player is in check.

        Parameters
        ----------
        player : str
            The player to check if is in check.

        Returns
        -------
        check : bool
            True if the player is in check.
        """
        king = self.kings[player]
        other_player = "black" if player == "white" else "white"
        for piece in self.pieces[other_player]:
            for move in piece.get_moves():
                if move.destination_piece == king:
                    return True

        return False

    def check_won(self, player):
        """Return True if the player won by taking the other player's king.

        Parameters
        ----------
        player : str
            The player to check if won.

        Returns
        -------
        won : bool
            True if the player won by taking the other player's king.
        """
        other_player = "black" if player == "white" else "white"
        # Check to see if the other player's king is still on the board
        for piece in self.pieces[other_player]:
            if piece.piece_type == "king":
                return False

        return True

    def print_grid(self):
        """Print a representation of the board."""
        string_grid = "Board:\n"
        for row in range(7, -1, -1):
            string_grid += '-'*46
            string_grid += '\ny='
            string_grid += str(row)
            string_grid += '  '

            for col in range(8):
                string_grid += '|'
                if self.grid[row][col] == 'empty':
                    string_grid += '    '
                else:
                    string_grid += self.grid[row][col].__str__()
            string_grid += '|\n'
        string_grid += '-'*46
        string_grid += '\n     '
        for col in range(8):
            string_grid += '|x='
            string_grid += str(col)
            string_grid += ' '
        string_grid += '|'

        print(string_grid)
