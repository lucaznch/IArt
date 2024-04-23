# Grupo 15:
# 102637 Gabriel Silva
# 105994 Jorge Mendes

import sys
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
        # TODO
        pass

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        """Returns the values immediately to the left and right, respectively."""
        # TODO
        pass

    @staticmethod
    def parse_instance():
        n = 0
        matrix = []
        file = sys.argv[1]

        with open(file, 'r') as file:
            for line in file:
                row = line.split()
                matrix.append(row)
                n += 1
    
        return Board(matrix, n)





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


    if len(sys.argv) != 2:
        print("Usage: python3 program.py <initial-state.txt>")
        sys.exit(1)

    board = Board.parse_instance()
    board.get_board_display()
