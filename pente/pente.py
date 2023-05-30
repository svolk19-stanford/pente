
from game import GameStateData
from game import Game
from agents import cliAgent, randomAgent, AlphaBetaAgent, MinimaxAgent
import sys, types, time, random, os, cmd
import copy


class GameState:
    """
    A GameState specifies the full state of pieces played

    GameStates are used by the Game object to capture the actual state of the game and
    can be used by agents to reason about the game.
    """

    def __init__(self, board_size=4, captures_to_win=5, run_len_to_win=4, prevStateData=None):

        if prevStateData is not None: # Initial state
            self.data = GameStateData(board_size=board_size, 
                                      captures_to_win=captures_to_win, 
                                      run_len_to_win=run_len_to_win, prevStateData=prevStateData)
        else:
            self.data = GameStateData(board_size=board_size, 
                                      captures_to_win=captures_to_win, 
                                      run_len_to_win=run_len_to_win)

    def getLegalActions(self, agentIndex=0):
        """
        Returns the legal actions for the agent specified.
        """
        if self.isWin() or self.isLose(): return []

        return playerRules.getLegalActions(self, agentIndex)

    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        # Check that successors exist
        if self.isWin() or self.isLose(): raise Exception('Can\'t generate a successor of a terminal state.')

        # Copy current state
        state = GameState(board_size=self.data.board_size, 
                          run_len_to_win=self.data.run_len_to_win,
                          captures_to_win=self.data.captures_to_win,
                          prevStateData=self.deepCopyData())
        
        # Let agent's logic deal with its action's effects on the board
        playerRules.applyAction(state, action, agentIndex)
        return state

    def getScore(self):
        return self.data.score

    def getNumPieces(self, agentIndex):
        total = 0
        for i in range(self.data.board_size):
            for j in range(self.data.board_size):
                if self.getBoardPosition(i, j) == agentIndex + 1:
                    total += 1
        return total
    
    def getNumCaptures(self, agentIndex):
        if agentIndex == 0:
            return self.data.num_player_1_captures
        else:
            return self.data.num_player_2_captures

    def getBoard(self):
        return self.data.board
    
    def getBoardPosition(self, x, y):
        assert(x < self.data.board_size and x >= 0)
        assert(y < self.data.board_size and y >= 0)
        return self.data.board[x][y]
    
    def getRunLengths(self):

        directions = [(1, 0), (1, 1), (0, 1)]
        run_lengths_p1 = []
        run_lengths_p2 = []

        for i in range(self.data.board_size):
            for j in range(self.data.board_size):
                val = self.getBoardPosition(i, j)
                if val == 1: 
                    for direction in directions:
                        run_length = 0
                        val = self.getBoardPosition(i, j)
                        while val == 1: # move along direction, sampling positions
                            run_length += 1
                            new_x = i + (direction[0] * run_length)
                            new_y = j + (direction[1] * run_length)
                            try:
                                val = self.getBoardPosition(new_x, new_y)
                            except: # position out of bounds
                                break
                        run_lengths_p1.append(run_length)
                if val == 2:
                    for direction in directions:
                        run_length = 0
                        val = self.getBoardPosition(i, j)
                        while val == 2: # move along direction, sampling positions
                            run_length += 1
                            new_x = i + (direction[0] * run_length)
                            new_y = j + (direction[1] * run_length)
                            try:
                                val = self.getBoardPosition(new_x, new_y)
                            except: # position out of bounds
                                break
                        run_lengths_p2.append(run_length)

        return (run_lengths_p1, run_lengths_p2)        
        
    def isLose(self):
        if self.data.num_player_2_captures >= self.data.captures_to_win:
            return True
        (p1, p2) = self.getRunLengths()
        if max(p2, default=0) >= self.data.run_len_to_win:
            return True
        if self.data.turn == 0 and len(playerRules.getLegalActions(self, 0)) == 0:
            return True
        return False

    def isWin(self):
        if self.data.num_player_1_captures >= self.data.captures_to_win:
            return True
        (p1, p2) = self.getRunLengths()
        if max(p1, default=0) >= self.data.run_len_to_win:
            return True
        if self.data.turn == 1 and len(playerRules.getLegalActions(self, 1)) == 0:
            return True
        return False
        
    def deepCopyData(self):
        data = copy.deepcopy(self.data)
        return data


    def __eq__( self, other ):
        """
        Allows two states to be compared.
        """
        if other is None: return False
        return self.data == other.data

    def __hash__( self ):
        """
        Allows states to be keys of dictionaries.
        """
        return hash( self.data )

    def __str__( self ):

        return str(self.data)

class playerRules:
    """
    These functions govern how a player interacts with their environment under
    the classic game rules.
    """
    @staticmethod
    def getLegalActions(state, agentIndex):
        """
        Returns a list of possible actions.
        """
        possibleActions = []
        for i, row in enumerate(state.data.board):
            for j, val in enumerate(row):
                if val == 0:
                    possibleActions.append((i, j))
        return possibleActions

    @staticmethod
    def applyAction(state, action, agentIndex):
        try:
            assert(action[0] < state.data.board_size)
            assert(action[1] < state.data.board_size)
            assert(state.data.board[action[0]][action[1]] == 0)
            state.data.board[action[0]][action[1]] = agentIndex + 1  
            positions_freed = playerRules.is_capture(state, action, agentIndex)
            num_captures = len(positions_freed) / 2
            if agentIndex == 0:
                state.data.num_player_1_captures += num_captures
            else:
                state.data.num_player_2_captures += num_captures
            for position in positions_freed: # free positions on board
                state.data.board[position[0]][position[1]] = 0
        except:
            raise Exception("Invalid move")
        
    @staticmethod
    def is_capture(state, action, agentIndex):
        """
        determine whether a move creates a capture. Returns a list of liberated 
        gridpoints to be reset to 0.
        """
        # list of 8 directions in which to check for a capture, defined as the 
        # update values for a given position 
        directions = [(-1, 0), (-1, -1), (0, -1), # left, up left, up
                      (1, -1), (1, 0), (1, 1), # up right, right, down right
                      (0, 1), (-1, 1)] # down, down left
        positions_freed = []
        # this template is what a capture looks like in any direction from starting
        if agentIndex == 0:
            capture_template = [2, 2, 1] 
        else:
            capture_template = [1, 1, 2] 

        for direction in directions:
            position_vals = []
            positions = []
            for i in range(1, 4): # move three along direction, sampling positions
                new_x = action[0] + (direction[0] * i)
                new_y = action[1] + (direction[1] * i)
                try:
                    position_vals.append(state.getBoardPosition(new_x, new_y))
                    positions.append((new_x, new_y))
                except: # position out of bounds
                    break
            if position_vals == capture_template: #capture along direction
                positions_freed += [i for i in positions[:-1]]
        return positions_freed


if __name__ == '__main__':
    import time
    tic = time.perf_counter()
    player1 = cliAgent()
    player2 = AlphaBetaAgent()
    new_state = GameState()
    game = Game(state=new_state, agents=[player1, player2])
    game.run()
    toc = time.perf_counter()
    print("total times: " + str(toc - tic))
