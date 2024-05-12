import numpy as np
import sys
from copy import deepcopy
from search import (
    Problem,
    Node,
    breadth_first_tree_search,
    greedy_search,
)

FC = np.uint8(0)
FB = np.uint8(1)
FE = np.uint8(2)
FD = np.uint8(3)

BC = np.uint8(4)
BB = np.uint8(5)
BE = np.uint8(6)
BD = np.uint8(7)

VC = np.uint8(8)
VB = np.uint8(9)
VE = np.uint8(10)
VD = np.uint8(11)

LH = np.uint8(12)
LV = np.uint8(13)

TYPE_F = np.uint8(14)
TYPE_B = np.uint8(15)
TYPE_V = np.uint8(16)
TYPE_L = np.uint8(17)

DIR_LEFT = 0b1000
DIR_UP = 0b0100
DIR_RIGHT = 0b0010
DIR_DOWN = 0b0001



# all pieces that have left connections
hasLeftConnections = np.array([FE, BC, BB, BE, VC, VE, LH], dtype=np.uint8)

# all pieces that have up connections
hasUpConnections = np.array([FC, BC, BE, BD, VC, VD, LV], dtype=np.uint8)

# all pieces that have right connections
hasRightConnections = np.array([FD, BC, BB, BD, VB, VD, LH], dtype=np.uint8)

# all pieces that have down connections
hasDownConnections = np.array([FB, BB, BE, BD, VB, VE, LV], dtype=np.uint8)


total_connections = 0



