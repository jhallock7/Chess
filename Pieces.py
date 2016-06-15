"""Pieces for chess."""

import abc


class Move:
    """Move object containing all the info needed to make and unmake the move.

    Parameters
    ----------
    origin : tuple
        Position of piece to be moved.
    origin_piece : piece
        Piece being moved.
    destination : tuple
        Location where piece is being moved.
    destination_piece : piece
        Piece at destination; "empty" if empty.
    score_change : int
        Potential score change as result of move;
        used only in AI_make_move().
    pawn_change : bool
        Indicates if the move results in a pawn reaching the back of the board,
        therefore turning into a queen.

    Attributes
    ----------
    summary : str
        String representing the move.
    """

    def __init__(self, origin=None, origin_piece=None, destination=None,
                 destination_piece=None, score_change=0, pawn_change=False):
        """Initialize a Move object."""
        self.origin = origin
        self.origin_piece = origin_piece
        self.destination = destination
        self.destination_piece = destination_piece
        self.score_change = score_change
        self.pawn_change = pawn_change
        # if origin is None, this is a "dummy" move
        if origin is not None:
            self.summary = ("%s from %s to %s" %
                            (self.origin_piece.summary,
                             self.origin,
                             self.destination))


class Piece:
    """Piece object for chess pieces.

    Parameters
    ----------
    board : board
        Board of the chess game to which the piece belongs.
    position : tuple
        Position of the piece on the board.
    player : str
        "white" if the piece is white;
        "black" if the piece is black.
    piece_type : str
        The type of piece, such as "rook", "pawn", etc...

    Attributes
    ----------
    piece_behavior : piece_behavior
        Object containing the functionality specific to the piece type.
    piece_type : str
        Type of chess piece (delegated to piece_behavior object).
    value : int
        Integer value of the piece (delegated to piece_behavior object).
    directions : list
        List of movements the piece can make, grouped by direction
        (delegated to piece_behavior object).
    summary : str
        String representing piece color and type
        (delegated to piece_behavior object).

    Methods
    ----------
    __str__()
        Returns a string representing the piece color and type
        (delegated to piece_behavior object).
    get_moves()
        Returns a list of valid moves for this piece
        (delegated to piece_behavior object).
    """

    def __init__(self, board, position, player, piece_type):
        """Initialize a Piece object."""
        self.board = board
        self.position = position
        self.player = player
        self.piece_behavior = piece_type

    @property
    def piece_behavior(self):
        """Return the piece_behavior object containing the functionality specific to the piece type."""
        return self._piece_behavior

    @piece_behavior.setter
    def piece_behavior(self, piece_type):
        if piece_type == 'rook':
            self._piece_behavior = Rook_Behavior(self.player)
        elif piece_type == 'knight':
            self._piece_behavior = Knight_Behavior(self.player)
        elif piece_type == 'bishop':
            self._piece_behavior = Bishop_Behavior(self.player)
        elif piece_type == 'queen':
            self._piece_behavior = Queen_Behavior(self.player)
        elif piece_type == 'king':
            self._piece_behavior = King_Behavior(self.player)
        elif piece_type == 'pawn':
            self._piece_behavior = Pawn_Behavior(self.player)

    @property
    def piece_type(self):
        """Return the type of chess piece (delegated to piece_behavior object)."""
        return self.piece_behavior.piece_type

    @property
    def value(self):
        """Return the integer value of the piece (delegated to piece_behavior object)."""
        return self.piece_behavior.value

    @property
    def directions(self):
        """Return a list of movements the piece can make, grouped by direction (delegated to piece_behavior object)."""
        return self.piece_behavior.directions

    @property
    def summary(self):
        """Return a string representing piece color and type (delegated to piece_behavior object)."""
        return self.piece_behavior.summary

    def __str__(self):
        """Return a string representing the piece color and type (delegated to piece_behavior object)."""
        return self.piece_behavior.summary

    def get_moves(self):
        """Return a list of valid moves for this piece (delegated to piece_behavior object)."""
        return self.piece_behavior.get_moves(self.board, self.position)


