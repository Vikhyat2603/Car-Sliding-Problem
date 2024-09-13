from game import CarSlidingGame

coordsA = [(0,3), (0,4), (1,4), (2,3),
              (2,5), (3,0), (4,4), (4,5)]
isTrucksA = [0, 0, 0, 1, 0, 0, 1, 0]
directionsA = [3, 0, 0, 2, 2, 1, 2, 1]
gameA = CarSlidingGame((6,6), 5, coordsA, isTrucksA, directionsA)
print(gameA)

# coordsB = [(0,0), (0,1), (0,3), (1,2),
#             (1,5), (2,3), (2,4), (3,1),
#             (4,4), (5,3)]
# isTrucksB = [1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
# directionsB = [3, 3, 0, 1, 2, 2, 0, 2, 1, 2]
# gameB = CarSlidingGame((6,6), 4, coordsB, isTrucksB, directionsB)
# print(gameB)

# coordsC = [(0,2), (0,5), (1,4), (2,1),
#               (2,3), (3,0), (3,4), (3,5), (4,3)]
# isTrucksC = [1, 1, 0, 1, 0, 1, 1, 0, 1]
# directionsC = [3, 2, 0, 3, 1, 3, 2, 1, 0]
# gameC = CarSlidingGame((6,6), 5, coordsC, isTrucksC, directionsC)
# print(gameC)