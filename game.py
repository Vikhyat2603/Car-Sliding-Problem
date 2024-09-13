class CarSlidingGame:
    def __init__(self, n, m , coords, isTrucks, directions):
        self.n, self.m = n, m
        self.n_vehicles = len(coords)
        self.coords = coords
        self.isTrucks = isTrucks
        self.directions = directions

        if self.check_conflict():
            raise ValueError, "Vehicles provided are already in conflict!"

    def check_conflict(self):
        pass

    def __repr__(self):
        print_arr = [[' ']*self.m for i in range(self.n)]

        for v_i in range(self.n_vehicles):
            x, y = self.coords[v_i]
            isTruck = self.isTrucks[v_i]
            direction = self.directions[v_i]

            print_arr[x,y] = chr(65+v_i)
            match direction:
                case 0:
                    #right
                    print_arr[x, y+1] = chr(97+v_i)
                    if isTruck:
                        print_arr[x, y+2] = chr(97+v_i)
                case 1:
                    #up
                    print_arr[x-1, y] = chr(97+v_i)
                    if isTruck:
                        print_arr[x-2, y] = chr(97+v_i)
                case 2:
                    #left
                    print_arr[x, y-1] = chr(97+v_i)
                    if isTruck:
                        print_arr[x, y-2] = chr(97+v_i)
                case 3:
                    #down
                    print_arr[x+1, y] = chr(97+v_i)
                    if isTruck:
                        print_arr[x+2, y] = chr(97+v_i)

        return print_arr