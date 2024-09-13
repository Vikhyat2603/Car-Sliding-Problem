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
                
        new_repr_arr = ['-'*(2*self.door_col) + ' ' + '-'*(2*(self.m - self.door_col) - 2)]
        for i in range(self.n):
            this_row = []
            for j in range(self.m):
                if j!=0:
                    this_row.append('|')
                this_row.append(repr_arr[i][j])
            if i!=0:
                new_repr_arr.append(['-']*(2*self.m-1))
            new_repr_arr.append(this_row[:])
        new_repr_arr.append('-'*(2*self.m-1))
        # for i in new_repr_arr:
        #     print(i)

        for i in range(1,2*self.n-1-1):
            for j in range(2*self.m-1):
                element = new_repr_arr[i][j]
                if element == '|':
                    left = new_repr_arr[i][j-1].lower()
                    right = new_repr_arr[i][j+1].lower()
                    if left==right and left.isalpha():
                        new_repr_arr[i][j] = ' '
                elif element == '-':
                    up = new_repr_arr[i-1][j].lower()
                    down = new_repr_arr[i+1][j].lower()
                    if up==down and up.isalpha():
                        new_repr_arr[i][j] = ' '
        # print(new_repr_arr)

        repr_string = '■' + new_repr_arr[0] + '■\n'
        for row in new_repr_arr[1:-1]:
            repr_string += '|' + ''.join(row) + '|\n'
        repr_string += '■' + new_repr_arr[-1] + '■'
        return repr_string