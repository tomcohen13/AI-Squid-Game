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

        # find move with best IS score
        am_scores = np.array([AM(state, self.player_num) for state in states])

        new_pos = available_moves[np.argmax(am_scores)]
        
        return new_pos

    def getTrap(self, grid : Grid):

        """EasyAI throws randomly to the immediate neighbors of the opponent"""
        
        # find players
        opponent = grid.find(3 - self.player_num)

        # find all available cells in the grid
        available_neighbors = grid.get_neighbors(opponent, only_available = True)

        # edge case - if there are no available cell around opponent, then 
        # player constitutes last trap and will win. throwing randomly.
        if not available_neighbors:
            return random.choice(grid.getAvailableCells())
            
        states = [grid.clone().trap(cell) for cell in available_neighbors]

        # find trap that minimizes opponent's moves
        is_scores = np.array([IS(state, 3 - self.player_num) for state in states])

        # throw to one of the available cells randomly
        trap = available_neighbors[np.argmin(is_scores)] 
    
        return trap


def AM(grid : Grid, player_num):

    available_moves = grid.get_neighbors(grid.find(player_num), only_available = True)

    return len(available_moves)

def IS(grid : Grid, player_num):

    # find all available moves by Player
    player_moves    = grid.get_neighbors(grid.find(player_num), only_available = True)
    
    # find all available moves by Opponent
    opp_moves       = grid.get_neighbors(grid.find(3 - player_num), only_available = True)
    
    return len(player_moves) - len(opp_moves)

