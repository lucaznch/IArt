# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from enum import Enum
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
from copy import deepcopy

class Direction(Enum):
    UP = "C"
    DOWN = "B"
    LEFT = "E"
    RIGHT = "D"

direction_operations = {
    Direction.UP: lambda row, col: (row - 1, col),
    Direction.DOWN: lambda row, col: (row + 1, col),
    Direction.LEFT: lambda row, col: (row, col - 1),
    Direction.RIGHT: lambda row, col: (row, col + 1)
}

class PieceOrientation(Enum):
    UP = "C"
    DOWN = "B"
    LEFT = "E"
    RIGHT = "D"
    HORIZONTAL = "H"
    VERTICAL = "V"

class PieceAction(Enum):
    TURN_UP = "U"
    TURN_DOWN = "D"
    TURN_LEFT = "L"
    TURN_RIGHT = "R"
    TURN_HORIZONTAL = "H"
    TURN_VERTICAL = "V"
    MOVE_RIGHT = "NHR"
    MOVE_LEFT = "NHL"
    MOVE_UP = "NVU"
    MOVE_DOWN = "NVD"

class Piece:
    def __init__(self, orientation):
        self.orientation = orientation
        self.connections = 0

    def __str__(self):
        return f'{self.get_type()}{self.orientation.value}'

    def __repr__(self):
        return f'{self.get_type()}{self.orientation.value}'

    def get_type(self):
        raise NotImplementedError("Subclasses must implement get_type method")

    def get_orientation(self):
        return self.orientation

    def get_actions(self):
        raise NotImplementedError("Subclasses must implement get_actions method")

    @staticmethod
    def parse_instance(string):
        piece_type = string[0]
        orientation = string[1]

        if piece_type == 'F':
            return LockPiece(PieceOrientation(orientation))
        elif piece_type == 'B':
            return JunctionPiece(PieceOrientation(orientation))
        elif piece_type == 'V':
            return TurnPiece(PieceOrientation(orientation))
        elif piece_type == 'L':
            return ConnectionPiece(PieceOrientation(orientation))
        else:
            raise ValueError("Invalid piece type")

class LockPiece(Piece):
    def get_type(self):
        return 'F'
    
    def get_actions(self):
        if self.orientation == PieceOrientation.UP:
            return [PieceAction.TURN_DOWN, PieceAction.TURN_LEFT, PieceAction.TURN_RIGHT]
        elif self.orientation == PieceOrientation.DOWN:
            return [PieceAction.TURN_UP, PieceAction.TURN_LEFT, PieceAction.TURN_RIGHT]
        elif self.orientation == PieceOrientation.LEFT:
            return [PieceAction.TURN_RIGHT, PieceAction.TURN_UP, PieceAction.TURN_DOWN]
        elif self.orientation == PieceOrientation.RIGHT:
            return [PieceAction.TURN_LEFT, PieceAction.TURN_UP, PieceAction.TURN_DOWN]

    def can_receive(self, direction):
        if self.orientation == PieceOrientation.UP and direction == Direction.DOWN:
            return True
        elif self.orientation == PieceOrientation.DOWN and direction == Direction.UP:
            return True
        elif self.orientation == PieceOrientation.LEFT and direction == Direction.RIGHT:
            return True
        elif self.orientation == PieceOrientation.RIGHT and direction == Direction.LEFT:
            return True
        else:
            return False
    
    def can_emit(self, direction):
        if self.orientation == PieceOrientation.UP and direction == Direction.UP:
            return True
        elif self.orientation == PieceOrientation.DOWN and direction == Direction.DOWN:
            return True
        elif self.orientation == PieceOrientation.LEFT and direction == Direction.LEFT:
            return True
        elif self.orientation == PieceOrientation.RIGHT and direction == Direction.RIGHT:
            return True
        else:
            return False      

    def get_max_connections(self):
        return 1

