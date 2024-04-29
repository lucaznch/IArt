# Grupo 15:
# 102637 Gabriel Silva
# 105994 Jorge Mendes

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
PieceRotations = {'FC': ['E', 'D'],
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

# Piece connections:
PieceConnections = {'FC': ['BB', 'BE', 'BD', 'VB', 'VE', 'LV'],
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
        """ way: 0 for anti clockwise, 1 for clockwise"""
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
    
    def get_board_display(self):
        for i in range(self.len):
            for j in range(self.len):
                if j == self.len - 1:
                    print(self.board[i][j].get_piece())
                else:
                    print(self.board[i][j].get_piece() + "\t", end='')

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
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        """Returns a list of actions that can be performed from the state passed as an argument."""
        state.board
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Returns the state resulting from executing the 'action' on 'state' passed as an argument.
        The action to be executed must be one of those present in the list obtained by executing self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        """Returns True if and only if the state passed as an argument is an objective state.
        You must check that all positions on the board are filled according to the rules of the problem."""
        
        
        
        # TODO
        pass

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
    initial_state = PipeManiaState(board)


    print("initial state:")
    board.get_board_display()


    print("piece at (2,2)")
    print(initial_state.board.get_value(2, 2))


    print("\nadjacent vertical values of 0,0")
    print(board.adjacent_vertical_values(0, 0))
    print("\nadjacent horizontal values of 0,0")
    print(board.adjacent_horizontal_values(0, 0))

    print("\nadjacent vertical values of 1,1")
    print(board.adjacent_vertical_values(1, 1))
    print("\nadjacent horizontal values of 1,1")
    print(board.adjacent_horizontal_values(1, 1))

    print("\nrotating piece at (0,0) clockwise(=1)")
    print("rotating piece at (1,1) anticlockwise(=0)")
    print("rotating piece at (0,1) clockwise(=1)")
    print("rotating piece at (1,0) anticlockwise(=0)\n")

    board.rotate_one_piece(0, 0, 1)
    board.rotate_one_piece(1, 1, 0)
    board.rotate_one_piece(0, 1, 1)
    board.rotate_one_piece(1, 0, 0)

    board.get_board_display()



    # Perform the action of rotating the part 90° clockwise (2, 2)
    # result_state = problem.result(initial_state, (2, 2, True))

    # Show value at position (2, 2):
    # print(result_state.board.get_value(2, 2))
