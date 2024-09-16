from game import CarSlidingGame
from queue import PriorityQueue

# coords = [(0,3), (0,4), (1,4), (2,3),
#               (2,5), (3,0), (4,4), (4,5)]
# n = len(coords)
# isTrucks = [0, 0, 0, 1, 0, 0, 1, 0]
# directions = [3, 0, 0, 2, 2, 1, 2, 1]
# doorIdx = 5
# redCarIdx = 7
# heuristic_choice = 2
#### 14 moves?

# coords = [(0,0), (0,1), (0,3), (1,2),
#             (1,5), (2,3), (2,4), (3,1),
#             (4,4), (5,3)]
# n = len(coords)
# isTrucks = [1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
# directions = [3, 3, 0, 1, 2, 2, 0, 2, 1, 2]
# doorIdx = 4
# redCarIdx = 8
# heuristic_choice = 1
# print(gameB)

# coords = [(0,2), (0,5), (1,4), (2,1),
#               (2,3), (3,0), (3,4), (3,5), (4,3)]
# n = len(coords)
# isTrucks = [1, 1, 0, 1, 0, 1, 1, 0, 1]
# directions = [3, 2, 0, 3, 1, 3, 2, 1, 0]
# doorIdx = 5
# redCarIdx = 7
# heuristic_choice = 2

path = []

def find_path(state):
    while state is not None:
        path.append(state)
        state = parentDict[tuple(state)]

    path.reverse()

q = PriorityQueue()
visited = set()
parentDict = {tuple(coords): None} # key: state (list of coords), value: cheapest parent state of the given state
# queue element format: (expected f(n)=cost from start to goal through state n, state)
thisConfig = CarSlidingGame((6,6), doorIdx, redCarIdx, coords, isTrucks, directions)
heuristic_cost = (thisConfig.h1() if heuristic_choice == 1 else thisConfig.h2())
q.put((heuristic_cost, coords))
n_goal_tested = 0

while not q.empty():
    
    # print('getting queue element from', q.qsize())
    dist, coords = q.get()
    #print(loop_ct)

    #check if visited:
    if tuple(coords) in visited:
        continue

    thisConfig = CarSlidingGame((6,6), doorIdx, redCarIdx, coords, isTrucks, directions)

    #check if goal state:
    n_goal_tested += 1
    if thisConfig.at_goal_state():
        find_path(coords)
        break
    
    #marking current state as visited:
    visited.add(tuple(coords))

    for action_i in range(2*n):
        vehicle_index = action_i//2
        move_direction = 2*(action_i % 2)-1

        #calculating current heuristics:
        parent_heuristic_cost = (thisConfig.h1() if heuristic_choice == 1 else thisConfig.h2())

        parent_coords = coords[:]

        thisConfig.takeAction(vehicle_index, move_direction)
        if tuple(thisConfig.coords) in visited:
            #undo here
            thisConfig.takeAction(vehicle_index, -move_direction)
            continue

        # check conflict
        if thisConfig.hasConflict():
            thisConfig.takeAction(vehicle_index, -move_direction)
            continue

        #calculating new heuristics:
        heuristic_cost = (thisConfig.h1() if heuristic_choice == 1 else thisConfig.h2())

        parentDict[tuple(thisConfig.coords[:])] = tuple(parent_coords)
        q.put((dist - parent_heuristic_cost + 1 + heuristic_cost, thisConfig.coords[:]))
        
        # undo the action taken so we can re-use 'thisConfig' to find future state neighbours
        thisConfig.takeAction(vehicle_index, -move_direction)
    
# for step in path:
#     thisConfig = CarSlidingGame((6,6), doorIdx, redCarIdx, list(step), isTrucks, directions)
#     print(thisConfig)

print('Path length: ', len(path)-1)
print('Number of states goal tested:', n_goal_tested)