class Piece_Behavior(abc.ABC):
    """Abstract class for piece-type-specific methods and attributes.

    Attributes
    ----------
    piece_type : str (abstract)
        Type of chess piece.
    value : int (abstract)
        Integer value of the piece.
    summary : str (abstract)
        String representing piece color and type.
    directions : list (abstract)
        List of movements the piece can make, grouped by direction.

    Methods
    ----------
    get_moves(board, position)
        Returns a list of valid moves for this piece.
    _is_valid_move(vector, current_piece, other_piece)
        Returns True if the move is valid based on custom criteria.
    """

    @property
    @abc.abstractmethod
    def piece_type(self):
        """Return the type of chess piece."""
        return ''

    @property
    @abc.abstractmethod
    def value(self):
        """Return the integer value of the piece."""
        return 0

    @property
    @abc.abstractmethod
    def summary(self):
        """Return a string representing the piece color and type."""
        return ''

    @property
    @abc.abstractmethod
    def directions(self):
        """Return a list of movements the piece can make, grouped by direction."""
        return []

    def get_moves(self, board, position):
        """Return a list of valid moves for this piece.

        Parameters
        ----------
        board : board
            The current board.
        position : tuple
            The current position of the piece on the board.

        Returns
        -------
        moves : list
            List of valid moves for the piece.
        """
        current_piece = board.grid[position[1]][position[0]]

        moves = []

        # For each direction in which the piece can move...
        for direction in self.directions:
            # for each vector in that direction...
            # (once a piece is encountered in a direction,
            # further positions in that direction are unaccessible,
            # therefore break out of inner FOR loop)
            for vector in direction:
                new_position = (position[0] + vector[0], position[1] + vector[1])

                # Check if the proposed destination is inbounds
                if board._inbounds(new_position) is False:
                    break

                other_piece = board.grid[new_position[1]][new_position[0]]

                # Check if the proposed destination is occupied by a friendly piece
                if other_piece != "empty" and other_piece.player == current_piece.player:
                    break

                # Check other validity conditions, mainly for pawn
                if self._is_valid_move(vector, current_piece, other_piece) is False:
                    break

                # The destination is viable, add the move
                moves.append(Move(position, current_piece, new_position, other_piece))

                # If there was an enemy piece on the square
                if other_piece != "empty":
                    break

        return moves

    def _is_valid_move(self, vector, current_piece, other_piece):
        """Return True if the move is a valid move based on custom criteria.

        Parameters
        ----------
        vector : tuple
            The potential move, relative to the piece's current position.
        current_piece : piece
            The current piece.
        other_piece : piece
            The (possibly-empty) piece located at the destination of the proposed move.

        Returns
        -------
        valid : bool
            True if the move is a valid move for a pawn.
        """
        return True


class Rook_Behavior(Piece_Behavior):
    """Concrete subclass of Piece_Behavior for Rooks.

    Parameters
    ----------
    player : str
        "white" if the piece is white;
        "black" if the piece is black.

    Attributes
    ----------
    piece_type : str
        Type of chess piece.
    value : int
        Integer value of the piece.
    summary : str
        String representing piece color and type.
    directions : list
        List of movements the piece can make, grouped by direction.
    """

    def __init__(self, player):
        """Initialize a Rook_Behavior object."""
        self._piece_type = 'rook'
        self._value = 10 if player == "white" else -10
        self._summary = 'W-Rk' if player == "white" else 'B-Rk'

        self._directions = []
        for _ in range(4):
            self._directions.append([])

        for i in range(1, 8):
            self._directions[0].append((i, 0))
            self._directions[1].append((-i, 0))
            self._directions[2].append((0, i))
            self._directions[3].append((0, -i))

    @property
    def piece_type(self):
        """Return the type of chess piece."""
        return self._piece_type

    @property
    def value(self):
        """Return the integer value of the piece."""
        return self._value

    @property
    def summary(self):
        """Return a string representing the piece color and type."""
        return self._summary

    @property
    def directions(self):
        """Return a list of movements the piece can make, grouped by direction."""
        return self._directions


