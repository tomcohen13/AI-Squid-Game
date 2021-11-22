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

        The function should return a tuple of (x,y) coordinates to which the player *wants* 
        to throw the trap. 
        
        You do not need to account for probabilities. We've implemented that for you.

        You may adjust the input variables as you wish but output has to be the coordinates.
        
        """
        pass

    def getPosition(self):
        pass
        

    