class JunctionPiece(Piece):
    def get_type(self):
        return 'B'
    
    def get_actions(self):
        if self.orientation == PieceOrientation.UP:
            return [PieceAction.TURN_DOWN, PieceAction.TURN_LEFT, PieceAction.TURN_RIGHT]
        elif self.orientation == PieceOrientation.DOWN:
            return [PieceAction.TURN_UP, PieceAction.TURN_LEFT, PieceAction.TURN_RIGHT]
        elif self.orientation == PieceOrientation.LEFT:
            return [PieceAction.TURN_RIGHT, PieceAction.TURN_UP, PieceAction.TURN_DOWN]
        elif self.orientation == PieceOrientation.RIGHT:
            return [PieceAction.TURN_LEFT, PieceAction.TURN_UP, PieceAction.TURN_DOWN]

    def can_receive(self, direction):
        if self.orientation == PieceOrientation.UP and direction != Direction.UP:
            return True
        elif self.orientation == PieceOrientation.DOWN and direction != Direction.DOWN:
            return True
        elif self.orientation == PieceOrientation.LEFT and direction != Direction.LEFT:
            return True
        elif self.orientation == PieceOrientation.RIGHT and direction != Direction.RIGHT:
            return True
        else:
            return False
        
    def can_emit(self, direction):
        if self.orientation == PieceOrientation.UP and direction != Direction.DOWN:
            return True
        elif self.orientation == PieceOrientation.DOWN and direction != Direction.UP:
            return True
        elif self.orientation == PieceOrientation.LEFT and direction != Direction.RIGHT:
            return True
        elif self.orientation == PieceOrientation.RIGHT and direction != Direction.LEFT:
            return True
        else:
            return False
    
    def get_max_connections(self):
        return 3

class TurnPiece(Piece):
    def get_type(self):
        return 'V'
    
    def get_actions(self):
        if self.orientation == PieceOrientation.UP:
            return [PieceAction.TURN_DOWN, PieceAction.TURN_LEFT, PieceAction.TURN_RIGHT]
        elif self.orientation == PieceOrientation.DOWN:
            return [PieceAction.TURN_UP, PieceAction.TURN_LEFT, PieceAction.TURN_RIGHT]
        elif self.orientation == PieceOrientation.LEFT:
            return [PieceAction.TURN_RIGHT, PieceAction.TURN_UP, PieceAction.TURN_DOWN]
        elif self.orientation == PieceOrientation.RIGHT:
            return [PieceAction.TURN_LEFT, PieceAction.TURN_UP, PieceAction.TURN_DOWN]

    def can_receive(self, direction):
        if self.orientation == PieceOrientation.UP and (direction == Direction.RIGHT or direction == Direction.DOWN):
            return True
        elif self.orientation == PieceOrientation.DOWN and (direction == Direction.LEFT or direction == Direction.UP):
            return True
        elif self.orientation == PieceOrientation.LEFT and (direction == Direction.RIGHT or direction == Direction.UP):
            return True
        elif self.orientation == PieceOrientation.RIGHT and (direction == Direction.LEFT or direction == Direction.DOWN):
            return True
        else:
            return False

    def can_emit(self, direction):
        if self.orientation == PieceOrientation.UP and (direction == Direction.LEFT or direction == Direction.UP):
            return True
        elif self.orientation == PieceOrientation.DOWN and (direction == Direction.RIGHT or direction == Direction.DOWN):
            return True
        elif self.orientation == PieceOrientation.LEFT and (direction == Direction.LEFT or direction == Direction.DOWN):
            return True
        elif self.orientation == PieceOrientation.RIGHT and (direction == Direction.RIGHT or direction == Direction.UP):
            return True
        else:
            return False

    def get_max_connections(self):
        return 2

class ConnectionPiece(Piece):
    def get_type(self):
        return 'L'
    
    def get_actions(self):
        if self.orientation == PieceOrientation.HORIZONTAL:
            return [PieceAction.TURN_VERTICAL]
        elif self.orientation == PieceOrientation.VERTICAL:
            return [PieceAction.TURN_HORIZONTAL]

    def can_receive(self, direction):
        if self.orientation == PieceOrientation.HORIZONTAL and (direction == Direction.LEFT or direction == Direction.RIGHT):
            return True
        elif self.orientation == PieceOrientation.VERTICAL and (direction == Direction.DOWN or direction == Direction.UP):
            return True
        else:
            return False

    def can_emit(self, direction):
        if self.orientation == PieceOrientation.HORIZONTAL and (direction == Direction.LEFT or direction == Direction.RIGHT):
            return True
        elif self.orientation == PieceOrientation.VERTICAL and (direction == Direction.DOWN or direction == Direction.UP):
            return True
        else:
            return False

    def get_max_connections(self):
        return 2

