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


# Piece types:
PIECE_TYPE_F = 'F' # Closed piece
PIECE_TYPE_B = 'B' # Forked piece
PIECE_TYPE_V = 'V' # Turning piece
PIECE_TYPE_L = 'L' # Connection piece

# Piece orientations:
PIECE_ORIENTATION_UP = 'C'
PIECE_ORIENTATION_DOWN = 'B'
PIECE_ORIENTATION_LEFT = 'E'
PIECE_ORIENTATION_RIGHT = 'D'

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

hasLeftConnections = ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']

hasRightConnections = ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH']

hasUpConnections = ['FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV']

hasDownConnections = ['FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV']


LeftConnections = ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH']

RightConnections = ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']

UpConnections = ['FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV']

DownConnections = ['FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV']

# Piece connections:
PieceConnections = {'FC': [UpConnections],
                    'FB': [DownConnections],
                    'FE': [LeftConnections],
                    'FD': [RightConnections],
                    'BC': [LeftConnections, UpConnections, RightConnections],
                    'BB': [LeftConnections, DownConnections, RightConnections],
                    'BE': [DownConnections, LeftConnections, UpConnections],
                    'BD': [DownConnections, RightConnections, UpConnections],
                    'VC': [LeftConnections, UpConnections],
                    'VB': [DownConnections, RightConnections],
                    'VE': [LeftConnections, DownConnections],
                    'VD': [RightConnections, UpConnections],
                    'LH': [LeftConnections, RightConnections],
                    'LV': [UpConnections, DownConnections]}




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
            above = "None"
            below = self.board[row + 1][col].get_piece()

        elif row != 0 and row == self.len - 1:
            above = self.board[row - 1][col].get_piece()
            below = "None"
        
        elif row == 0 and row == self.len - 1:
            above = "None"
            below = "None"
        
        else:
            above = self.board[row - 1][col].get_piece()
            below = self.board[row + 1][col].get_piece()

        return "(" + above + ", " + below + ")"


    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        """Returns the values immediately to the left and right, respectively."""
        if col == 0 and col != self.len - 1:
            left = "None"
            right = self.board[row][col + 1].get_piece()

        elif col != 0 and col == self.len - 1:
            left = self.board[row][col - 1].get_piece()
            right = "None"
        
        elif col == 0 and col == self.len - 1:
            left = "None"
            right = "None"
        
        else:
            left = self.board[row][col - 1].get_piece()
            right = self.board[row][col + 1].get_piece()

        return "(" + left + ", " + right + ")"


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
        
        return (2, 2, True)
        
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Returns the state resulting from executing the 'action' on 'state' passed as an argument.
        The action to be executed must be one of those present in the list obtained by executing self.actions(state)."""
        board_cp = copy.deepcopy(state.board)
        board_cp.rotate_one_piece(action[0], action[1], action[2])
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
    # Create an instance of PipeMania:
    problem = PipeMania(board)
    # Create a state with the initial configuration:
    s0 = PipeManiaState(board)
    # Apply the actions that resolve the instance
    s1 = problem.result(s0, (0, 1, True))
    s2 = problem.result(s1, (0, 1, True))
    s3 = problem.result(s2, (0, 2, True))
    s4 = problem.result(s3, (0, 2, True))
    s5 = problem.result(s4, (1, 0, True))
    s6 = problem.result(s5, (1, 1, True))
    s7 = problem.result(s6, (2, 0, False)) # anti-clockwise (example of use)
    s8 = problem.result(s7, (2, 0, False)) # anti-clockwise (usage example)
    s9 = problem.result(s8, (2, 1, True))
    s10 = problem.result(s9, (2, 1, True))
    s11 = problem.result(s10, (2, 2, True))
    # Check if the solution has been reached
    print("Is goal?", problem.goal_test(s5))
    print("Is goal?", problem.goal_test(s11))
    print("Solution:\n", s11.board.print(), sep="")