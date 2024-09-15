class CarSlidingGame:
    unit_vectors = [(0, 1), (-1, 0), (0, -1), (1, 0)] # possible directions of movement

    def __init__(self, gridSize, doorCol, redCarIdx, coords, isTrucks, directions):
        self.n, self.m = gridSize
        self.doorCol = doorCol # notes which column the door is in
        self.nVehicles = len(coords)
        self.redCarIdx = redCarIdx # stores index of the red car among the given vehicles
        self.coords = coords # stores the coordinate tuple for the trunk of each vehicle
        self.isTrucks = isTrucks # stores 1/0 whether each vehicle is a truck or not
        self.directions = directions # stores direction for each vehicle, 0 is right, 1 is up, 2 is left, 3 is down

    def _outsideGrid(self, i, j):
        '''check whether a coordinate (i,j) is outside the grid.'''
        return not ((0<=i<=self.n) and (0<=j<=self.m))

    def takeAction(self, vehicleIdx, move_direction):
        '''change the current game state to move vehicle (vehicleIdx) forward/backword according to (move_direction) '''
        delx, dely = self.unit_vectors[self.directions[vehicleIdx]]
        delx *= move_direction
        dely *= move_direction
        self.coords[vehicleIdx] = (self.coords[vehicleIdx][0] + delx, self.coords[vehicleIdx][1] + dely)

    def createGrid(self):
        grid = [[' ']*self.m for i in range(self.n)]

        for v_i in range(self.nVehicles):
            x, y = self.coords[v_i]
            isTruck = self.isTrucks[v_i]
            direction = self.directions[v_i]

            # if the trunk coordinate is already occupied by another vehicle, conflict found
            if grid[x][y] != ' ':
                raise ValueError("Found vehicle Conflict in grid")
            grid[x][y] = chr(65+v_i) # place upper case letter corresponding to vehicle index, as the trunk marker

            delx, dely = self.unit_vectors[direction] # get change in coordinates corresponding to direction
            
            # if the vehicle is jutting out the grid, or clashing with some other already placed vehicle, conflict found
            if self._outsideGrid(x+delx, y+dely) or (grid[x+delx][y+dely] != ' '):
                raise ValueError("Found vehicle conflict in grid")
            grid[x+delx][y+dely] = chr(97+v_i) # set the next cell of the vehicle to the corresponding lower case letter

            # if the vehicle is a truck, repeat this check for the next coordinate
            if isTruck:
                if self._outsideGrid(x+delx*2, y+dely*2) or grid[x+delx*2][y+dely*2] != ' ':
                    raise ValueError("Found vehicle Conflict in grid")
                grid[x+delx*2][y+dely*2] = chr(97+v_i)

        return grid

    def hasConflict(self):
        '''check if the game state has a conflict (cars overlapping or moving out of the grid)'''
        try:
            self.createGrid()
            return True
        except ValueError:
            return False

    def at_goal_state(self):
        '''checks if the current state is a goal state (red car is at the door)'''
        # if red car points upward, return true if its in the second-topmost row
        if self.directions[self.redCarIdx] == 1:
            return (self.coords[self.redCarIdx][0] == 1)
        
        # else return true if its in the topmost row
        return (self.coords[self.redCarIdx][0] == 0)
        
    def __repr__(self):
        '''creates a neat string representation for the state'''
        # store ' ' for an empty cell, otherwise a letter corresponding to the vehicle index (a, b, c...).
        # the trunk coordinate letter will be capitalised, the others will be lowercase
        grid = self.createGrid()

        # make a neat string representation of this game state, along with border and door
        repr_string = ''
        repr_string += '■' + '-'*self.doorCol + ' ' + '-'*(self.m-self.doorCol-1) + '■\n'
        for row in grid:
            repr_string += '|' + ''.join(row) + '|\n'
        repr_string += '■' + '-'*self.m + '■'
        return repr_string
    
    def h1(self):
        '''calculate heuristic 1: number of cells between red car and door'''
        if self.directions[self.redCarIdx] == 1:
            return (self.coords[self.redCarIdx][0] - 1)
        else:
            # else return true if its in the topmost row
            return (self.coords[self.redCarIdx][0])

    def h2(self):
        '''calculate heuristic 2: number of cells between red car and door + number of those that are occupied'''
        if self.directions[self.redCarIdx] == 1:
            cost = (self.coords[self.redCarIdx][0] - 1)
            
        else:
            cost = (self.coords[self.redCarIdx][0])
        
        return cost