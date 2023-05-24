
from game import GameStateData
from game import Game
from agents import cliAgent, randomAgent
import sys, types, time, random, os, cmd
import copy


class GameState:
    """
    A GameState specifies the full state of pieces played

    GameStates are used by the Game object to capture the actual state of the game and
    can be used by agents to reason about the game.
    """

    def __init__(self, board_size=19, prevStateData=None):

        if prevStateData is not None: # Initial state
            self.data = GameStateData(board_size=board_size, prevStateData=prevStateData)
        else:
            self.data = GameStateData(board_size=board_size)

    def getLegalActions(self, agentIndex=0):
        """
        Returns the legal actions for the agent specified.
        """
        if self.isWin() or self.isLose(): return []

        return playerRules.getLegalActions(self.data.board, agentIndex)

    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        # Check that successors exist
        if self.isWin() or self.isLose(): raise Exception('Can\'t generate a successor of a terminal state.')

        # Copy current state
        state = GameState(board_size=self.data.board_size, prevStateData=self.deepCopyData())

        # Let agent's logic deal with its action's effects on the board
        playerRules.applyAction(state, action, agentIndex)
        return state

    def getScore(self):
        return self.data.score

    def getGameStateInfo():
        #TODO

        # this method will return relevant info about the gamestate
        # number adjacent pairs, lengths of runs, number of pieces, number of captures, etc.
        # this may be split into multiple methods
        return
    
    def getBoard(self):
        return self.data.board

    def isLose(self):
        #TODO: uncomment once the rest of the class is in place
        # if self.data.num_player_2_captures >= self.data.captures_to_win:
        #     return True
        # if max(self.getRunLengths(1)) >= self.data.run_len_to_win:
        #     return True
        # if self.data.turn == 0 and len(playerRules.getLegalActions(self, 0)) == 0:
        #     return True
        return False

    def isWin(self):
        #TODO: uncomment once the rest of the class is in place
        # if self.data.num_player_1_captures >= self.data.captures_to_win:
        #     return True
        # if max(self.getRunLengths(0)) >= self.data.run_len_to_win:
        #     return True
        # if self.data.turn == 1 and len(playerRules.getLegalActions(self, 1)) == 0:
        #     return True
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
    def getLegalActions(board, agentIndex):
        """
        Returns a list of possible actions.
        """
        possibleActions = []
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 0:
                    possibleActions.append((j, i))
        return possibleActions

    @staticmethod
    def applyAction(state, action, agentIndex):
        try:
            assert(action[0] < state.data.board_size)
            assert(action[1] < state.data.board_size)
            assert(state.data.board[action[1]][action[0]] == 0)
            state.data.board[action[1]][action[0]] = agentIndex + 1       
        except:
            raise Exception("Invalid move")

if __name__ == '__main__':
    import time
    tic = time.perf_counter()
    player1 = cliAgent()
    player2 = randomAgent()
    new_state = GameState()
    game = Game(state=new_state, agents=[player1, player2])
    game.run()
    toc = time.perf_counter()
    print("total times: " + str(toc - tic))
