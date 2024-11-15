from ScrambleRubixcube import xInitial, make_move
import numpy as np
from datetime import datetime
import time
import sys
sys.setrecursionlimit(10000)  # Set to a higher value like 10000 or 20000 if needed

# Defining move names for tracking moves
MOVE_NAMES = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]

# Global array defining the cube structure

array = np.array([
    [[0, 0, 2], [1, 0, 2], [2, 0, 2]],
    [[0, 0, 1], [1, 0, 1], [2, 0, 1]],
    [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
    [[0, 0, 2], [0, 1, 2], [0, 2, 2]],
    [[0, 0, 1], [0, 1, 1], [0, 2, 1]],
    [[0, 0, 0], [0, 1, 0], [0, 2, 0]],
    [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
    [[0, 1, 0], [1, 1, 0], [2, 1, 0]],
    [[0, 2, 0], [1, 2, 0], [2, 2, 0]],
    [[2, 0, 0], [2, 0, 1], [2, 0, 2]],
    [[2, 1, 0], [2, 1, 1], [2, 1, 2]],
    [[2, 2, 0], [2, 2, 1], [2, 2, 2]],
    [[2, 0, 2], [1, 0, 2], [0, 0, 2]],
    [[2, 1, 2], [1, 1, 2], [0, 1, 2]],
    [[2, 2, 2], [1, 2, 2], [0, 2, 2]],
    [[0, 2, 0], [1, 2, 0], [2, 2, 0]],
    [[0, 2, 1], [1, 2, 1], [2, 2, 1]],
    [[0, 2, 2], [1, 2, 2], [2, 2, 2]],
])


# State class to represent the cube configuration and associated information
class State:
    def __init__(self, cube=None, g=0, h=0, parent=None, move=None, moves_list=None):
        self.cube = cube
        self.g = g  # Cost to reach this state
        self.h = h  # Heuristic estimate to goal
        self.parent = parent  # Link to the parent state
        self.move = move  # Move that led to this state
        
        self.moves_list = moves_list if moves_list is not None else []


# Example initial cube state for reference
xInitial = np.array([
    ['W', 'W', 'W'],
        ['W', 'W', 'W'],
        ['W', 'W', 'W'],
        ['G', 'G', 'G'],
        ['G', 'G', 'G'],
        ['R', 'R', 'R'],
        ['R', 'R', 'R'],
        ['R', 'R', 'R'],
        ['B', 'B', 'B'],
        ['B', 'B', 'B'],
        ['B', 'B', 'B'],
        ['O', 'O', 'O'],
        ['O', 'O', 'O'],
        ['O', 'O', 'O'],
        ['G', 'G', 'G'],
        ['Y', 'Y', 'Y'],
        ['Y', 'Y', 'Y'],
        ['Y', 'Y', 'Y']
])


def rotate_face_clockwise(face):
    """Rotate a 3x3 face of the cube clockwise."""
    return np.rot90(face, -1)

def rotate_face_counterclockwise(face):
    """Rotate a 3x3 face of the cube counterclockwise."""
    return np.rot90(face, 1)

def FrontCW(cube):
    """Rotate the front face clockwise."""
    # Rotate the front face itself
    cube[6:9, :] = rotate_face_clockwise(cube[6:9, :])
    
    # Save edge pieces for rotation
    top = cube[2, :].copy()
    left = cube[3:6, 2].copy()
    bottom = cube[15, :].copy()
    right = cube[9:12, 0].copy()
    
    # Rotate edges
    cube[2, :] = np.flip(left)
    cube[3:6, 2] = bottom
    cube[15, :] = np.flip(right)
    cube[9:12, 0] = top

def FrontACW(cube):
    """Rotate the front face counterclockwise."""
    FrontCW(cube)
    FrontCW(cube)
    FrontCW(cube)

def UpCW(cube):
    """Rotate the top (Up) face clockwise."""
    cube[0:3, :] = rotate_face_clockwise(cube[0:3, :])
    
    # Save edge pieces for rotation
    front = cube[3, :].copy()
    left = cube[12, :].copy()
    back = cube[9, :].copy()
    right = cube[6, :].copy()
    
    # Rotate edges
    cube[3, :] = right
    cube[12, :] = front
    cube[9, :] = left
    cube[6, :] = back

def UpACW(cube):
    """Rotate the top (Up) face counterclockwise."""
    UpCW(cube)
    UpCW(cube)
    UpCW(cube)

# Similarly, you would define DownCW, DownACW, LeftCW, LeftACW, RightCW, RightACW, BackCW, BackACW functions 
# following similar principles as above.

# Example DownCW rotation function
def DownCW(cube):
    """Rotate the bottom (Down) face clockwise."""
    cube[15:18, :] = rotate_face_clockwise(cube[15:18, :])
    
    # Save edge pieces for rotation
    front = cube[8, :].copy()
    left = cube[5, :].copy()
    back = cube[14, :].copy()
    right = cube[11, :].copy()
    
    # Rotate edges
    cube[8, :] = left
    cube[5, :] = np.flip(back)
    cube[14, :] = right
    cube[11, :] = np.flip(front)

def DownACW(cube):
    """Rotate the bottom (Down) face counterclockwise."""
    DownCW(cube)
    DownCW(cube)
    DownCW(cube)

def LeftCW(cube):
    """Rotate the left face clockwise."""
    cube[3:6, :] = rotate_face_clockwise(cube[3:6, :])
    
    # Save edge pieces for rotation
    top = cube[0:3, 0].copy()
    front = cube[3:6, 0].copy()
    bottom = cube[15:18, 0].copy()
    back = cube[9:12, 2].copy()
    
    # Rotate edges
    cube[0:3, 0] = np.flip(back)
    cube[3:6, 0] = top
    cube[15:18, 0] = front
    cube[9:12, 2] = np.flip(bottom)

def LeftACW(cube):
    """Rotate the left face counterclockwise."""
    LeftCW(cube)
    LeftCW(cube)
    LeftCW(cube)

def RightCW(cube):
    """Rotate the right face clockwise."""
    cube[9:12, :] = rotate_face_clockwise(cube[9:12, :])
    
    # Save edge pieces for rotation
    top = cube[0:3, 2].copy()
    front = cube[3:6, 2].copy()
    bottom = cube[15:18, 2].copy()
    back = cube[9:12, 0].copy()
    
    # Rotate edges
    cube[0:3, 2] = front
    cube[3:6, 2] = bottom
    cube[15:18, 2] = np.flip(back)
    cube[9:12, 0] = np.flip(top)

def RightACW(cube):
    """Rotate the right face counterclockwise."""
    RightCW(cube)
    RightCW(cube)
    RightCW(cube)

def BackCW(cube):
    """Rotate the back face clockwise."""
    cube[12:15, :] = rotate_face_clockwise(cube[12:15, :])
    
    # Save edge pieces for rotation
    top = cube[0, :].copy()
    left = cube[3:6, 0].copy()
    bottom = cube[15, :].copy()
    right = cube[9:12, 2].copy()
    
    # Rotate edges
    cube[0, :] = right
    cube[3:6, 0] = np.flip(bottom)
    cube[15, :] = np.flip(left)
    cube[9:12, 2] = top

def BackACW(cube):
    """Rotate the back face counterclockwise."""
    BackCW(cube)
    BackCW(cube)
    BackCW(cube)


def make_move(x, move, reverse, moves_list):
    if reverse == 1:
        if move % 2 == 0:
            move = move - 1
        else:
            move = move + 1

    move_name = ""
    if move == 1:
        FrontCW(x)
        move_name = "FrontCW"
    elif move == 2:
        FrontACW(x)
        move_name = "FrontACW"
    elif move == 3:
        UpCW(x)
        move_name = "UpCW"
    elif move == 4:
        UpACW(x)
        move_name = "UpACW"
    elif move == 5:
        DownCW(x)
        move_name = "DownCW"
    elif move == 6:
        DownACW(x)
        move_name = "DownACW"
    elif move == 7:
        LeftCW(x)
        move_name = "LeftCW"
    elif move == 8:
        LeftACW(x)
        move_name = "LeftACW"
    elif move == 9:
        RightCW(x)
        move_name = "RightCW"
    elif move == 10:
        RightACW(x)
        move_name = "RightACW"
    elif move == 11:
        BackCW(x)
        move_name = "BackCW"
    elif move == 12:
        BackACW(x)
        move_name = "BackACW"

    moves_list.append(move_name)
    return move_name


# Goal check
def goal_reached(curr, moves_list):
    # Define a solved state configuration (this is just an example)
    solved_state = np.array([
        ['W', 'W', 'W'],
        ['W', 'W', 'W'],
        ['W', 'W', 'W'],
        ['G', 'G', 'G'],
        ['G', 'G', 'G'],
        ['G', 'G', 'G'],
        ['R', 'R', 'R'],
        ['R', 'R', 'R'],
        ['R', 'R', 'R'],
        ['B', 'B', 'B'],
        ['B', 'B', 'B'],
        ['B', 'B', 'B'],
        ['O', 'O', 'O'],
        ['O', 'O', 'O'],
        ['O', 'O', 'O'],
        ['Y', 'Y', 'Y'],
        ['Y', 'Y', 'Y'],
        ['Y', 'Y', 'Y']
    ])

    if np.array_equal(curr.cube, solved_state):
        print("Goal state reached!")
        print("Number of moves:", len(moves_list))
        print("Moves sequence:", " -> ".join(moves_list))

        with open('output.txt', 'w') as file:
            file.write("Final Cube State:\n")
            file.write(str(curr.cube))

        return True
    return False

# Path to goal by moves
def get_solution_path(curr):
    path = []
    while curr.move is not None:
        path.append(curr.move)
        curr = curr.parent
    path.reverse()
    return path

# Checks for repeated states in parent chain
def contains1(child, parent):
    curr = parent
    while curr is not None:
        if np.array_equal(curr.cube, child):
            return True
        curr = curr.parent
    return False

# Checks if frontier contains the child state
def contains2(child, frontier):
    for curr in frontier:
        if np.array_equal(curr.cube, child):
            return True
    return False

# Manhattan distance heuristic calculation
def manhattan_distance(cube, i, z, corner):
    c1 = array[i, z]
    center = None
    for c in [1, 4, 7, 10, 13, 16]:
        if cube[i, z] == cube[c, 1]:
            center = c
            break

    if corner:
        return min(
            abs(c1[0] - array[center - 1, 0][0]) + abs(c1[1] - array[center - 1, 0][1]) + abs(c1[2] - array[center - 1, 0][2]),
            abs(c1[0] - array[center + 1, 2][0]) + abs(c1[1] - array[center + 1, 2][1]) + abs(c1[2] - array[center + 1, 2][2])
        )
    else:
        return abs(c1[0] - array[center - 1, 1][0]) + abs(c1[1] - array[center - 1, 1][1]) + abs(c1[2] - array[center - 1, 1][2])

# Combined heuristic
def corner_edge_sum_max(cube):
    corners, edges = 0, 0
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            corners += manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
            edges += manhattan_distance(cube, i, 1, False)
        else:
            edges += manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)
    return max(corners / 12, edges / 8)

def ida(curr, moves_list):
    max_iterations = 100000  # Set the max iteration limit
    iterations = 0

    # Set heuristic value for the start state
    curr.h = corner_edge_sum_max(curr.cube)
    cost_limit = curr.h  # Initial cost limit is set to heuristic value
    nodes = 0  # To keep track of nodes generated

    visited = set()  # Store visited states

    while True:
        minimum = None
        frontier = [curr]  # Start with the initial state in the frontier
        branching_factors = []  # To calculate branching factor during the search
        b = 0  # Number of child nodes generated from current state

        # Iteration over the frontier to explore states
        while frontier:
            if iterations >= max_iterations:
                print("Reached maximum iterations.")
                return  # Exit if iteration limit reached
            
            curr = frontier.pop()  # Get the current state to process
            iterations += 1  # Increment the iteration counter

            cube_tuple = tuple(map(tuple, curr.cube))

            # Check if the state has already been visited
            if cube_tuple in visited:
                continue
            visited.add(cube_tuple)

            # Debugging prints for the state being explored
            print(f"Exploring state {iterations}:")
            print(f"Cube state: {curr.cube}")
            print(f"Moves list: {curr.moves_list}")
            print(f"Heuristic value (h): {curr.h}")
            print(f"Cost limit: {cost_limit}")
            
            # Check goal and perform other operations as needed...
            if goal_reached(curr):  # If the goal is reached (make sure goal_reached is correct)
                print(f'Goal Height: {curr.g}')
                print(f'Branching Factor: {sum(branching_factors) / len(branching_factors) if branching_factors else 1}')
                solution_path = get_solution_path(curr)  # Get the solution path
                print(f"Solution Moves: {', '.join(MOVE_NAMES[move] for move in solution_path)}")
                print(f"Nodes Generated: {nodes}")
                return

            nodes += 12  # Track number of nodes generated

            # Expanding current state into its neighbors (12 possible moves)
            for i in range(12):
                new = State(cube=np.copy(curr.cube), g=curr.g + 1, parent=curr, move=i, moves_list=list(curr.moves_list))  # Creating a new state

                # Making the move
                print(f"Applying move: {i + 1}")  # Debugging which move is being applied
                move_name = make_move(new.cube, i + 1, 0, new.moves_list)

                # Update heuristic for the new state
                new.h = corner_edge_sum_max(new.cube)

                print(f"New cube state after move {i + 1}: {new.cube}")
                print(f"New heuristic value: {new.h}")

                if new.g + new.h > cost_limit:  # If the cost exceeds the limit, prune the search
                    if minimum is None or new.g + new.h < minimum:
                        minimum = new.g + new.h
                    continue

                # Check if the state already exists in parent chain or frontier to avoid duplicates
                if curr.parent and (contains1(new.cube, curr) or contains2(new.cube, frontier)):
                    continue

                frontier.append(new)  # Add the new state to the frontier
                b += 1  # Increment branching factor count

            if b > 0:
                branching_factors.append(b)  # Track the branching factor

        if minimum is None:  # If no valid states are found, terminate
            print("No valid moves found, terminating...")
            return

        cost_limit = minimum  # Update the cost limit for the next iteration



# Initialize and start IDA* search
curr = State()
curr.cube = np.array(xInitial)
moves_list = []
ida(curr, moves_list)
