import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
    iterative_deepening_search,
    depth_limited_search
)
import numpy as np
import copy

number_of_pieces = 0

O_UP = np.uint8(0)
O_DOWN = np.uint8(1)
O_LEFT = np.uint8(2)
O_RIGHT = np.uint8(3)
O_HORIZONTAL = np.uint8(4)
O_VERTICAL = np.uint8(5)

T_LOCK = np.uint8(6)
T_JUNCTION = np.uint8(7)
T_TURN = np.uint8(8)
T_CONNECTION = np.uint8(9)

D_UP = np.uint8(0)
D_LEFT = np.uint8(1)
D_RIGHT = np.uint8(2)
D_DOWN = np.uint8(3)

direction_operations = {
    D_UP: lambda row, col: (row - 1, col),
    D_DOWN: lambda row, col: (row + 1, col),
    D_LEFT: lambda row, col: (row, col - 1),
    D_RIGHT: lambda row, col: (row, col + 1)
}

def piece_from_str(string):
    orientation = None
    if string[1] == "C":
        orientation = np.uint8(O_UP)
    elif string[1] == "B":
        orientation = np.uint8(O_DOWN)
    elif string[1] == "E":
        orientation = np.uint8(O_LEFT)
    elif string[1] == "D":
        orientation = np.uint8(O_RIGHT)
    elif string[1] == "H":
        orientation = np.uint8(O_HORIZONTAL)
    elif string[1] == "V":
        orientation = np.uint8(O_VERTICAL)

    if string[0] == 'F':
        return np.array([T_LOCK, orientation], dtype=np.uint8)
    elif string[0] == 'B':
        return np.array([T_JUNCTION, orientation], dtype=np.uint8)
    elif string[0] == 'V':
        return np.array([T_TURN, orientation], dtype=np.uint8)
    elif string[0] == 'L':
        return np.array([T_CONNECTION, orientation], dtype=np.uint8)

def str_from_type(piece_type):
    if piece_type == T_LOCK:
        return 'F'
    elif piece_type == T_JUNCTION:
        return 'B'
    elif piece_type == T_TURN:
        return 'V'
    elif piece_type == T_CONNECTION:
        return 'L'

def str_from_orientation(orientation):
    if orientation == O_UP:
        return 'C'
    elif orientation == O_DOWN:
        return 'B'
    elif orientation == O_LEFT:
        return 'E'
    elif orientation == O_RIGHT:
        return 'D'
    elif orientation == O_HORIZONTAL:
        return 'H'
    elif orientation == O_VERTICAL:
        return 'V'


def directions_from_piece(piece_type, piece_orientation):
    if piece_type == T_JUNCTION:
        if piece_orientation == O_UP:
            return np.array([D_UP, D_LEFT, D_RIGHT], dtype=np.uint8)
        elif piece_orientation == O_LEFT:
            return np.array([D_UP, D_LEFT, D_DOWN], dtype=np.uint8)
        elif piece_orientation == O_RIGHT:
            return np.array([D_UP, D_RIGHT, D_DOWN], dtype=np.uint8)
        elif piece_orientation == O_DOWN:
            return np.array([D_LEFT, D_RIGHT, D_DOWN], dtype=np.uint8)
    elif piece_type == T_LOCK:
        if piece_orientation == O_UP:
            return np.array([D_UP], dtype=np.uint8)
        elif piece_orientation == O_LEFT:
            return np.array([D_LEFT], dtype=np.uint8)
        elif piece_orientation == O_RIGHT:
            return np.array([D_RIGHT], dtype=np.uint8)
        elif piece_orientation == O_DOWN:
            return np.array([ D_DOWN], dtype=np.uint8)
    elif piece_type == T_TURN:
        if piece_orientation == O_UP:
            return np.array([D_UP, D_LEFT], dtype=np.uint8)
        elif piece_orientation == O_LEFT:
            return np.array([D_LEFT, D_DOWN], dtype=np.uint8)
        elif piece_orientation == O_RIGHT:
            return np.array([D_UP, D_RIGHT], dtype=np.uint8)
        elif piece_orientation == O_DOWN:
            return np.array([D_RIGHT, D_DOWN], dtype=np.uint8)
    elif piece_type == T_CONNECTION:
        if piece_orientation == O_VERTICAL:
            return np.array([D_UP, D_DOWN], dtype=np.uint8)
        elif piece_orientation == O_HORIZONTAL:
            return np.array([D_LEFT, D_RIGHT], dtype=np.uint8)



