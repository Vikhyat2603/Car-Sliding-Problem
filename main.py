from game import CarSlidingGame
from queue import PriorityQueue

coords = [(0,3), (0,4), (1,4), (2,3),
              (2,5), (3,0), (4,4), (4,5)]
n = len(coords)
isTrucks = [0, 0, 0, 1, 0, 0, 1, 0]
directions = [3, 0, 0, 2, 2, 1, 2, 1]
doorIdx = 5
redCarIdx = 3 #change?
gameA = CarSlidingGame((6,6), doorIdx, redCarIdx, coords, isTrucks, directions)
heuristic_choice = 1
print(gameA)
# 14?

# coordsB = [(0,0), (0,1), (0,3), (1,2),
#             (1,5), (2,3), (2,4), (3,1),
#             (4,4), (5,3)]
# isTrucksB = [1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
# directionsB = [3, 3, 0, 1, 2, 2, 0, 2, 1, 2]
# doorIdxB = 4
# gameB = CarSlidingGame((6,6), doorIdxB, coordsB, isTrucksB, directionsB)
# print(gameB)

# coordsC = [(0,2), (0,5), (1,4), (2,1),
#               (2,3), (3,0), (3,4), (3,5), (4,3)]
# isTrucksC = [1, 1, 0, 1, 0, 1, 1, 0, 1]
# directionsC = [3, 2, 0, 3, 1, 3, 2, 1, 0]
# doorIdxC = 5
# gameC = CarSlidingGame((6,6), doorIdxC, coordsC, isTrucksC, directionsC)
# print(gameC)

path = []

def find_path(state):
    #path.append(state)
    while state is not None:
        path.append(state)
        state = parentDict[state]

    path.reverse()

q = PriorityQueue()
visited = set()
parentDict = dict() # key: state (list of coords), value: cheapest parent state of the given state
# queue element format: (expected f(n)=cost from start to goal through state n, state)
thisConfig = CarSlidingGame((6,6), doorIdx, redCarIdx, coords, isTrucks, directions)
heuristic_cost = (thisConfig.h1() if heuristic_choice == 1 else thisConfig.h2())
q.put((heuristic_cost, coords))
loop_ct = 0
while q:
    dist, coords = q.get()
    # print(coords)

    #check if visited:
    if tuple(coords) in visited:
        continue

    thisConfig = CarSlidingGame((6,6), doorIdx, redCarIdx, coords, isTrucks, directions)

    #check if goal state:
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

        thisConfig.takeAction(vehicle_index, move_direction)
        print(thisConfig.coords)
        # check visited
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

        q.put((dist - parent_heuristic_cost + 1 + heuristic_cost, thisConfig.coords))
        
        # undo the action taken so we can re-use 'thisConfig' to find future state neighbours
        thisConfig.takeAction(vehicle_index, -move_direction)

    loop_ct += 1
    
print(len(path))