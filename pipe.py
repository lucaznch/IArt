# Grupo 15:
# 102637 Gabriel Silva
# 105994 Jorge Mendes

import copy

from sys import stdin

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

# Pieces:
PIECE_FC = 'FC'
PIECE_FB = 'FB'
PIECE_FE = 'FE'
PIECE_FD = 'FD'
PIECE_BC = 'BC'
PIECE_BB = 'BB'
PIECE_BE = 'BE'
PIECE_BD = 'BD'
PIECE_VC = 'VC'
PIECE_VB = 'VB'
PIECE_VE = 'VE'
PIECE_VD = 'VD'
PIECE_LH = 'LH'
PIECE_LV = 'LV'


# Board status:
BOARD_INITIAL = 1
BOARD_ORGANIZED_CORNERS = 2


# Piece rotations:
PieceRotations = {'FC': ['E', 'D'], # index 0 is anticlockwise, index 1 is clockwise
                  'FB': ['D', 'E'],
                  'FE': ['B', 'C'],
                  'FD': ['C', 'B'],
                  'BC': ['E', 'D'],
                  'BB': ['D', 'E'],
                  'BE': ['B', 'C'],
                  'BD': ['C', 'B'],
                  'VC': ['E', 'D'],
                  'VB': ['D', 'E'],
                  'VE': ['B', 'C'],
                  'VD': ['C', 'B'],
                  'LH': ['V', 'V'],
                  'LV': ['H', 'H']}


# pieces that have connections on the left
hasLeftConnections = ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']

# pieces that have connections on the right
hasRightConnections = ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH']

# pieces that have connections above
hasUpConnections = ['FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV']

# pieces that have connections below
hasDownConnections = ['FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV']


# pieces that connect to the right, so they are LEFT connections
LeftConnections = ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH']

# pieces that connect to the left, so they are RIGHT connections
RightConnections = ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']

# pieces that connect below, so they are UP connections
UpConnections = ['FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV']

# pieces that connect above, so they are DOWN connections
DownConnections = ['FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV']






class Piece:
    def __init__(self, piece):
        self.type = piece[0]
        self.orientation = piece[1]
        self.piece = piece
    
    def get_type(self):
        return self.type
    
    def get_orientation(self):
        return self.orientation

    def get_piece(self):
        return self.piece
    
    def set_orientation(self, orientation):
        self.orientation = orientation

    def rotate(self, way):
        """ way: True for clockwise, False for anti clockwise"""
        way = 1 if way else 0

        new_orientation = PieceRotations[self.piece][way]
        self.orientation = new_orientation
        new_piece = self.type + new_orientation
        self.piece = new_piece





class Board:
    """Internal representation of a PipeMania board."""

    def __init__(self, board, len):
        self.board = board
        self.len = len


    def get_value(self, row: int, col: int) -> str:
        """Returns the value at the respective position on the board."""
        return self.board[row][col].get_piece()


    def get_len(self):
        return self.len


    def get_board(self):
        """Returns the board. The board is a list of lists. Each list represents a row of the board."""
        # example: [[Piece1, Piece2], [Piece3, Piece4]]
        return self.board
    

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[str, str]:
        """Returns the values immediately above and below, respectively."""
        if row == 0 and row != self.len - 1:
            above = None
            below = self.board[row + 1][col].get_piece()

        elif row != 0 and row == self.len - 1:
            above = self.board[row - 1][col].get_piece()
            below = None
        
        elif row == 0 and row == self.len - 1:
            above = None
            below = None
        
        else:
            above = self.board[row - 1][col].get_piece()
            below = self.board[row + 1][col].get_piece()
        
        values = (above, below)

        return values


    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        """Returns the values immediately to the left and right, respectively."""
        if col == 0 and col != self.len - 1:
            left = None
            right = self.board[row][col + 1].get_piece()

        elif col != 0 and col == self.len - 1:
            left = self.board[row][col - 1].get_piece()
            right = None
        
        elif col == 0 and col == self.len - 1:
            left = None
            right = None
        
        else:
            left = self.board[row][col - 1].get_piece()
            right = self.board[row][col + 1].get_piece()
        
        values = (left, right)

        return values

    def rotate_one_piece(self, row, col, way):
        self.board[row][col].rotate(way)
    
    def print(self):
        board_display = ''
        for i in range(self.len):
            for j in range(self.len):
                if j == self.len - 1:
                    board_display += self.board[i][j].get_piece() + "\n"
                else:
                    board_display += self.board[i][j].get_piece() + "\t"
        return board_display


    @staticmethod
    def parse_instance():
        n = 0
        pieces = []

        while True:
            line = stdin.readline().split()
            if not line:
                break
            n += 1
            pieces.append([Piece(piece) for piece in line])

        return Board(pieces, n)





