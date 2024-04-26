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


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: more methods?


class Board:
    """Internal representation of a PipeMania board."""

    def __init__(self, board, len):
        self.board = board
        self.len = len

    def get_value(self, row: int, col: int) -> str:
        """Returns the value at the respective position on the board."""
        # TODO
        pass

    def get_len(self):
        return self.len

    def get_board(self):
        """Returns the board. The board is a list of lists. Each list represents a row of the board."""
        # example: [['VB', 'VE'], ['FC', 'FC']]
        return self.board
    
    def get_board_display(self):
        for i in range(self.len):
            for j in range(self.len):
                if j == self.len - 1:
                    print(self.board[i][j])
                else:
                    print(self.board[i][j] + "\t", end='')
        

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[str, str]:
        """Returns the values immediately above and below, respectively."""
        if row == 0 and row != self.len - 1:
            above = "None"
            below = self.board[row + 1][col]

        elif row != 0 and row == self.len - 1:
            above = self.board[row - 1][col]
            below = "None"
        
        elif row == 0 and row == self.len - 1:
            above = "None"
            below = "None"
        
        else:
            above = self.board[row - 1][col]
            below = self.board[row + 1][col]


        return "(" + above + ", " + below + ")"

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        """Returns the values immediately to the left and right, respectively."""
        if col == 0 and col != self.len - 1:
            left = "None"
            right = self.board[row][col + 1]

        elif col != 0 and col == self.len - 1:
            left = self.board[row][col - 1]
            right = "None"
        
        elif col == 0 and col == self.len - 1:
            left = "None"
            right = "None"
        
        else:
            left = self.board[row][col - 1]
            right = self.board[row][col + 1]


        return "(" + left + ", " + right + ")"

    @staticmethod
    def parse_instance():
        n = 0
        matrix = []

        while True:
            line = stdin.readline().split()
            if not line:
                break
            matrix.append(line)

        return Board(matrix, len(matrix))





class PipeMania(Problem):
    def __init__(self, board: Board):
        """The constructor specifies the initial state."""
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        """Returns a list of actions that can be performed from the state passed as an argument."""
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

    board = Board.parse_instance()

    print("\n")
    board.get_board_display()
    print("\n")
    print(board.get_board())
    print("\n")

    print(board.adjacent_vertical_values(0, 0))
    print(board.adjacent_horizontal_values(0, 0))
    print(board.adjacent_vertical_values(1, 1))
    print(board.adjacent_horizontal_values(1, 1))
