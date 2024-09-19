class GameState:
    ''' this class is designed to store all information regarding a particular state (snapshot of the game at a given time) '''

    unit_vectors = [(0, 1), (-1, 0), (0, -1), (1, 0)] # possible directions of movement

    def __init__(self, gridSize, doorCol, redCarIdx, coords, isTrucks, directions):
        '''create a game state object
        Parameters:
        - gridSize: (n_rows,n_columns), tuple denoting size of grid
        - doorCol: column index of the door (0-indexed)
        - redCarIdx: index of the red car (as per the next few list parameters)
        - coords: list of coordinate tuples of the vehicles
        - isTrucks: list of 1/0s whether each vehicle is a truck or not
        - directions: list of directions for each vehicle - 0 is right, 1 is up, 2 is left, 3 is down
        '''
        
        self.n, self.m = gridSize
        self.doorCol = doorCol
        self.nVehicles = len(coords)
        self.redCarIdx = redCarIdx
        self.coords = coords
        self.isTrucks = isTrucks
        self.directions = directions

    def _outsideGrid(self, i, j):
        '''check whether a coordinate (i,j) is outside the grid'''
        return not ((0<=i<self.n) and (0<=j<self.m))

    def takeAction(self, vehicleIdx, move_direction):
        '''change the current game state to move vehicle (vehicleIdx) forward/backword according to (move_direction)'''
        delx, dely = self.unit_vectors[self.directions[vehicleIdx]]
        delx *= move_direction
        dely *= move_direction
        self.coords[vehicleIdx] = (self.coords[vehicleIdx][0] + delx, self.coords[vehicleIdx][1] + dely)

    def createGrid(self):
        '''creates and returns a 2d-character-array representation of the game state'''
        grid = [[' ']*self.m for i in range(self.n)]

        for v_i in range(self.nVehicles):
            x, y = self.coords[v_i]
            isTruck = self.isTrucks[v_i]
            direction = self.directions[v_i]

            # if the trunk coordinate is already occupied or outside grid, conflict found
            if self._outsideGrid(x, y) or (grid[x][y] != ' '):
                raise ValueError("Found vehicle conflict or out-of-bounds error")
            grid[x][y] = chr(65+v_i) # place upper case letter corresponding to vehicle index, as the trunk marker

            delx, dely = self.unit_vectors[direction] # get change in coordinates corresponding to direction
            
            # if the next vehicle coordinate is already occupied or outside grid, conflict found
            if self._outsideGrid(x+delx, y+dely) or (grid[x+delx][y+dely] != ' '):
                raise ValueError("Found vehicle conflict or out-of-bounds error")
            grid[x+delx][y+dely] = chr(97+v_i) # set the next cell of the vehicle to the corresponding lower case letter

            # if the vehicle is a truck, repeat the conflict check and letter placement for another spot
            if isTruck:
                if self._outsideGrid(x+delx*2, y+dely*2) or (grid[x+delx*2][y+dely*2] != ' '):
                    raise ValueError("Found vehicle conflict or out-of-bounds error")
                grid[x+delx*2][y+dely*2] = chr(97+v_i)

        return grid

    def hasConflict(self):
        '''check and return True if the game state has a conflict (cars overlapping or moving out of the grid)'''
        try:
            self.createGrid()
            return False # if we can run createGrid without exceptions there's no conflict
        except Exception as e:
            # if the exception is a ValueError then it's due to a conflict we detected
            if isinstance(e, ValueError):
                return True
            # otherwise there's some actual error exception that should be raised for us to debug
            else:
                raise e

    def at_goal_state(self):
        '''checks if the current state is a goal state (red car is at the door)'''
        # if red car points upward, return true if its in the second-topmost row
        if self.directions[self.redCarIdx] == 1:
            return (self.coords[self.redCarIdx][0] == 1)

        # else it must point downward, so true if its in the topmost row
        return (self.coords[self.redCarIdx][0] == 0)

    def __repr__(self):
        '''creates a neat string representation for the state'''
        # store ' ' for an empty cell, otherwise a letter corresponding to the vehicle index (a, b, c, ...)
        # the letter placed on trunk coordinate will be capitalised, the others will be lowercase
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
        # if the red car points upward then the number of cells before the door is the row index minus 1
        if self.directions[self.redCarIdx] == 1:
            return (self.coords[self.redCarIdx][0] - 1)

        # otherwise it's just the row index 
        return (self.coords[self.redCarIdx][0])

    def h2(self):
        '''calculate heuristic 2: number of cells between red car and door + number of those that are occupied'''
        grid = self.createGrid()

        # find the number of cells between the red car and door
        if self.directions[self.redCarIdx] == 1:
            redCarDistance = (self.coords[self.redCarIdx][0] - 1)
        else:
            redCarDistance = (self.coords[self.redCarIdx][0])

        cost = redCarDistance
        # check how many of the counted cells are occupied
        for i in range(redCarDistance):
            if grid[i][self.doorCol] != ' ':
                cost += 1
        return cost