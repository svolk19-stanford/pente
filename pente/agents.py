# multiAgents.py
# --------------

import random, util

from game import Agent

class cliAgent(Agent):
    def getAction(self, gameState):
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
                return move_coords
            except:
                print("input 'y' or 'n' please.\n")
                continue

class randomAgent(Agent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        bestIndices = [index for index in range(len(legalMoves))]
        chosenIndex = random.choice(bestIndices) # Pick randomly 
        return legalMoves[chosenIndex]
        

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState) -> str:
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
        def get_V_minmax(agent_idx: int, gameState, depth: int) -> int:
            actions = gameState.getLegalActions(agent_idx)
            if gameState.isWin() or gameState.isLose() or len(actions) == 0 or depth == 0: # terminal state
                return betterEvaluationFunction(gameState)
            else: # find V_minmax through recursion on actions
                successors = [gameState.generateSuccessor(agent_idx, action) for action in actions]
                if agent_idx == 0: # max agent
                    scores = [get_V_minmax(1, succ, depth) for succ in successors]
                    return max(scores)
                elif agent_idx == 1: # min agent
                    scores = [get_V_minmax(0, succ, depth - 1) for succ in successors]
                    return min(scores)
                else:
                    raise Exception("unknown agent")

        legalMoves = gameState.getLegalActions(1)
        successors = [gameState.generateSuccessor(1, action) for action in legalMoves]
        scores = [get_V_minmax(0, succ, self.depth) for succ in successors] 
        bestScore = min(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]
        # END_YOUR_CODE


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (problem 2)
      You may reference the pseudocode for Alpha-Beta pruning here:
      en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
    """

    def getAction(self, gameState) -> str:
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        # BEGIN_YOUR_CODE (our solution is 43 lines of code, but don't worry if you deviate from this)
        def get_V_minmax_ab(agent_idx: int, gameState, depth: int, alpha: int, beta: int) -> float:
            actions = gameState.getLegalActions(agent_idx)
            if gameState.isWin() or gameState.isLose() or len(actions) == 0 or depth == 0: # terminal state
                return betterEvaluationFunction(gameState)
            else: # find V_minmax through recursion on actions
                if agent_idx == self.index: # max agent
                    value = float("-inf")
                    best_action = ""
                    for action in actions:
                        successor = gameState.generateSuccessor(agent_idx, action)
                        succ_value = get_V_minmax_ab(1, successor, depth, alpha, beta)
                        if succ_value >= value:
                            value = succ_value
                            best_action = action  
                        if beta <= value:
                            break
                        alpha = max([alpha, value])
                    return value

                elif agent_idx == 1: # min agent
                    value = float("inf")
                    for action in actions:
                        successor = gameState.generateSuccessor(agent_idx, action)
                        succ_value = get_V_minmax_ab(0, successor, depth - 1, alpha, beta)
                        if succ_value <= value:
                            value = succ_value
                        if value <= alpha:
                            break
                        beta = min([beta, value])
                    return value
                else:
                    raise Exception("unknown agent")

        legalMoves = gameState.getLegalActions(self.index + 1)
        successors = [gameState.generateSuccessor(self.index + 1, action) for action in legalMoves]
        scores = []
        for i, s in enumerate(successors):
            print(i)
            scores.append(get_V_minmax_ab(self.index, s, self.depth, float("-inf"), float("inf")))
        print(scores)
        # scores = [get_V_minmax_ab(self.index, succ, self.depth, float("-inf"), float("inf")) for succ in successors]
        worstScore = min(scores)
        indices = [index for index in range(
            len(scores)) if scores[index] == worstScore]
        chosenIndex = random.choice(indices)
        return legalMoves[chosenIndex]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (problem 3)
    """

    def getAction(self, gameState) -> str:
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
        def get_V_expectimax(agent_idx: int, gameState, depth: int) -> int:
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

def betterEvaluationFunction(currentGameState) -> float:
    """
      Our unstoppable evaluation function
    """

    # return large rewards for win/loss
    loss_pentalty = -1000
    win_reward = 1000
    if currentGameState.isWin():
        return win_reward
    if currentGameState.isLose():
        return loss_pentalty
    
    # otherwise, calculate relative reward
    (run_lengths_p1, run_lengths_p2) = currentGameState.getRunLengths()
    num_p1_doubles = sum([i == 2 for i in run_lengths_p1]) \
                        - sum([i == 3 for i in run_lengths_p1])
    num_p2_doubles = sum([i == 2 for i in run_lengths_p2]) \
                        - sum([i == 3 for i in run_lengths_p2])
    num_p1_triples = sum([i == 3 for i in run_lengths_p1]) \
                        - sum([i == 4 for i in run_lengths_p1])
    num_p2_triples = sum([i == 3 for i in run_lengths_p2]) \
                        - sum([i == 4 for i in run_lengths_p2])
    num_p1_quadruples = sum([i == 4 for i in run_lengths_p1])
    num_p2_quadruples = sum([i == 4 for i in run_lengths_p2])
    num_p1_pieces = currentGameState.getNumPieces(0)
    num_p2_pieces = currentGameState.getNumPieces(1)
    num_p1_captures = currentGameState.getNumCaptures(0)
    num_p2_captures = currentGameState.getNumCaptures(1)    
    
    state_features = [num_p1_pieces,
                      num_p2_pieces,
                      num_p1_captures,
                      num_p2_captures,
                      num_p1_doubles,
                      num_p2_doubles,
                      num_p1_triples,
                      num_p2_triples,
                      num_p1_quadruples,
                      num_p2_quadruples]
    
    weights = [1, -1, 5, -5, 2, -2, 3, -3, 4, -4]
    return sum([state_features[i] * weights[i] for i in range(len(state_features))])