def preprocessing(n, matrix):
    global total_connections
    connections = 0
    
    # fix all the pieces on the edges of the board that are neccesarily fixed and their neighbors
    for row in range(n):
        for col in range(n):
            piece = matrix[row, col]
            piece_type = piece.get_type()

            if piece_type == TYPE_F:
                total_connections += 1
            elif piece_type == TYPE_B:
                total_connections += 3
            elif piece_type == TYPE_V:
                total_connections += 2
            else:
                total_connections += 2
            

            if row == 0:
                if col == 0:
                    if piece_type == TYPE_V:
                        piece.value = VB
                        piece.isFixed = True

                        right = matrix[row, col + 1]
                        down = matrix[row + 1, col]
                    
                        if right.get_type() == TYPE_F:
                            right.value = FE
                            right.isFixed = True
                        elif right.get_type() == TYPE_V:
                            right.value = VE
                            right.isFixed = True
                        if down.get_type() == TYPE_F:
                            down.value = FC
                            down.isFixed = True
                        elif down.get_type() == TYPE_V:
                            down.value = VD
                            down.isFixed = True
                    elif not piece.isFixed:
                        piece.value = FB
                        piece.add_action(DIR_DOWN | DIR_RIGHT)
                elif col == n - 1:
                    if piece_type == TYPE_V:
                        piece.value = VE
                        piece.isFixed = True

                        left = matrix[row, col - 1]
                        down = matrix[row + 1, col]

                        if left.get_type() == TYPE_F:
                            left.value = FD
                            left.isFixed = True
                        elif left.get_type() == TYPE_V:
                            left.value = VB
                            left.isFixed = True
                        if down.get_type() == TYPE_F:
                            down.value = FC
                            down.isFixed = True
                        elif down.get_type() == TYPE_V:
                            down.value = VC
                            down.isFixed = True
                    elif not piece.isFixed:
                        piece.value = FB
                        piece.add_action(DIR_DOWN | DIR_LEFT)
                else:
                    if piece_type == TYPE_B or piece_type == TYPE_L:
                        if piece_type == TYPE_B:
                            piece.value = BB
                        else:
                            piece.value = LH
                        piece.isFixed = True

                        left = matrix[row, col - 1]
                        right = matrix[row, col + 1]
                        down = matrix[row + 1, col]

                        if left.get_type() == TYPE_F:
                            left.value = FD
                            left.isFixed = True
                        elif left.get_type() == TYPE_V:
                            left.value = VB
                            left.isFixed = True
                        if right.get_type() == TYPE_F:
                            right.value = FE
                            right.isFixed = True
                        elif right.get_type() == TYPE_V:
                            right.value = VE
                            right.isFixed = True
                        if piece_type == TYPE_B and (down.get_type() == TYPE_F or down.get_type() == TYPE_L):
                            if down.get_type() == TYPE_F:
                                down.value = FC
                            else:
                                down.value = LV
                            down.isFixed = True
                        elif piece_type == TYPE_L and (down.get_type() == TYPE_B or down.get_type() == TYPE_L):
                            if down.get_type() == TYPE_B:
                                down.value = BB
                            else:
                                down.value = LH
                            down.isFixed = True
                    elif not piece.isFixed:
                        if piece_type == TYPE_F:
                            piece.value = FB
                            piece.add_action(DIR_LEFT | DIR_DOWN | DIR_RIGHT)
                        else:
                            piece.value = VB
                            piece.add_action(DIR_LEFT | DIR_DOWN)

            elif row == n - 1:
                if col == 0:
                    if piece_type == TYPE_V:
                        piece.value = VD
                        piece.isFixed = True

                        right = matrix[row, col + 1]
                        up = matrix[row - 1, col]

                        if right.get_type() == TYPE_F:
                            right.value = FE
                            right.isFixed = True
                        elif right.get_type() == TYPE_V:
                            right.value = VC
                            right.isFixed = True
                        if up.get_type() == TYPE_F:
                            up.value = FB
                            up.isFixed = True
                        elif up.get_type() == TYPE_V:
                            up.value = VB
                            up.isFixed = True
                    elif not piece.isFixed:
                        piece.value = FC
                        piece.add_action(DIR_UP | DIR_RIGHT)
                elif col == n - 1:
                    if piece_type == TYPE_V:
                        piece.value = VC
                        piece.isFixed = True

                        left = matrix[row, col - 1]
                        up = matrix[row - 1, col]

                        if left.get_type() == TYPE_F:
                            left.value = FD
                            left.isFixed = True
                        elif left.get_type() == TYPE_V:
                            left.value = VD
                            left.isFixed = True
                        if up.get_type() == TYPE_F:
                            up.value = FB
                            up.isFixed = True
                        elif up.get_type() == TYPE_V:
                            up.value = VE
                            up.isFixed = True
                    elif not piece.isFixed:
                        piece.value = FC
                        piece.add_action(DIR_UP | DIR_LEFT)
                else:
                    if piece_type == TYPE_B or piece_type == TYPE_L:
                        if piece_type == TYPE_B:
                            piece.value = BC
                        else:
                            piece.value = LH
                        piece.isFixed = True

                        left = matrix[row, col - 1]
                        right = matrix[row, col + 1]
                        up = matrix[row - 1, col]

                        if left.get_type() == TYPE_F:
                            left.value = FD
                            left.isFixed = True
                        elif left.get_type() == TYPE_V:
                            left.value = VD
                            left.isFixed = True
                        if right.get_type() == TYPE_F:
                            right.value = FE
                            right.isFixed = True
                        elif right.get_type() == TYPE_V:
                            right.value = VC
                            right.isFixed = True
                        if piece_type == TYPE_B and (up.get_type() == TYPE_F or up.get_type() == TYPE_L):
                            if up.get_type() == TYPE_F:
                                up.value = FB
                            else:
                                up.value = LV
                            up.isFixed = True
                        elif piece_type == TYPE_L and (up.get_type() == TYPE_B or up.get_type() == TYPE_L):
                            if up.get_type() == TYPE_B:
                                up.value = BC
                            else:
                                up.value = LH
                            up.isFixed = True
                    elif not piece.isFixed:
                        if piece_type == TYPE_F:
                            piece.value = FC
                            piece.add_action(DIR_LEFT | DIR_UP | DIR_RIGHT)
                        else:
                            piece.value = VD
                            piece.add_action(DIR_UP | DIR_RIGHT)

            else:
                if col == 0:
                    if piece_type == TYPE_B or piece_type == TYPE_L:
                        if piece_type == TYPE_B:
                            piece.value = BD
                        else:
                            piece.value = LV
                        piece.isFixed = True

                        up = matrix[row - 1, col]
                        down = matrix[row + 1, col]
                        right = matrix[row, col + 1]

                        if up.get_type() == TYPE_F:
                            up.value = FB
                            up.isFixed = True
                        elif up.get_type() == TYPE_V:
                            up.value = VB
                            up.isFixed = True
                        if down.get_type() == TYPE_F:
                            down.value = FC
                            down.isFixed = True
                        elif down.get_type() == TYPE_V:
                            down.value = VD
                            down.isFixed = True
                        if piece_type == TYPE_B and (right.get_type() == TYPE_F or right.get_type() == TYPE_L):
                            if right.get_type() == TYPE_F:
                                right.value = FE
                            else:
                                right.value = LH
                            right.isFixed = True
                        elif piece_type == TYPE_L and (right.get_type() == TYPE_B or right.get_type() == TYPE_L):
                            if right.get_type() == TYPE_B:
                                right.value = BD
                            else:
                                right.value = LV
                            right.isFixed = True
                    elif not piece.isFixed:
                        if piece_type == TYPE_F:
                            piece.value = FD
                            piece.add_action(DIR_UP | DIR_DOWN | DIR_RIGHT)
                        else:
                            piece.value = VB
                            piece.add_action(DIR_DOWN | DIR_RIGHT)
                elif col == n - 1:
                    if piece_type == TYPE_B or piece_type == TYPE_L:
                        if piece_type == TYPE_B:
                            piece.value = BE
                        else:
                            piece.value = LV
                        piece.isFixed = True

                        up = matrix[row - 1, col]
                        down = matrix[row + 1, col]
                        left = matrix[row, col - 1]

                        if up.get_type() == TYPE_F:
                            up.value = FB
                            up.isFixed = True
                        elif up.get_type() == TYPE_V:
                            up.value = VE
                            up.isFixed = True
                        if down.get_type() == TYPE_F:
                            down.value = FC
                            down.isFixed = True
                        elif down.get_type() == TYPE_V:
                            down.value = VC
                            down.isFixed = True
                        if piece_type == TYPE_B and (left.get_type() == TYPE_F or left.get_type() == TYPE_L):
                            if left.get_type() == TYPE_F:
                                left.value = FD
                            else:
                                left.value = LH
                            left.isFixed = True
                        elif piece_type == TYPE_L and (left.get_type() == TYPE_B or left.get_type() == TYPE_L):
                            if left.get_type() == TYPE_B:
                                left.value = BE
                            else:
                                left.value = LV
                            left.isFixed = True
                    elif not piece.isFixed:
                        if piece_type == TYPE_F:
                            piece.value = FE
                            piece.add_action(DIR_UP | DIR_DOWN | DIR_LEFT)
                        else:
                            piece.value = VE
                            piece.add_action(DIR_LEFT | DIR_UP)
                else:
                    if not piece.isFixed:
                        left = matrix[row, col - 1]
                        up = matrix[row - 1, col]
                        right = matrix[row, col + 1]
                        down = matrix[row + 1, col]

                        if up.isFixed and up.get_type() == TYPE_F and (piece_type == TYPE_B or piece_type == TYPE_L):
                            if piece_type == TYPE_B:
                                piece.value = BB
                            else:
                                piece.value = LH
                            piece.isFixed = True
                        elif up.isFixed and up.get_type() == TYPE_V and (piece_type == TYPE_F or piece_type == TYPE_L):
                            if piece_type == TYPE_F:
                                piece.value = FC
                            else:
                                piece.value = LV
                            piece.isFixed = True
                        elif left.isFixed and left.get_type() == TYPE_F and (piece_type == TYPE_B or piece_type == TYPE_L):
                            if piece_type == TYPE_B:
                                piece.value = BD
                            else:
                                piece.value = LV
                            piece.isFixed = True
                        elif left.isFixed and left.get_type() == TYPE_V and (piece_type == TYPE_F or piece_type == TYPE_L):
                            if piece_type == TYPE_F:
                                piece.value = FE
                            else:
                                piece.value = LH
                            piece.isFixed = True
                        elif down.isFixed and down.get_type() == TYPE_F and (piece_type == TYPE_B or piece_type == TYPE_L):
                            if piece_type == TYPE_B:
                                piece.value = BC
                            else:
                                piece.value = LH
                            piece.isFixed = True
                        elif down.isFixed and down.get_type() == TYPE_V and (piece_type == TYPE_F or piece_type == TYPE_L):
                            if piece_type == TYPE_F:
                                piece.value = FB
                            else:
                                piece.value = LV
                            piece.isFixed = True
                        elif right.isFixed and right.get_type() == TYPE_F and (piece_type == TYPE_B or piece_type == TYPE_L):
                            if piece_type == TYPE_B:
                                piece.value = BE
                            else:
                                piece.value = LV
                            piece.isFixed = True
                        elif right.isFixed and right.get_type() == TYPE_V and (piece_type == TYPE_F or piece_type == TYPE_L):
                            if piece_type == TYPE_F:
                                piece.value = FD
                            else:
                                piece.value = LH
                            piece.isFixed = True

    # fix all possible pieces taking advantage of all that we know are fixed now: O(n^2)

    while True:
        done = True

        for row in range(n):
            for col in range(n):
                piece = matrix[row, col]
                
                if piece.isFixed:
                    continue
                
                piece_type = piece.get_type()

                if row == 0:        # ROW 0
                    if col == 0:            # COL 0
                        right = matrix[row, col + 1]
                        down = matrix[row + 1, col]

                        if right.isFixed or down.isFixed:
                            
                            if right.isFixed and right.value in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FD
                                    piece.isFixed = True
                                    done = False
                            elif right.isFixed and right.value not in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FB
                                    piece.isFixed = True
                                    done = False
                            
                            if down.isFixed and down.value in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FB
                                    piece.isFixed = True
                                    done = False
                            elif down.isFixed and down.value not in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FD
                                    piece.isFixed = True
                                    done = False

                    elif col == n - 1:      # COL n - 1
                        left = matrix[row, col - 1]
                        down = matrix[row + 1, col]

                        if left.isFixed or down.isFixed:
                                
                                if left.isFixed and left.value in hasRightConnections:
                                    if piece_type == TYPE_F:
                                        piece.value = FE
                                        piece.isFixed = True
                                        done = False
                                elif left.isFixed and left.value not in hasRightConnections:
                                    if piece_type == TYPE_F:
                                        piece.value = FB
                                        piece.isFixed = True
                                        done = False

                                if down.isFixed and down.value in hasUpConnections:
                                    if piece_type == TYPE_F:
                                        piece.value = FB
                                        piece.isFixed = True
                                        done = False
                                elif down.isFixed and down.value not in hasUpConnections:
                                    if piece_type == TYPE_F:
                                        piece.value = FE
                                        piece.isFixed = True
                                        done = False

                    else:                   # COL in between
                        left = matrix[row, col - 1]
                        right = matrix[row, col + 1]
                        down = matrix[row + 1, col]

                        if left.isFixed or right.isFixed or down.isFixed:
                            
                            if left.isFixed and left.value in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FE
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.value = VE
                                    piece.isFixed = True
                                    done = False
                            elif left.isFixed and left.value not in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_LEFT | DIR_UP)
                                elif piece_type == TYPE_V:
                                    piece.value = VB
                                    piece.isFixed = True
                                    done = False

                            if right.isFixed and right.value in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FD
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.value = VB
                                    piece.isFixed = True
                                    done = False
                            elif right.isFixed and right.value not in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_RIGHT | DIR_UP)
                                elif piece_type == TYPE_V:
                                    piece.value = VE
                                    piece.isFixed = True
                                    done = False

                            if down.isFixed and down.value in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FB
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_RIGHT | DIR_UP)
                            elif down.isFixed and down.value not in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_DOWN | DIR_UP)
                                elif piece_type == TYPE_V: # impossible contidion
                                    pass                        


                elif row == n - 1:     # ROW n - 1
                    if col == 0:                # COL 0
                        right = matrix[row, col + 1]
                        up = matrix[row - 1, col]

                        if right.isFixed or up.isFixed:

                            if right.isFixed and right.value in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FD
                                    piece.isFixed = True
                                    done = False
                            elif right.isFixed and right.value not in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FC
                                    piece.isFixed = True
                                    done = False
                            
                            if up.isFixed and up.value in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FC
                                    piece.isFixed = True
                                    done = False
                            elif up.isFixed and up.value not in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FD
                                    piece.isFixed = True
                                    done = False

                    elif col == n - 1:          # COL n - 1
                        left = matrix[row, col - 1]
                        up = matrix[row - 1, col]

                        if left.isFixed or up.isFixed:

                            if left.isFixed and left.value in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FE
                                    piece.isFixed = True
                                    done = False
                            elif left.isFixed and left.value not in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FC
                                    piece.isFixed = True
                                    done = False
                            
                            if up.isFixed and up.value in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FC
                                    piece.isFixed = True
                                    done = False
                            elif up.isFixed and up.value not in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FE
                                    piece.isFixed = True
                                    done = False

                    else:                       # COL in between
                        left = matrix[row, col - 1]
                        up = matrix[row - 1, col]
                        right = matrix[row, col + 1]

                        if left.isFixed or up.isFixed or right.isFixed:
                            
                            if left.isFixed and left.value in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FE
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.value = VC
                                    piece.isFixed = True
                                    done = False
                            elif left.isFixed and left.value not in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_LEFT | DIR_DOWN)
                                elif piece_type == TYPE_V:
                                    piece.value = VD
                                    piece.isFixed = True
                                    done = False
                            
                            if up.isFixed and up.value in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FC
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_LEFT | DIR_DOWN)
                            elif up.isFixed and up.value not in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_UP | DIR_DOWN)
                                elif piece_type == TYPE_V: # impossible contidion
                                    piece.remove_action(DIR_UP | DIR_RIGHT)
                            
                            if right.isFixed and right.value in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FD
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.value = VD
                                    piece.isFixed = True
                                    done = False
                            elif right.isFixed and right.value not in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_RIGHT | DIR_DOWN)
                                elif piece_type == TYPE_V:
                                    piece.value = VC
                                    piece.isFixed = True
                                    done = False

                else:                   # ROW in between
                    if col == 0:                # COL 0
                        up = matrix[row - 1, col]
                        right = matrix[row, col + 1]
                        down = matrix[row + 1, col]

                        if up.isFixed or right.isFixed or down.isFixed:
                            
                            if up.isFixed and up.value in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FC
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.value = VD
                                    piece.isFixed = True
                                    done = False
                            elif up.isFixed and up.value not in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_UP | DIR_LEFT)
                                elif piece_type == TYPE_V:
                                    piece.value = VB
                                    piece.isFixed = True
                                    done = False
                            
                            if right.isFixed and right.value in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FD
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_UP | DIR_LEFT)
                            elif right.isFixed and right.value not in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_RIGHT | DIR_LEFT)
                                elif piece_type == TYPE_V: # impossible contidion
                                    pass
                            
                            if down.isFixed and down.value in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FB
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.value = VB
                                    piece.isFixed = True
                                    done = False
                            elif down.isFixed and down.value not in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_DOWN | DIR_LEFT)
                                elif piece_type == TYPE_V:
                                    piece.value = VD
                                    piece.isFixed = True
                                    done = False


                    elif col == n - 1:          # COL n - 1
                        left = matrix[row, col - 1]
                        up = matrix[row - 1, col]
                        down = matrix[row + 1, col]

                        if left.isFixed or up.isFixed or down.isFixed:
                            
                            if left.isFixed and left.value in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FE
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_DOWN | DIR_RIGHT)
                            elif left.isFixed and left.value not in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_LEFT | DIR_RIGHT)
                                elif piece_type == TYPE_V: # impossible contidion
                                    pass
                            
                            if up.isFixed and up.value in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FC
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.value = VC
                                    piece.isFixed = True
                                    done = False
                            elif up.isFixed and up.value not in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_UP | DIR_RIGHT)
                                elif piece_type == TYPE_V:
                                    piece.value = VE
                                    piece.isFixed = True
                                    done = False
                            
                            if down.isFixed and down.value in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FB
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.value = VE
                                    piece.isFixed = True
                                    done = False
                            elif down.isFixed and down.value not in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_DOWN | DIR_RIGHT)
                                elif piece_type == TYPE_V:
                                    piece.value = VC
                                    piece.isFixed = True
                                    done = False
                        
                    else:                       # COL in between
                        left = matrix[row, col - 1]
                        up = matrix[row - 1, col]
                        right = matrix[row, col + 1]
                        down = matrix[row + 1, col]

                        if left.isFixed or up.isFixed or right.isFixed or down.isFixed:

                            if left.isFixed and left.value in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FE
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_B:
                                    piece.remove_action(DIR_RIGHT)
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_DOWN | DIR_RIGHT)
                                elif piece_type == TYPE_L:
                                    piece.value = LH
                                    piece.isFixed = True
                                    done = False
                            elif left.isFixed and left.value not in hasRightConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_LEFT)
                                elif piece_type == TYPE_B:
                                    piece.value = BD
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_LEFT | DIR_UP)
                                elif piece_type == TYPE_L:
                                    piece.value = LV
                                    piece.isFixed = True
                                    done = False

                            if up.isFixed and up.value in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FC
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_B:
                                    piece.remove_action(DIR_DOWN)
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_LEFT | DIR_DOWN)
                                elif piece_type == TYPE_L:
                                    piece.value = LV
                                    piece.isFixed = True
                                    done = False
                            elif up.isFixed and up.value not in hasDownConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_UP)
                                elif piece_type == TYPE_B:
                                    piece.value = BB
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_UP | DIR_RIGHT)
                                elif piece_type == TYPE_L:
                                    piece.value = LH
                                    piece.isFixed = True
                                    done = False
                            
                            if right.isFixed and right.value in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FD
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_B:
                                    piece.remove_action(DIR_LEFT)
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_UP | DIR_LEFT)
                                elif piece_type == TYPE_L:
                                    piece.value = LH
                                    piece.isFixed = True
                                    done = False
                            elif right.isFixed and right.value not in hasLeftConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_RIGHT)
                                elif piece_type == TYPE_B:
                                    piece.value = BE
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_RIGHT | DIR_DOWN)
                                elif piece_type == TYPE_L:
                                    piece.value = LV
                                    piece.isFixed = True
                                    done = False
                            
                            if down.isFixed and down.value in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.value = FB
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_B:
                                    piece.remove_action(DIR_UP)
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_RIGHT | DIR_UP)
                                elif piece_type == TYPE_L:
                                    piece.value = LV
                                    piece.isFixed = True
                                    done = False
                            elif down.isFixed and down.value not in hasUpConnections:
                                if piece_type == TYPE_F:
                                    piece.remove_action(DIR_DOWN)
                                elif piece_type == TYPE_B:
                                    piece.value = BC
                                    piece.isFixed = True
                                    done = False
                                elif piece_type == TYPE_V:
                                    piece.remove_action(DIR_DOWN | DIR_LEFT)
                                elif piece_type == TYPE_L:
                                    piece.value = LH
                                    piece.isFixed = True
                                    done = False

                if piece.actions == DIR_LEFT:
                    if piece_type == TYPE_F:
                        piece.value = FE
                        piece.isFixed = True
                        done = False
                    elif piece_type == TYPE_B:
                        piece.value = BE
                        piece.isFixed = True
                        done = False
                    elif piece_type == TYPE_V:
                        piece.value = VE
                        piece.isFixed = True
                        done = False
                    else:
                        if piece.value == LH:
                            piece.value = LV
                        else:
                            piece.value = LH
                        piece.isFixed = True
                        done = False

                elif piece.actions == DIR_UP:
                    if piece_type == TYPE_F:
                        piece.value = FC
                        piece.isFixed = True
                        done = False
                    elif piece_type == TYPE_B:
                        piece.value = BC
                        piece.isFixed = True
                        done = False
                    elif piece_type == TYPE_V:
                        piece.value = VC
                        piece.isFixed = True
                        done = False
                    else:
                        if piece.value == LH:
                            piece.value = LV
                        else:
                            piece.value = LH
                        piece.isFixed = True
                        done = False
                
                elif piece.actions == DIR_RIGHT:
                    if piece_type == TYPE_F:
                        piece.value = FD
                        piece.isFixed = True
                        done = False
                    elif piece_type == TYPE_B:
                        piece.value = BD
                        piece.isFixed = True
                        done = False
                    elif piece_type == TYPE_V:
                        piece.value = VD
                        piece.isFixed = True
                        done = False
                    else:
                        if piece.value == LH:
                            piece.value = LV
                        else:
                            piece.value = LH
                        piece.isFixed = True
                        done = False
                
                elif piece.actions == DIR_DOWN:
                    if piece_type == TYPE_F:
                        piece.value = FB
                        piece.isFixed = True
                        done = False
                    elif piece_type == TYPE_B:
                        piece.value = BB
                        piece.isFixed = True
                        done = False
                    elif piece_type == TYPE_V:
                        piece.value = VB
                        piece.isFixed = True
                        done = False
                    else:
                        if piece.value == LH:
                            piece.value = LV
                        else:
                            piece.value = LH
                        piece.isFixed = True
                        done = False

        if done:
            break
    
    for row in range(n):
        for col in range(n):
            connections += get_piece_connections(row, col, n, matrix)
    
    return connections