class Knight_Behavior(Piece_Behavior):
    """Concrete subclass of Piece_Behavior for Knights.

    Parameters
    ----------
    player : str
        "white" if the piece is white;
        "black" if the piece is black.

    Attributes
    ----------
    piece_type : str
        Type of chess piece.
    value : int
        Integer value of the piece.
    summary : str
        String representing piece color and type.
    directions : list
        List of movements the piece can make, grouped by direction.
    """

    def __init__(self, player):
        """Initialize a Knight_Behavior object."""
        self._piece_type = 'knight'
        self._value = 6 if player == "white" else -6
        self._summary = 'W-Kt' if player == "white" else 'B-Kt'

        self._directions = []
        self._directions.append([(-2, -1)])
        self._directions.append([(-2, 1)])
        self._directions.append([(2, -1)])
        self._directions.append([(2, 1)])
        self._directions.append([(-1, -2)])
        self._directions.append([(-1, 2)])
        self._directions.append([(1, -2)])
        self._directions.append([(1, 2)])

    @property
    def piece_type(self):
        """Return the type of chess piece."""
        return self._piece_type

    @property
    def value(self):
        """Return the integer value of the piece."""
        return self._value

    @property
    def summary(self):
        """Return a string representing the piece color and type."""
        return self._summary

    @property
    def directions(self):
        """Return a list of movements the piece can make, grouped by direction."""
        return self._directions


class Bishop_Behavior(Piece_Behavior):
    """Concrete subclass of Piece_Behavior for Bishops.

    Parameters
    ----------
    player : str
        "white" if the piece is white;
        "black" if the piece is black.

    Attributes
    ----------
    piece_type : str
        Type of chess piece.
    value : int
        Integer value of the piece.
    summary : str
        String representing piece color and type.
    directions : list
        List of movements the piece can make, grouped by direction.
    """

    def __init__(self, player):
        """Initialize a Bishop_Behavior object."""
        self._piece_type = 'bishop'
        self._value = 6 if player == "white" else -6
        self._summary = 'W-Bs' if player == "white" else 'B-Bs'

        self._directions = []
        for _ in range(4):
            self._directions.append([])

        for i in range(1, 8):
            self._directions[0].append((i, i))
            self._directions[1].append((i, -i))
            self._directions[2].append((-i, i))
            self._directions[3].append((-i, -i))

    @property
    def piece_type(self):
        """Return the type of chess piece."""
        return self._piece_type

    @property
    def value(self):
        """Return the integer value of the piece."""
        return self._value

    @property
    def summary(self):
        """Return a string representing the piece color and type."""
        return self._summary

    @property
    def directions(self):
        """Return a list of movements the piece can make, grouped by direction."""
        return self._directions


class Queen_Behavior(Piece_Behavior):
    """Concrete subclass of Piece_Behavior for Queens.

    Parameters
    ----------
    player : str
        "white" if the piece is white;
        "black" if the piece is black.

    Attributes
    ----------
    piece_type : str
        Type of chess piece.
    value : int
        Integer value of the piece.
    summary : str
        String representing piece color and type.
    directions : list
        List of movements the piece can make, grouped by direction.
    """

    def __init__(self, player):
        """Initialize a Queen_Behavior object."""
        self._piece_type = 'queen'
        self._value = 18 if player == "white" else -18
        self._summary = 'W-Qn' if player == "white" else 'B-Qn'

        self._directions = []
        for _ in range(8):
            self._directions.append([])

        for i in range(1, 8):
            self._directions[0].append((i, 0))
            self._directions[1].append((-i, 0))
            self._directions[2].append((0, i))
            self._directions[3].append((0, -i))
            self._directions[4].append((i, i))
            self._directions[5].append((i, -i))
            self._directions[6].append((-i, i))
            self._directions[7].append((-i, -i))

    @property
    def piece_type(self):
        """Return the type of chess piece."""
        return self._piece_type

    @property
    def value(self):
        """Return the integer value of the piece."""
        return self._value

    @property
    def summary(self):
        """Return a string representing the piece color and type."""
        return self._summary

    @property
    def directions(self):
        """Return a list of movements the piece can make, grouped by direction."""
        return self._directions


