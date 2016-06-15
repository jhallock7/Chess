"""Board object for chess."""

from Pieces import Piece


class Board():
    """Chess board object.

    Attributes
    ----------
    grid : list
        List of lists representing the board and containing pointers to the pieces.

    score : int
        The current score.

    score : num_pieces
        The number of pieces remaining on the board.

    kings : dict
        Dictionary containing pointers to the two kings.

    pieces : dict
        Dictionary containing pointers to the pieces on the board, grouped by color.

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
        for piece in self.pieces["white"]:
            if piece.piece_type == "king":
                self.kings["white"] = piece
        for piece in self.pieces["black"]:
            if piece.piece_type == "king":
                self.kings["black"] = piece

    def _inbounds(self, position):
        """Returns True if the position is within the bounds of the board.

        Parameters
        ----------
        position : tuple
            A position potentially on the board.

        Returns
        -------
        valid : bool
            True if the position is within the bounds of the board.
        """
        if position[0] < 0:
            return False
        if 7 < position[0]:
            return False
        if position[1] < 0:
            return False
        if 7 < position[1]:
            return False
        return True

    def make_move(self, move):
        """Makes the move on the board.

        Parameters
        ----------
        move : move
            A move objects to make on the board.
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
        """Unmakes the move on the board.

        Parameters
        ----------
        move : move
            A move objects to undo on the board.
        """
        # Change grid pointers
        self.grid[move.origin[1]][move.origin[0]] = move.origin_piece

        if move.destination_piece != 'empty':
            self.grid[move.destination[1]][move.destination[0]] = move.destination_piece
            # Add dest piece back to list of pieces
            self.pieces[move.destination_piece.player].append(move.destination_piece)
            # Change score and num_pieces
            self.score += move.destination_piece.value
            self.num_pieces += 1
        else:
            self.grid[move.destination[1]][move.destination[0]] = "empty"

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
        """Returns True if the player is in check.

        Parameters
        ----------
        player : str
            The player to check if is in check.

        Returns
        -------
        valid : bool
            True if the player is in check.
        """
        king_position = self.kings[player].position

        # Check corridors

        # Right
        for i in range(1, 8):
            new_position = (king_position[0] + i, king_position[1])

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type in ["rook", "queen"]:
                        return True
                break

        # Left
        for i in range(1, 8):
            new_position = (king_position[0] - i, king_position[1])

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type in ["rook", "queen"]:
                        return True
                break

        # Up
        for i in range(1, 8):
            new_position = (king_position[0], king_position[1] + i)

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type in ["rook", "queen"]:
                        return True
                break

        # Down
        for i in range(1, 8):
            new_position = (king_position[0], king_position[1] - i)

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type in ["rook", "queen"]:
                        return True
                break

        # Check diagonals

        # Up-Right
        for i in range(1, 8):
            new_position = (king_position[0] + i, king_position[1] + i)

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type in ["bishop", "queen"]:
                        return True
                break

        # Right-Down
        for i in range(1, 8):
            new_position = (king_position[0] + i, king_position[1] - i)

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type in ["bishop", "queen"]:
                        return True
                break

        # Down-Left
        for i in range(1, 8):
            new_position = (king_position[0] - i, king_position[1] - i)

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type in ["bishop", "queen"]:
                        return True
                break

        # Left-Up
        for i in range(1, 8):
            new_position = (king_position[0] - i, king_position[1] + i)

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type in ["bishop", "queen"]:
                        return True
                break

        # Knight
        vectors = [(2,  1),
                   (2, -1),
                   (-2, 1),
                   (-2, -1),
                   (1, 2),
                   (1, -2),
                   (-1, 2),
                   (-1, -2)]

        for vector in vectors:
            new_position = (king_position[0] + vector[0], king_position[1] + vector[1])

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type == "knight":
                        return True
                break

        # Pawn
        # Note that the vectors are the opposite of the pawn attack vectors
        # because these are relative to the king
        white_pawn_vectors = [(-1, -1), (1, -1)]
        black_pawn_vectors = [(-1, 1), (1, 1)]

        if player == 'black':
            for vector in white_pawn_vectors:
                new_position = (king_position[0] + vector[0], king_position[1] + vector[1])

                # If out of bounds, continue, don't break!
                if not self._inbounds(new_position):
                    continue

                piece = self.grid[new_position[1]][new_position[0]]
                if piece != 'empty':
                    if piece.player != player:
                        if piece.piece_type == 'pawn':
                            return True
        if player == 'white':
            for vector in black_pawn_vectors:
                new_position = (king_position[0] + vector[0], king_position[1] + vector[1])

                # If out of bounds, continue, don't break!
                if not self._inbounds(new_position):
                    continue

                piece = self.grid[new_position[1]][new_position[0]]
                if piece != 'empty':
                    if piece.player != player:
                        if piece.piece_type == 'pawn':
                            return True

        # King
        vectors = [(1,  1),
                   (1, 0),
                   (1, -1),
                   (0, -1),
                   (-1, -1),
                   (-1, 0),
                   (-1, 1),
                   (0, 1)]

        for vector in vectors:
            new_position = (king_position[0] + vector[0], king_position[1] + vector[1])

            if not self._inbounds(new_position):
                break
            piece = self.grid[new_position[1]][new_position[0]]
            if piece != 'empty':
                if piece.player != player:
                    if piece.piece_type == "king":
                        return True
                break

        return False

    def check_won(self, player):
        """Returns True if the player won by taking the other player's king.

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
        for piece in self.pieces[other_player]:
            if piece.piece_type == "king":
                return False

        return True

    def print_grid(self):
        """Prints a representation of the board."""
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