def get_piece_connections(row, col, n, matrix):
    piece = matrix[row, col]
    c = 0

    if piece.value in hasLeftConnections and col > 0 and matrix[row, col - 1].value in hasRightConnections:
        c += 1
    if piece.value in hasUpConnections and row > 0 and matrix[row - 1, col].value in hasDownConnections:
        c += 1
    if piece.value in hasRightConnections and col < n - 1 and matrix[row, col + 1].value in hasLeftConnections:
        c += 1
    if piece.value in hasDownConnections and row < n - 1 and matrix[row + 1, col].value in hasUpConnections:
        c += 1
    
    return c






class Piece:
    def __init__(self, value):
        self.value = value
        self.isFixed = False
        self.actions = 0b1111

    def get_value(self):
        if self.value == FC:
            return "FC"
        elif self.value == FB:
            return "FB"
        elif self.value == FE:
            return "FE"
        elif self.value == FD:
            return "FD"
        elif self.value == BC:
            return "BC"
        elif self.value == BB:
            return "BB"
        elif self.value == BE:
            return "BE"
        elif self.value == BD:
            return "BD"
        elif self.value == VC:
            return "VC"
        elif self.value == VB:
            return "VB"
        elif self.value == VE:
            return "VE"
        elif self.value == VD:
            return "VD"
        elif self.value == LH:
            return "LH"
        else:
            return "LV"

    def get_type(self):
        if self.value < BC:
            return TYPE_F
        elif self.value < VC:
            return TYPE_B
        elif self.value < LH:
            return TYPE_V
        else:
            return TYPE_L
    
    def add_action(self, action):
        self.actions |= action
    
    def remove_action(self, action):
        self.actions &= ~action
    