def directions_from_bin(bin):
    if bin == 0b0000:
        return np.array([], dtype=np.uint8)
    elif bin == 0b1000:
        return np.array([D_UP], dtype=np.uint8)
    elif bin == 0b0100:
        return np.array([D_LEFT], dtype=np.uint8)
    elif bin == 0b0010:
        return np.array([D_RIGHT], dtype=np.uint8)
    elif bin == 0b0001:
        return np.array([D_DOWN], dtype=np.uint8)
    elif bin == 0b0110:
        return np.array([D_LEFT, D_RIGHT], dtype=np.uint8)
    elif bin == 0b1010:
        return np.array([D_UP, D_RIGHT], dtype=np.uint8)
    elif bin == 0b0011:
        return np.array([D_RIGHT, D_DOWN], dtype=np.uint8)
    elif bin == 0b1100:
        return np.array([D_UP, D_LEFT], dtype=np.uint8)
    elif bin == 0b0101:
        return np.array([D_LEFT, D_DOWN], dtype=np.uint8)
    elif bin == 0b1001:
        return np.array([D_UP, D_DOWN], dtype=np.uint8)
    elif bin == 0b0111:
        return np.array([D_LEFT, D_RIGHT, D_DOWN], dtype=np.uint8)
    elif bin == 0b1011:
        return np.array([D_UP, D_RIGHT, D_DOWN], dtype=np.uint8)
    elif bin == 0b1101:
        return np.array([D_UP, D_LEFT, D_DOWN], dtype=np.uint8)
    elif bin == 0b1110:
        return np.array([D_UP, D_LEFT, D_RIGHT], dtype=np.uint8)

def add_direction(bin, direction):
    if direction == D_UP:
        masc = 0b1000
    elif direction == D_LEFT:
        masc = 0b0100
    elif direction == D_RIGHT:
        masc = 0b0010
    elif direction == D_DOWN:
        masc = 0b0001
    
    return bin ^ masc

def remove_direction(bin, direction):
    if direction == D_UP:
        masc = 0b0111
    elif direction == D_LEFT:
        masc = 0b1011
    elif direction == D_RIGHT:
        masc = 0b1101
    elif direction == D_DOWN:
        masc = 0b1110

    return bin & masc



def inverse_direction(direction):
    if direction == D_UP:
        res = D_DOWN
    elif direction == D_LEFT:
        res = D_RIGHT
    elif direction == D_RIGHT:
        res = D_LEFT
    elif direction == D_DOWN:
        res = D_UP
    
    return res

def max_connections(piecetype):
    if piecetype == T_LOCK:
        return 1
    elif piecetype == T_JUNCTION:
        return 3
    else:
        return 2



def intersect_bin(bin1, bin2):
    return bin1 & bin2



