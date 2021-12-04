import numpy as np
import random
import sys
import os 
# setting path to parent directory
sys.path.append(os.getcwd())

from BaseAI import BaseAI
from Grid import Grid

class MediumAI(BaseAI):

    def __init__(self, position = None) -> None:
        super().__init__()
        self.pos = position
        self.player_num = None

    def setPosition(self, new_pos: tuple):
        self.pos = new_pos
    
    def getPosition(self):
        return self.pos 

    def setPlayerNum(self, num):
        self.player_num = num

    def getPlayerNum(self):
        return self.player_num

    def getMove(self, grid : Grid):
        """ Moves based on available moves """
        
        # find all available moves 
        available_moves = grid.get_neighbors(self.pos, only_available = True)

        states = [grid.clone().move(mv, self.player_num) for mv in available_moves]

        # find move with best AM score
        am_scores = np.array([AM(state, self.player_num) for state in states])

        new_pos = available_moves[np.argmax(am_scores)]
        
        return new_pos

    def getTrap(self, grid : Grid):

        """MediumAI throws trap to the position that minimizes AM score of Opponent's immediate neigghbors"""
        
        # find opponent
        opponent = grid.find(3 - self.player_num)

        # find all available cells around opponent
        available_cells = grid.get_neighbors(opponent, only_available = True)

        # edge case - if there are no available cell around opponent, 
        # player constitutes last trap and wins. Throwing randomly.
        if not available_cells:
            return random.choice(grid.getAvailableCells())
        
        # make child states
        states = [grid.clone().trap(cell) for cell in available_cells]

        # find AM scores of child states
        am_scores = np.array([AM(state, 3 - self.player_num) for state in states])

        # throw to the cell that minimizes that
        trap = available_cells[np.argmin(am_scores)] 
    
        return trap

def AM(grid : Grid, player_num):

    available_moves = grid.get_neighbors(grid.find(player_num), only_available = True)

    return len(available_moves)

