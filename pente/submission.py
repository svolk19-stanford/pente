import random
import util

from game import Agent
from pacman import GameState



class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def __init__(self):
        self.lastPositions = []
        self.dc = None

    def getAction(self, gameState: GameState):
        """
        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East}
        ------------------------------------------------------------------------------
        Description of GameState and helper functions:

        A GameState specifies the full game state, including the food, capsules,
        agent configurations and score changes. In this function, the |gameState| argument
        is an object of GameState class. Following are a few of the helper methods that you
        can use to query a GameState object to gather information about the present state
        of Pac-Man, the ghosts and the maze.

        gameState.getLegalActions(agentIndex):
            Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

        gameState.generateSuccessor(agentIndex, action):
            Returns the successor state after the specified agent takes the action.
            Pac-Man is always agent 0.

        gameState.getPacmanState():
            Returns an AgentState object for pacman (in game.py)
            state.configuration.pos gives the current position
            state.direction gives the travel vector

        gameState.getGhostStates():
            Returns list of AgentState objects for the ghosts

        gameState.getNumAgents():
            Returns the total number of agents in the game

        gameState.getScore():
            Returns the score corresponding to the current state of the game


        The GameState class is defined in pacman.py and you might want to look into that for
        other helper methods, though you don't need to.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)


        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action: str) -> float:
        """
        The evaluation function takes in the current GameState (defined in pacman.py)
        and a proposed action and returns a rough estimate of the resulting successor
        GameState's value.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState: GameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (problem 1)
    """

    def getAction(self, gameState: GameState) -> str:
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction. Terminal states can be found by one of the following:
          pacman won, pacman lost or there are no legal moves.

          Don't forget to limit the search depth using self.depth. Also, avoid modifying
          self.depth directly (e.g., when implementing depth-limited search) since it
          is a member variable that should stay fixed throughout runtime.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.getScore():
            Returns the score corresponding to the current state of the game

          gameState.isWin():
            Returns True if it's a winning state

          gameState.isLose():
            Returns True if it's a losing state

          self.depth:
            The depth to which search should continue

        """

        # BEGIN_YOUR_CODE (our solution is 22 lines of code, but don't worry if you deviate from this)
        def get_V_minmax(agent_idx: int, gameState: GameState, depth: int) -> int:
            actions = gameState.getLegalActions(agent_idx)
            if gameState.isWin() or gameState.isLose() or len(actions) == 0: # terminal state
                return gameState.getScore()
            elif depth == 0:
                return self.evaluationFunction(gameState)
            else: # find V_minmax through recursion on actions
                successors = [gameState.generateSuccessor(agent_idx, action) for action in actions]
                if agent_idx == self.index: # max agent
                    scores = [get_V_minmax(agent_idx + 1, succ, depth) for succ in successors]
                    return max(scores)
                elif agent_idx > self.index and agent_idx < gameState.getNumAgents() - 1: # min agent
                    scores = [get_V_minmax(agent_idx + 1, succ, depth) for succ in successors]
                    return min(scores)
                elif agent_idx == gameState.getNumAgents() - 1: # last min agent: decrements depth in recursion
                    scores = [get_V_minmax(self.index, succ, depth - 1) for succ in successors]
                    return min(scores)
                else:
                    raise Exception("unknown agent")

        legalMoves = gameState.getLegalActions(self.index)
        successors = [gameState.generateSuccessor(self.index, action) for action in legalMoves]
        scores = [get_V_minmax(self.index + 1, succ, self.depth) for succ in successors]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]
        # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (problem 2)
      You may reference the pseudocode for Alpha-Beta pruning here:
      en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
    """

    def getAction(self, gameState: GameState) -> str:
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        # BEGIN_YOUR_CODE (our solution is 43 lines of code, but don't worry if you deviate from this)
        def get_V_minmax_ab(agent_idx: int, gameState: GameState, depth: int, alpha: int, beta: int) -> float:
            actions = gameState.getLegalActions(agent_idx)
            if gameState.isWin() or gameState.isLose() or len(actions) == 0: # terminal state
                return gameState.getScore()
            elif depth == 0:
                return self.evaluationFunction(gameState)
            else: # find V_minmax through recursion on actions
                if agent_idx == self.index: # max agent
                    value = float("-inf")
                    best_action = ""
                    for action in actions:
                        successor = gameState.generateSuccessor(agent_idx, action)
                        succ_value = get_V_minmax_ab(agent_idx + 1, successor, depth, alpha, beta)
                        if succ_value >= value:
                            value = succ_value
                            best_action = action  
                        if beta <= value:
                            break
                        alpha = max([alpha, value])
                    return value

                elif agent_idx > self.index and agent_idx < gameState.getNumAgents() - 1: # min agent
                    value = float("inf")
                    for action in actions:
                        successor = gameState.generateSuccessor(agent_idx, action)
                        succ_value = get_V_minmax_ab(agent_idx + 1, successor, depth, alpha, beta)
                        if succ_value <= value:
                            value = succ_value
                        if value <= alpha:
                            break
                        beta = min([beta, value])
                    return value

                elif agent_idx == gameState.getNumAgents() - 1: # last min agent: decrements depth in recursion
                    value = float("inf")
                    for action in actions:
                        successor = gameState.generateSuccessor(agent_idx, action)
                        succ_value = get_V_minmax_ab(self.index, successor, depth - 1, alpha, beta)
                        if succ_value <= value:
                            value = succ_value
                        if value <= alpha:
                            break
                        beta = min([beta, value])
                    return value
                else:
                    raise Exception("unknown agent")

        legalMoves = gameState.getLegalActions(self.index)
        successors = [gameState.generateSuccessor(self.index, action) for action in legalMoves]
        scores = [get_V_minmax_ab(self.index + 1, succ, self.depth, float("-inf"), float("inf")) for succ in successors]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]
        # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (problem 3)
    """

    def getAction(self, gameState: GameState) -> str:
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
        def get_V_expectimax(agent_idx: int, gameState: GameState, depth: int) -> int:
                actions = gameState.getLegalActions(agent_idx)
                if gameState.isWin() or gameState.isLose() or len(actions) == 0: # terminal state
                    return gameState.getScore()
                elif depth == 0:
                    return self.evaluationFunction(gameState)
                else: # find V_minmax through recursion on actions
                    successors = [gameState.generateSuccessor(agent_idx, action) for action in actions]
                    if agent_idx == self.index: # max agent
                        scores = [get_V_expectimax(agent_idx + 1, succ, depth) for succ in successors]
                        return max(scores)
                    elif agent_idx > self.index and agent_idx < gameState.getNumAgents() - 1: # min agent
                        scores = [get_V_expectimax(agent_idx + 1, succ, depth) for succ in successors]
                        return sum(scores) / len(scores)
                    elif agent_idx == gameState.getNumAgents() - 1: # last min agent: decrements depth in recursion
                        scores = [get_V_expectimax(self.index, succ, depth - 1) for succ in successors]
                        return sum(scores) / len(scores)
                    else:
                        raise Exception("unknown agent")

        legalMoves = gameState.getLegalActions(self.index)
        successors = [gameState.generateSuccessor(self.index, action) for action in legalMoves]
        scores = [get_V_expectimax(self.index + 1, succ, self.depth) for succ in successors]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]
     # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function


