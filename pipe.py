from sys import stdin
from copy import deepcopy
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




def preprocessing(n, board):
    total_connections = 0
    connections = 0

    for i in range(n):
        for j in range(n):
            piece = board[i][j]
            piece_type = piece.value[0]

            if piece_type == PIECE_TYPE_F:
                total_connections += 1
            elif piece_type == PIECE_TYPE_B:
                total_connections += 3
            elif piece_type == PIECE_TYPE_V:
                total_connections += 2
            elif piece_type == PIECE_TYPE_L:
                total_connections += 2

            if i == 0:
                if j == 0:
                    if piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VB
                        piece.isFixed = True
                        
                        right = board[i][j + 1]
                        down = board[i + 1][j]

                        if right.value[0] == PIECE_TYPE_F:
                            right.value = PIECE_FE
                            right.isFixed = True
                        elif right.value[0] == PIECE_TYPE_V:
                            right.value = PIECE_VE
                            right.isFixed = True
                        if down.value[0] == PIECE_TYPE_F:
                            down.value = PIECE_FC
                            down.isFixed = True
                        elif down.value[0] == PIECE_TYPE_V:
                            down.value = PIECE_VD
                            down.isFixed = True
                    elif piece_type == PIECE_TYPE_F and not piece.isFixed:
                        piece.value = PIECE_FB
                elif j != 0 and j != n - 1:
                    if piece_type == PIECE_TYPE_B or piece_type == PIECE_TYPE_L:
                        if piece_type == PIECE_TYPE_B:
                            piece.value = PIECE_BB
                        else:
                            piece.value = PIECE_LH
                        piece.isFixed = True

                        left = board[i][j - 1]
                        right = board[i][j + 1]

                        if left.value[0] == PIECE_TYPE_F:
                            left.value = PIECE_FD
                            left.isFixed = True
                        elif left.value[0] == PIECE_TYPE_V:
                            left.value = PIECE_VB
                            left.isFixed = True
                        if right.value[0] == PIECE_TYPE_F:
                            right.value = PIECE_FE
                            right.isFixed = True
                        elif right.value[0] == PIECE_TYPE_V:
                            right.value = PIECE_VE
                            right.isFixed = True
                        if piece_type == PIECE_TYPE_B:
                            down = board[i + 1][j]
                            if down.value[0] == PIECE_TYPE_F:
                                down.value = PIECE_FC
                                down.isFixed = True
                    elif piece_type == PIECE_TYPE_F and not piece.isFixed:
                        piece.value = PIECE_FB
                    elif piece_type == PIECE_TYPE_V and not piece.isFixed:
                        piece.value = PIECE_VB
                elif j == n - 1:
                    if piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VE
                        piece.isFixed = True

                        left = board[i][j - 1]
                        down = board[i + 1][j]

                        if left.value[0] == PIECE_TYPE_F:
                            left.value = PIECE_FD
                            left.isFixed = True
                        elif left.value[0] == PIECE_TYPE_V:
                            left.value = PIECE_VB
                            left.isFixed = True
                        if down.value[0] == PIECE_TYPE_F:
                            down.value = PIECE_FC
                            down.isFixed = True
                        elif down.value[0] == PIECE_TYPE_V:
                            down.value = PIECE_VC
                            down.isFixed = True
                    elif piece_type == PIECE_TYPE_F and not piece.isFixed:
                        piece.value = PIECE_FB
                    
            elif i != 0 and i != n - 1:
                if j == 0:
                    if piece_type == PIECE_TYPE_B or piece_type == PIECE_TYPE_L:
                        if piece_type == PIECE_TYPE_B:
                            piece.value = PIECE_BD
                        else:
                            piece.value = PIECE_LV
                        piece.isFixed = True

                        up = board[i - 1][j]
                        down = board[i + 1][j]

                        if up.value[0] == PIECE_TYPE_F:
                            up.value = PIECE_FB
                            up.isFixed = True
                        elif up.value[0] == PIECE_TYPE_V:
                            up.value = PIECE_VB
                            up.isFixed = True
                        if down.value[0] == PIECE_TYPE_F:
                            down.value = PIECE_FC
                            down.isFixed = True
                        elif down.value[0] == PIECE_TYPE_V:
                            down.value = PIECE_VD
                            down.isFixed = True
                        if piece_type == PIECE_TYPE_B:
                            right = board[i][j + 1]
                            if right.value[0] == PIECE_TYPE_F:
                                right.value = PIECE_FE
                                right.isFixed = True
                    elif piece_type == PIECE_TYPE_F and not piece.isFixed:
                        piece.value = PIECE_FD
                    elif piece_type == PIECE_TYPE_V and not piece.isFixed:
                        piece.value = PIECE_VB
                elif j != 0 and j != n - 1:
                    continue # not an edge piece
                elif j == n - 1:
                    if piece_type == PIECE_TYPE_B or piece_type == PIECE_TYPE_L:
                        if piece_type == PIECE_TYPE_B:
                            piece.value = PIECE_BE
                        else:
                            piece.value = PIECE_LV
                        piece.isFixed = True

                        up = board[i - 1][j]
                        down = board[i + 1][j]

                        if up.value[0] == PIECE_TYPE_F:
                            up.value = PIECE_FB
                            up.isFixed = True
                        elif up.value[0] == PIECE_TYPE_V:
                            up.value = PIECE_VE
                            up.isFixed = True
                        if down.value[0] == PIECE_TYPE_F:
                            down.value = PIECE_FC
                            down.isFixed = True
                        elif down.value[0] == PIECE_TYPE_V:
                            down.value = PIECE_VC
                            down.isFixed = True
                        if piece_type == PIECE_TYPE_B:
                            left = board[i][j - 1]
                            if left.value[0] == PIECE_TYPE_F:
                                left.value = PIECE_FD
                                left.isFixed = True
                    elif piece_type == PIECE_TYPE_F and not piece.isFixed:
                        piece.value = PIECE_FE
                    elif piece_type == PIECE_TYPE_V and not piece.isFixed:
                        piece.value = PIECE_VE

            elif i == n - 1:
                if j == 0:
                    if piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VD
                        piece.isFixed = True

                        right = board[i][j + 1]
                        up = board[i - 1][j]

                        if right.value[0] == PIECE_TYPE_F:
                            right.value = PIECE_FE
                            right.isFixed = True
                        elif right.value[0] == PIECE_TYPE_V:
                            right.value = PIECE_VC
                            right.isFixed = True
                        if up.value[0] == PIECE_TYPE_F:
                            up.value = PIECE_FB
                            up.isFixed = True
                        elif up.value[0] == PIECE_TYPE_V:
                            up.value = PIECE_VB
                            up.isFixed = True
                    elif piece_type == PIECE_TYPE_F and not piece.isFixed:
                        piece.value = PIECE_FC
                elif j != 0 and j != n - 1:
                    if piece_type == PIECE_TYPE_B or piece_type == PIECE_TYPE_L:
                        if piece_type == PIECE_TYPE_B:
                            piece.value = PIECE_BC
                        else:
                            piece.value = PIECE_LH
                        piece.isFixed = True

                        left = board[i][j - 1]
                        right = board[i][j + 1]

                        if left.value[0] == PIECE_TYPE_F:
                            left.value = PIECE_FD
                            left.isFixed = True
                        elif left.value[0] == PIECE_TYPE_V:
                            left.value = PIECE_VD
                            left.isFixed = True
                        if right.value[0] == PIECE_TYPE_F:
                            right.value = PIECE_FE
                            right.isFixed = True
                        elif right.value[0] == PIECE_TYPE_V:
                            right.value = PIECE_VC
                            right.isFixed = True
                        if piece_type == PIECE_TYPE_B:
                            up = board[i - 1][j]
                            if up.value[0] == PIECE_TYPE_F:
                                up.value = PIECE_FB
                                up.isFixed = True
                    elif piece_type == PIECE_TYPE_F and not piece.isFixed:
                        piece.value = PIECE_FC
                    elif piece_type == PIECE_TYPE_V and not piece.isFixed:
                        piece.value = PIECE_VC
                elif j == n - 1:
                    if piece_type == PIECE_TYPE_V:
                        piece.value = PIECE_VC
                        piece.isFixed = True

                        left = board[i][j - 1]
                        up = board[i - 1][j]

                        if left.value[0] == PIECE_TYPE_F:
                            left.value = PIECE_FD
                            left.isFixed = True
                        elif left.value[0] == PIECE_TYPE_V:
                            left.value = PIECE_VD
                            left.isFixed = True
                        if up.value[0] == PIECE_TYPE_F:
                            up.value = PIECE_FB
                            up.isFixed = True
                        elif up.value[0] == PIECE_TYPE_V:
                            up.value = PIECE_VE
                            up.isFixed = True
                    elif piece_type == PIECE_TYPE_F and not piece.isFixed:
                        piece.value = PIECE_FC
    while True:
        stuck = True

        for i in range(n):
            for j in range(n):
                piece = board[i][j]
                piece_type = piece.value[0]

                if piece.isFixed:
                    continue

                if i == 0:
                    if j == 0:
                        if piece_type == PIECE_TYPE_F:
                            if board[i][j + 1].isFixed:
                                piece.value = PIECE_FB
                                piece.isFixed = True
                                stuck = False
                            elif board[i + 1][j].isFixed:
                                piece.value = PIECE_FD
                                piece.isFixed = True
                                stuck = False
                    elif j != 0 and j != n - 1:
                        if piece_type == PIECE_TYPE_V:
                            if board[i][j + 1].isFixed:
                                if board[i][j + 1].value == PIECE_FE:
                                    piece.value = PIECE_VB
                                else:
                                    piece.value = PIECE_VE
                                piece.isFixed = True
                                stuck = False
                            elif board[i][j - 1].isFixed:
                                if board[i][j - 1].value == PIECE_FD:
                                    piece.value = PIECE_VE
                                else:
                                    piece.value = PIECE_VB
                                piece.isFixed = True
                                stuck = False
                        elif piece_type == PIECE_TYPE_F:
                            if board[i][j + 1].isFixed and board[i][j + 1].value == PIECE_VE:
                                piece.value = PIECE_FD
                                piece.isFixed = True
                                stuck = False
                            elif board[i][j - 1].isFixed and board[i][j - 1].value == PIECE_VB:
                                piece.value = PIECE_FE
                                piece.isFixed = True
                                stuck = False
                            # i will probably forget the logic of this contition and it might be wrong
                            elif board[i][j + 1].isFixed and board[i][j - 1].isFixed:
                                piece.value = PIECE_FB
                                piece.isFixed = True
                                stuck = False
                    elif j == n - 1:
                        if piece_type == PIECE_TYPE_F:
                            if board[i][j - 1].isFixed:
                                piece.value = PIECE_FB
                                piece.isFixed = True
                                stuck = False
                            elif board[i + 1][j].isFixed:
                                piece.value = PIECE_FE
                                piece.isFixed = True
                                stuck = False

                elif i != 0 and i != n - 1:
                    if j == 0:
                        if piece_type == PIECE_TYPE_V:
                            if board[i - 1][j].isFixed:
                                if board[i - 1][j].value == PIECE_FB:
                                    piece.value = PIECE_VD
                                else:
                                    piece.value = PIECE_VB
                                piece.isFixed = True
                                stuck = False
                            elif board[i + 1][j].isFixed:
                                if board[i + 1][j].value == PIECE_FC:
                                    piece.value = PIECE_VB
                                else:
                                    piece.value = PIECE_VD
                                piece.isFixed = True
                                stuck = False
                        elif piece_type == PIECE_TYPE_F:
                            if board[i - 1][j].isFixed and board[i - 1][j].value == PIECE_VB:
                                piece.value = PIECE_FC
                                piece.isFixed = True
                                stuck = False
                            elif board[i + 1][j].isFixed and board[i + 1][j].value == PIECE_VD:
                                piece.value = PIECE_FB
                                piece.isFixed = True
                                stuck = False
                            # i will probably forget the logic of this contition and it might be wrong
                            elif board[i - 1][j].isFixed and board[i + 1][j].isFixed:
                                piece.value = PIECE_FD
                                piece.isFixed = True
                                stuck = False
                    elif j != 0 and j != n - 1:
                        continue # not an edge piece
                    elif j == n - 1:
                        if piece_type == PIECE_TYPE_V:
                            if board[i - 1][j].isFixed:
                                if board[i - 1][j].value == PIECE_FB:
                                    piece.value = PIECE_VC
                                else:
                                    piece.value = PIECE_VE
                                piece.isFixed = True
                                stuck = False
                            elif board[i + 1][j].isFixed:
                                if board[i + 1][j].value == PIECE_FC:
                                    piece.value = PIECE_VE
                                else:
                                    piece.value = PIECE_VC
                                piece.isFixed = True
                                stuck = False
                        elif piece_type == PIECE_TYPE_F:
                            if board[i - 1][j].isFixed and board[i - 1][j].value == PIECE_VE:
                                piece.value = PIECE_FC
                                piece.isFixed = True
                                stuck = False
                            elif board[i + 1][j].isFixed and board[i + 1][j].value == PIECE_VC:
                                piece.value = PIECE_FB
                                piece.isFixed = True
                                stuck = False
                            # i will probably forget the logic of this contition and it might be wrong
                            elif board[i - 1][j].isFixed and board[i + 1][j].isFixed:
                                piece.value = PIECE_FE
                                piece.isFixed = True
                                stuck = False

                elif i == n - 1:
                    if j == 0:
                        if piece_type == PIECE_TYPE_F:
                            if board[i][j + 1].isFixed:
                                piece.value = PIECE_FC
                                piece.isFixed = True
                                stuck = False
                            elif board[i - 1][j].isFixed:
                                piece.value = PIECE_FD
                                piece.isFixed = True
                                stuck = False
                    elif j != 0 and j != n - 1:
                        if piece_type == PIECE_TYPE_V:
                            if board[i][j + 1].isFixed:
                                if board[i][j + 1].value == PIECE_FE:
                                    piece.value = PIECE_VD
                                else:
                                    piece.value = PIECE_VC
                                piece.isFixed = True
                                stuck = False
                            elif board[i][j - 1].isFixed:
                                if board[i][j - 1].value == PIECE_FD:
                                    piece.value = PIECE_VC
                                else:
                                    piece.value = PIECE_VD
                                piece.isFixed = True
                                stuck = False
                        elif piece_type == PIECE_TYPE_F:
                            if board[i][j + 1].isFixed and board[i][j + 1].value == PIECE_VC:
                                piece.value = PIECE_FD
                                piece.isFixed = True
                                stuck = False
                            elif board[i][j - 1].isFixed and board[i][j - 1].value == PIECE_VD:
                                piece.value = PIECE_FE
                                piece.isFixed = True
                                stuck = False
                            # i will probably forget the logic of this contition and it might be wrong
                            elif board[i][j + 1].isFixed and board[i][j - 1].isFixed:
                                piece.value = PIECE_FC
                                piece.isFixed = True
                                stuck = False
                    elif j == n - 1:
                        if piece_type == PIECE_TYPE_F:
                            if board[i][j - 1].isFixed:
                                piece.value = PIECE_FC
                                piece.isFixed = True
                                stuck = False
                            elif board[i - 1][j].isFixed:
                                piece.value = PIECE_FE
                                piece.isFixed = True
                                stuck = False
        if stuck:
            break

    for i in range(n):
        for j in range(n):
            connections += get_piece_connections(i, j, n, board)

    return (total_connections, connections)





