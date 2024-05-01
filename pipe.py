# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
import numpy
from copy import deepcopy
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

class PieceAction(Enum):
    TURN_UP = "U"
    TURN_DOWN = "D"
    TURN_LEFT = "L"
    TURN_RIGHT = "R"
    TURN_HORIZONTAL = "H"
    TURN_VERTICAL = "V"
    NEXT_HORIZONTAL_RIGHT_PIECE = "NHR"
    NEXT_HORIZONTAL_LEFT_PIECE = "NHL"
    NEXT_VERTICAL_UP_PIECE = "NVU"
    NEXT_VERTICAL_DOWN_PIECE = "NVD"

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

    def get_max_connections(self):
        if self.type == PieceType.LOCK:
            return 1
        elif self.type == PieceType.JUNCTION:
            return 3
        elif self.type == PieceType.TURN:
            return 2
        else:
            return 2
    
    def get_possible_actions(self):
        if self.type != PieceType.CONNECTION:
            return [PieceAction.TURN_UP, PieceAction.TURN_DOWN, PieceAction.TURN_LEFT, PieceAction.TURN_RIGHT, PieceAction.NEXT_HORIZONTAL_RIGHT_PIECE, PieceAction.NEXT_HORIZONTAL_LEFT_PIECE, PieceAction.NEXT_VERTICAL_UP_PIECE, PieceAction.NEXT_VERTICAL_DOWN_PIECE]
        else:
            return [PieceAction.TURN_HORIZONTAL, PieceAction.TURN_VERTICAL, PieceAction.NEXT_HORIZONTAL_RIGHT_PIECE, PieceAction.NEXT_HORIZONTAL_LEFT_PIECE, PieceAction.NEXT_VERTICAL_UP_PIECE, PieceAction.NEXT_VERTICAL_DOWN_PIECE]
    
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
            
            if connected_direction != None:
                possible.remove(connected_direction)
            return possible
        
        elif self.type == PieceType.CONNECTION:
            possible = []

            if self.orientation == PieceOrientation.HORIZONTAL:
                possible = [Direction.RIGHT, Direction.LEFT]
            elif self.orientation == PieceOrientation.VERTICAL:
                possible = [Direction.DOWN, Direction.UP]
            
            if connected_direction != None:
                possible.remove(connected_direction)
            return possible

class Board():
    def __init__(self, field, max_connections):
        self.field = field
        self.max_connections = max_connections

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

        max_connections = 0
        for row in field:
            for piece in row:
                max_connections += piece.get_max_connections()

        return Board(field, max_connections)

    def get_value(self, row:int, col:int):
        return self.field[row][col]

    def get_size(self):
        return len(self.field)*len(self.field[0])
    
    def rotate_piece(self, x, y, rotation_type):
        if rotation_type == PieceAction.TURN_UP:
            self.field[y][x] = Piece(self.field[y][x].type, PieceOrientation.UP)
        elif rotation_type == PieceAction.TURN_DOWN:
            self.field[y][x] = Piece(self.field[y][x].type, PieceOrientation.DOWN)
        elif rotation_type == PieceAction.TURN_LEFT:
            self.field[y][x] = Piece(self.field[y][x].type, PieceOrientation.LEFT)
        elif rotation_type == PieceAction.TURN_RIGHT:
            self.field[y][x] = Piece(self.field[y][x].type, PieceOrientation.RIGHT)
        elif rotation_type == PieceAction.TURN_HORIZONTAL:
            self.field[y][x] = Piece(self.field[y][x].type, PieceOrientation.HORIZONTAL)
        elif rotation_type == PieceAction.TURN_VERTICAL:
            self.field[y][x] = Piece(self.field[y][x].type, PieceOrientation.VERTICAL)

class PipeManiaState():
    state_id = 0

    def __init__(self, board, x, y, connected_pieces):
        self.board = board

        self.x = x
        self.y = y

        self.connected_pieces = connected_pieces
        self.max_connections = board.max_connections

        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class PipeMania(Problem):
    def __init__(self, board: Board):
        self.initial = PipeManiaState(board, 0, 0, 0)

    def actions(self, state: PipeManiaState):
        actions = state.board.get_value(state.y, state.x).get_possible_actions()

        if state.x == len(state.board.field[0]) - 1:
            actions.remove(PieceAction.NEXT_HORIZONTAL_RIGHT_PIECE)
        elif state.x == 0:
            actions.remove(PieceAction.NEXT_HORIZONTAL_LEFT_PIECE)

        if state.y == len(state.board.field) - 1:
            actions.remove(PieceAction.NEXT_VERTICAL_DOWN_PIECE)
        elif state.y == 0:
            actions.remove(PieceAction.NEXT_VERTICAL_UP_PIECE)

        return actions

    def result(self, state: PipeManiaState, action):
        clone = deepcopy(state)

        if action in (PieceAction.TURN_UP, PieceAction.TURN_DOWN, PieceAction.TURN_LEFT, PieceAction.TURN_RIGHT, PieceAction.TURN_HORIZONTAL, PieceAction.TURN_VERTICAL):
            clone.board.rotate_piece(clone.x, clone.y, action)
        elif action == PieceAction.NEXT_HORIZONTAL_RIGHT_PIECE:
            clone.x = clone.x + 1
        elif action == PieceAction.NEXT_HORIZONTAL_LEFT_PIECE:
            clone.x = clone.x - 1
        elif action == PieceAction.NEXT_VERTICAL_UP_PIECE:
            clone.y = clone.y - 1
        elif action == PieceAction.NEXT_VERTICAL_DOWN_PIECE:
            clone.y = clone.y + 1

        return clone

    def goal_test(self, state: PipeManiaState):
        '''return state.max_connections == state.connected_pieces'''
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
        return node.state.max_connections - node.state.connected_pieces

def main():
    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    goal_node = breadth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.print(), sep="")

if __name__ == "__main__":
    main()
    pass
