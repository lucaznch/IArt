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
    iterative_deepening_search
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
PieceRotations = {'FC': ('FD', 'FE', 'FB'), 
                  'FB': ('FE', 'FD', 'FC'),
                  'FE': ('FC', 'FB', 'FD'),
                  'FD': ('FB', 'FC', 'FE'),
                  'BC': ('BD', 'BE', 'BB'),
                  'BB': ('BE', 'BD', 'BC'),
                  'BE': ('BC', 'BB', 'BD'),
                  'BD': ('BB', 'BC', 'BE'),
                  'VC': ('VD', 'VE', 'VB'),
                  'VB': ('VE', 'VD', 'VC'),
                  'VE': ('VC', 'VB', 'VD'),
                  'VD': ('VB', 'VC', 'VE'),
                  'LH': ('LV', 'LV', 'LH'),
                  'LV': ('LH', 'LH', 'LV')}

# Rotations to index the PieceRotations dictionary where,
# index 0, 1 and 2 correspond to a 90 degree clockwise rotation, 90 degree counter-clockwise rotation and 180 degree rotation, respectively
ROTATION_90_CLOCKWISE = 0
ROTATION_90_COUNTER_CLOCKWISE = 1
ROTATION_180 = 2
ROTATION_NONE = 3



RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3



# pieces that have connections on the left
hasLeftConnections = ('FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH')

# pieces that have connections on the right
hasRightConnections = ('FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH')

# pieces that have connections above
hasUpConnections = ('FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV')

# pieces that have connections below
hasDownConnections = ('FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV')



# pieces that connect to the right, so they are LEFT connections
LeftConnections = ('FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH')

# pieces that connect to the left, so they are RIGHT connections
RightConnections = ('FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH')

# pieces that connect below, so they are UP connections
UpConnections = ('FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV')

# pieces that connect above, so they are DOWN connections
DownConnections = ('FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV')