def get_piece_connections(row, col, n, board):
    piece = board[row][col]
    piece_value = piece.value

    if row == 0:
        if col == 0:
            if piece_value == PIECE_FB and board[row + 1][col].value in hasUpConnections:
                return 1
            elif piece_value == PIECE_FD and board[row][col + 1].value in hasLeftConnections:
                return 1
            elif piece_value == PIECE_VB:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            else:
                return 0
        elif col != 0 and col != n - 1:
            if piece_value == PIECE_FB and board[row + 1][col].value in hasUpConnections:
                return 1
            elif piece_value == PIECE_FD and board[row][col + 1].value in hasLeftConnections:
                return 1
            elif piece_value == PIECE_FE and board[row][col - 1].value in hasRightConnections:
                return 1
            elif piece_value == PIECE_VB:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            elif piece_value == PIECE_VE:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_BB:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_LH:
                c = 0
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            else:
                return 0
        elif col == n - 1:
            if piece_value == PIECE_FB and board[row + 1][col].value in hasUpConnections:
                return 1
            elif piece_value == PIECE_FE and board[row][col - 1].value in hasRightConnections:
                return 1
            elif piece_value == PIECE_VE:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            else:
                return 0

    elif row != 0 and row != n - 1:
        if col == 0:
            if piece_value == PIECE_FB and board[row + 1][col].value in hasUpConnections:
                return 1
            elif piece_value == PIECE_FD and board[row][col + 1].value in hasLeftConnections:
                return 1
            elif piece_value == PIECE_FC and board[row - 1][col].value in hasDownConnections:
                return 1
            elif piece_value == PIECE_VB:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            elif piece_value == PIECE_VD:
                c = 0
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                return c
            elif piece_value == PIECE_BD:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                return c
            elif piece_value == PIECE_LV:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                return c
            else:
                return 0
        elif col != 0 and col != n - 1:
            if piece_value == PIECE_FB and board[row + 1][col].value in hasUpConnections:
                return 1
            elif piece_value == PIECE_FD and board[row][col + 1].value in hasLeftConnections:
                return 1
            elif piece_value == PIECE_FE and board[row][col - 1].value in hasRightConnections:
                return 1
            elif piece_value == PIECE_FC and board[row - 1][col].value in hasDownConnections:
                return 1
            elif piece_value == PIECE_VB:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            elif piece_value == PIECE_VE:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_VC:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_VD:
                c = 0
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                return c
            elif piece_value == PIECE_BB:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_BC:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            elif piece_value == PIECE_BD:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                return c
            elif piece_value == PIECE_BE:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_LH:
                c = 0
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            elif piece_value == PIECE_LV:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                return c
            else:
                return 0
        elif col == n - 1:
            if piece_value == PIECE_FE and board[row][col - 1].value in hasRightConnections:
                return 1
            elif piece_value == PIECE_FC and board[row - 1][col].value in hasDownConnections:
                return 1
            elif piece_value == PIECE_FB and board[row + 1][col].value in hasUpConnections:
                return 1
            elif piece_value == PIECE_VE:
                c = 0
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_VC:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_BE:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_LV:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row + 1][col].value in hasUpConnections:
                    c += 1
                return c
            else:
                return 0

    elif row == n - 1:
        if col == 0:
            if piece_value == PIECE_FC and board[row - 1][col].value in hasDownConnections:
                return 1
            elif piece_value == PIECE_FD and board[row][col + 1].value in hasLeftConnections:
                return 1
            elif piece_value == PIECE_VD:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            else:
                return 0
        elif col != 0 and col != n - 1:
            if piece_value == PIECE_FC and board[row - 1][col].value in hasDownConnections:
                return 1
            elif piece_value == PIECE_FD and board[row][col + 1].value in hasLeftConnections:
                return 1
            elif piece_value == PIECE_FE and board[row][col - 1].value in hasRightConnections:
                return 1
            elif piece_value == PIECE_VC:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_VD:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            elif piece_value == PIECE_BC:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            elif piece_value == PIECE_LH:
                c = 0
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                if board[row][col + 1].value in hasLeftConnections:
                    c += 1
                return c
            else:
                return 0
        elif col == n - 1:
            if piece_value == PIECE_FC and board[row - 1][col].value in hasDownConnections:
                return 1
            elif piece_value == PIECE_FE and board[row][col - 1].value in hasRightConnections:
                return 1
            elif piece_value == PIECE_VC:
                c = 0
                if board[row - 1][col].value in hasDownConnections:
                    c += 1
                if board[row][col - 1].value in hasRightConnections:
                    c += 1
                return c
            else:
                return 0
    return 0






