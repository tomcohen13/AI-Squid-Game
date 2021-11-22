import numpy as np
from Grid import Grid
from ComputerAI import ComputerAI
from Displayer import Displayer
from PlayerAI import PlayerAI
from Utils import *

PLAYER_TURN, COMPUTER_TURN = 0,1

class Game():
    def __init__(self, playerAI = None, computerAI = None, N = 7, displayer = None):
        '''
        Parameters
        -----------
        playerAI   - Human player AI, of type PlayerAI. default = None 

        computerAI - Human or Computer Opponent. default = None
        
        N  - dimension of grid.

        '''
        self.grid       = Grid(N)
        self.playerAI   = playerAI or ComputerAI() 
        self.computerAI = computerAI or ComputerAI() 
        self.dim        = N
        self.over       = False
        self.displayer = displayer

    def initialize_game(self):

        p1_index, p2_index = (0, self.dim // 2), (self.dim -1, self.dim // 2)
        
        self.grid.setCellValue(p1_index, 1)
        self.playerAI.setPosition(p1_index)

        self.grid.setCellValue(p2_index, 2)
        self.computerAI.setPosition(p2_index)
        
    def is_over(self):

        # check if Player has won
        # find available neighbors of player 1
        opponent_neighbors = self.grid.get_neighbors(self.computerAI.getPosition(), only_available=True)
        # if none - win
        if len(opponent_neighbors) == 0:
            self.over = True
            return 1

        # check if Opponent has won
        player_neighbors = self.grid.get_neighbors(self.playerAI.getPosition(), only_available=True)

        if len(player_neighbors) == 0:
            self.over = True
            return 2
        
        else: 
            return 0

    def is_valid_move(self, grid : Grid, move : tuple):
        '''Validate move - cell has to be 0'''
        if grid.getCellValue(move) == 0:
            return True

        return False

    def is_valid_trap(self, grid : Grid, trap : tuple):
        '''Validate trap - cell can't be greater than zero'''

        if grid.getCellValue(trap) > 0:
            return False
        return True

    def throw(self, player, grid : Grid, intended_position : tuple) :
        '''
        Description
        ----------
        Function returns the coordinates in which the trap lands, given an intended location.

        Parameters
        ----------

        player : the player throwing the trap

        grid : current game Grid

        intended position : the (x,y) coordinates to which the player intends to throw the trap to.
        '''
        print(intended_position)
        # find neighboring cells
        neighbors = grid.get_neighbors(intended_position)

        neighbors = [neighbor for neighbor in neighbors if grid.getCellValue(neighbor) <= 0]
        n = len(neighbors)
        
        probs = np.ones(1 + n)
        
        # compute probability of success, p
        p = 1 - 0.05*(manhattan_distance(player.getPosition(), intended_position) - 1)

        probs[0] = p

        probs[1:] = np.ones(len(neighbors)) * ((1-p)/n)

        # add desired coordinates to neighbors
        neighbors.insert(0, intended_position)
        
        result = np.random.choice(np.arange(n + 1), p = probs)
        
        return neighbors[result]



    def play(self):
        
        self.initialize_game()

        self.displayer.display(self.grid)

        turn = PLAYER_TURN
        
        while not self.over:

            grid_copy = self.grid.clone()

            move = None
            
            if turn == 0:
                
                print("Player's Turn: ")

                # find best move; should return two coordinates - new position and bombed tile.
                move = self.playerAI.getMove(grid_copy)

                # if move is valid, perform it
                if self.is_valid_move(self.grid, move):
                    self.grid.move(move, turn + 1)
                    print(f"Moving to {move}")
                else:
                    self.over = True
                    print(f"Tried to move to : {move}")
                    print("invalid Player AI move!")
                
                intended_trap = self.playerAI.getTrap(self.grid.clone())

                if self.is_valid_trap(self.grid, intended_trap) and not self.is_over():
                    trap = self.throw(self.playerAI, self.grid, intended_trap)
                    self.grid.trap(trap)
                    print(f"Placing a trap in {trap}")

                else: 
                    self.over = True
                    print(f"Tried to put trap in {trap}")
                    print("Invalid trap!")

            else:
                
                print("Opponent's Turn : ")
                
                # make move
                move = self.computerAI.getMove(grid_copy)

                # check if move is valid; perform if it is.
                if self.is_valid_move(self.grid, move) and not self.is_over():
                    self.grid.move(move, turn + 1)
                    print(f"Moving to {move}")

                else:
                    self.over = True
                    print("invalid Computer AI Move")

                intended_trap = self.computerAI.getTrap(self.grid.clone())

                if self.is_valid_trap(self.grid, intended_trap) and not self.is_over():
                    trap = self.throw(self.computerAI, self.grid, intended_trap)
                    self.grid.trap(trap)
                    print(f"Placing a trap in {trap}")

            turn = 1 - turn
            self.displayer.display(self.grid)
            # self.grid.print_grid()

        return self.is_over()

def main():
    playerAI = ComputerAI() # change this to PlayerAI() to test your player!
    computerAI = ComputerAI()
    displayer = Displayer()
    game = Game(playerAI = playerAI, computerAI = computerAI, N = 7, displayer=displayer)
    

    result = game.play()
    if result == 1: 
        print("Player 1 wins!")
    elif result == 2:
        print("Player 1 loses!")

if __name__ == "__main__":
    main()