def orientations_from_bin(bin):
    if bin == 0b0000:
        return np.array([], dtype=np.uint8)
    elif bin == 0b1000:
        return np.array([O_UP], dtype=np.uint8)
    elif bin == 0b0100:
        return np.array([O_LEFT], dtype=np.uint8)
    elif bin == 0b0010:
        return np.array([O_RIGHT], dtype=np.uint8)
    elif bin == 0b0001:
        return np.array([O_DOWN], dtype=np.uint8)
    elif bin == 0b0110:
        return np.array([O_LEFT, O_RIGHT], dtype=np.uint8)
    elif bin == 0b1010:
        return np.array([O_UP, O_RIGHT], dtype=np.uint8)
    elif bin == 0b0011:
        return np.array([O_RIGHT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1100:
        return np.array([O_UP, O_LEFT], dtype=np.uint8)
    elif bin == 0b0101:
        return np.array([O_LEFT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1001:
        return np.array([O_UP, O_DOWN], dtype=np.uint8)
    elif bin == 0b0111:
        return np.array([O_LEFT, O_RIGHT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1011:
        return np.array([O_UP, O_RIGHT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1101:
        return np.array([O_UP, O_LEFT, O_DOWN], dtype=np.uint8)
    elif bin == 0b1110:
        return np.array([O_UP, O_LEFT, O_RIGHT], dtype=np.uint8)
    elif bin == 0b1111:
        return np.array([O_UP, O_LEFT, O_RIGHT, O_DOWN], dtype=np.uint8)

def add_orientation(bin, orientation):
    if orientation == O_UP:
        masc = 0b1000
    elif orientation == O_LEFT:
        masc = 0b0100
    elif orientation == O_RIGHT:
        masc = 0b0010
    elif orientation == O_DOWN:
        masc = 0b0001
    
    return bin ^ masc

def remove_orientation(bin, orientation):
    if orientation == O_UP:
        masc = 0b0111
    elif orientation == O_LEFT:
        masc = 0b1011
    elif orientation == O_RIGHT:
        masc = 0b1101
    elif orientation == O_DOWN:
        masc = 0b1110

    return bin & masc

def is_unique(bin): # SQL REFERENCE ASPODAKDA+PS
    if bin == 0b1000 or bin == 0b0100 or bin == 0b0010 or bin == 0b0001:
        return True
    return False 

def number_of_orientations(numero):
    if numero == 0:
        return 4
    
    contagem = 0
    while numero:
        contagem += numero & 1
        numero >>= 1
    return contagem

def orientation_to_direction(orientation):
    if orientation == O_UP:
        return D_UP
    elif orientation == O_RIGHT:
        return D_RIGHT
    elif orientation == O_DOWN:
        return D_DOWN
    elif orientation == O_LEFT:
        return D_LEFT


def find_min(state):
    board_array = state.board.board_array
    mask = (board_array[:,:,2] != 1) & ((board_array[:,:,2] == 0) | (board_array[:,:,2] == 2))
    
    indices = np.argwhere(mask)
    if len(indices) == 0:
        return None
    
    orientations = board_array[indices[:, 0], indices[:, 1], 4]
    num_orientations = np.vectorize(number_of_orientations)(orientations)
    
    min_indices = np.where(num_orientations == np.min(num_orientations))[0]
    min_index = indices[min_indices[-1]]  # Pick the last index
    
    return min_index


class Board:
    def __init__(self, board_array):
        self.board_array = board_array # 0 - tipo, 1 - orientação, 2 - é definitivo?, 3 - conexões, 4 - orientações possiveis
        self.fixed_number = 0

        last_fixed_number = self.fixed_number
        global number_of_pieces
        number_of_pieces = board_array.shape[0] * board_array.shape[1]

        current = self.pre_processing(bypass_border=False)
        while(last_fixed_number != current):
            last_fixed_number = current
            current = self.pre_processing(bypass_border=True)       

    def __repr__(self):
        string = ""
        for x in range(self.board_array.shape[0]):
            for y in range(self.board_array.shape[1]):
                string += str_from_type(self.board_array[x,y,0]) + str_from_orientation(self.board_array[x,y,1])
                if y != self.board_array.shape[1] - 1:
                    string += "\t"
            string += "\n"    
        return string

    def can_emit(self, direction, row, col):
        tile_type = self.board_array[row, col, 0]
        orientation = self.board_array[row, col, 1]

        if tile_type == T_LOCK:
            if (orientation == O_UP and direction == D_UP) or \
            (orientation == O_DOWN and direction == D_DOWN) or \
            (orientation == O_LEFT and direction == D_LEFT) or \
            (orientation == O_RIGHT and direction == D_RIGHT):
                return True
        elif tile_type == T_JUNCTION:
            if (orientation == O_UP and direction != D_DOWN) or \
            (orientation == O_DOWN and direction != D_UP) or \
            (orientation == O_LEFT and direction != D_RIGHT) or \
            (orientation == O_RIGHT and direction != D_LEFT):
                return True
        elif tile_type == T_TURN:
            if (orientation == O_UP and (direction == D_LEFT or direction == D_UP)) or \
            (orientation == O_DOWN and (direction == D_RIGHT or direction == D_DOWN)) or \
            (orientation == O_LEFT and (direction == D_LEFT or direction == D_DOWN)) or \
            (orientation == O_RIGHT and (direction == D_RIGHT or direction == D_UP)):
                return True
        elif tile_type == T_CONNECTION:
            if (orientation == O_HORIZONTAL and (direction == D_LEFT or direction == D_RIGHT)) or \
            (orientation == O_VERTICAL and (direction == D_DOWN or direction == D_UP)):
                return True

        return False

    # CAN YOU HEAR THE SILENCE CAN YOU FEEL THE DARK CAN YOU FIX THE BROKEN CAN YOU FEEL CAN YOU FEEL MY HEART (can receive the flow)
    def can_receive(self, direction, row, col):
        tile_type = self.board_array[row, col, 0]
        orientation = self.board_array[row, col, 1]

        if tile_type == T_LOCK:
            if (orientation == O_UP and direction == D_DOWN) or \
            (orientation == O_DOWN and direction == D_UP) or \
            (orientation == O_LEFT and direction == D_RIGHT) or \
            (orientation == O_RIGHT and direction == D_LEFT):
                return True
        elif tile_type == T_JUNCTION:
            if (orientation == O_UP and direction != D_UP) or \
            (orientation == O_DOWN and direction != D_DOWN) or \
            (orientation == O_LEFT and direction != D_LEFT) or \
            (orientation == O_RIGHT and direction != D_RIGHT):
                return True
        elif tile_type == T_TURN:
            if (orientation == O_UP and (direction == D_RIGHT or direction == D_DOWN)) or \
            (orientation == O_DOWN and (direction == D_LEFT or direction == D_UP)) or \
            (orientation == O_LEFT and (direction == D_RIGHT or direction == D_UP)) or \
            (orientation == O_RIGHT and (direction == D_LEFT or direction == D_DOWN)):
                return True
        elif tile_type == T_CONNECTION:
            if (orientation == O_HORIZONTAL and (direction == D_LEFT or direction == D_RIGHT)) or \
            (orientation == O_VERTICAL and (direction == D_DOWN or direction == D_UP)):
                return True

        return False

    def update_connections(self, row, col):
        directions = directions_from_bin(self.board_array[row, col, 3])

        for direction in directions:
            self.number_of_connections -= 2
            other_row, other_col = direction_operations[direction](row, col)
            self.board_array[other_row, other_col, 3] = remove_direction(self.board_array[other_row, other_col, 3], inverse_direction(direction))

        self.board_array[row, col, 3] = 0

        for direction in (D_UP, D_DOWN, D_RIGHT, D_LEFT):
            if self.can_emit(direction, row, col):
                other_row, other_col = direction_operations[direction](row, col)
                if 0 <= other_row < self.board_array.shape[0] and 0 <= other_col < self.board_array.shape[1]:
                    if self.can_receive(direction, other_row, other_col):
                        self.number_of_connections += 2
                        self.board_array[row, col, 3] = add_direction(self.board_array[row, col, 3], direction)
                        self.board_array[other_row, other_col, 3] = add_direction(self.board_array[other_row, other_col, 3], inverse_direction(direction))

    def rotate_piece(self, row, col, orientation):
        self.board_array[row, col, 1] = orientation
        self.update_connections(row, col)

    def piece_actions(self, row, col):
        if self.board_array[row, col, 2] == 2:
            set = orientations_from_bin(self.board_array[row, col, 4])
            #set = np.setdiff1d(set, self.board_array[row, col, 1])
        elif self.board_array[row, col, 0] == T_CONNECTION:
            set = np.array([O_VERTICAL, O_HORIZONTAL], dtype=np.uint8)
            set = np.setdiff1d(set, self.board_array[row, col, 1])
        else:
            set = np.array([O_UP, O_DOWN, O_LEFT, O_RIGHT], dtype=np.uint8)
            set = np.setdiff1d(set, self.board_array[row, col, 1])
        
        return set
    
    def relax_border_piece(self, row, col):
        if self.board_array[row, col, 0] == T_JUNCTION:
            # Fixar
            if row == 0:
                self.board_array[row, col, 1] = O_DOWN
                self.board_array[row, col, 2] = 1
            elif row == self.board_array.shape[0] - 1:
                self.board_array[row, col, 1] = O_UP
                self.board_array[row, col, 2] = 1
            elif col == 0:
                self.board_array[row, col, 1] = O_RIGHT
                self.board_array[row, col, 2] = 1
            elif col == self.board_array.shape[1] - 1:
                self.board_array[row, col, 1] = O_LEFT
                self.board_array[row, col, 2] = 1
        elif self.board_array[row, col, 0] == T_CONNECTION:
            # Fixar
            if row == 0 or row == self.board_array.shape[0] - 1:
                self.board_array[row, col, 1] = O_HORIZONTAL
                self.board_array[row, col, 2] = 1
            elif col == 0 or col == self.board_array.shape[1] - 1:
                self.board_array[row, col, 1] = O_VERTICAL
                self.board_array[row, col, 2] = 1
        elif self.board_array[row, col, 0] == T_TURN:
            # Fixar
            if row == 0 and col == 0:
                self.board_array[row, col, 1] = O_DOWN
                self.board_array[row, col, 2] = 1
            elif row == 0 and col == self.board_array.shape[1] - 1:
                self.board_array[row, col, 1] = O_LEFT
                self.board_array[row, col, 2] = 1
            elif row == self.board_array.shape[0] - 1 and col == 0:
                self.board_array[row, col, 1] = O_RIGHT
                self.board_array[row, col, 2] = 1
            elif row == self.board_array.shape[0] - 1 and col == self.board_array.shape[1] - 1:
                self.board_array[row, col, 1] = O_UP
                self.board_array[row, col, 2] = 1
            # Limitar opções
            elif row == 0:
                self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_DOWN)
                self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_LEFT)
                self.board_array[row, col, 2] = 2
            elif col == 0:
                self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_DOWN)
                self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_RIGHT)
                self.board_array[row, col, 2] = 2
            elif row == self.board_array.shape[0] - 1:
                self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_UP)
                self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_RIGHT)
                self.board_array[row, col, 2] = 2
            elif col == self.board_array.shape[1] - 1:
                self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_UP)
                self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_LEFT)
                self.board_array[row, col, 2] = 2
        elif self.board_array[row, col, 0] == T_LOCK:
            # Limitar opções
            self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_UP)
            self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_LEFT)
            self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_RIGHT)
            self.board_array[row, col, 4] = add_orientation(self.board_array[row, col, 4], O_DOWN)

            if row == 0:
                self.board_array[row, col, 4] = remove_orientation(self.board_array[row, col, 4], O_UP)
            elif row == self.board_array.shape[0] - 1:
                self.board_array[row, col, 4] = remove_orientation(self.board_array[row, col, 4], O_DOWN)

            if col == 0:
                self.board_array[row, col, 4] = remove_orientation(self.board_array[row, col, 4], O_LEFT)
            elif col == self.board_array.shape[1] - 1:
                self.board_array[row, col, 4] = remove_orientation(self.board_array[row, col, 4], O_RIGHT)

            self.board_array[row, col, 2] = 2

    def fixa(self, row, col, connections):
        if self.board_array[row, col, 0] != T_CONNECTION:
            for orientation in (O_UP, O_LEFT, O_RIGHT, O_DOWN):
                no_connected_connections = 0
                self.board_array[row, col, 1] = orientation

                for direction in connections:
                    if self.can_receive(direction, row, col):
                        no_connected_connections += 1
                        
                        if no_connected_connections == connections.shape[0]:
                            break

                if no_connected_connections == connections.shape[0]:
                    self.board_array[row, col, 1] = orientation
                    self.board_array[row, col, 2] = 1
                    break
        else:
            for orientation in (O_VERTICAL, O_HORIZONTAL):
                no_connected_connections = 0
                self.board_array[row, col, 1] = orientation

                for direction in connections:
                    if self.can_receive(direction, row, col):
                        no_connected_connections += 1
                        
                        if no_connected_connections == connections.shape[0]:
                            break

                if no_connected_connections == connections.shape[0]:
                    self.board_array[row, col, 1] = orientation
                    self.board_array[row, col, 2] = 1
                    break

    def reduz_possibilidades(self, row, col, connections, n_possibilities):        
        bin = 0
        
        possibilities = 0
        for orientation in (O_UP, O_LEFT, O_RIGHT, O_DOWN):
            no_connected_connections = 0
            self.board_array[row, col, 1] = orientation
            for direction in connections:
                if self.can_receive(direction, row, col):
                    no_connected_connections += 1
                if no_connected_connections == connections.shape[0]:
                    bin = add_orientation(bin, orientation)
                    possibilities += 1
                    break

            if possibilities == n_possibilities:
                break

        if self.board_array[row, col, 2] == 2: # se já tinha possibilidades limitadas, faz a interseção
            self.board_array[row, col, 4] = intersect_bin(bin, self.board_array[row, col, 4])
            self.board_array[row, col, 1] = orientations_from_bin(self.board_array[row, col, 4])[0]
        elif self.board_array[row, col, 2] == 0: # se ainda não haviam possibilidades limitadas 
            self.board_array[row, col, 4] = bin
            self.board_array[row, col, 2] = 2
            self.board_array[row, col, 1] = orientations_from_bin(self.board_array[row, col, 4])[0]

        if is_unique(self.board_array[row, col, 4]):
            self.board_array[row, col, 2] = 1
            other_row, other_col = direction_operations[D_UP](row, col) 
            if 0 <= other_row and self.board_array[other_row, other_col, 2] != 1:
                self.relax_piece_with_dependencies(other_row, other_col)
            
            other_row, other_col = direction_operations[D_LEFT](row, col)
            if 0 <= other_col and self.board_array[other_row, other_col, 2] != 1:
                self.relax_piece_with_dependencies(other_row, other_col)
            return True
        return False

    def reduz_possibilidades_por_contradicao(self, row, col, void, no_possibilities):        
        bin = 0
        possibilities = 0
        for orientation in (O_UP, O_LEFT, O_RIGHT, O_DOWN):
            no_not_connected_connections = 0
            self.board_array[row, col, 1] = orientation

            for direction in void:
                if not self.can_receive(direction, row, col):
                    no_not_connected_connections += 1
                if no_not_connected_connections == void.shape[0]:
                    bin = add_orientation(bin, orientation)
                    possibilities += 1
                    break

            if possibilities == no_possibilities:
                break
            

        if self.board_array[row, col, 2] == 2: # se já tinha possibilidades limitadas, faz a interseção
            self.board_array[row, col, 4] = intersect_bin(bin, self.board_array[row, col, 4])
            self.board_array[row, col, 1] = orientations_from_bin(self.board_array[row, col, 4])[0]
        elif self.board_array[row, col, 2] == 0: # se ainda não haviam possibilidades limitadas 
            self.board_array[row, col, 4] = bin
            self.board_array[row, col, 2] = 2
            self.board_array[row, col, 1] = orientations_from_bin(self.board_array[row, col, 4])[0]

        if is_unique(self.board_array[row, col, 4]):
            self.board_array[row, col, 2] = 1

            other_row, other_col = direction_operations[D_UP](row, col) 
            if 0 <= other_row and self.board_array[other_row, other_col, 2] != 1:
                self.relax_piece_with_dependencies(other_row, other_col)
            
            other_row, other_col = direction_operations[D_LEFT](row, col)
            if 0 <= other_col and self.board_array[other_row, other_col, 2] != 1:
                self.relax_piece_with_dependencies(other_row, other_col)
            return True
        return False

    def fixa_por_contradicao(self, row, col, void):
        if self.board_array[row, col, 0] != T_CONNECTION:
            for orientation in (O_UP, O_LEFT, O_RIGHT, O_DOWN):
                no_not_connected_connections = 0
                self.board_array[row, col, 1] = orientation

                for direction in void:
                    if not self.can_receive(direction, row, col):
                        no_not_connected_connections += 1
                        
                        if no_not_connected_connections == void.shape[0]:
                            break


                if no_not_connected_connections == void.shape[0]:
                    self.board_array[row, col, 1] = orientation
                    self.board_array[row, col, 2] = 1
                    break
        else:
            for orientation in (O_VERTICAL, O_HORIZONTAL):
                no_not_connected_connections = 0
                self.board_array[row, col, 1] = orientation

                for direction in void:
                    if not self.can_receive(direction, row, col):
                        no_not_connected_connections += 1
                        
                        if no_not_connected_connections == void.shape[0]:
                            break
                
                if no_not_connected_connections == void.shape[0]:
                    self.board_array[row, col, 1] = orientation
                    self.board_array[row, col, 2] = 1
                    break
 
    def relax_piece_with_dependencies(self, row, col):
        if self.board_array[row, col, 2] != 1:
            connections_list = []
            void_list = [] # a minha vida

            for direction in (D_UP, D_LEFT, D_RIGHT, D_DOWN): # PICKING THROUGH THE CARDS KNOWING WHATS NEARBY 
                other_row, other_col = direction_operations[direction](row, col)

                if 0 <= other_row < self.board_array.shape[0] and 0 <= other_col < self.board_array.shape[1]:

                    if self.board_array[other_row, other_col, 2] == 1:

                        if self.can_emit(inverse_direction(direction), other_row, other_col):
                            connections_list.append(inverse_direction(direction))
                        else:

                            void_list.append(inverse_direction(direction))
                else:
                    void_list.append(inverse_direction(direction))
            
        

            connections = np.array(connections_list, dtype=np.uint8)
            void = np.array(void_list, dtype=np.uint8)

            # only know you love her when you let her go:
            del connections_list # and you let her go
            del void_list # (e a esta tambem)

            fixado = 0

            if self.board_array[row, col, 0] == T_JUNCTION: 
                if connections.shape[0] == 3:
                    self.fixa(row, col, connections)
                    fixado = 1
                elif connections.shape[0] == 2:
                    fixado = self.reduz_possibilidades(row, col, connections, 2)
                elif connections.shape[0] == 1:
                    fixado = self.reduz_possibilidades(row, col, connections, 3)
            elif self.board_array[row, col, 0] == T_CONNECTION:
                if connections.shape[0] == 1 or connections.shape[0] == 2:
                    self.fixa(row, col, connections)
                    fixado = 1
            elif self.board_array[row, col, 0] == T_TURN:
                if connections.shape[0] == 2:
                    self.fixa(row, col, connections)
                    fixado = 1
                elif connections.shape[0] == 1:
                    fixado = self.reduz_possibilidades(row, col, connections, 2)
            elif self.board_array[row, col, 0] == T_LOCK:
                if connections.shape[0] == 1:
                    self.fixa(row, col, connections)
                    fixado = 1
                

            # POR CONTRADIÇÃO QUOD ERAT DEMONSTRANDUM
            if fixado == 0:
                if self.board_array[row, col, 0] == T_JUNCTION:
                    if void.shape[0] == 1:
                        self.fixa_por_contradicao(row, col, void)
                        fixado = 1
                elif self.board_array[row, col, 0] == T_TURN:
                    if void.shape[0] == 2:
                        self.fixa_por_contradicao(row, col, void)
                        fixado = 1
                    elif void.shape[0] == 1:
                        self.reduz_possibilidades_por_contradicao(row, col, void, 2)
                elif self.board_array[row, col, 0] == T_LOCK:
                    if void.shape[0] == 3:
                        self.fixa_por_contradicao(row, col, void)
                        fixado = 1
                    #elif void.shape[0] == 2:
                    #    self.reduz_possibilidades_por_contradicao(row, col, void, 2)
                    #elif void.shape[0] == 1:
                    #    self.reduz_possibilidades_por_contradicao(row, col, void, 3)

                elif self.board_array[row, col, 0] == T_CONNECTION:
                    if void.shape[0] == 2 or void.shape[0] == 1:
                        self.fixa_por_contradicao(row, col, void)
                        fixado = 1

            if fixado:
                other_row, other_col = direction_operations[D_UP](row, col)
                if 0 <= other_row and self.board_array[other_row, other_col, 2] != 1:
                    self.relax_piece_with_dependencies(other_row, other_col)

                other_row, other_col = direction_operations[D_LEFT](row, col)
                if 0 <= other_col and self.board_array[other_row, other_col, 2] != 1:
                    self.relax_piece_with_dependencies(other_row, other_col)

                #TODO: Problema com recursão
                #other_row, other_col = direction_operations[D_RIGHT](row, col)
                #if 0 <= other_col < self.board_array.shape[1] and self.board_array[other_row, other_col, 2] != 1:
                #    self.relax_piece_with_dependencies(other_row, other_col)
                
    def pre_processing(self, bypass_border=False, row=0, col=0, max_row=0, max_col=0):
        rows = self.board_array.shape[0]
        columns = self.board_array.shape[1]
        
        if bypass_border == False:
            for i in range(rows):
                for j in range(columns):
                    if i == 0 or i == rows - 1 or j == 0 or j == columns - 1:
                        self.relax_border_piece(i, j) 
        
        res = 0
        change = 1
        while (change != 0):
            change = 0
            for i in range(rows):
                for j in range(columns):
                    if self.board_array[i, j, 2] != 1:
                        self.relax_piece_with_dependencies(i, j)
                    else:
                        res += 1

        self.fixed_number = res
        return res
        
    @staticmethod
    def parse_instance():
        lines = sys.stdin.readlines()
        n_lines = len(lines)
        matrix = np.zeros((n_lines, n_lines, 5), dtype=np.uint8)
        for row, line in enumerate(lines):
            split = line.split()
            for col, strpiece in enumerate(split):
                piece = piece_from_str(strpiece)
                matrix[row, col, 0] = piece[0]
                matrix[row, col, 1] = piece[1]
        return Board(matrix)

