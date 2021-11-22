import numpy as np
from Grid import Grid
from ComputerAI import ComputerAI
from Displayer import Displayer
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

        # check if player 1 has won
        if not any([self.grid.getCellValue(neighbor) == 0 for neighbor in self.grid.get_neighbors(self.computerAI.getPosition())]):
            self.over = True
            return 1

        # check if player 2 has won
        elif not any([self.grid.getCellValue(neighbor) == 0 for neighbor in self.grid.get_neighbors(self.playerAI.getPosition())]):
            self.over = True
            return 2
        
        else: return 0

    def is_valid(self, grid, move):
        """
        Validate move by checking if the cell has a value of anything but 0.
        """
        if grid.getCellValue(move) > 0:
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
                if self.is_valid(self.grid, move) and not self.is_over():
                    self.grid.move(move, turn + 1)
                    print(f"Moving to {move}")
                else:
                    self.over = True
                    print("invalid Player AI move!")
                
                intended_trap = self.playerAI.getTrap(self.grid.clone())

                if self.is_valid(self.grid, intended_trap) and not self.is_over():
                    trap = self.throw(player=self.playerAI, grid=self.grid, intended_position=intended_trap)
                    self.grid.trap(trap)
                    print(f"Placing a trap in {trap}")

                else: 
                    self.over = True
                    print("Invalid trap!")

            else:
                
                print("Opponent's Turn : ")
                
                # make move
                move = self.computerAI.getMove(grid_copy)

                # check if move is valid; perform if it is.
                if self.is_valid(self.grid, move) and not self.is_over():
                    self.grid.move(move, turn + 1)
                    print(f"Moving to {move}")

                else:
                    self.over = True
                    print("invalid Computer AI Move")

                intended_trap = self.computerAI.getTrap(self.grid.clone())

                if self.is_valid(self.grid, intended_trap) and not self.is_over():
                    trap = self.throw(player=self.computerAI, grid=self.grid, intended_position=intended_trap)
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