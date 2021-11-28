import random
from BaseAI import BaseAI
import numpy as np
from Grid import Grid

# TO BE IMPLEMENTED
# 
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        
    
    def getMove(self, grid: Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        You may adjust the input variables as you wish but output has to be the coordinates.
        
        """
        pass

    def getTrap(self, grid : Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        
        Here you'll need to implement the Expectiminimax algorithm, taking into account the probabilities of it landing
        in the positions you wan. Note that you are not required to account for the probabilities of it landing in a
        different cell.

        You may adjust the input variables as you wish but output has to be the coordinates.
        
        """
        pass
    
    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position 
        

    