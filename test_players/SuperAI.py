import numpy as np
import random
import time
import sys
import os 
# setting path to parent directory
sys.path.append(os.getcwd())
from BaseAI import BaseAI
from Grid import Grid
from Utils import manhattan_distance

MAX_DEPTH = 3
MOVE_TIME_LIMIT = 0.49
TRAP_TIME_LIMIT = 0.49

class SuperAI(BaseAI):

    def __init__(self, position = None) -> None:
        super().__init__()
        self.pos = position
        self.player_num = None

    def getPosition(self):
        return self.pos
    
    def setPosition(self, new_position):
        self.pos = new_position
    
    def getPlayerNum(self):
        return self.player_num
        
    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid : Grid):
        move, util = self._best_move(grid)

        return move

    def _best_move(self, grid : Grid):

        start = time.process_time()

        # Funny edge case: check if player has won by trapping Opponent with previous move.
        if len(grid.get_neighbors(grid.find(3 - self.player_num), only_available=True)) == 0:
            return grid.getAvailableCells()[0], 1000
        
        return self.maximize_move(grid, alpha = -np.inf, beta = np.inf, depth = 0, start_time = start)

    def maximize_move(self, grid : Grid, alpha : float, beta : float, depth : int, start_time):
        """ 
        Description
        -----------
        The Max node of the Minimax search tree of Move.
        The function maximizes utility over a *static* opponent throwing traps strategically.
        Uses Alpha-Beta Pruning to skip unpromising branches of the tree.

        Parameters
        ----------
        grid (Grid) : a state of the game described by a Grid object.

        alpha : Maximizer's lower bound on utility

        beta : Minimizer's upper bound on utility

        depth : current depth of the state in the search tree

        start_time : a timestamp of when the turn has started to make sure move does not exceed it.

        Returns
        -------
        The action corresponding to the maximum utility move, given an intelligent opponent.

        """
        if self.terminal_test(grid, time = time.process_time() - start_time, depth = depth, mode = 'move'):
            return None, self.utility(grid)
        
        maxMove, maxUtility = None, -np.inf
        
        available_moves = grid.get_neighbors(grid.find(self.player_num), only_available = True)

        states = [grid.clone().move(mv, self.player_num) for mv in available_moves]
       
        ## add sorting of moves and states?
        children = list(zip(available_moves, states))
        children.sort(key = lambda x: OSL(x[1], self.player_num))
        for (move, state) in children:

            _, utility = self.minimize_move(state, alpha, beta, depth + 1, start_time)

            if utility > maxUtility:
                maxMove, maxUtility = move, utility
            
            # if Max lower bound crosses Min's upper bound - break
            if maxUtility >= beta:
                break

            # update lower bound
            alpha = max(alpha, maxUtility)

        return maxMove, maxUtility

    def chance_move(self, state : Grid, p : float, alpha, beta, depth, start_time):
        """
        Description
        -----------

        # multiply incoming node by probability.
        Parameters
        ---------

        Returns: 

        """
        
        # 
        
        expected_utility = p * self.maximize_move(state, alpha, beta, depth + 1, start_time)[1]

        return None, expected_utility

    def minimize_move(self, grid : Grid, alpha, beta, depth, start_time):
        """ 
        Description
        -----------
        The Min node of the Minimax search tree of Move, which simulates Opponent's throw actions. 
        
        The function minimizes utility over the player's future moves by finding ideal position to place a trap.
        
        Uses Alpha-Beta Pruning to skip unpromising branches of the tree.

        Parameters
        ----------
        grid (Grid) : a state of the game described by a Grid object.

        alpha : Maximizer's lower bound on utility

        beta : Minimizer's upper bound on utility

        depth : current depth of the state in the search tree

        start_time : a timestamp of when the turn has started to make sure move does not exceed it.

        Returns
        -------
        The action corresponding to the maximum utility move, given an intelligent opponent.
        
        """
        if self.terminal_test(grid, time = time.process_time() - start_time, depth = depth, mode = 'move'):
            return None, self.utility(grid)

        minChild, minUtility = None, np.inf
        # 
        actions = grid.get_neighbors(grid.find(self.player_num), only_available=True)
        
        states = [grid.clone().trap(pos = a) for a in actions]
        
        opponent_pos = grid.find(3 - self.player_num)

        probabilities = [compute_p(opponent_pos, a) for a in actions]
        # probably sort moves based on heuristic

        for (action, state, p) in zip(actions, states, probabilities):

            _, utility = self.chance_move(state, p, alpha, beta, depth, start_time)

            if utility < minUtility:
                minChild, minUtility = action, utility
            
            if minUtility <= alpha:
                break

            beta = min(beta, minUtility)

        return minChild, minUtility


    def terminal_test(self, state : Grid, time, depth, mode = 'move'):
        
        lose = not state.get_neighbors(state.find(self.player_num), only_available=True)
        
        win  = not state.get_neighbors(state.find(3 - self.player_num), only_available=True)

        if mode == 'move' :
            return lose or win or time >= MOVE_TIME_LIMIT or depth >= MAX_DEPTH
        else :
            return lose or win or time >= TRAP_TIME_LIMIT or depth >= MAX_DEPTH

    def getTrap(self, grid : Grid):
        trap, _ = self._best_trap(grid)
        return trap

    def _best_trap(self, grid: Grid):
        start = time.process_time()
        if len(grid.get_neighbors(grid.find(3 - self.player_num), only_available=True)) == 0:
            return grid.getAvailableCells()[0], 100
        return self.maximize_trap(grid, -np.inf, np.inf, depth = 0, start_time = start)


    def maximize_trap(self, grid : Grid, alpha, beta, depth, start_time):

        if self.terminal_test(grid, time.process_time() - start_time, depth, mode = 'trap'):
            return None, self.utility(grid)
        
        maxUtility = -np.inf
        
        # only consider immediate neighbors of Opponent
        actions = grid.get_neighbors(grid.find(3 - self.player_num), only_available = True)
        
        # create states corresponding to each action
        states = [grid.clone().trap(target) for target in actions]

        probabilities = [compute_p(self.pos, target) for target in actions]

        for (action, state, p) in zip(actions, states, probabilities):

            # _, utility = self.minimize_trap(state, alpha, beta, depth + 1, start_time)
            _, utility = self.chance_trap(state, p, alpha, beta, depth, start_time)

            if utility > maxUtility:
                maxTrap, maxUtility = action, utility

            if utility >= beta:
                break
            
            alpha = max(alpha, utility)

        return maxTrap, maxUtility
        
    def chance_trap(self, state : Grid, p, alpha, beta, depth, start_time):
        expected_utility = p * self.minimize_move(state, alpha, beta, depth + 1, start_time)[1]
        return None, expected_utility

    def minimize_trap(self, grid : Grid, alpha, beta, depth, start_time):
        
        if self.terminal_test(grid, time.process_time() - start_time, depth, mode = 'trap'):
            return None, self.utility(grid)

        minMove, minUtility = None, np.inf
        
        # find all possible immediate moves by Opponent
        available_moves = grid.get_neighbors(grid.find(3 - self.player_num), only_available=True)

        # create states corresponding to those possible moves
        states = [grid.clone().move(mv, player = 3 - self.player_num) for mv in available_moves]

        for (move, state) in zip(available_moves, states):

            _, utility = self.maximize_trap(state, alpha, beta, depth + 1, start_time)
            
            if utility < minUtility:
                minMove, minUtility = move, utility

            if utility <= alpha: 
                break

            beta = min(beta, minUtility)

        return minMove, minUtility


    def utility(self, state : Grid) -> float:

        # if win
        if not state.get_neighbors(state.find(3 - self.player_num), only_available=True):
            return 100
        # if lose
        if not state.get_neighbors(state.find(self.player_num), only_available=True):
            return -100
        
        # return 0.7 * AIS(state, player_num = self.player_num) + 0.5 * OSL(state, player_num = self.player_num)
        # return M2B(state, self.player_num) + AIS(state, self.player_num) #+ 0.25 * OSL(state, self.player_num) 
        return OTD(state, player_num=self.player_num)


