from game import GameState
from queue import PriorityQueue

# change these two variables and run the code
input_case = 'A' # initial state A, B, or C
heuristic_choice = 1 # heuristic 1 or 2 or 0 for UCS

# initialize variables based on which initial state we want to test
if input_case == 'A':
    coords = [(0,3), (0,4), (1,4), (2,3),
                    (2,5), (3,0), (4,4), (4,5)]
    n = len(coords)
    isTrucks = [0, 0, 0, 1, 0, 0, 1, 0] # types of vehicles (0 for car, 1 for truck)
    directions = [3, 0, 0, 2, 2, 1, 2, 1] # directions of vehicles (0 is right, 1 is up, 2 is left, 3 is down)
    doorIdx = 5 # column index of door
    redCarIdx = 7 # index of red car in the lists above
        
elif input_case == 'A':
    coords = [(0,0), (0,1), (0,3), (1,2),
                (1,5), (2,3), (2,4), (3,1),
                (4,4), (5,3)]
    n = len(coords)
    isTrucks = [1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
    directions = [3, 3, 0, 1, 2, 2, 0, 2, 1, 2]
    doorIdx = 4
    redCarIdx = 8

elif input_case == 'C':
    coords = [(0,2), (0,5), (1,4), (2,1),
                (2,3), (3,0), (3,4), (3,5), (4,3)]
    n = len(coords)
    isTrucks = [1, 1, 0, 1, 0, 1, 1, 0, 1]
    directions = [3, 2, 0, 3, 1, 3, 2, 1, 0]
    doorIdx = 5
    redCarIdx = 7

# if the red car is not pointing upward or downward, a solution is impossible
if directions[redCarIdx] not in [1,3]:
    print('Puzzle is unsolvable since red car is not vertical')
    quit()

q = PriorityQueue() # queue element format: (f(n) [= cost from start to goal through state n], state [= list of coords])
visited = set() # set of visited states
parentDict = {tuple(coords): None} # key: state (list of coords), value: cheapest parent state of the given state
n_goal_tested = 0 # counter for how many nodes we goal-test
path = [] # used eventually to store the optimal path

# given a state, trace down the path of states leading to it, as tracked by parentDict
def find_path(state):
    temp_path = []
    while state is not None:
        temp_path.append(state)
        state = parentDict[tuple(state)]

    temp_path.reverse() # reverse path so that its in the start to target order
    return temp_path

initialState = GameState((6,6), doorIdx, redCarIdx, coords, isTrucks, directions) # initialise an initial state object
heuristic_cost = 0 if heuristic_choice==0 else (initialState.h1() if heuristic_choice == 1 else initialState.h2()) # get h(initial state)
q.put((0 + heuristic_cost, coords)) # f(initial state) = 0 + h(initial state)

while not q.empty():
    dist, coords = q.get()
    
    # check if this state is already visited:
    if tuple(coords) in visited:
        continue

    # mark current state as visited:
    visited.add(tuple(coords))

    # create state object for current state
    thisState = GameState((6,6), doorIdx, redCarIdx, coords, isTrucks, directions)

    # calculate heuristic cost h(n) for current state to be used later
    parent_heuristic_cost = 0 if heuristic_choice==0 else (thisState.h1() if heuristic_choice == 1 else thisState.h2())

    # create a copy of the current state(=coords) to be used later
    original_parent_coords = coords[:] 

    # check if we are at a goal state:
    n_goal_tested += 1
    if thisState.at_goal_state():
        path = find_path(coords)
        break
    
    # iterate through
    for action_i in range(2*n):
        thisState.coords = original_parent_coords[:]

        vehicle_index = action_i//2 # which vehicle we chose to move (0<=i<n)
        move_direction = 2*(action_i % 2)-1 # which direction we chose to move in (+/-1)

        thisState.takeAction(vehicle_index, move_direction) # move vehicle in the given direction

        # if we've already explored this child state, continue
        if tuple(thisState.coords) in visited:
            continue

        # if this child state has a conflict (vehicle overlap or out of bounds), continue
        if thisState.hasConflict():
            continue

        # calculate heuristic cost for this child state
        child_heuristic_cost = 0 if heuristic_choice==0 else (thisState.h1() if heuristic_choice == 1 else thisState.h2())

        # mark the child state's parent in the dictionary
        parentDict[tuple(thisState.coords)] = tuple(original_parent_coords)

        # calculate the distance from start to the parent using g(parent) = f(parent) - h(parent)
        dist_s_to_parent = dist - parent_heuristic_cost

        # add the child state to the priority queue, with f(child) = (g(parent) + 1) + h(child)
        q.put((dist_s_to_parent + 1 + child_heuristic_cost, thisState.coords[:]))

if len(path)==0:
    print('Puzzle is unsolvable')
    quit()

# print path in neat row-wise gride format to fit well in a Google Doc
concat_path = []
i = 0
n_cols = 7
while i <= len(path)//7:
    row = ['']*8
    for j in range(7):
        step_i = 7*i + j
        if step_i >= len(path):
            break
        step_config = GameState((6,6), doorIdx, redCarIdx, list(path[step_i]), isTrucks, directions)
        step = str(step_config).split('\n')
        for sub_row_i in range(8):
            row[sub_row_i] += ' ' + step[sub_row_i]
    i += 1
    concat_path.append(row.copy())

for r in concat_path:
    print('\n'.join(r))

print('Path length: ', len(path)-1)
print('Number of states goal tested:', n_goal_tested)