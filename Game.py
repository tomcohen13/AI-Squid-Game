
import numpy as np
from Grid import Grid
from ComputerAI import ComputerAI

PLAYER_TURN, COMPUTER_TURN = 0,1

class Game():
    def __init__(self, playerAI, computerAI = None, N = 7):
        '''
        Parameters
        -----------
        playerAI   - Human player AI, of type PlayerAI.
        computerAI - Human or Computer Opponent
        N  - dimension of grid; has to be an odd number.

        '''
        self.grid      = Grid(N)
        self.playerAI   = playerAI or ComputerAI() # That's you!
        self.computerAI = computerAI or ComputerAI() # That's your opponent
        self.dim        = N
        self.over       = False

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
    '''
    def get_neighbors(self, player):
        indices = np.where(self.board == player)
        x,y = list(zip(indices[0], indices[1]))[0]
        range_x = range(max(x-1, 0), min(x+2, self.dim))
        range_y = range(max(y-1, 0), min(y+2, self.dim))
        neighbors = {(a,b) for a in range_x for b in range_y} - {(x,y)}
        return neighbors
    '''
    def is_valid(self, grid, move):
        pos, bomb = move
        if (grid.getCellValue(pos) or grid.getCellValue(bomb)):
            return False
        return True

    def play(self):
        self.initialize_game()
        turn = PLAYER_TURN
        i = 0
        while not self.over and i < 6:

            grid_copy = self.grid.clone()

            move = None
            
            if turn == 0:
                
                print("Player's Turn!")

                # find best move; should return two coordinates - new position and bombed tile.
                move = self.playerAI.getMove(grid_copy)

                # if move is valid, perform it
                if self.is_valid(self.grid, move) and not self.is_over():
                    self.grid.move(move, turn + 1)
                
                else:
                    self.over = True
                    print("invalid Player AI move!")
                
                # trap = self.playerAI.getTrap()

                # if self.is_valid(self.grid, trap) and not self.is_over():
                    # self.grid.trap(trap, turn + 1)
                # else: 
                #   self.over = True
                #   print("Invalid trap!")

            else:
                print("Opponent's Turn")
                move = pos, bomb = self.computerAI.getMove(grid_copy)

                if self.is_valid(self.grid, move) and not self.is_over():
                    self.grid.move(move, turn + 1)
                else:
                    self.over = True
                    print("invalid Computer AI Move")
            turn = 1 - turn
            self.grid.print_grid()
            i += 1

        return self.is_over()

def main():
    playerAI = ComputerAI()
    computerAI = ComputerAI()
    game = Game(playerAI=playerAI, computerAI=computerAI, N = 7)
    result = game.play()
    if result == 1: 
        print("Player 1 wins!")
    elif result == 2:
        print("Player 1 loses!")

if __name__ == "__main__":
    main()