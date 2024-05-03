# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from copy import deepcopy
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

# Piece types:
PIECE_TYPE_F = 'F' # Closed piece
PIECE_TYPE_B = 'B' # Forked piece
PIECE_TYPE_V = 'V' # Turning piece
PIECE_TYPE_L = 'L' # Connection piece


# Piece rotations:
# index 0, 1 and 2 correspond to a 90 degree clockwise rotation, 90 degree counter-clockwise rotation and 180 degree rotation, respectively
PieceRotations = {'FC': ['FD', 'FE', 'FB'], 
                  'FB': ['FE', 'FD', 'FC'],
                  'FE': ['FC', 'FB', 'FD'],
                  'FD': ['FB', 'FC', 'FE'],
                  'BC': ['BD', 'BE', 'BB'],
                  'BB': ['BE', 'BD', 'BC'],
                  'BE': ['BC', 'BB', 'BD'],
                  'BD': ['BB', 'BC', 'BE'],
                  'VC': ['VD', 'VE', 'VB'],
                  'VB': ['VE', 'VD', 'VC'],
                  'VE': ['VC', 'VB', 'VD'],
                  'VD': ['VB', 'VC', 'VE'],
                  'LH': ['LV', 'LV', 'LH'],
                  'LV': ['LH', 'LH', 'LV']}

ROTATION_90_CLOCKWISE = 0
ROTATION_90_COUNTER_CLOCKWISE = 1
ROTATION_180 = 2
ROTATION_NONE = 3



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




def preprocessing(pieces, n):
    for i in range(n):
        for j in range(n):
            piece = pieces[i][j]
            piece_value = pieces[i][j].get_piece_value()
            
            if i == 0:
                if j == 0:
                    if piece_value == PIECE_FE:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_FC:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VC:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VE:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_VD:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                elif j != 0 and j != n - 1:
                    if piece_value == PIECE_FC:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VC:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_VD:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_LV:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_BC:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_BE:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_BD:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                elif j == n - 1:
                    if piece_value == PIECE_FD:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_FC:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_VC:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_VD:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VB:
                        piece.rotate(ROTATION_90_CLOCKWISE)
            
            elif i != 0 and i != n - 1:
                if j != 0 and j != n - 1:
                    # if not an egde, move on!
                    continue
                if j == 0:
                    if piece_value == PIECE_FE:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_BC:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_BB:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_BE:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VC:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VE:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_LH:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                elif j == n - 1:
                    if piece_value == PIECE_FD:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_BC:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_BB:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_BD:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VB:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VD:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_LH:
                        piece.rotate(ROTATION_90_CLOCKWISE)
            
            elif i == n - 1:
                if j == 0:
                    if piece_value == PIECE_FE:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_FB:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_VC:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VE:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VB:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                elif j != 0 and j != n - 1:
                    if piece_value == PIECE_FB:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_BE:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_BD:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_BB:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VB:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_VE:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_LV:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                elif j == n - 1:
                    if piece_value == PIECE_FB:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_FD:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_VD:
                        piece.rotate(ROTATION_90_COUNTER_CLOCKWISE)
                    elif piece_value == PIECE_VB:
                        piece.rotate(ROTATION_90_CLOCKWISE)
                        piece.rotate(ROTATION_90_CLOCKWISE)
                    elif piece_value == PIECE_VE:
                        piece.rotate(ROTATION_90_CLOCKWISE)


class Piece:
    def __init__(self, value):
        self.value = value
    
    def get_piece_type(self):
        return self.value[0]
    
    def get_piece_orientation(self):
        return self.value[1]
    
    def get_piece_value(self):
        return self.value

    def rotate(self, rotation):
        if rotation == ROTATION_NONE:
            pass
        else:
            self.value = PieceRotations[self.value][rotation]