def preprocessing(pieces, n):
    connections = 0
    fixed_pieces = 0

    for i in range(n):
        for j in range(n):

            piece = pieces[i][j]
            piece_type = piece.value[0]
            
            # count the number of connections
            if piece_type == PIECE_TYPE_F:
                connections += 1
            elif piece_type == PIECE_TYPE_B:
                connections += 3
            elif piece_type == PIECE_TYPE_V:
                connections += 2
            elif piece_type == PIECE_TYPE_L:
                connections += 2

            if i == 0:
                if j == 0:
                    if piece_type == PIECE_TYPE_F:
                        piece.value = PIECE_FB
                    elif piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VB
                        piece.isFixed = True
                        fixed_pieces += 1

                    if piece.isFixed:
                        right = pieces[i][j + 1]
                        down = pieces[i + 1][j]

                        if right.value[0] == PIECE_TYPE_F:
                            right.value = PIECE_FE
                            right.isFixed = True
                            fixed_pieces += 1
                        elif right.value[0] == PIECE_TYPE_V:
                            right.value = PIECE_VE
                            right.isFixed = True
                            fixed_pieces += 1
                        
                        if down.value[0] == PIECE_TYPE_F:
                            down.value = PIECE_FC
                            down.isFixed = True
                            fixed_pieces += 1
                        elif down.value[0] == PIECE_TYPE_V:
                            down.value = PIECE_VD
                            down.isFixed = True
                            fixed_pieces += 1
                            
                elif j != 0 and j != n - 1:
                    if piece.isFixed and (piece_type == PIECE_TYPE_F or piece_type == PIECE_TYPE_V):
                        continue

                    if piece_type == PIECE_TYPE_F:
                        piece.value = PIECE_FB
                    elif piece_type == PIECE_TYPE_B:
                        piece.value = PIECE_BB
                        piece.isFixed = True
                        fixed_pieces += 1
                    elif piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VE
                    elif piece_type == PIECE_TYPE_L:
                        piece.value = PIECE_LH
                        piece.isFixed = True
                        fixed_pieces += 1
                    
                    if piece.isFixed:
                        left = pieces[i][j - 1]
                        right = pieces[i][j + 1]

                        if left.value[0] == PIECE_TYPE_F:
                            left.value = PIECE_FD
                            if not left.isFixed:
                                left.isFixed = True
                                fixed_pieces += 1
                        elif left.value[0] == PIECE_TYPE_V:
                            left.value = PIECE_VB
                            if not left.isFixed:
                                left.isFixed = True
                                fixed_pieces += 1
                        if right.value[0] == PIECE_TYPE_F:
                            right.value = PIECE_FE
                            right.isFixed = True
                            fixed_pieces += 1
                        elif right.value[0] == PIECE_TYPE_V:
                            right.value = PIECE_VE
                            right.isFixed = True
                            fixed_pieces += 1
                        if piece_type == PIECE_TYPE_B:
                            down = pieces[i + 1][j]
                            if down.value[0] == PIECE_TYPE_F:
                                down.value = PIECE_FC
                                down.isFixed = True
                                fixed_pieces += 1

                elif j == n - 1:
                    if piece.isFixed and piece_type == PIECE_TYPE_F:
                        continue

                    if piece_type == PIECE_TYPE_F:
                        piece.value = PIECE_FB
                    elif piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VE
                        piece.isFixed = True
                        fixed_pieces += 1
                    
                    if piece.isFixed:
                        left = pieces[i][j - 1]
                        down = pieces[i + 1][j]

                        if left.value[0] == PIECE_TYPE_F:
                            left.value = PIECE_FD
                            if not left.isFixed:
                                left.isFixed = True
                                fixed_pieces += 1
                        elif left.value[0] == PIECE_TYPE_V:
                            left.value = PIECE_VB
                            if not left.isFixed:
                                left.isFixed = True
                                fixed_pieces += 1
                        if down.value[0] == PIECE_TYPE_F:
                            down.value = PIECE_FC
                            down.isFixed = True
                            fixed_pieces += 1
                        elif down.value[0] == PIECE_TYPE_V:
                            down.value = PIECE_VC
                            down.isFixed = True
                            fixed_pieces += 1
                    

            elif i != 0 and i != n - 1:
                if j == 0:
                    if piece.isFixed and (piece_type == PIECE_TYPE_F or piece_type == PIECE_TYPE_V):
                        continue
                    
                    if piece_type == PIECE_TYPE_F:
                        piece.value = PIECE_FD
                    elif piece_type == PIECE_TYPE_B:
                        piece.value = PIECE_BD
                        piece.isFixed = True
                        fixed_pieces += 1
                    elif piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VB
                    elif piece_type == PIECE_TYPE_L:
                        piece.value = PIECE_LV
                        piece.isFixed = True
                        fixed_pieces += 1

                    if piece.isFixed:
                        up = pieces[i - 1][j]
                        down = pieces[i + 1][j]

                        if up.value[0] == PIECE_TYPE_F:
                            up.value = PIECE_FB
                            if not up.isFixed:
                                up.isFixed = True
                                fixed_pieces += 1
                        elif up.value[0] == PIECE_TYPE_V:
                            up.value = PIECE_VB
                            if not up.isFixed:
                                up.isFixed = True
                                fixed_pieces += 1
                        if down.value[0] == PIECE_TYPE_F:
                            down.value = PIECE_FC
                            down.isFixed = True
                        elif down.value[0] == PIECE_TYPE_V:
                            down.value = PIECE_VD
                            down.isFixed = True
                        if piece_type == PIECE_TYPE_B:
                            right = pieces[i][j + 1]
                            if right.value[0] == PIECE_TYPE_F:
                                right.value = PIECE_FE
                                right.isFixed = True
                                fixed_pieces += 1

                elif j != 0 and j != n - 1:
                    continue # not an egde

                elif j == n - 1:
                    if piece.isFixed and (piece_type == PIECE_TYPE_F or piece_type == PIECE_TYPE_V):
                        continue
                    
                    if piece_type == PIECE_TYPE_F:
                        piece.value = PIECE_FE
                    elif piece_type == PIECE_TYPE_B:
                        piece.value = PIECE_BE
                        piece.isFixed = True
                        fixed_pieces += 1
                    elif piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VE
                    elif piece_type == PIECE_TYPE_L:
                        piece.value = PIECE_LV
                        piece.isFixed = True
                        fixed_pieces += 1
                    
                    if piece.isFixed:
                        up = pieces[i - 1][j]
                        down = pieces[i + 1][j]

                        if up.value[0] == PIECE_TYPE_F:
                            up.value = PIECE_FB
                            if not up.isFixed:
                                up.isFixed = True
                                fixed_pieces += 1
                        elif up.value[0] == PIECE_TYPE_V:
                            up.value = PIECE_VE
                            if not up.isFixed:
                                up.isFixed = True
                                fixed_pieces += 1
                        if down.value[0] == PIECE_TYPE_F:
                            down.value = PIECE_FC
                            down.isFixed = True
                            fixed_pieces += 1
                        elif down.value[0] == PIECE_TYPE_V:
                            down.value = PIECE_VC
                            down.isFixed = True
                            fixed_pieces += 1
                        if piece_type == PIECE_TYPE_B:
                            left = pieces[i][j - 1]
                            if left.value[0] == PIECE_TYPE_F:
                                left.value = PIECE_FD
                                left.isFixed = True
                                fixed_pieces += 1

            elif i == n - 1:
                if j == 0:
                    if piece.isFixed and piece_type == PIECE_TYPE_F:
                        continue

                    if piece_type == PIECE_TYPE_F:
                        piece.value = PIECE_FC
                    elif piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VD
                        piece.isFixed = True
                        fixed_pieces += 1
                    
                    if piece.isFixed:
                        right = pieces[i][j + 1]
                        up = pieces[i - 1][j]

                        if right.value[0] == PIECE_TYPE_F:
                            right.value = PIECE_FE
                            right.isFixed = True
                            fixed_pieces += 1
                        elif right.value[0] == PIECE_TYPE_V:
                            right.value = PIECE_VC
                            right.isFixed = True
                            fixed_pieces += 1
                        if up.value[0] == PIECE_TYPE_F:
                            up.value = PIECE_FB
                            if not up.isFixed:
                                up.isFixed = True
                                fixed_pieces += 1
                        elif up.value[0] == PIECE_TYPE_V:
                            up.value = PIECE_VB
                            if not up.isFixed:
                                up.isFixed = True
                                fixed_pieces += 1

                elif j != 0 and j != n - 1:
                    if piece.isFixed and (piece_type == PIECE_TYPE_F or piece_type == PIECE_TYPE_V):
                        continue
                    
                    if piece_type == PIECE_TYPE_F:
                        piece.value = PIECE_FC
                    elif piece_type == PIECE_TYPE_B:
                        piece.value = PIECE_BC
                        piece.isFixed = True
                        fixed_pieces += 1
                    elif piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VC
                    elif piece_type == PIECE_TYPE_L:
                        piece.value = PIECE_LH
                        piece.isFixed = True
                        fixed_pieces += 1
                    
                    if piece.isFixed:
                        left = pieces[i][j - 1]
                        right = pieces[i][j + 1]

                        if left.value[0] == PIECE_TYPE_F:
                            left.value = PIECE_FD
                            if not left.isFixed:
                                left.isFixed = True
                                fixed_pieces += 1
                        elif left.value[0] == PIECE_TYPE_V:
                            left.value = PIECE_VD
                            if not left.isFixed:
                                left.isFixed = True
                                fixed_pieces += 1
                        if right.value[0] == PIECE_TYPE_F:
                            right.value = PIECE_FE
                            right.isFixed = True
                            fixed_pieces += 1
                        elif right.value[0] == PIECE_TYPE_V:
                            right.value = PIECE_VC
                            right.isFixed = True
                            fixed_pieces += 1
                        if piece_type == PIECE_TYPE_B:
                            up = pieces[i - 1][j]
                            if up.value[0] == PIECE_TYPE_F:
                                up.value = PIECE_FB
                                up.isFixed = True
                                fixed_pieces += 1

                elif j == n - 1:
                    if piece.isFixed and piece_type == PIECE_TYPE_F:
                        continue

                    if piece_type == PIECE_TYPE_F:
                        piece.value = PIECE_FC
                    elif piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VC
                        piece.isFixed = True
                        fixed_pieces += 1
                    
                    if piece.isFixed:
                        left = pieces[i][j - 1]
                        up = pieces[i - 1][j]

                        if left.value[0] == PIECE_TYPE_F:
                            left.value = PIECE_FD
                            if not left.isFixed:
                                left.isFixed = True
                                fixed_pieces += 1
                        elif left.value[0] == PIECE_TYPE_V:
                            left.value = PIECE_VD
                            if not left.isFixed:
                                left.isFixed = True
                                fixed_pieces += 1
                        if up.value[0] == PIECE_TYPE_F:
                            up.value = PIECE_FB
                            if not up.isFixed:
                                up.isFixed = True
                                fixed_pieces += 1
                        elif up.value[0] == PIECE_TYPE_V:
                            up.value = PIECE_VE
                            if not up.isFixed:
                                up.isFixed = True
                                fixed_pieces += 1
    fixed_pieces = 0
    for i in range(n):
        for j in range(n):
            piece = pieces[i][j]
            piece_type = piece.value[0]

            if not piece.isFixed:
                if i == 0:
                    if j == 0:
                        if piece_type == PIECE_TYPE_F:
                            if pieces[i][j + 1].isFixed:
                                piece.value = PIECE_FB
                                piece.isFixed = True
                            elif pieces[i + 1][j].isFixed:
                                piece.value = PIECE_FD
                                piece.isFixed = True
                    elif j != 0 and j != n - 1:
                        if piece_type == PIECE_TYPE_V and pieces[i][j + 1].isFixed:
                            piece.value = PIECE_VE
                            piece.isFixed = True
                    elif j == n - 1:
                        if piece_type == PIECE_TYPE_F and pieces[i + 1][j].isFixed:
                            piece.value = PIECE_FE
                            piece.isFixed = True

                elif i != 0 and i != n - 1:
                    if j == 0:
                        if piece_type == PIECE_TYPE_V and pieces[i + 1][j].isFixed:
                            piece.value = PIECE_VD
                            piece.isFixed = True
                    elif j != 0 and j != n - 1:
                        # TODO
                        pass
                    elif j == n - 1:
                        if piece_type == PIECE_TYPE_V and pieces[i + 1][j].isFixed:
                            piece.value = PIECE_VC
                            piece.isFixed = True

                elif i == n - 1:
                    if j == 0:
                        if piece_type == PIECE_TYPE_F and pieces[i][j + 1].isFixed:
                            piece.value = PIECE_FC
                            piece.isFixed = True
                    elif j != 0 and j != n - 1:
                        if piece_type == PIECE_TYPE_V and pieces[i][j + 1].isFixed:
                            piece.value = PIECE_VC
                            piece.isFixed = True
                    elif j == n - 1:                        
                        pass


            if piece.isFixed:
                fixed_pieces += 1
    
    return (connections, fixed_pieces)





