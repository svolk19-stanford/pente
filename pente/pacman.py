"""
Pacman.py holds the logic for the classic pacman game along with the main
code to run a game.  This file is divided into three sections:

  (i)  Your interface to the pacman world:
          Pacman is a complex environment.  You probably don't want to
          read through all of the code we wrote to make the game runs
          correctly.  This section contains the parts of the code
          that you will need to understand in order to complete the
          project.  There is also some code in game.py that you should
          understand.

  (ii)  The hidden secrets of pacman:
          This section contains all of the logic code that the pacman
          environment uses to decide who can move where, who dies when
          things collide, etc.  You shouldn't need to read this section
          of code, but you can if you want.

  (iii) Framework to start a game:
          The final section contains the code for reading the command
          you use to set up the game, then starting up a new game, along with
          linking in all the external parts (agent functions, graphics).
          Check this section out to see all the options available to you.
"""
from game import GameStateData
from game import Game
from game import Directions
from game import Actions
from util import nearestPoint
from util import manhattanDistance
import util, layout
import sys, types, time, random, os

###################################################
# YOUR INTERFACE TO THE PACMAN WORLD: A GameState #
###################################################

class GameState:
  """
  A GameState specifies the full state of pieces played

  GameStates are used by the Game object to capture the actual state of the game and
  can be used by agents to reason about the game.
  """

  ####################################################
  # Accessor methods: use these to access state data #
  ####################################################

  def getLegalActions( self, agentIndex=0 ):
    """
    Returns the legal actions for the agent specified.
    """
    if self.isWin() or self.isLose(): return []

    if agentIndex == 0:  # Pacman is moving
      return player_1_rules.getLegalActions( self )
    else:
      return player_2_rules.getLegalActions( self, agentIndex )

  def generateSuccessor( self, agentIndex, action):
    """
    Returns the successor state after the specified agent takes the action.
    """
    # Check that successors exist
    if self.isWin() or self.isLose(): raise Exception('Can\'t generate a successor of a terminal state.')

    # Copy current state
    state = GameState(self)

    # Let agent's logic deal with its action's effects on the board
    if agentIndex == 0:  # first player is moving
      player_1_rules.applyAction( state, action )
    else:      
      player_2_rules.applyAction( state, action, agentIndex )

    # Book keeping
    state.data._agentMoved = agentIndex
    return state

  def getLegalActions( self ):
    return self.getLegalActions( 0 )

  def generatePlayer1Successor( self, action ):
    """
    Generates the successor state after the specified pacman move
    """
    return self.generateSuccessor( 0, action )

  def getScore( self ):
    return self.data.score

  def getGameStateInfo():
    #TODO

    # this method will return relevant info about the gamestate
    # number adjacent pairs, lengths of runs, number of pieces, number of captures, etc.
    # this may be split into multiple methods
    return

  def isLose( self ):
    return self.data._lose

  def isWin( self ):
    return self.data._win

  #############################################
  #             Helper methods:               #
  #############################################

  def __init__( self, prevState = None ):
    """
    Generates a new state by copying information from its predecessor.
    """
    if prevState is not None: # Initial state
      self.data = GameStateData(prevState.data)
    else:
      self.data = GameStateData()

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

  def initialize( self, layout, numGhostAgents=1000 ):
    """
    Creates an initial game state from a layout array (see layout.py).
    """
    self.data.initialize(layout, numGhostAgents)

############################################################################
############################################################################

class ClassicGameRules:
  """
  These game rules manage the control flow of a game, deciding when
  and how the game starts and ends.
  """
  def __init__(self, timeout=30):
    self.timeout = timeout

  def newGame( self, layout, pacmanAgent, ghostAgents, display, quiet = False, catchExceptions=False):
    agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
    initState = GameState()
    initState.initialize( layout, len(ghostAgents) )
    game = Game(agents, display, self, catchExceptions=catchExceptions)
    game.state = initState
    self.initialState = initState.deepCopy()
    self.quiet = quiet
    return game

  def process(self, state, game):
    """
    Checks to see whether it is time to end the game.
    """
    if state.isWin(): self.win(state, game)
    if state.isLose(): self.lose(state, game)

  def win( self, state, game ):
    if not self.quiet: print(("Pacman emerges victorious! Score: %d" % state.data.score))
    game.gameOver = True

  def lose( self, state, game ):
    if not self.quiet: print(("Pacman died! Score: %d" % state.data.score))
    game.gameOver = True

  def getProgress(self, game):
    return float(game.state.getNumFood()) / self.initialState.getNumFood()

  def agentCrash(self, game, agentIndex):
    if agentIndex == 0:
      print("Pacman crashed")
    else:
      print("A ghost crashed")

  def getMaxTotalTime(self, agentIndex):
    return self.timeout

  def getMaxStartupTime(self, agentIndex):
    return self.timeout

  def getMoveWarningTime(self, agentIndex):
    return self.timeout

  def getMoveTimeout(self, agentIndex):
    return self.timeout

  def getMaxTimeWarnings(self, agentIndex):
    return 0

class player_1_rules:
    """
    These functions govern how player 1 interacts with their environment under
    the classic game rules.
    """
    @staticmethod
    def getLegalActions( state ):
        """
        Returns a list of possible actions.
        """
        possibleActions = Actions.getPossibleActions( state.getPacmanState().configuration, state.data.layout.walls )
        if Directions.STOP in possibleActions:
        possibleActions.remove( Directions.STOP )
        return possibleActions
    getLegalActions = staticmethod( getLegalActions )

    def applyAction( state, action ):
        return
  
class player_2_rules:
"""
These functions govern how player 2 interacts with their environment under
the classic game rules.
"""

  def getLegalActions( state ):
    """
    Returns a list of possible actions.
    """
    possibleActions = Actions.getPossibleActions( state.getPacmanState().configuration, state.data.layout.walls )
    if Directions.STOP in possibleActions:
      possibleActions.remove( Directions.STOP )
    return possibleActions
  getLegalActions = staticmethod( getLegalActions )

  def applyAction( state, action ):
    return
 
 

if __name__ == '__main__':
  """
  The main function called when pacman.py is run
  from the command line:

  > python pacman.py

  See the usage string for more details.

  > python pacman.py --help
  """
  import time
  tic = time.perf_counter()

  toc = time.perf_counter()
  print("total times: " + str(toc - tic))

  # import cProfile
  # cProfile.run("runGames( **args )")
  pass