class King_Behavior(Piece_Behavior):
    """Concrete subclass of Piece_Behavior for Kings.

    Parameters
    ----------
    player : str
        "white" if the piece is white;
        "black" if the piece is black.

    Attributes
    ----------
    piece_type : str
        Type of chess piece.
    value : int
        Integer value of the piece.
    summary : str
        String representing piece color and type.
    directions : list
        List of movements the piece can make, grouped by direction.
    """

    def __init__(self, player):
        """Initialize a King_Behavior object."""
        self._piece_type = 'king'
        self._value = 200 if player == "white" else -200
        self._summary = 'W-Kg' if player == "white" else 'B-Kg'

        self._directions = []
        self._directions.append([(1, 1)])
        self._directions.append([(1, 0)])
        self._directions.append([(1, -1)])
        self._directions.append([(0, -1)])
        self._directions.append([(-1, -1)])
        self._directions.append([(-1, 0)])
        self._directions.append([(-1, 1)])
        self._directions.append([(0, 1)])

    @property
    def piece_type(self):
        """Return the type of chess piece."""
        return self._piece_type

    @property
    def value(self):
        """Return the integer value of the piece."""
        return self._value

    @property
    def summary(self):
        """Return a string representing the piece color and type."""
        return self._summary

    @property
    def directions(self):
        """Return a list of movements the piece can make, grouped by direction."""
        return self._directions


class Pawn_Behavior(Piece_Behavior):
    """Concrete subclass of Piece_Behavior for Pawns.

    Parameters
    ----------
    player : str
        "white" if the piece is white;
        "black" if the piece is black.

    Attributes
    ----------
    piece_type : str
        Type of chess piece.
    value : int
        Integer value of the piece.
    summary : str
        String representing piece color and type.
    directions : list
        List of movements the piece can make, grouped by direction.

    Methods
    ----------
    _is_valid_move(vector, current_piece, other_piece)
        Returns True if the move is a valid move for a pawn.
    """

    def __init__(self, player):
        """Initialize a Pawn_Behavior object."""
        self._piece_type = 'pawn'
        self._value = 2 if player == "white" else -2
        self._summary = 'W-Pw' if player == "white" else 'B-Pw'

        self._directions = []
        if player == "white":
            self._directions.append([(-1, 1)])
            self._directions.append([(0, 1), (0, 2)])
            self._directions.append([(1, 1)])
        else:
            self._directions.append([(-1, -1)])
            self._directions.append([(0, -1), (0, -2)])
            self._directions.append([(1, -1)])

    @property
    def piece_type(self):
        """Return the type of chess piece."""
        return self._piece_type

    @property
    def value(self):
        """Return the integer value of the piece."""
        return self._value

    @property
    def summary(self):
        """Return a string representing the piece color and type."""
        return self._summary

    @property
    def directions(self):
        """Return a list of movements the piece can make, grouped by direction."""
        return self._directions

    def _is_valid_move(self, vector, current_piece, other_piece):
        """Return True if the move is a valid move for a pawn.

        Parameters
        ----------
        vector : tuple
            The potential move, relative to the piece's current position.
        current_piece : piece
            The current piece.
        other_piece : piece
            The (possibly-empty) piece located at the destination of the proposed move.

        Returns
        -------
        valid : bool
            True if the move is a valid move for a pawn.
        """
        # If direction is forward and the space is non-empty, break
        if vector[0] == 0 and other_piece != "empty":
            return False
        # If direction is diagonal and space is empty, break
        if vector[0] != 0 and other_piece == "empty":
            return False
        # If moving by 2 spaces, check if in starting row
        if vector[1] == 2 and current_piece.position[1] != 1:
            return False
        if vector[1] == -2 and current_piece.position[1] != 6:
            return False

        return True
