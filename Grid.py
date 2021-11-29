from copy import deepcopy
import numpy as np


class Grid():
    
    def __init__(self, N = 7) -> None:
        self.dim  = N
        self.map = np.zeros((N,N)) # empty board
    

    def getAvailableCells(self):
        """
        Returns all available cells in the grid in the form of [(x_0,y_0), ..., (x_n, y_n)]
        """
        
        return [(x,y) for x,y in np.argwhere(self.map == 0)]
    
    def getMap(self):
        return self.map

    def setCellValue(self, pos: tuple, val):
        self.map[pos] = val

    def getCellValue(self, pos: tuple):
        return self.map[pos]

    def clone(self):
        """
        Makes a full copy of current grid
        """
        grid_copy = Grid(self.dim)
        grid_copy.map = deepcopy(self.map)
        return grid_copy

    def find(self, player_num : int):
        """Find a player given the player's number."""
        
        assert(player_num in [1,2])
        
        result = tuple(np.argwhere(self.map == player_num)[0])

        return result

    def get_neighbors(self, pos, only_available = False):

        """
        Description
        -----------
        The function returns the neighboring cells of a certain cell in the board, given its x,y coordinates

        Parameters
        -----------
        pos : position (x,y) whose neighbors are desired

        only_available (bool) : if True, the function will return only available neighboring cells. 
                                default = False
        
        """
        x,y = pos
        
        valid_range = lambda t: range(max(t-1, 0), min(t+2, self.dim))

        # find all neighbors
        neighbors = list({(a,b) for a in valid_range(x) for b in valid_range(y)} - {(x,y)})
        
        # select only neighboring cells which aren't occupying by a player or trap
        if only_available:
            return [neighbor for neighbor in neighbors if self.map[neighbor] == 0]
        
        return neighbors


    def move(self, move, player):

        """
        Description 
        -----------
        Apply a move by specified player to the grid. 

        Parameters
        -----------

        move: coordinates of new position to which the player decides to move

        player: the identifier of the player (1 for human, 2 for computer)

        Returns
        -------
        the grid with the new configuration. 

        """

        old_pos = np.where(self.map == player)
        self.map[old_pos] = 0
        self.map[move] = player

        return self

    def trap(self, pos):
        """
        Description 
        -----------
        Apply a trap to specified loaction

        Parameters
        -----------

        pos: a tuple (x,y) reprsenting the coordinates in which to place trap

        Returns
        -------
        the grid with the new configuration.

        """
        self.map[pos] = -1

        return self

    def print_grid(self):
        print(self.map)