class PipeManiaState:
    state_id = np.uint16(0)

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class PipeMania(Problem):
    def __init__(self, board: Board):
        self.initial = PipeManiaState(board)

    def actions(self, state: PipeManiaState):
        res = []
        
        min = find_min(state)

        if min is None:
            return res
        min_x, min_y = min
        
        actions = state.board.piece_actions(min_x, min_y)
        for action in actions:
            res.append((min_x, min_y, action))

        return res
    
    def result(self, state: PipeManiaState, action):
        new_state = copy.deepcopy(state)
        new_state.board.board_array[action[0], action[1], 1] = action[2]
        new_state.board.board_array[action[0], action[1], 2] = 1

        last_fixed_number = new_state.board.fixed_number
        current = new_state.board.pre_processing(bypass_border=True)

        while(last_fixed_number != current):
            last_fixed_number = current
            current = new_state.board.pre_processing(bypass_border=True)        

        return new_state

    def goal_test(self, state: PipeManiaState):
        global number_of_pieces
        if number_of_pieces == state.board.fixed_number:
            visited = np.zeros(state.board.board_array.shape[:2], dtype=np.uint8)
            board_shape = state.board.board_array.shape
            queue = [(0, 0)]
            visited[0, 0] = 1

            while queue:
                cord = queue.pop(0)
                for direction in directions_from_piece(state.board.board_array[cord[0], cord[1], 0], state.board.board_array[cord[0], cord[1], 1]):
                    other_cord = direction_operations[direction](cord[0], cord[1])
                    if 0 <= other_cord[0] < board_shape[0] and 0 <= other_cord[1] < board_shape[1]:
                        if state.board.can_receive(direction, other_cord[0], other_cord[1]):
                            if visited[other_cord[0], other_cord[1]] == 0:
                                visited[other_cord[0], other_cord[1]] = 1
                                queue.append(other_cord)
                        else:
                            return False
                    else:
                        return False

            
            return np.sum(visited) == number_of_pieces
        else:
            return False

    def h(self, node: Node):
        #global total_number_of_connections
        #return total_number_of_connections - node.state.board.number_of_connections
        global number_of_pieces
        return number_of_pieces - node.state.board.fixed_number

def main():
    board = Board.parse_instance()

    problem = PipeMania(board)
    node = greedy_search(problem)
    # node = depth_first_tree_search(problem)
    print(node.state.board, end="")

if __name__ == "__main__":
    main()
