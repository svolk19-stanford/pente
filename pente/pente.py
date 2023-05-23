
from game import GameStateData
from game import Game
from game import Actions
import util
import sys, types, time, random, os, cmd

class GameState:
    """
    A GameState specifies the full state of pieces played

    GameStates are used by the Game object to capture the actual state of the game and
    can be used by agents to reason about the game.
    """

    def __init__(self, prevState=None):

        if prevState is not None: # Initial state
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()

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
        state = GameState(self)

        # Let agent's logic deal with its action's effects on the board
        playerRules.applyAction(state, action, agentIndex)

        # Book keeping
        return state

    def getLegalActions(self):
        return self.getLegalActions(0)

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
    
    def getRunLengths(self, agentIndex):
        return

    def isLose(self):
        if self.data.num_player_2_captures >= self.data.captures_to_win:
            return True
        if max(self.getRunLengths(1)) >= self.data.run_len_to_win:
            return True
        if self.data.turn == 0 and len(playerRules.getLegalActions(self, 0)) == 0:
            return True
        return False

    def isWin(self):
        if self.data.num_player_1_captures >= self.data.captures_to_win:
            return True
        if max(self.getRunLengths(0)) >= self.data.run_len_to_win:
            return True
        if self.data.turn == 1 and len(playerRules.getLegalActions(self, 1)) == 0:
            return True
        return False
        
    def deepCopy( self ):
        state = GameState( self )
        state.data = self.data.deepCopy()
        return state

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
        possibleActions = Actions.getPossibleActions()
        return possibleActions

    def applyAction(state, action, agentIndex):
        #TODO
        return

if __name__ == '__main__':
    import time
    tic = time.perf_counter()
    game = Game()
    print(game)
    agent = 0
    while True:
        text = input("input a move as 'x, y': ")
        try:
            move_coords = text.split(",")
            move_coords = [int(i) for i in move_coords]
            assert(len(move_coords) == 2)
        except:
            print("input failed \n")
            continue

        text = input(f"confirm {move_coords} (y/n): ")
        try:
            assert(text == "y" or text == "n")
            if text != "y":
                continue

        except:
            print("input 'y' or 'n' please.\n")
            continue

        try:
            if agent == 0:
                game.move(0, move_coords)
                agent=1
            else:
                game.move(1, move_coords)
                agent = 0
        except:
            print("invalid move\n")
            continue

        print(game)
        
    toc = time.perf_counter()
    print("total times: " + str(toc - tic))
