from ScrambleRubixcube import xInitial, make_move
import numpy as np
from datetime import datetime
import time

array = np.array([
    #Coordinates(x,y,z) where front face 1st corner piece is (0,0,0)
    [[0, 0, 2], [1, 0, 2], [2, 0, 2]],  #Top 
    [[0, 0, 1], [1, 0, 1], [2, 0, 1]],  
    [[0, 0, 0], [1, 0, 0], [2, 0, 0]],  
    [[0, 0, 2], [0, 1, 2], [0, 2, 2]],  #Left 
    [[0, 0, 1], [0, 1, 1], [0, 2, 1]],
    [[0, 0, 0], [0, 1, 0], [0, 2, 0]],
    [[0, 0, 0], [1, 0, 0], [2, 0, 0]],  #Front
    [[0, 1, 0], [1, 1, 0], [2, 1, 0]],
    [[0, 2, 0], [1, 2, 0], [2, 2, 0]],
    [[2, 0, 0], [2, 0, 1], [2, 0, 2]],  #Right
    [[2, 1, 0], [2, 1, 1], [2, 1, 2]],
    [[2, 2, 0], [2, 2, 1], [2, 2, 2]],
    [[2, 0, 2], [1, 0, 2], [0, 0, 2]],  #Back
    [[2, 1, 2], [1, 1, 2], [0, 1, 2]],
    [[2, 2, 2], [1, 2, 2], [0, 2, 2]],
    [[0, 2, 0], [1, 2, 0], [2, 2, 0]],  #Bottom
    [[0, 2, 1], [1, 2, 1], [2, 2, 1]],
    [[0, 2, 2], [1, 2, 2], [2, 2, 2]],
])

class State:
    cube = None
    g = 0
    h = 0
    parent = None
    move = None

# checks if goal reached. if reached writes goal state in output.txt
def goal_reached(curr):
    if curr is None or curr.h != 0:
        return False

    moves = []
    final_cube = np.copy(curr.cube)  # Copy the final state before backtracking

    while curr is not None:
        if curr.move is not None:
            moves.append(curr.move)
        if curr.parent is None:
            break
        curr = curr.parent
            
    # Reversing moves to show from start to goal
    moves.reverse()
    print("Moves to reach goal:", moves)

    # Goal reached, write output
    try:
        with open('output.txt', 'w') as file:
            file.write("Moves to reach goal:\n")
            file.write("\n".join(moves))
            file.write("\n\n")
            file.write("Final Cube State:\n")
            file.write("              " + str(final_cube[0, 0:3]) + '\n')
            file.write("              " + str(final_cube[1, 0:3]) + '\n')
            file.write("              " + str(final_cube[2, 0:3]) + '\n')
            file.write(str(final_cube[3, 0:3]) + ' ' + str(final_cube[6, 0:3]) + ' ' + str(final_cube[9, 0:3]) + ' ' + str(final_cube[12, 0:3]) + '\n')
            file.write(str(final_cube[4, 0:3]) + ' ' + str(final_cube[7, 0:3]) + ' ' + str(final_cube[10, 0:3]) + ' ' + str(final_cube[13, 0:3]) + '\n')
            file.write(str(final_cube[5, 0:3]) + ' ' + str(final_cube[8, 0:3]) + ' ' + str(final_cube[11, 0:3]) + ' ' + str(final_cube[14, 0:3]) + '\n')
            file.write("              " + str(final_cube[15, 0:3]) + '\n')
            file.write("              " + str(final_cube[16, 0:3]) + '\n')
            file.write("              " + str(final_cube[17, 0:3]) + '\n')

    except IOError as e:
        print("Error writing to file:", e)
        return False

    return True


# checks if child ascendant of parent
def contains1(child, parent):
    curr = parent.parent
    while curr is not None:
        if np.array_equal(curr.cube, child): return True
        curr = curr.parent

    return False


# checks if frontier contains child
def contains2(child, frontier):
    for curr in frontier:
        if np.array_equal(curr.cube, child): return True

    return False


def ida(start):
    start.h = corner_edge_sum_max(start.cube)
    cost_limit = start.h
    nodes = 0
    frontier = list()
    branching_factors = list()

    while True:
        minimum = None
        frontier.append(start)

        while len(frontier) != 0:
            curr = frontier.pop()
            print(f"Heuristic Value: {curr.h}")


            if goal_reached(curr):
                print('Goal Height:', curr.g)
                print('Branching Factor:', sum(branching_factors)/len(branching_factors))
                # while curr is not None:
                #    if curr.move is not None:
                #        print(curr.move)
                #    curr = curr.parent
                print("Nodes Generated:", nodes)
                return

            b = 0
            nodes = nodes + 12
            for i in range(12):
                new = State()
                new.cube = np.array(curr.cube)
                new.g = curr.g + 1
                new.parent = curr
                new.move = make_move(new.cube, i + 1, 0)
                new.h = corner_edge_sum_max(new.cube)

                if new.g + new.h > cost_limit:
                    if minimum is None or new.g + new.h < minimum:
                        minimum = new.g + new.h
                    continue
                if curr.parent is not None and (contains1(new.cube, curr) or contains2(new.cube, frontier)):
                    continue
                frontier.append(new)
                b = b + 1
            if b != 0:
                branching_factors.append(b)
        cost_limit = minimum

def manhattan_distance(cube, i, z, corner):
    c1 = array[i, z]
    center = None
    for c in [1, 4, 7, 10, 13, 16]:
        if cube[i, z] == cube[c, 1]:
            center = c
            break

    if corner:
        c2 = array[center - 1, 0]
        d1 = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])
        c2 = array[center - 1, 2]
        d2 = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])
        c2 = array[center + 1, 0]
        d3 = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])
        c2 = array[center + 1, 2]
        d4 = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])
        return min(d1, d2, d3, d4)
    else:
        c2 = array[center - 1, 1]
        d1 = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])
        c2 = array[center, 0]
        d2 = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])
        c2 = array[center, 2]
        d3 = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])
        c2 = array[center + 1, 1]
        d4 = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])
        return min(d1, d2, d3, d4)


def corner_edge_sum_max(cube):
    corners = 0
    edges = 0
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            corners = corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
            edges = edges + manhattan_distance(cube, i, 1, False)
        else:
            edges = edges + manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)
    return max(corners / 12, edges / 8)

##########################################

curr = State()
curr.cube = np.array(xInitial)
handle = open('input.txt')
indexes = [0, 1, 2, 3, 6, 9, 12, 4, 7, 10, 13, 5, 8, 11, 14, 15, 16, 17]
index = 0
for line in handle:
    line = line.replace(' ', '')
    for row in line.split('['):
        if len(row) != 0:
            i = indexes[index]
            curr.cube[i, 0] = row[1]
            curr.cube[i, 1] = row[4]
            curr.cube[i, 2] = row[7]
            index = index + 1
            
time.ctime()
fmt = '%H:%M:%S'
start = time.strftime(fmt)
ida(curr)
time.ctime()
end = time.strftime(fmt)
print("Time taken(sec):", datetime.strptime(end, fmt) - datetime.strptime(start, fmt))