import numpy as np
import random
from BaseAI import BaseAI
from Grid import Grid

class EasyAI(BaseAI):

    def __init__(self, initial_position = None) -> None:
        super().__init__()
        self.pos = initial_position

    def setPosition(self, new_pos: tuple):
        self.pos = new_pos
    
    def getPosition(self):
        return self.pos 

    def getMove(self, grid):
        """ Returns a random, valid move """
        
        # find all available moves 
        available_moves = grid.get_neighbors(self.pos, only_available = True)

        # make random move
        new_pos = random.choice(available_moves) if available_moves else None
        
        self.setPosition(new_pos)

        return new_pos

    def getTrap(self, grid : Grid):
        
        # find all available cells in the grid
        available_cells = grid.getAvailableCells()

        # find all available cells
        trap = random.choice(available_cells) if available_cells else None

        return trap