class Board:
    def __init__(self, field):
        self.field = field
        self.number_of_connections = 0
        #for row in range(len(field)):
        #    for col in range(len(field[0])):
        #        self.check_connections(row, col)

        self.total_number_of_connections = 0
        for row in field:
            for piece in row:
                self.total_number_of_connections += piece.get_max_connections()

    def __repr__(self):
        result = ""
        for row in range(len(self.field)):
            for column in range(len(self.field[0])):
                result += str(self.field[row][column])
                if column == len(self.field[0]) - 1:
                    result += "\n"
                else:
                    result += "\t"
        return result

    def get_piece(self, row: int, col: int):
        return self.field[row][col]

    def rotate_piece(self, row, col, rotation_type):
        piece = self.get_piece(row, col)
        orientation = piece.get_orientation()

        if rotation_type == PieceAction.TURN_UP:
            orientation = PieceOrientation.UP
        elif rotation_type == PieceAction.TURN_DOWN:
            orientation = PieceOrientation.DOWN
        elif rotation_type == PieceAction.TURN_LEFT:
            orientation = PieceOrientation.LEFT
        elif rotation_type == PieceAction.TURN_RIGHT:
            orientation = PieceOrientation.RIGHT
        elif rotation_type == PieceAction.TURN_HORIZONTAL:
            orientation = PieceOrientation.HORIZONTAL
        elif rotation_type == PieceAction.TURN_VERTICAL:
            orientation = PieceOrientation.VERTICAL

        piece.orientation = orientation
        self.check_connections(row, col)

    def check_connections(self, row, col):
        piece = self.field[row][col]

        self.number_of_connections -= 2 * piece.connections # cada "conexão" precisa de 2 conexões, uma de cada peça
        piece.connections = 0

        for dir in Direction:
            other_row, other_col = direction_operations[dir](row, col)
            if 0 <= other_row < len(self.field) and 0 <= other_col < len(self.field[0]):
                if piece.can_emit(dir) and self.field[other_row][other_col].can_receive(dir):
                    piece.connections += 1
        
        self.number_of_connections += 2 * piece.connections

    @staticmethod
    def parse_instance():
        lines = sys.stdin.readlines()
        field = [[Piece.parse_instance(str_piece) if str_piece.strip() else None for str_piece in line.split()] for line in lines]
        return Board(field)

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class PipeMania(Problem):
    def __init__(self, board: Board):
        self.initial = PipeManiaState(board)
        
    def pre_processamento(self, board):
        for row in range(len(board.field)):
            for col in range(len(board.field[0])):
                piece = board.get_piece(row, col)
                
                if row == 0 and piece.can_emit(Direction.UP):
                    if isinstance(piece, ConnectionPiece):
                        board.rotate_piece(row, col, PieceOrientation.HORIZONTAL)
                    else:
                        board.rotate_piece(row, col, PieceOrientation.DOWN)
                elif row == len(board.field) - 1 and piece.can_emit(Direction.UP):
                    if isinstance(piece, ConnectionPiece):
                        board.rotate_piece(row, col, PieceOrientation.HORIZONTAL)
                    else:
                        board.rotate_piece(row, col, PieceOrientation.UP)
                
                if col == 0 and piece.can_emit(Direction.LEFT):
                    if isinstance(piece, ConnectionPiece):
                        board.rotate_piece(row, col, PieceOrientation.VERTICAL)
                    else:
                        board.rotate_piece(row, col, PieceOrientation.RIGHT)
                elif col == len(board.field[0]) - 1 and piece.can_emit(Direction.RIGHT):
                    if isinstance(piece, ConnectionPiece):
                        board.rotate_piece(row, col, PieceOrientation.VERTICAL)
                    else:
                        board.rotate_piece(row, col, PieceOrientation.LEFT)
                    
    def actions(self, state: PipeManiaState):
        actions = []
        
        i = 0
        for row in state.board.field:
            j = 0
            for piece in row:
                piece_actions = piece.get_actions()
                for action in piece_actions:
                    actions.append((i, j, action))
                j += 1
            i += 1

        return actions

    def result(self, state: PipeManiaState, action):
        clone = deepcopy(state)
        clone.board.rotate_piece(action[0], action[1], action[2])
        return clone

    def goal_test(self, state: PipeManiaState):
        return state.board.number_of_connections == state.board.total_number_of_connections

    def h(self, node: Node):
        return node.state.board.total_number_of_connections - node.state.board.number_of_connections

def main():
    board = Board.parse_instance()
    problem = PipeMania(board)
    problem.pre_processamento(board)
    node = astar_search(problem, problem.h)
    print(node.state.board)

if __name__ == "__main__":
    main()

