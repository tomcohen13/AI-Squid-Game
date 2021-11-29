import numpy as np
import random
import sys
import os 
# setting path to parent directory
sys.path.append(os.getcwd())

from BaseAI import BaseAI
from Grid import Grid

OPPONENT = lambda player: 3 - player

class EasyAI(BaseAI):

    def __init__(self, initial_position = None) -> None:
        super().__init__()
        self.pos = initial_position
        self.player_num = None

    def setPosition(self, new_pos: tuple):
        self.pos = new_pos
    
    def getPosition(self):
        return self.pos 

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid):
        """ Returns a random, valid move """
        
        # find all available moves 
        available_moves = grid.get_neighbors(self.pos, only_available = True)

        # make random move
        new_pos = random.choice(available_moves) if available_moves else None
        
        return new_pos

    def getTrap(self, grid : Grid):

        """EasyAI throws randomly to the immediate neighbors of the opponent"""
        
        # find opponent
        opponent = grid.find(3 - self.player_num)
        
        # find all available cells surrounding Opponent
        available_cells = grid.get_neighbors(opponent, only_available=True)

        # throw to one of the available cells randomly
        trap = random.choice(available_cells)
    
        return trap