class Piece:
    def __init__(self, value):
        self.value = value
        self.isFixed = False
    
    def rotate(self, rotation):
        if rotation != ROTATION_NONE:
            self.value = PieceRotations[self.value][rotation]





class Board:
    def __init__(self, matrix, len, total_connections, fixed_pieces):
        self.matrix = matrix
        self.len = len
        self.total_connections = total_connections
        self.total_pieces = len * len
        self.fixed_pieces = fixed_pieces

    def __repr__(self):
        result = ''
        for i in range(self.len):
            for j in range(self.len):
                if j == self.len - 1:
                    result += self.matrix[i][j].value + "\n"
                else:
                    result += self.matrix[i][j].value + "\t"
        return result

    @staticmethod
    def parse_instance():
        n = 0
        matrix = []

        while True:
            line = stdin.readline().split()
            if not line:
                break
            n += 1
            matrix.append([Piece(p) for p in line])
        
        result = preprocessing(matrix, n)

        return Board(matrix, n, result[0], result[1])





class PipeManiaState:
    state_id = 0

    def __init__(self, board, row=0, col=0):
        self.board = board
        self.current_row = row
        self.current_col = col
        self.connections = 0
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id





class PipeMania(Problem):
    def __init__(self, board: Board):
        self.initial = PipeManiaState(board)
        self.goal = None

    def actions(self, state: PipeManiaState):
        row = state.current_row
        col = state.current_col
        n = state.board.len
        piece = state.board.matrix[row][col]
        actions = []

        if piece.isFixed:
            while True:
                col += 1
                if col == n:
                    col = 0
                    row += 1
                if row == n:
                    return actions
                if not state.board.matrix[row][col].isFixed:
                    piece = state.board.matrix[row][col]
                    break
        
        p = piece.value
        
        if row == 0:
            if col == 0:
                if p[0] == PIECE_TYPE_F:
                    if state.board.matrix[row][col + 1].isFixed:
                        actions.append((row, col, PIECE_FB, row, col + 1))
                    elif state.board.matrix[row + 1][col].isFixed:
                        actions.append((row, col, PIECE_FD, row, col + 1))
                    else:
                        actions.append((row, col, PIECE_FB, row, col + 1))
                        actions.append((row, col, PIECE_FD, row, col + 1))
                    piece.isFixed = True
            elif col != 0 and col != n - 1:
                if p[0] == PIECE_TYPE_F:
                    if state.board.matrix[row][col + 1].isFixed:
                        actions.append((row, col, PIECE_FB, row, col + 1))
                        actions.append((row, col, PIECE_FE, row, col + 1))
                    else:
                        actions.append((row, col, PIECE_FB, row, col + 1))
                        actions.append((row, col, PIECE_FE, row, col + 1))
                        actions.append((row, col, PIECE_FD, row, col + 1))
                    piece.isFixed = True
                elif p[0] == PIECE_TYPE_V:
                    if state.board.matrix[row][col + 1].isFixed:
                        actions.append((row, col, PIECE_VE, row, col + 1))
                    else:
                        actions.append((row, col, PIECE_VB, row, col + 1))
                        actions.append((row, col, PIECE_VE, row, col + 1))
                    piece.isFixed = True
            elif col == n - 1:
                if p[0] == PIECE_TYPE_F: 
                    if state.board.matrix[row - 1][col].isFixed:
                        actions.append((row, col, PIECE_FE, row + 1, 0))
                    else:
                        actions.append((row, col, PIECE_FB, row + 1, 0))
                        actions.append((row, col, PIECE_FE, row + 1, 0))
                    piece.isFixed = True

        elif row != 0 and row != n - 1:
            if col == 0:
                if p[0] == PIECE_TYPE_F: #
                    if state.board.matrix[row + 1][col].isFixed:
                        actions.append((row, col, PIECE_FD, row, col + 1))
                        actions.append((row, col, PIECE_FC, row, col + 1))
                    else:
                        actions.append((row, col, PIECE_FB, row, col + 1))
                        actions.append((row, col, PIECE_FD, row, col + 1))
                        actions.append((row, col, PIECE_FC, row, col + 1))
                    piece.isFixed = True
                elif p[0] == PIECE_TYPE_V:
                    if state.board.matrix[row + 1][col].isFixed:
                        actions.append((row, col, PIECE_VD, row, col + 1))
                    else:
                        actions.append((row, col, PIECE_VD, row, col + 1))
                        actions.append((row, col, PIECE_VB, row, col + 1))
                    piece.isFixed = True
            elif col != 0 and col != n - 1: #TODO - optimize!
                if p[0] == PIECE_TYPE_F:
                    actions.append((row, col, PIECE_FC, row, col + 1))
                    actions.append((row, col, PIECE_FD, row, col + 1))
                    actions.append((row, col, PIECE_FE, row, col + 1))
                    actions.append((row, col, PIECE_FB, row, col + 1))
                elif p[0] == PIECE_TYPE_V:
                    actions.append((row, col, PIECE_VC, row, col + 1))
                    actions.append((row, col, PIECE_VD, row, col + 1))
                    actions.append((row, col, PIECE_VB, row, col + 1))
                    actions.append((row, col, PIECE_VE, row, col + 1))
                elif p[0] == PIECE_TYPE_B:
                    actions.append((row, col, PIECE_BC, row, col + 1))
                    actions.append((row, col, PIECE_BB, row, col + 1))
                    actions.append((row, col, PIECE_BE, row, col + 1))
                    actions.append((row, col, PIECE_BD, row, col + 1))
                elif p[0] == PIECE_TYPE_L:
                    actions.append((row, col, PIECE_LH, row, col + 1))
                    actions.append((row, col, PIECE_LV, row, col + 1))
                piece.isFixed = True
            elif col == n - 1:
                if p[0] == PIECE_TYPE_F:
                    if state.board.matrix[row + 1][col].isFixed:
                        actions.append((row, col, PIECE_FE, row + 1, 0))
                        actions.append((row, col, PIECE_FC, row + 1, 0))
                    else:
                        actions.append((row, col, PIECE_FE, row + 1, 0))
                        actions.append((row, col, PIECE_FC, row + 1, 0))
                        actions.append((row, col, PIECE_FB, row + 1, 0))
                    piece.isFixed = True
                elif p[0] == PIECE_TYPE_V:
                    if state.board.matrix[row + 1][col].isFixed:
                        actions.append((row, col, PIECE_VC, row + 1, 0))
                    else:
                        actions.append((row, col, PIECE_VE, row + 1, 0))
                        actions.append((row, col, PIECE_VC, row + 1, 0))
                    piece.isFixed = True

        elif row == n - 1:
            if col == 0:
                if p[0] == PIECE_TYPE_F:
                    if state.board.matrix[row][col + 1].isFixed:
                        actions.append((row, col, PIECE_FC, row, col + 1))
                    else:
                        actions.append((row, col, PIECE_FD, row, col + 1))
                        actions.append((row, col, PIECE_FC, row, col + 1))
                    piece.isFixed = True
            elif col != 0 and col != n - 1:
                if p[0] == PIECE_TYPE_F:
                    if state.board.matrix[row][col + 1].isFixed:
                        actions.append((row, col, PIECE_FC, row, col + 1))
                        actions.append((row, col, PIECE_FE, row, col + 1))
                    else:
                        actions.append((row, col, PIECE_FC, row, col + 1))
                        actions.append((row, col, PIECE_FE, row, col + 1))
                        actions.append((row, col, PIECE_FD, row, col + 1))
                    piece.isFixed = True
                elif p[0] == PIECE_TYPE_V:
                    if state.board.matrix[row][col + 1].isFixed:
                        actions.append((row, col, PIECE_VC, row, col + 1))
                    else:
                        actions.append((row, col, PIECE_VC, row, col + 1))
                        actions.append((row, col, PIECE_VD, row, col + 1))
                    piece.isFixed = True
            elif col == n - 1:
                if p[0] == PIECE_TYPE_F:
                    actions.append((row, col, PIECE_FC, row, col))
                    actions.append((row, col, PIECE_FE, row, col))
                    piece.isFixed = True
        state.board.fixed_pieces += 1
        return actions

    def result(self, state: PipeManiaState, action):
        row = action[0]
        col = action[1]
        new_piece = action[2]
        new_row = action[3]
        new_col = action[4]
        new_board = deepcopy(state.board)

        new_board.matrix[row][col].value = new_piece
        return PipeManiaState(new_board, new_row, new_col)

    def goal_test(self, state: PipeManiaState):
        return state.board.fixed_pieces == state.board.total_pieces

    def h(self, node: Node):
        # TODO
        pass






if __name__ == "__main__":

    board = Board.parse_instance()

    print(board, end="")
    #print(board.fixed_pieces)

    #problem = PipeMania(board)
    
    #node = breadth_first_tree_search(problem)
    
    #print(node.state.board, end="")