def betterEvaluationFunction(currentGameState: GameState) -> float:
    """
      Your extreme, unstoppable evaluation function (problem 4). Note that you can't fix a seed in this function.
    """

    # BEGIN_YOUR_CODE (our solution is 16 lines of code, but don't worry if you deviate from this)
    num_ghosts = currentGameState.getNumAgents() - 1
    p_pos = currentGameState.getPacmanPosition()
    food_pos = currentGameState.getFood()
    g_scared = [currentGameState.getGhostState(i).scaredTimer for i in range(1, num_ghosts + 1)]
    g_pos = [currentGameState.getGhostPosition(i) for i in range(1, num_ghosts + 1)]
    g_pos_scared = [g_pos[i] for i in range(len(g_pos)) if g_scared[i] > 0]
    g_pos_not_scared = [g_pos[i] for i in range(len(g_pos)) if g_scared[i] == 0]
    capsules = currentGameState.getCapsules()
    g_dists_ns = [util.manhattanDistance(gp, p_pos) for gp in g_pos_not_scared]
    g_dists_s = [util.manhattanDistance(gp, p_pos) for gp in g_pos_scared]
    capsule_dists = [util.manhattanDistance(c, p_pos) for c in capsules]
    food_dists = []
    food_loc = []
    total_food = 0
    for x, row in enumerate(food_pos):
        for y, val in enumerate(row):
            if val:
                total_food += 1
                food_dists.append(util.manhattanDistance((x, y), p_pos))
                food_loc.append((x, y))
    
    state_features = [currentGameState.getScore(), 
                      min(food_dists, default=0), 
                      min(capsule_dists, default=0), 
                      total_food,
                      len(capsules), 
                      min(g_dists_ns, default=0),
                      min(g_dists_s, default=0)]
    # print(state_features)
    weights = [1.2, -2, 0, -3, -22, 0.5, -0.5]
    return sum([state_features[i] * weights[i] for i in range(len(state_features))])
    # END_YOUR_CODE


# Abbreviation
better = betterEvaluationFunction
