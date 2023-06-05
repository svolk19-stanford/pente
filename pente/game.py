

class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:
  """
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    """
    The Agent will receive a GameState and must return an action
    """
    raiseNotDefined()

class GameStateData:

  def __init__(self, board_size, captures_to_win, run_len_to_win, prevStateData=None):
    """
    Generates a new data packet by copying information from its predecessor.
    """
    self.board = {}
    self.board_size = board_size
    self.captures_to_win = captures_to_win
    self.run_len_to_win = run_len_to_win
    self.score = 0
    self.num_player_1_captures = 0
    self.num_player_2_captures = 0
    self.turn = 0 # begin with player 1 turn

    if prevStateData != None:
        self.board_size = prevStateData.board_size
        self.board = prevStateData.board
        self.captures_to_win = prevStateData.captures_to_win
        self.run_len_to_win = prevStateData.run_len_to_win
        self.score = prevStateData.score
        self.num_player_1_captures = prevStateData.num_player_1_captures
        self.num_player_2_captures = prevStateData.num_player_2_captures
        self.turn = prevStateData.turn

class Game:
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, state, agents, first_turn=0):
        self.first_turn = first_turn
        self.gameOver = False
        self.moveHistory = []
        self.startingIndex = 0
        self.agents = agents
        self.state = state        

    def __str__(self):
       
        board_grid = [[0 for i in range(self.state.data.board_size)] for j in range(self.state.data.board_size)]
        for (location, val) in self.state.data.board.items():
            board_grid[location[0]][location[1]] = val
            
        board_str = " _ "
        for i in range(self.state.data.board_size):
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

    def run(self): # run an instance of the game, querying actions from agents
        self.numMoves = 0
        agentIndex = self.startingIndex
        print_board = True

        while not self.gameOver:
            if print_board:
                print(self)
                # otherwise, calculate relative reward
                (all_p1, all_p2, protected_p1, protected_p2, half_protected_p1, \
                half_protected_p2, unprotected_p1, unprotected_p2) = self.state.getRunLengths()
                
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
        
                state_features = [p1_doubles_prot,
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
                print(state_features)
    
            self.state.setTurn(agentIndex)
            agent = self.agents[agentIndex]
            action = agent.getAction(self.state)
            self.moveHistory.append((agentIndex, action))
            try:
                if agentIndex == 0:
                    self.state = self.state.generateSuccessor(agentIndex, action)
                    agentIndex = 1
                    print_board = False
                else:
                    self.state = self.state.generateSuccessor(agentIndex, action)
                    agentIndex = 0
                    print_board = True
            except:
                print("invalid move\n")
                print_board = False
                continue

            if self.state.isWin():
                print("You win!!\n")
                self.gameOver = True
            if self.state.isLose():
                print("You loose :(\n")
                self.gameOver = True





                
                    