class Piece:
    def __init__(self, value):
        self.value = value
        self.isFixed = False





class Board:
    def __init__(self, n, matrix, total_connections, connections):
        self.n = n
        self.matrix = matrix
        self.total_connections = total_connections
        self.connections = connections
    
    def __repr__(self):
        result = ''
        for i in range(self.n):
            for j in range(self.n):
                if j == self.n - 1:
                    result += self.matrix[i][j].value + '\n'
                else:
                    result += self.matrix[i][j].value + '\t'
        return result
    
    def execute_action(self, row, col, piece):
        current_piece_connections = get_piece_connections(row, col, self.n, self.matrix)
        current_side_connections = self.update_connections(row, col)

        self.matrix[row][col].value = piece

        new_piece_connections = get_piece_connections(row, col, self.n, self.matrix)
        new_side_connections = self.update_connections(row, col)

        c = self.connections - (current_piece_connections + current_side_connections[0] + current_side_connections[1] + current_side_connections[2] + current_side_connections[3]) + (new_piece_connections + new_side_connections[0] + new_side_connections[1] + new_side_connections[2] + new_side_connections[3])
        self.connections = c


    def update_connections(self, row, col):
        n = self.n
        if row == 0:
            if col == 0:
                left = 0
                up = 0
                right = get_piece_connections(row, col + 1, n, self.matrix)
                down = get_piece_connections(row + 1, col, n, self.matrix)
            elif col != 0 and col != n - 1:
                left = get_piece_connections(row, col - 1, n, self.matrix)
                up = 0
                right = get_piece_connections(row, col + 1, n, self.matrix)
                down = get_piece_connections(row + 1, col, n, self.matrix)
            elif col == n - 1:
                left = get_piece_connections(row, col - 1, n, self.matrix)
                up = 0
                right = 0
                down = get_piece_connections(row + 1, col, n, self.matrix)
        elif row != 0 and row != n - 1:
            if col == 0:
                left = 0
                up = get_piece_connections(row - 1, col, n, self.matrix)
                right = get_piece_connections(row, col + 1, n, self.matrix)
                down = get_piece_connections(row + 1, col, n, self.matrix)
            elif col != 0 and col != n - 1:
                left = get_piece_connections(row, col - 1, n, self.matrix)
                up = get_piece_connections(row - 1, col, n, self.matrix)
                right = get_piece_connections(row, col + 1, n, self.matrix)
                down = get_piece_connections(row + 1, col, n, self.matrix)
            elif col == n - 1:
                left = get_piece_connections(row, col - 1, n, self.matrix)
                up = get_piece_connections(row - 1, col, n, self.matrix)
                right = 0
                down = get_piece_connections(row + 1, col, n, self.matrix)
        elif row == n - 1:
            if col == 0:
                left = 0
                up = get_piece_connections(row - 1, col, n, self.matrix)
                right = get_piece_connections(row, col + 1, n, self.matrix)
                down = 0
            elif col != 0 and col != n - 1:
                left = get_piece_connections(row, col - 1, n, self.matrix)
                up = get_piece_connections(row - 1, col, n, self.matrix)
                right = get_piece_connections(row, col + 1, n, self.matrix)
                down = 0
            elif col == n - 1:
                left = get_piece_connections(row, col - 1, n, self.matrix)
                up = get_piece_connections(row - 1, col, n, self.matrix)
                right = 0
                down = 0
        return (left, up, right, down)


    @staticmethod
    def parse_instance():
        n = 0
        matrix = []

        while True:
            line = stdin.readline().split()
            if not line:
                break
            n += 1
            matrix.append([Piece(value) for value in line])

        result = preprocessing(n, matrix)
        return Board(n, matrix, result[0], result[1])