class Board:
    def __init__(self, n, matrix, connections):
        self.n = n
        self.matrix = matrix
        self.connections = connections
    
    def __repr__(self):
        s = ""
        for row in range(self.n):
            for col in range(self.n):
                if col == self.n - 1:
                    s += self.matrix[row, col].get_value() + "\n"
                else:
                    s += self.matrix[row, col].get_value() + "\t"
        return s

    def execute_action(self, row, col, direction):
        piece = self.matrix[row, col]
        piece_type = piece.get_type()

        current_piece_connections = get_piece_connections(row, col, self.n, self.matrix)
        current_left, current_up, current_right, current_down = self.get_side_connections(row, col)


        if direction == DIR_LEFT:
            if piece_type == TYPE_F:
                piece.value = FE
            elif piece_type == TYPE_B:
                piece.value = BE
            elif piece_type == TYPE_V:
                piece.value = VE
            else:
                if piece.value == LH:
                    piece.value = LV
                else:
                    piece.value = LH
        elif direction == DIR_UP:
            if piece_type == TYPE_F:
                piece.value = FC
            elif piece_type == TYPE_B:
                piece.value = BC
            elif piece_type == TYPE_V:
                piece.value = VC
            else:
                if piece.value == LH:
                    piece.value = LV
                else:
                    piece.value = LH
        elif direction == DIR_RIGHT:
            if piece_type == TYPE_F:
                piece.value = FD
            elif piece_type == TYPE_B:
                piece.value = BD
            elif piece_type == TYPE_V:
                piece.value = VD
            else:
                if piece.value == LH:
                    piece.value = LV
                else:
                    piece.value = LH
        else:
            if piece_type == TYPE_F:
                piece.value = FB
            elif piece_type == TYPE_B:
                piece.value = BB
            elif piece_type == TYPE_V:
                piece.value = VB
            else:
                if piece.value == LH:
                    piece.value = LV
                else:
                    piece.value = LH


        new_piece_connections = get_piece_connections(row, col, self.n, self.matrix)
        new_left, new_up, new_right, new_down = self.get_side_connections(row, col)

        c = self.connections - (current_piece_connections + current_left + current_up + current_right + current_down) + (new_piece_connections + new_left + new_up + new_right + new_down)
        self.connections = c

    def get_side_connections(self, row, col):
        n = self.n

        if col == 0:
            left = 0
        else:
            left = get_piece_connections(row, col - 1, n, self.matrix)
        
        if row == 0:
            up = 0
        else:
            up = get_piece_connections(row - 1, col, n, self.matrix)
        
        if col == n - 1:
            right = 0
        else:
            right = get_piece_connections(row, col + 1, n, self.matrix)
        
        if row == n - 1:
            down = 0
        else:
            down = get_piece_connections(row + 1, col, n, self.matrix)
        
        return left, up, right, down

    @staticmethod
    def parse_instance():
        lines = sys.stdin.readlines()
        n = len(lines)
        
        matrix = np.zeros((n, n), dtype=object)

        for row in range(n):
            line = lines[row].split()
            for col in range(n):
                s = line[col]
                if s == "FC":
                    p = FC
                elif s == "FB":
                    p = FB
                elif s == "FE":
                    p = FE
                elif s == "FD":
                    p = FD
                elif s == "BC":
                    p = BC
                elif s == "BB":
                    p = BB
                elif s == "BE":
                    p = BE
                elif s == "BD":
                    p = BD
                elif s == "VC":
                    p = VC
                elif s == "VB":
                    p = VB
                elif s == "VE":
                    p = VE
                elif s == "VD":
                    p = VD
                elif s == "LH":
                    p = LH
                elif s == "LV":
                    p = LV
                else:
                    raise ValueError("Invalid piece")

                matrix[row, col] = Piece(p)
        
        connections = preprocessing(n, matrix)

        return Board(n, matrix, connections)






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

    def actions(self, state: PipeManiaState):
        row = state.current_row
        new_row = row
        col = state.current_col
        new_col = col + 1
        n = state.board.n
        piece = state.board.matrix[row, col]
        actions = []

        if piece.isFixed:
            while True:
                col += 1
                if col == n:
                    col = 0
                    row += 1
                    if row == n:
                        return actions
                if not state.board.matrix[row, col].isFixed:
                    piece = state.board.matrix[row, col]
                    break

        if new_col == n:
            new_col = 0
            new_row = row + 1
            if new_row == n:
                new_row = 0
        
        if piece.actions & DIR_LEFT:
            actions.append((row, col, DIR_LEFT, new_row, new_col))
        if piece.actions & DIR_UP:
            actions.append((row, col, DIR_UP, new_row, new_col))
        if piece.actions & DIR_RIGHT:
            actions.append((row, col, DIR_RIGHT, new_row, new_col))
        if piece.actions & DIR_DOWN:
            actions.append((row, col, DIR_DOWN, new_row, new_col))
        
        return actions

    def result(self, state: PipeManiaState, action):
        b = deepcopy(state.board)
        b.execute_action(action[0], action[1], action[2])
        return PipeManiaState(b, action[3], action[4])

    def goal_test(self, state: PipeManiaState):
        global total_connections
        return state.board.connections == total_connections

    def h(self, node: Node):
        global total_connections
        return total_connections - node.state.board.connections






class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


if __name__ == "__main__":
    board = Board.parse_instance()
    problem = PipeMania(board)
    node = greedy_search(problem, problem.h)
    print(node.state.board, end="")


    """fixed_pieces = 0
    n = board.n
    print()
    for row in range(n):
        for col in range(n):
            if col == n - 1:
                if board.matrix[row, col].isFixed:
                    fixed_pieces += 1
                    print(colors.GREEN + board.matrix[row, col].get_value() + colors.END)
                else:
                    print(colors.RED + bin(board.matrix[row, col].actions) + colors.END)
            else:
                if board.matrix[row, col].isFixed:
                    fixed_pieces += 1
                    print(colors.GREEN + board.matrix[row, col].get_value(), end="\t" + colors.END)
                else:
                    print(colors.RED + bin(board.matrix[row, col].actions), end="\t" + colors.END)
    print("Fixed pieces:", fixed_pieces)
    print("Total connections:", total_connections)
    print("Connections:", board.connections)
    """