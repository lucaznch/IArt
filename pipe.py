# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from enum import Enum
import numpy
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class PieceType(Enum): # Different types of pieces
    LOCK = "F"
    JUNCTION = "B"
    TURN = "V"
    CONNECTION = "L"

class PieceOrientation(Enum): # Different orientations of pieces
    UP = "C"
    DOWN = "B"
    LEFT = "E"
    RIGHT = "D"
    HORIZONTAL = "H"
    VERTICAL = "V"

class Direction(Enum):
    UP = "C"
    DOWN = "B"
    LEFT = "E"
    RIGHT = "D"

class Piece():
    def __init__(self, type, orientation):
        self.type = type
        self.orientation = orientation

    def __str__(self):
        return f'{self.type.value}{self.orientation.value}'
    
    def __repr__(self):
        return f'{self.type.value}{self.orientation.value}'
    
    @staticmethod
    def parse_instance(string):
        if len(string) == 2:
            type = None
            orientation = None
            
            # Parse the type of the piece
            if string[0] == 'F':
                type = PieceType.LOCK
            elif string[0] == 'B':
                type = PieceType.JUNCTION
            elif string[0] == 'V':
                type = PieceType.TURN
            elif string[0] == 'L':
                type = PieceType.CONNECTION

            # Parse the orientation of the piece
            if string[0] != 'L':
                if string[1] == 'C':
                    orientation = PieceOrientation.UP
                elif string[1] == 'B':
                    orientation = PieceOrientation.DOWN
                elif string[1] == 'E':
                    orientation = PieceOrientation.LEFT
                elif string[1] == 'D':
                    orientation = PieceOrientation.RIGHT
            else:
                if string[1] == 'H':
                    orientation = PieceOrientation.HORIZONTAL
                elif string[1] == 'V':
                    orientation = PieceOrientation.VERTICAL
            
            return Piece(type, orientation)
        else:
            raise ValueError("Error")

    def type(self):
        return self.type

    def orientation(self):
        return self.orientation

    def can_accept_the_flow(self, direction):
        if self.type == PieceType.LOCK:
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

        elif self.type == PieceType.JUNCTION:
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

        elif self.type == PieceType.TURN:
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

        elif self.type == PieceType.CONNECTION:
            if self.orientation == PieceOrientation.HORIZONTAL and (direction == Direction.LEFT or direction == Direction.RIGHT):
                return True
            elif self.orientation == PieceOrientation.VERTICAL and (direction == Direction.DOWN or direction == Direction.UP):
                return True
            else:
                return False

    def get_flow_directions(self, connected_direction):
        if self.type == PieceType.LOCK:
            if self.orientation == PieceOrientation.UP:
                return [Direction.UP]
            elif self.orientation == PieceOrientation.DOWN:
                return [Direction.DOWN]
            elif self.orientation == PieceOrientation.LEFT:
                return [Direction.LEFT]
            elif self.orientation == PieceOrientation.RIGHT:
                return [Direction.RIGHT]
        
        elif self.type == PieceType.JUNCTION:
            possible = []

            if self.orientation == PieceOrientation.UP:
                possible = [Direction.UP, Direction.LEFT, Direction.RIGHT]
            elif self.orientation == PieceOrientation.DOWN:
                possible = [Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            elif self.orientation == PieceOrientation.LEFT:
                possible = [Direction.DOWN, Direction.LEFT, Direction.UP]
            elif self.orientation == PieceOrientation.RIGHT:
                possible = [Direction.DOWN, Direction.RIGHT, Direction.UP]
            
            possible.remove(connected_direction)
            return possible
        
        elif self.type == PieceType.TURN:
            possible = []

            if self.orientation == PieceOrientation.UP:
                possible = [Direction.UP, Direction.LEFT]
            elif self.orientation == PieceOrientation.DOWN:
                possible = [Direction.DOWN, Direction.RIGHT]
            elif self.orientation == PieceOrientation.LEFT:
                possible = [Direction.DOWN, Direction.LEFT]
            elif self.orientation == PieceOrientation.RIGHT:
                possible = [Direction.RIGHT, Direction.UP]
            
            possible.remove(connected_direction)
            return possible
        
        elif self.type == PieceType.CONNECTION:
            possible = []

            if self.orientation == PieceOrientation.HORIZONTAL:
                possible = [Direction.RIGHT, Direction.LEFT]
            elif self.orientation == PieceOrientation.VERTICAL:
                possible = [Direction.DOWN, Direction.UP]
            
            possible.remove(connected_direction)
            return possible

class PipeManiaState():
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.x = 0
        self.y = 0
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    
    def move_pos(self, x=0, y=0):
        self.pos = [self.pos[0] + x, self.pos[1] + y]

class Board():
    def __init__(self, field):
        self.field = field

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

    @staticmethod
    def parse_instance():
        lines = sys.stdin.readlines()
        field = [[Piece.parse_instance(str_piece) if str_piece.strip() else None for str_piece in line.split()] for line in lines]
        return Board(field)

    def get_value(self, row:int, col:int):
        return self.field[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        return (None if row == 0 else self.field[row-1][col], None if row == len(self.field) - 1 else self.field[row+1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        return (None if col == 0 else self.field[row][col-1], None if col == len(self.field[0]) - 1 else self.field[row][col+1])
    
    def get_size(self):
        return len(self.field)*len(self.field[0])

class PipeMania(Problem):
    def __init__(self, board: Board):
        self.initial = PipeManiaState(board)

    def actions(self, state: PipeManiaState):
        piece = state.board.get_value(state.x, state.y)

        if piece.type() != PieceType.CONNECTION:
            if piece.orientation() == PieceOrientation.DOWN:
                return ['TURN UP', 'TURN LEFT', 'TURN RIGHT', 'TRY TO CONNECT']
            elif piece.orientation() == PieceOrientation.UP:
                return ['TURN DOWN', 'TURN LEFT', 'TURN RIGHT', 'TRY TO CONNECT']
            elif piece.orientation() == PieceOrientation.LEFT:
                return ['TURN RIGHT', 'TURN UP', 'TURN DOWN', 'TRY TO CONNECT']
            elif piece.orientation() == PieceOrientation.RIGHT:
                return ['TURN LEFT', 'TURN UP', 'TURN DOWN', 'TRY TO CONNECT']
        else:
            if piece.orientation() == PieceOrientation.HORIZONTAL:
                return ['TURN VERTICAL', 'TRY TO CONNECT']
            else:
                return ['TURN HORIZONTAL', 'TRY TO CONNECT']

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        accepted = {}
        possibilities = [((0,0), None)] # ((x,y), direction)

        for possibility in possibilities:
            if possibility[0] not in accepted:
                piece = state.board.get_value(possibility[0][0], possibility[0][1])
                potential_candidates_to_possibilities = piece.get_flow_directions(possibility[1])
                
                for potential_candidate in potential_candidates_to_possibilities:
                    if potential_candidate == Direction.UP:
                        if state.board.get_value(possibility[0][0] - 1, possibility[0][1]).can_accept_the_flow(Direction.DOWN):
                            possibilities.append(((possibility[0][0] - 1, possibility[0][1]), Direction.DOWN))
                    elif potential_candidate == Direction.DOWN:
                        if state.board.get_value(possibility[0][0] + 1, possibility[0][1]).can_accept_the_flow(Direction.UP):
                            possibilities.append(((possibility[0][0] + 1, possibility[0][1]), Direction.UP))
                    elif potential_candidate == Direction.LEFT:
                        if state.board.get_value(possibility[0][0], possibility[0][1] - 1).can_accept_the_flow(Direction.RIGHT):
                            possibilities.append(((possibility[0][0], possibility[0][1] - 1), Direction.RIGHT))
                    elif potential_candidate == Direction.RIGHT:
                        if state.board.get_value(possibility[0][0], possibility[0][1] + 1).can_accept_the_flow(Direction.LEFT):
                            possibilities.append(((possibility[0][0], possibility[0][1] + 1), Direction.LEFT))
                    else:
                        return False
                        
                accepted[possibility[0]] = True

        return state.board.get_size() == len(accepted)
    
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

def main():
    board = Board.parse_instance()
    problem = PipeMania(board)
    print(board)
    print("Is goal?", problem.goal_test(problem.initial))

if __name__ == "__main__":
    main()
    pass