def M2B(state : Grid, player_num : int) -> float:
    """
    Moves to Board
    """
    p = len(state.get_neighbors(state.find(player_num), only_available=True))
    o = len(state.get_neighbors(state.find(3 - player_num), only_available=True))
    m = len(state.getAvailableCells())
    n = state.getMap().shape[0]

    return 2 * p * m / n - o

def OTD(state : Grid, player_num) -> float:
    N = state.getMap().shape[0] 
    m = len(state.getAvailableCells()) / N ** 2 
    p = len(state.get_neighbors(state.find(player_num), only_available = True)) # player moves
    o = len(state.get_neighbors(state.find(3 - player_num), only_available = True))
    return 2*p - o if m > 0.5 else p - 2*o


def AIS(grid : Grid, player_num):

    # find all available moves by Player
    player_moves    = grid.get_neighbors(grid.find(player_num), only_available = True)
    
    # find all available moves by Opponent
    opp_moves       = grid.get_neighbors(grid.find(3 - player_num), only_available = True)
    
    return 2 * len(player_moves) - len(opp_moves)

def OSL(state : Grid, player_num) -> float:
    """
    One-Step-Lookahead heuristics

    Description
    ----------
    function computes the sum of the num of available moves one step ahead.

    Parameters:
    - state (Grid) : a game state, containing board, players, traps.

    - player_num : player number


    """
    available_moves = state.get_neighbors(state.find(player_num))

    child_states = [state.clone().move(pos, player_num) for pos in available_moves]

    return sum([len(s.get_neighbors(pos, only_available = True)) for pos, s in zip(available_moves, child_states)])


def compute_p(position, target):
    p = 1 - 0.05*(manhattan_distance(position, target) - 1)
    return p