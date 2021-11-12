from copy import deepcopy
import numpy as np

class Grid():
    
    def __init__(self, N = 7) -> None:
        self.dim  = N
        self.map = np.zeros((N,N)) # empty board
    

    def getAvailableCells(self):
        indices = np.where(self.map == 0)
        available = [(x,y) for x,y in list(zip(indices[0], indices[1]))]
        
        return available
    

    def setCellValue(self, pos: tuple, val):
        self.map[pos] = val
    

    def getCellValue(self, pos: tuple):
        return self.map[pos]


    def clone(self):
        grid_copy = Grid(self.dim)
        grid_copy.map = deepcopy(self.map)
        return grid_copy


    def get_neighbors(self, pos, only_available = False):
        """
        Description
        -----------
        The function returns the neighboring cells of a certain cell in the board, given its x,y coordinates

        Parameters
        -----------
        pos : position (x,y) whose neighbors are desired

        only_available (bool) : if True, the function will return only available neighboring cells. default = False
        """
        x,y     = pos
        range_x = range(max(x-1, 0), min(x+2, self.dim))
        range_y = range(max(y-1, 0), min(y+2, self.dim))
        neighbors = list({(a,b) for a in range_x for b in range_y} - {(x,y)})
        
        if only_available:
            return [neighbor for neighbor in neighbors if self.map[neighbor] == 0]
        
        return neighbors

    def move(self, move, player):
        new_pos, bomb = move
        old_pos = np.where(self.map == player)
        self.map[old_pos] = 0
        self.map[new_pos] = player
        self.map[bomb] = -1
        return

    def print_grid(self):
        print(self.map)