
from game import GameStateData
from game import Game
from agents import cliAgent, randomAgent, AlphaBetaAgent, MinimaxAgent
import sys, types, time, random, os, cmd
import copy
from agents import betterEvaluationFunction

class GameState:
    """
    A GameState specifies the full state of pieces played

    GameStates are used by the Game object to capture the actual state of the game and
    can be used by agents to reason about the game.
    """

    def __init__(self, board_size=9, captures_to_win=5, run_len_to_win=5, prevStateData=None):

        if prevStateData is not None: # Initial state
            self.data = GameStateData(board_size=board_size, 
                                      captures_to_win=captures_to_win, 
                                      run_len_to_win=run_len_to_win, prevStateData=prevStateData)
        else:
            self.data = GameStateData(board_size=board_size, 
                                      captures_to_win=captures_to_win, 
                                      run_len_to_win=run_len_to_win)
            
    def setTurn(self, agentIndex):
        self.data.turn = agentIndex

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
        for (loc, val) in self.data.board.items():
            if val == agentIndex + 1:
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
        return self.data.board[(x, y)]
    
    def getRunLengths(self):

        directions = [(1, 0), (1, 1), (0, 1), (-1, 1)]
        protected_p1 = []
        protected_p2 = []
        unprotected_p1 = []
        unprotected_p2 = []
        half_protected_p1 = []
        half_protected_p2 = []
        all_p1 = []
        all_p2 = []

        for (loc, start) in self.data.board.items():
            if start == 1: 
                for direction in directions:
                    run_length = 0
                    val = start
                    while val == 1: # move along direction, sampling positions
                        run_length += 1
                        new_x = loc[0] + (direction[0] * run_length)
                        new_y = loc[1] + (direction[1] * run_length)
                        try:
                            val = self.getBoardPosition(new_x, new_y)
                        except: # position out of bounds
                            break

                    try:
                        prev_val = self.getBoardPosition(loc[0] - direction[0], loc[1] - direction[1])
                    except: # position not in board or out of bounds
                        prev_val = None
                    try:
                        next_val = self.getBoardPosition(new_x, new_y)
                    except:
                        next_val = None

                    all_p1.append(run_length)

                    # establish the protection of the run
                    prev_x = loc[0] - direction[0]
                    prev_y = loc[1] - direction[1]
                    if new_x < self.data.board_size and new_x >= 0 \
                        and new_y < self.data.board_size and new_y >= 0:
                        if prev_x < self.data.board_size and prev_x >= 0 \
                            and prev_y < self.data.board_size and prev_y >= 0:
                            if (next_val == 2 and (prev_val == 0 or prev_val == None)) \
                                or ((next_val == 0 or next_val == None) and prev_val == 2):
                                half_protected_p1.append(run_length)
                            elif (next_val== 0 or next_val == None) and (prev_val == 0 or prev_val == None):
                                unprotected_p1.append(run_length)
                            elif next_val== 2 and prev_val == 2:
                                protected_p1.append(run_length)
                        else:
                            if next_val == 2:
                                protected_p1.append(run_length)
                            elif (next_val == 0 or next_val == None) and run_length > 2:
                                half_protected_p1.append(run_length)
                            elif (next_val == 0 or next_val == None) and run_length == 2:
                                unprotected_p1.append(run_length)
                    else:
                        if prev_x < self.data.board_size and prev_x >= 0 \
                            and prev_y < self.data.board_size and prev_y >= 0:
                            if prev_val == 2:
                                protected_p1.append(run_length)
                            elif (prev_val == 0 or prev_val == None) and run_length > 2:
                                half_protected_p1.append(run_length)
                            elif (prev_val == 0 or prev_val == None) and run_length == 2:
                                unprotected_p1.append(run_length)
                        else:
                            protected_p1.append(run_length)


            if start == 2:
                for direction in directions:
                    run_length = 0
                    val = start
                    while val == 2: # move along direction, sampling positions
                        run_length += 1
                        new_x = loc[0] + (direction[0] * run_length)
                        new_y = loc[1] + (direction[1] * run_length)
                        try:
                            val = self.getBoardPosition(new_x, new_y)
                        except: # position out of bounds
                            break

                    try:
                        prev_val = self.getBoardPosition(loc[0] - direction[0], loc[1] - direction[1])
                    except: # position not in board or out of bounds
                        prev_val = None
                    try:
                        next_val = self.getBoardPosition(new_x, new_y)
                    except:
                        next_val = None
                    
                    all_p2.append(run_length)

                    # establish the protection of the run
                    prev_x = loc[0] - direction[0]
                    prev_y = loc[1] - direction[1]
                    if new_x < self.data.board_size and new_x >= 0 \
                        and new_y < self.data.board_size and new_y >= 0:
                        if prev_x < self.data.board_size and prev_x >= 0 \
                            and prev_y < self.data.board_size and prev_y >= 0:
                            if (next_val == 1 and (prev_val == 0 or prev_val == None)) \
                                or ((next_val == 0 or next_val == None) and prev_val == 1):
                                half_protected_p2.append(run_length)
                            elif (next_val == 0 or next_val == None) and (prev_val == 0 or prev_val == None):
                                unprotected_p2.append(run_length)
                            elif next_val == 1 and prev_val == 1:
                                protected_p2.append(run_length)
                        else:
                            if next_val == 1:
                                protected_p2.append(run_length)
                            elif (next_val == 0 or next_val == None) and run_length > 2:
                                half_protected_p2.append(run_length)
                            elif (next_val == 0 or next_val == None) and run_length == 2:
                                unprotected_p2.append(run_length)
                    else:
                        if prev_x < self.data.board_size and prev_x >= 0 \
                            and prev_y < self.data.board_size and prev_y >= 0:
                            if prev_val == 1:
                                protected_p2.append(run_length)
                            elif (prev_val == 0 or prev_val == None) and run_length > 2:
                                half_protected_p2.append(run_length)
                            elif (prev_val == 0 or prev_val == None) and run_length == 2:
                                unprotected_p2.append(run_length)
                        else:
                            protected_p2.append(run_length)

        return (all_p1, all_p2, protected_p1, protected_p2, half_protected_p1, half_protected_p2, unprotected_p1, unprotected_p2)  

    def addPositionsInRadius(self, position, radius):
        new_positions = []
        for i in range(position[0] - radius, position[0] + radius):
            for j in range(position[1] - radius, position[1] + radius + 1):
                if i < 0 or i >= self.data.board_size:
                    continue
                if j < 0 or j >= self.data.board_size:
                    continue
                if (i, j) in list(self.data.board.keys()):
                    continue
                self.data.board[(i, j)] = 0    

        
    def isLose(self):
        if self.data.num_player_2_captures >= self.data.captures_to_win:
            return True
        p2 = self.getRunLengths()[1]
        if max(p2, default=0) >= self.data.run_len_to_win:
            return True
        if self.data.turn == 0 and len(playerRules.getLegalActions(self, 0)) == 0:
            return True
        return False

    def isWin(self):
        if self.data.num_player_1_captures >= self.data.captures_to_win:
            return True
        p1 = self.getRunLengths()[0]
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

    def __str__(self):
       
        board_grid = [[0 for i in range(self.data.board_size)] for j in range(self.data.board_size)]
        for (location, val) in self.data.board.items():
            board_grid[location[0]][location[1]] = val
            
        board_str = " _ "
        for i in range(self.data.board_size):
            if i < 10:
                board_str += f" {i} "
            else:
                board_str += f" {i}"

        board_str += "\n"
        for j in range(len(board_grid[0])):
            if j < 10:
                row_str = f" {j} "
            else:
                row_str = f" {j}"
            for i in range(len(board_grid)):
                val = board_grid[i][j]
                if val == 0:
                    row_str += "-|-"
                elif val == 1:
                    row_str += " 1 "
                elif val == 2:
                    row_str += " 2 "
                else:
                    raise Exception("invalid player index in board")
            row_str += "\n"
            board_str += row_str
        return board_str

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
        if agentIndex == 1:
            possibleActions = [loc for (loc, val) in state.data.board.items() if val == 0]
        else:
            possibleActions = []
            for i in range(state.data.board_size):
                for j in range(state.data.board_size):
                    if (i, j) in list(state.data.board.keys()):
                        if state.data.board[(i, j)] == 0:
                            possibleActions.append((i, j))
                    else:
                        possibleActions.append((i, j))
        return possibleActions

    @staticmethod
    def applyAction(state, action, agentIndex):
        try:
            action = tuple(action)
            assert(action[0] < state.data.board_size)
            assert(action[1] < state.data.board_size)
            if action in list(state.data.board.keys()):
                assert(state.data.board[action] == 0)
            if agentIndex == 0:  
                state.data.board[action] = agentIndex + 1  
                positions_freed = playerRules.is_capture(state, action, agentIndex)
                num_captures = len(positions_freed) / 2
                if agentIndex == 0:
                    state.data.num_player_1_captures += num_captures
                else:
                    state.data.num_player_2_captures += num_captures
                for position in positions_freed: # free positions on board
                    state.data.board[position] = 0

                state.addPositionsInRadius(action, 2)
            else:
                state.data.board[action] = agentIndex + 1  
                positions_freed = playerRules.is_capture(state, action, agentIndex)
                num_captures = len(positions_freed) / 2
                if agentIndex == 0:
                    state.data.num_player_1_captures += num_captures
                else:
                    state.data.num_player_2_captures += num_captures
                for position in positions_freed: # free positions on board
                    state.data.board[position] = 0
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


    # gameState = GameState()
    # gameState.data.board = {(1, 3): 1, (2, 2): 1, (3, 4): 2, (4, 4): 2}
    # # otherwise, calculate relative reward
    # (all_p1, all_p2, protected_p1, protected_p2, half_protected_p1, \
    #  half_protected_p2, unprotected_p1, unprotected_p2) = gameState.getRunLengths()
    
    # # number of protected runs
    # p1_doubles_prot = sum([i == 2 for i in protected_p1])
    # p2_doubles_prot = sum([i == 2 for i in protected_p2]) 
    # p1_triples_prot = sum([i == 3 for i in protected_p1]) 
    # p2_triples_prot = sum([i == 3 for i in protected_p2]) 
    # p1_quadruples_prot = sum([i == 4 for i in protected_p1])
    # p2_quadruples_prot = sum([i == 4 for i in protected_p2])

    # # number of unprotected runs
    # p1_doubles_unprot = sum([i == 2 for i in unprotected_p1])
    # p2_doubles_unprot = sum([i == 2 for i in unprotected_p2]) 
    # p1_triples_unprot = sum([i == 3 for i in unprotected_p1]) 
    # p2_triples_unprot = sum([i == 3 for i in unprotected_p2]) 
    # p1_quadruples_unprot = sum([i == 4 for i in unprotected_p1])
    # p2_quadruples_unprot = sum([i == 4 for i in unprotected_p2])

    # # number of half-protected runs
    # p1_doubles_half_prot = sum([i == 2 for i in half_protected_p1]) 
    # p2_doubles_half_prot = sum([i == 2 for i in half_protected_p2]) 
    # p1_triples_half_prot = sum([i == 3 for i in half_protected_p1]) 
    # p2_triples_half_prot = sum([i == 3 for i in half_protected_p2]) 
    # p1_quadruples_half_prot = sum([i == 4 for i in half_protected_p1])
    # p2_quadruples_half_prot = sum([i == 4 for i in half_protected_p2])

    # # Other features
    # p1_pieces = gameState.getNumPieces(0)
    # p2_pieces = gameState.getNumPieces(1)
    # p1_captures = gameState.getNumCaptures(0)
    # p2_captures = gameState.getNumCaptures(1) 
    
    # num_p1_doubles = sum([i == 2 for i in all_p1]) \
    #                     - sum([i == 3 for i in all_p1])
    # num_p2_doubles = sum([i == 2 for i in all_p2]) \
    #                     - sum([i == 3 for i in all_p2])
    # num_p1_triples = sum([i == 3 for i in all_p1]) \
    #                     - sum([i == 4 for i in all_p1])
    # num_p2_triples = sum([i == 3 for i in all_p2]) \
    #                     - sum([i == 4 for i in all_p2])
    # num_p1_quadruples = sum([i == 4 for i in all_p1])
    # num_p2_quadruples = sum([i == 4 for i in all_p2])  

    # print("number of values:")
    # print(num_p1_doubles)
    # print(p1_doubles_prot)
    # print(p1_doubles_unprot)
    # print(p1_doubles_half_prot)
    # print(gameState)
    # assert(num_p1_doubles == p1_doubles_prot + p1_doubles_unprot + p1_doubles_half_prot)
    # assert(num_p2_doubles == p2_doubles_prot + p2_doubles_unprot + p2_doubles_half_prot)
    # assert(num_p1_triples == p1_triples_prot + p1_triples_unprot + p1_triples_half_prot)
    # assert(num_p2_triples == p2_triples_prot + p2_triples_unprot + p2_triples_half_prot)
    # assert(num_p1_quadruples == p1_quadruples_prot + p1_quadruples_unprot + p1_quadruples_half_prot)
    # assert(num_p2_quadruples == p2_quadruples_prot + p2_quadruples_unprot + p2_quadruples_half_prot)