class Board:
    def __init__(self, matrix, len):
        self.matrix = matrix
        self.len = len

    def get_value(self, row: int, col: int) -> str:
        return self.matrix[row][col].get_piece_value()
    
    def get_piece(self, row: int, col: int) -> Piece:
        return self.matrix[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[str, str]:
        if row == 0:
            return (None, self.matrix[row + 1][col].get_piece_value())
        elif row == self.len - 1:
            return (self.matrix[row - 1][col].get_piece_value(), None)
        else:
            return (self.matrix[row - 1][col].get_piece_value(), self.matrix[row + 1][col].get_piece_value())

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        if col == 0:
            return (None, self.matrix[row][col + 1].get_piece_value())
        elif col == self.len - 1:
            return (self.matrix[row][col - 1].get_piece_value(), None)
        else:
            return (self.matrix[row][col - 1].get_piece_value(), self.matrix[row][col + 1].get_piece_value())

    def print(self):
        board_display = ''
        for i in range(self.len):
            for j in range(self.len):
                if j == self.len - 1:
                    board_display += self.matrix[i][j].get_piece_value() + "\n"
                else:
                    board_display += self.matrix[i][j].get_piece_value() + "\t"
        return board_display
    
    def execute_action(self, row, col, rotation):
        self.matrix[row][col].rotate(rotation)

    @staticmethod
    def parse_instance():
        n = 0
        matrix = [] # e.g. [[Piece1, Piece2], [Piece3, Piece4]]

        while True:
            line = stdin.readline().split()
            if not line:
                break
            n += 1
            matrix.append([Piece(p) for p in line])
        
        preprocessing(matrix, n)

        return Board(matrix, n)





class PipeManiaState:
    state_id = 0

    def __init__(self, board, row=0, col=0):
        self.board = board
        self.row = row
        self.col = col
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id







class PipeMania(Problem):
    def __init__(self, board: Board):
        self.initial = PipeManiaState(board)
        self.goal = None

    def actions(self, state: PipeManiaState):
        row = state.row
        col = state.col
        n = state.board.len
        piece = state.board.get_piece(row, col)
        p = piece.get_piece_value()
        actions = []

        if row == 0:
            if col == 0:
                if p == PIECE_FD:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FB:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VB:
                    actions.append((row, col, ROTATION_NONE))
                state.col = 1
            elif col != 0 and col != n - 1:
                if p == PIECE_FD:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_180))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FE:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_180))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FB:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_BB:
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VB:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VE:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_LH:
                    actions.append((row, col, ROTATION_NONE))
                state.col += 1
            elif col == n - 1:
                if p == PIECE_FB:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FE:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VE:
                    actions.append((row, col, ROTATION_NONE))
                state.row += 1
                state.col = 0

        elif row != 0 and row != n - 1:
            if col == 0:
                if p == PIECE_FD:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FC:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_180))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FB:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_180))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_BD:
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VD:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VB:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_LV:
                    actions.append((row, col, ROTATION_NONE))
                state.col = 1
            elif col != 0 and col != n - 1:
                if p[0] == PIECE_TYPE_F or p[0] == PIECE_TYPE_B or p[0] == PIECE_TYPE_V:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_180))
                    actions.append((row, col, ROTATION_NONE))
                else:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                state.col += 1
            elif col == n - 1:
                if p == PIECE_FB:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_180))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FE:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FC:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_180))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_BE:
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VE:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VC:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_LV:
                    actions.append((row, col, ROTATION_NONE))
                state.row += 1
                state.col = 0

        elif row == n - 1:
            if col == 0:
                if p == PIECE_FD:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FC:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VD:
                    actions.append((row, col, ROTATION_NONE))
                state.col = 1
            elif col != 0 and col != n - 1:
                if p == PIECE_FD:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_180))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FE:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_180))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FC:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_BC:
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VC:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VD:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_LH:
                    actions.append((row, col, ROTATION_NONE))
                state.col += 1
            elif col == n - 1:
                if p == PIECE_FC:
                    actions.append((row, col, ROTATION_90_COUNTER_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_FE:
                    actions.append((row, col, ROTATION_90_CLOCKWISE))
                    actions.append((row, col, ROTATION_NONE))
                elif p == PIECE_VC:
                    actions.append((row, col, ROTATION_NONE))

        return actions

    def result(self, state: PipeManiaState, action):
        new_board = deepcopy(state.board)
        new_board.execute_action(action[0], action[1], action[2])
        return PipeManiaState(new_board, state.row, state.col)

    def goal_test(self, state: PipeManiaState):
        n = state.board.len

        for i in range(n):
            for j in range(n):
                piece = state.board.get_value(i, j)

                if i == 0:
                    if j == 0:
                        if piece in hasUpConnections or piece in hasLeftConnections:
                            return False

                        if piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False

                        if piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False
                    elif j != 0 and j != n - 1:
                        if piece in hasUpConnections:
                            return False

                        if piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False

                        if piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False
                        
                        if piece in hasLeftConnections:
                            if state.board.get_value(i, j - 1) not in LeftConnections:
                                return False
                    elif j == n - 1:
                        if piece in hasUpConnections or piece in hasRightConnections:
                            return False

                        if piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False

                elif i != 0 and i != n - 1:
                    if j == 0:
                        if piece in hasLeftConnections:
                            return False
                        
                        if piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False
                        
                        if piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False
                        
                        if piece in hasUpConnections:
                            if state.board.get_value(i - 1, j) not in UpConnections:
                                return False
                    elif j == n - 1:
                        if piece in hasRightConnections:
                            return False
                        
                        if piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False
                        
                        if piece in hasUpConnections:
                            if state.board.get_value(i - 1, j) not in UpConnections:
                                return False
                        
                        if piece in hasLeftConnections:
                            if state.board.get_value(i, j - 1) not in LeftConnections:
                                return False
                    else:
                        if piece in hasDownConnections:
                            if state.board.get_value(i + 1, j) not in DownConnections:
                                return False
                        
                        if piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False
                        
                        if piece in hasUpConnections:
                            if state.board.get_value(i - 1, j) not in UpConnections:
                                return False
                        
                        if piece in hasLeftConnections:
                            if state.board.get_value(i, j - 1) not in LeftConnections:
                                return False

                elif i == n - 1:
                    if j == 0:
                        if piece in hasLeftConnections or piece in hasDownConnections:
                            return False
                        
                        if piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False
                        
                        if piece in hasUpConnections:
                            if state.board.get_value(i - 1, j) not in UpConnections:
                                return False
                        
                    elif j != 0 and j != n - 1:
                        if piece in hasDownConnections:
                            return False
                        if piece in hasRightConnections:
                            if state.board.get_value(i, j + 1) not in RightConnections:
                                return False
                        if piece in hasUpConnections:
                            if state.board.get_value(i - 1, j) not in UpConnections:
                                return False
                        if piece in hasLeftConnections:
                            if state.board.get_value(i, j - 1) not in LeftConnections:
                                return False
                    elif j == n - 1:
                        if piece in hasRightConnections or piece in hasDownConnections:
                            return False
                        if piece in hasUpConnections:
                            if state.board.get_value(i - 1, j) not in UpConnections:
                                return False
                        if piece in hasLeftConnections:
                            if state.board.get_value(i, j - 1) not in LeftConnections:
                                return False
        return True

    def h(self, node: Node):
        # TODO
        pass




if __name__ == "__main__":
    # Read the grid in figure 1a:
    board = Board.parse_instance()
    # Create an instance of PipeMania:
    problem = PipeMania(board)
    # Get the solution node using depth-first search:
    goal_node = breadth_first_tree_search(problem)

    print(goal_node.state.board.print(), end="")