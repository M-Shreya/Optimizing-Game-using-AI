from ScrambleRubixcube import xInitial, make_move
import numpy as np
from collections import deque
import time

class State:
    def __init__(self, cube, path, move=None, parent=None):
        self.cube = cube
        self.path = path
        self.move = move
        self.parent = parent

def goal_reached(curr):
    if curr is None:
        return False

    goal_cube = np.array([['W', 'W', 'W'],
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
        ['Y', 'Y', 'Y']])  # This should be the solved state of the cube

    if np.array_equal(curr.cube, goal_cube):  # Assuming you have a 'goal_cube' representing the solved state
        moves = []
        while curr is not None:
            if curr.move is not None:
                moves.append(curr.move)
            curr = curr.parent

        moves.reverse()
        print("Moves to reach goal:", moves)

        # Write the solution to a file
        try:
            with open('output_BFS.txt', 'w') as file:
                file.write("Moves to reach goal:\n")
                file.write("\n".join(moves))
                file.write("\n")
                file.write("\n")
                # Writing the final cube state
                file.write("Final Cube State:\n")
                for i in range(6):
                    file.write(" ".join(curr.cube[i]) + "\n")

        except IOError as e:
            print("Error writing to file:", e)
            return False

    return True

def bidirectional_bfs(start_cube, end_cube):
    visited_f = {}
    visited_b = {}

    queue_f = deque([State(start_cube, [], None, None)])
    queue_b = deque([State(end_cube, [], None, None)])

    # Store initial state and goal state representations in dictionaries
    visited_f[tuple(start_cube.flatten())] = queue_f[0]
    visited_b[tuple(end_cube.flatten())] = queue_b[0]

    while queue_f and queue_b:
        # Forward BFS
        current_state_f = queue_f.popleft()
        current_cube_f = current_state_f.cube
        path_f = current_state_f.path

        cube_tuple_f = tuple(current_cube_f.flatten())
        if cube_tuple_f in visited_b:
            print("Intersection found in forward BFS!")
            # Combine paths from forward and backward search
            path_b = visited_b[cube_tuple_f].path
            solution_path = path_f + path_b[::-1]
            return solution_path

        for move_id in range(12):
            new_cube_f = np.copy(current_cube_f)
            move_name_f = make_move(new_cube_f, move_id + 1, 0)
            new_state_f = State(new_cube_f, path_f + [move_name_f], move_name_f, current_state_f)
            queue_f.append(new_state_f)
            visited_f[tuple(new_cube_f.flatten())] = new_state_f

        # Backward BFS
        current_state_b = queue_b.popleft()
        current_cube_b = current_state_b.cube
        path_b = current_state_b.path

        cube_tuple_b = tuple(current_cube_b.flatten())
        if cube_tuple_b in visited_f:
            print("Intersection found in backward BFS!")
            # Combine paths from forward and backward search
            path_f = visited_f[cube_tuple_b].path
            solution_path = path_f + path_b[::-1]
            return solution_path

        for move_id in range(12):
            new_cube_b = np.copy(current_cube_b)
            move_name_b = make_move(new_cube_b, move_id + 1, 0)
            new_state_b = State(new_cube_b, path_b + [move_name_b], move_name_b, current_state_b)
            queue_b.append(new_state_b)
            visited_b[tuple(new_cube_b.flatten())] = new_state_b
            

    return None  # If no solution is found



# Load the initial cube state from input.txt
start_cube = np.array(xInitial)  # This assumes xInitial is already loaded correctly.
handle = open('input.txt')
indexes = [0, 1, 2, 3, 6, 9, 12, 4, 7, 10, 13, 5, 8, 11, 14, 15, 16, 17]
index = 0
for line in handle:
    line = line.replace(' ', '')
    for row in line.split('['):
        if len(row) != 0:
            i = indexes[index]
            start_cube[i, 0] = row[1]
            start_cube[i, 1] = row[4]
            start_cube[i, 2] = row[7]
            index += 1

# Goal cube (solved state)
goal_cube = np.array([['W', 'W', 'W'],
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
    ['Y', 'Y', 'Y']])

# Measure the time taken to solve the cube
start_time = time.time()
solution = bidirectional_bfs(start_cube, goal_cube)
end_time = time.time()

# Output the solution and time taken to output.txt
try:
    with open('output_BFS.txt', 'w') as output_file:
        if solution:
            output_file.write("Solution found with {} moves:\n".format(len(solution)))
            output_file.write("\n".join(solution))
        else:
            output_file.write("No solution found.\n")
        output_file.write("\nTime taken (seconds): {:.2f}\n".format(end_time - start_time))
except IOError as e:
    print("Error writing to file:", e)
