class CarSlidingGame:
    def __init__(self, gridSize, door_col, coords, isTrucks, directions):
        self.n, self.m = gridSize
        self.door_col = door_col
        self.n_vehicles = len(coords)
        self.coords = coords
        self.isTrucks = isTrucks
        self.directions = directions

        # if self.check_conflict():
        #     raise ValueError, "Vehicles provided are already in conflict!"

    def check_conflict(self):
        pass

    def __repr__(self):
        repr_arr = [[' ']*self.m for i in range(self.n)]

        for v_i in range(self.n_vehicles):
            x, y = self.coords[v_i]
            isTruck = self.isTrucks[v_i]
            direction = self.directions[v_i]

            repr_arr[x][y] = chr(65+v_i)
            unit_vector = [(0, 1), (-1, 0), (0, -1), (1, 0)]
            delx, dely = unit_vector[direction]
            repr_arr[x+delx][y+dely] = chr(97+v_i)
            if isTruck:
                repr_arr[x+delx*2][y+dely*2] = chr(97+v_i)

        repr_string = ''
        repr_string += '■' + '-'*self.door_col + ' ' + '-'*(self.m-self.door_col-1) + '■\n'
        for row in repr_arr:
            repr_string += '|' + ''.join(row) + '|\n'
        repr_string += '■' + '-'*self.m + '■'
        return repr_string