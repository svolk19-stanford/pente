# multiAgents.py
# --------------

import random
from tqdm import tqdm


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
    return legalMoves[chosenIndex]

class MultiAgentSearchAgent(Agent):

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  
        self.evaluationFunction = betterEvaluationFunction
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState) -> str:

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


class AlphaBetaAgent(MultiAgentSearchAgent):
    
    def getAction(self, gameState) -> str:
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        def get_V_minmax_ab(agent_idx: int, gameState, depth: int, alpha: int, beta: int) -> float:
            actions = gameState.getLegalActions(agent_idx)
            if gameState.isWin() or gameState.isLose() or len(actions) == 0 or depth == 0: # terminal state
                return betterEvaluationFunction(gameState)
            else: # find V_minmax through recursion on actions
                if agent_idx == 0: # max agent
                    value = float("-inf")
                    best_action = ""
                    for action in actions:
                        successor = gameState.generateSuccessor(agent_idx, action)
                        succ_value = get_V_minmax_ab(1, successor, depth - 1, alpha, beta)
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
        for i in tqdm(range(len(successors)), desc="Calculating..."):
            scores.append(get_V_minmax_ab(self.index, successors[i], self.depth, float("-inf"), float("inf")))
        worstScore = min(scores)
        indices = [index for index in range(
            len(scores)) if scores[index] == worstScore]
        chosenIndex = random.choice(indices)
        return legalMoves[chosenIndex]

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
    (all_p1, all_p2, protected_p1, protected_p2, half_protected_p1, \
     half_protected_p2, unprotected_p1, unprotected_p2) = currentGameState.getRunLengths()
    
    # number of protected runs
    p1_doubles_prot = sum([i == 2 for i in protected_p1])
    p2_doubles_prot = sum([i == 2 for i in protected_p2]) 
    p1_triples_prot = sum([i == 3 for i in protected_p1]) 
    p2_triples_prot = sum([i == 3 for i in protected_p2]) 
    p1_quadruples_prot = sum([i == 4 for i in protected_p1])
    p2_quadruples_prot = sum([i == 4 for i in protected_p2])

    # number of unprotected runs
    p1_doubles_unprot = sum([i == 2 for i in unprotected_p1])
    p2_doubles_unprot = sum([i == 2 for i in unprotected_p2]) 
    p1_triples_unprot = sum([i == 3 for i in unprotected_p1]) 
    p2_triples_unprot = sum([i == 3 for i in unprotected_p2]) 
    p1_quadruples_unprot = sum([i == 4 for i in unprotected_p1])
    p2_quadruples_unprot = sum([i == 4 for i in unprotected_p2])

    # number of half-protected runs
    p1_doubles_half_prot = sum([i == 2 for i in half_protected_p1]) 
    p2_doubles_half_prot = sum([i == 2 for i in half_protected_p2]) 
    p1_triples_half_prot = sum([i == 3 for i in half_protected_p1]) 
    p2_triples_half_prot = sum([i == 3 for i in half_protected_p2]) 
    p1_quadruples_half_prot = sum([i == 4 for i in half_protected_p1])
    p2_quadruples_half_prot = sum([i == 4 for i in half_protected_p2])

    # Other features
    p1_pieces = currentGameState.getNumPieces(0)
    p2_pieces = currentGameState.getNumPieces(1)
    p1_captures = currentGameState.getNumCaptures(0)
    p2_captures = currentGameState.getNumCaptures(1) 
    
    num_p1_doubles = sum([i == 2 for i in all_p1]) \
                        - sum([i == 3 for i in all_p1])
    num_p2_doubles = sum([i == 2 for i in all_p2]) \
                        - sum([i == 3 for i in all_p2])
    num_p1_triples = sum([i == 3 for i in all_p1]) \
                        - sum([i == 4 for i in all_p1])
    num_p2_triples = sum([i == 3 for i in all_p2]) \
                        - sum([i == 4 for i in all_p2])
    num_p1_quadruples = sum([i == 4 for i in all_p1])
    num_p2_quadruples = sum([i == 4 for i in all_p2])  

    assert(num_p1_doubles == p1_doubles_prot + p1_doubles_unprot + p1_doubles_half_prot)
    assert(num_p2_doubles == p2_doubles_prot + p2_doubles_unprot + p2_doubles_half_prot)
    assert(num_p1_triples == p1_triples_prot + p1_triples_unprot + p1_triples_half_prot)
    assert(num_p2_triples == p2_triples_prot + p2_triples_unprot + p2_triples_half_prot)
    assert(num_p1_quadruples == p1_quadruples_prot + p1_quadruples_unprot + p1_quadruples_half_prot)
    assert(num_p2_quadruples == p2_quadruples_prot + p2_quadruples_unprot + p2_quadruples_half_prot)

    
    # state_features = [p1_pieces,
    #                   p2_pieces,
    #                   p1_captures,
    #                   p2_captures,
    #                   p1_doubles,
    #                   p2_doubles,
    #                   p1_triples,
    #                   p2_triples,
    #                   p1_quadruples,
    #                   p2_quadruples]

    state_features = [p1_pieces,
                      p2_pieces,
                      p1_captures,
                      p2_captures, 

                      p1_doubles_prot,
                      p2_doubles_prot,
                      p1_triples_prot,
                      p2_triples_prot,
                      p1_quadruples_prot,
                      p2_quadruples_prot,

                      p1_doubles_half_prot,
                      p2_doubles_half_prot,
                      p1_triples_half_prot,
                      p2_triples_half_prot,
                      p1_quadruples_half_prot,
                      p2_quadruples_half_prot,

                      p1_doubles_unprot,
                      p2_doubles_unprot,
                      p1_triples_unprot,
                      p2_triples_unprot,
                      p1_quadruples_unprot,
                      p2_quadruples_unprot]

    # subjective feature weights 
    weights = [1, -1, 30, -30, 
               2, -2, 3, -3, 4, -4, 
               -3, 3, 4, -4, 7, -7, 
               4, -4, 20, -20, 100, -100]
    return sum([state_features[i] * weights[i] for i in range(len(state_features))])