class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.board_status = BOARD_INITIAL
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: more methods?





class PipeMania(Problem):
    def __init__(self, board: Board):
        """The constructor specifies the initial state."""
        self.board = board

    def actions(self, state: PipeManiaState):
        """Returns a list of actions that can be performed from the state passed as an argument."""
        actions = []
        
        n = state.board.len
        
        # if state is in initial state, we can only rotate the pieces in the corners
        if state.board_status == BOARD_INITIAL:
            for i in range(n):
                for j in range(n):
                    piece = state.board.get_value(i, j)
                    
                    if i == 0:
                        if j == 0:
                            if piece == PIECE_FE:
                                actions.append((i, j, False))
                            elif piece == PIECE_FC:
                                actions.append((i, j, True))
                            elif piece == PIECE_VC:
                                actions.append((i, j, True))
                                actions.append((i, j, True))
                            elif piece == PIECE_VE:
                                actions.append((i, j, False))
                            elif piece == PIECE_VD:
                                actions.append((i, j, True))
                        elif j != 0 and j != n - 1:
                            if piece == PIECE_FC:
                                actions.append((i, j, True))
                            elif piece == PIECE_VC:
                                actions.append((i,j, False))
                            elif piece == PIECE_VD:
                                actions.append((i, j, True))
                            elif piece == PIECE_LV:
                                actions.append((i, j, True))
                            elif piece == PIECE_BC:
                                actions.append((i, j, True))
                                actions.append((i, j, True))
                            elif piece == PIECE_BE:
                                actions.append((i, j, False))
                            elif piece == PIECE_BD:
                                actions.append((i, j, True))
                        elif j == n - 1:
                            if piece == PIECE_FD:
                                actions.append((i, j, True))
                            elif piece == PIECE_FC:
                                actions.append((i, j, False))
                            elif piece == PIECE_VC:
                                actions.append((i, j, False))
                            elif piece == PIECE_VD:
                                actions.append((i, j, True))
                                actions.append((i, j, True))
                            elif piece == PIECE_VB:
                                actions.append((i, j, True))
                    
                    elif i != 0 and i != n - 1:
                        if j != 0 and j != n - 1:
                            # not a corner!
                            continue
                        if j == 0:
                            if piece == PIECE_FE:
                                actions.append((i, j, True))
                            elif piece == PIECE_BC:
                                actions.append((i, j, True))
                            elif piece == PIECE_BB:
                                actions.append((i, j, False))
                            elif piece == PIECE_BE:
                                actions.append((i, j, True))
                                actions.append((i, j, True))
                            elif piece == PIECE_VC:
                                actions.append((i, j, True))
                            elif piece == PIECE_VE:
                                actions.append((i, j, False))
                            elif piece == PIECE_LH:
                                actions.append((i, j, True))
                        elif j == n - 1:
                            if piece == PIECE_FD:
                                actions.append((i, j, True))
                            elif piece == PIECE_BC:
                                actions.append((i, j, False))
                            elif piece == PIECE_BB:
                                actions.append((i, j, True))
                            elif piece == PIECE_BD:
                                actions.append((i, j, True))
                                actions.append((i, j, True))
                            elif piece == PIECE_VB:
                                actions.append((i, j, True))
                            elif piece == PIECE_VD:
                                actions.append((i, j, False))
                            elif piece == PIECE_LH:
                                actions.append((i, j, True))
                    
                    elif i == n - 1:
                        if j == 0:
                            if piece == PIECE_FE:
                                actions.append((i, j, True))
                            elif piece == PIECE_FB:
                                actions.append((i, j, False))
                            elif piece == PIECE_VC:
                                actions.append((i, j, True))
                            elif piece == PIECE_VE:
                                actions.append((i, j, True))
                                actions.append((i, j, True))
                            elif piece == PIECE_VB:
                                actions.append((i, j, False))
                        elif j != 0 and j != n - 1:
                            if piece == PIECE_FB:
                                actions.append((i, j, False))
                            elif piece == PIECE_BE:
                                actions.append((i, j, True))
                            elif piece == PIECE_BD:
                                actions.append((i, j, False))
                            elif piece == PIECE_BB:
                                actions.append((i, j, True))
                                actions.append((i, j, True))
                            elif piece == PIECE_VB:
                                actions.append((i, j, False))
                            elif piece == PIECE_VE:
                                actions.append((i, j, True))
                            elif piece == PIECE_LV:
                                actions.append((i, j, True))
                        elif j == n - 1:
                            if piece == PIECE_FB:
                                actions.append((i, j, True))
                            elif piece == PIECE_FD:
                                actions.append((i, j, False))
                            elif piece == PIECE_VD:
                                actions.append((i, j, False))
                            elif piece == PIECE_VB:
                                actions.append((i, j, True))
                                actions.append((i, j, True))
                            elif piece == PIECE_VE:
                                actions.append((i, j, True))

        return actions

    def result(self, state: PipeManiaState, action):
        """Returns the state resulting from executing the 'action' on 'state' passed as an argument.
        The action to be executed must be one of those present in the list obtained by executing self.actions(state)."""
        board_cp = copy.deepcopy(state.board)

        if isinstance(action, list):
            for a in action:
                board_cp.rotate_one_piece(a[0], a[1], a[2])
        else:
            board_cp.rotate_one_piece(action[0], action[1], action[2])

        board_cp.board_status = BOARD_ORGANIZED_CORNERS
        return PipeManiaState(board_cp)


    def goal_test(self, state: PipeManiaState):
        """Returns True if and only if the state passed as an argument is an objective state.
        You must check that all positions on the board are filled according to the rules of the problem."""
        
        n = state.board.len

        for i in range(n):
            for j in range(n):
                piece = state.board.get_value(i, j)

                if i == 0:
                    if j == 0:
                        if piece in hasUpConnections or piece in hasLeftConnections:
                            return False

                        elif piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False

                        elif piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False
                    
                    elif j != 0 and j != n - 1:
                        if piece in hasUpConnections:
                            return False

                        elif piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False

                        elif piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False
                    
                    elif j == n - 1:
                        if piece in hasUpConnections or piece in hasRightConnections:
                            return False

                        elif piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False


                elif i != 0 and i != n - 1:
                    if j == 0:
                        if piece in hasLeftConnections:
                            return False
                        
                        elif piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False
                        
                        elif piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False
                    
                    elif j == n - 1:
                        if piece in hasRightConnections:
                            return False
                        
                        elif piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False

                    else:
                        if piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False
                        
                        elif piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False
                

                elif i == n - 1:
                    if j == 0:
                        if piece in hasLeftConnections or piece in hasDownConnections:
                            return False
                        
                        elif piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False
                    
                    elif j != 0 and j != n - 1:
                        if piece in hasDownConnections:
                            return False

                        elif piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False
                    
                    elif j == n - 1:
                        if piece in hasRightConnections or piece in hasDownConnections:
                            return False
        
        return True

    def h(self, node: Node):
        """Heuristic function used for the A* search."""
        # TODO
        pass

    # TODO: more methods?





if __name__ == "__main__":
    # TODO:
    # Read the standard input file,
    # Use a search technique to resolve the instance,
    # Remove the solution from the resulting node,
    # Print to standard output in the indicated format.

    # Read the grid in figure 1a:
    board = Board.parse_instance()
    
    print(board.adjacent_vertical_values(0, 0))
    print(board.adjacent_horizontal_values(0, 0))
    print(board.adjacent_vertical_values(1, 1))
    print(board.adjacent_horizontal_values(1, 1))