class PipeManiaState:
    state_id = 0

    def __init__(self, board, row=0, col=0):
        self.board = board
        self.current_row = row
        self.current_col = col
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id





class PipeMania(Problem):
    def __init__(self, board: Board):
        self.initial = PipeManiaState(board)
        self.goal = None

    def actions(self, state: PipeManiaState):
        n = state.board.n
        row = state.current_row
        col = state.current_col
        actions = [] # e.g. [(row, col, PIECE_FD, next_row, next_col), (row, col, PIECE_VB, next_row, next_col), ...]

        piece = state.board.matrix[row][col]

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

        piece_type = piece.value[0]

        if row == 0:
            if col == 0:
                # this piece must necessarily be an F
                actions.append((row, col, PIECE_FB, row, col + 1))
                actions.append((row, col, PIECE_FD, row, col + 1))
            elif col != 0 and col != n - 1:
                if piece_type == PIECE_TYPE_F:
                    actions.append((row, col, PIECE_FE, row, col + 1))
                    actions.append((row, col, PIECE_FB, row, col + 1))
                    actions.append((row, col, PIECE_FD, row, col + 1))
                elif piece_type == PIECE_TYPE_V:
                    actions.append((row, col, PIECE_VB, row, col + 1))
                    actions.append((row, col, PIECE_VE, row, col + 1))
            elif col == n - 1:
                # this piece must necessarily be an F
                actions.append((row, col, PIECE_FB, row + 1, 0))
                actions.append((row, col, PIECE_FE, row + 1, 0))

        elif row != 0 and row != n - 1:
            if col == 0:
                if piece_type == PIECE_TYPE_F:
                    actions.append((row, col, PIECE_FC, row, col + 1))
                    actions.append((row, col, PIECE_FD, row, col + 1))
                    actions.append((row, col, PIECE_FB, row, col + 1))
                elif piece_type == PIECE_TYPE_V:
                    actions.append((row, col, PIECE_VB, row, col + 1))
                    actions.append((row, col, PIECE_VD, row, col + 1))
            elif col != 0 and col != n - 1:
                # TODO - optimize
                if piece_type == PIECE_TYPE_F:
                    if state.board.matrix[row - 1][col].isFixed and state.board.matrix[row - 1][col].value in hasDownConnections and state.board.matrix[row - 1][col].value != PIECE_FB:
                        actions.append((row, col, PIECE_FC, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row + 1][col].isFixed and state.board.matrix[row + 1][col].value in hasUpConnections and state.board.matrix[row + 1][col].value != PIECE_FC:
                        actions.append((row, col, PIECE_FB, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row][col - 1].isFixed and state.board.matrix[row][col - 1].value in hasRightConnections and state.board.matrix[row][col - 1].value != PIECE_FD:
                        actions.append((row, col, PIECE_FE, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row][col + 1].isFixed and state.board.matrix[row][col + 1].value in hasLeftConnections and state.board.matrix[row][col + 1].value != PIECE_FE:
                        actions.append((row, col, PIECE_FD, row, col + 1))
                        piece.isFixed = True
                    else:
                        actions.append((row, col, PIECE_FE, row, col + 1))
                        actions.append((row, col, PIECE_FC, row, col + 1))
                        actions.append((row, col, PIECE_FD, row, col + 1))
                        actions.append((row, col, PIECE_FB, row, col + 1))
                elif piece_type == PIECE_TYPE_V:
                    actions.append((row, col, PIECE_VE, row, col + 1))
                    actions.append((row, col, PIECE_VC, row, col + 1))
                    actions.append((row, col, PIECE_VD, row, col + 1))
                    actions.append((row, col, PIECE_VB, row, col + 1))
                elif piece_type == PIECE_TYPE_B:
                    if state.board.matrix[row - 1][col].isFixed and state.board.matrix[row - 1][col].value == PIECE_FC:
                        actions.append((row, col, PIECE_BB, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row + 1][col].isFixed and state.board.matrix[row + 1][col].value == PIECE_FB:
                        actions.append((row, col, PIECE_BC, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row][col - 1].isFixed and state.board.matrix[row][col - 1].value == PIECE_FE:
                        actions.append((row, col, PIECE_BD, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row][col + 1].isFixed and state.board.matrix[row][col + 1].value == PIECE_FD:
                        actions.append((row, col, PIECE_BE, row, col + 1))
                        piece.isFixed = True
                    else:
                        actions.append((row, col, PIECE_BE, row, col + 1))
                        actions.append((row, col, PIECE_BC, row, col + 1))
                        actions.append((row, col, PIECE_BD, row, col + 1))
                        actions.append((row, col, PIECE_BB, row, col + 1))
                else:
                    if state.board.matrix[row - 1][col].isFixed and state.board.matrix[row - 1][col].value in hasDownConnections:
                        actions.append((row, col, PIECE_LV, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row + 1][col].isFixed and state.board.matrix[row + 1][col].value in hasUpConnections:
                        actions.append((row, col, PIECE_LV, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row][col - 1].isFixed and state.board.matrix[row][col - 1].value in hasRightConnections:
                        actions.append((row, col, PIECE_LH, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row][col + 1].isFixed and state.board.matrix[row][col + 1].value in hasLeftConnections:
                        actions.append((row, col, PIECE_LH, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row - 1][col].isFixed and state.board.matrix[row - 1][col].value[0] == PIECE_TYPE_F and (state.board.matrix[row - 1][col].value == PIECE_FE or state.board.matrix[row - 1][col].value == PIECE_FD):
                        actions.append((row, col, PIECE_LH, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row + 1][col].isFixed and state.board.matrix[row + 1][col].value[0] == PIECE_TYPE_F and (state.board.matrix[row + 1][col].value == PIECE_FE or state.board.matrix[row + 1][col].value == PIECE_FC):
                        actions.append((row, col, PIECE_LH, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row][col - 1].isFixed and state.board.matrix[row][col - 1].value[0] == PIECE_TYPE_F and (state.board.matrix[row][col - 1].value == PIECE_FC or state.board.matrix[row][col - 1].value == PIECE_FB):
                        actions.append((row, col, PIECE_LV, row, col + 1))
                        piece.isFixed = True
                    elif state.board.matrix[row][col + 1].isFixed and state.board.matrix[row][col + 1].value[0] == PIECE_TYPE_F and (state.board.matrix[row][col + 1].value == PIECE_FC or state.board.matrix[row][col + 1].value == PIECE_FB):
                        actions.append((row, col, PIECE_LV, row, col + 1))
                        piece.isFixed = True
                    else:
                        actions.append((row, col, PIECE_LH, row, col + 1))
                        actions.append((row, col, PIECE_LV, row, col + 1))
            elif col == n - 1:
                if piece_type == PIECE_TYPE_F:
                    actions.append((row, col, PIECE_FC, row + 1, 0))
                    actions.append((row, col, PIECE_FE, row + 1, 0))
                    actions.append((row, col, PIECE_FB, row + 1, 0))
                elif piece_type == PIECE_TYPE_V:
                    actions.append((row, col, PIECE_VC, row + 1, 0))
                    actions.append((row, col, PIECE_VE, row + 1, 0))

        elif row == n - 1:
            if col == 0:
                # this piece must necessarily be an F
                actions.append((row, col, PIECE_FD, row, col + 1))
                actions.append((row, col, PIECE_FC, row, col + 1))
            elif col != 0 and col != n - 1:
                if piece_type == PIECE_TYPE_F:
                    actions.append((row, col, PIECE_FE, row, col + 1))
                    actions.append((row, col, PIECE_FC, row, col + 1))
                    actions.append((row, col, PIECE_FD, row, col + 1))
                elif piece_type == PIECE_TYPE_V:
                    actions.append((row, col, PIECE_VD, row, col + 1))
                    actions.append((row, col, PIECE_VC, row, col + 1))
            elif col == n - 1:
                # this piece must necessarily be an F
                actions.append((row, col, PIECE_FD, None, None))
                actions.append((row, col, PIECE_FE, None, None))
        return actions


    def result(self, state: PipeManiaState, action):
        new_board = deepcopy(state.board)
        new_board.execute_action(action[0], action[1], action[2])
        return PipeManiaState(new_board, action[3], action[4])

    def goal_test(self, state: PipeManiaState):
        return state.board.connections == state.board.total_connections

    def h(self, node: Node):
        return node.state.board.total_connections - node.state.board.connections




if __name__ == "__main__":
    board = Board.parse_instance()
    problem = PipeMania(board)
    #node = breadth_first_tree_search(problem)
    node = greedy_search(problem, problem.h)
    print(node.state.board, end='')