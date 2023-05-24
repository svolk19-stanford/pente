from util import *
from util import raiseNotDefined

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

  def __init__(self, board_size, prevStateData=None):
    """
    Generates a new data packet by copying information from its predecessor.
    """
    self.board = [[0 for i in range(board_size)] for j in range(board_size)]
    self.board_size = board_size
    self.score = 0
    self.num_player_1_captures = 0
    self.num_player_2_captures = 0
    self.turn = 0 # begin with player 1 turn

    if prevStateData != None:
        self.board_size = prevStateData.board_size
        self.board = prevStateData.board
        self.score = prevStateData.score
        self.num_player_1_captures = prevStateData.num_player_1_captures
        self.num_player_2_captures = prevStateData.num_player_2_captures
        self.turn = prevStateData.turn


class Game:
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, state, agents, first_turn=0, captures_to_win=5, run_len_to_win=5):
        self.first_turn = first_turn
        self.gameOver = False
        self.captures_to_win = captures_to_win
        self.run_len_to_win = run_len_to_win
        self.moveHistory = []
        self.startingIndex = 0
        self.agents = agents
        self.state = state        

    def __str__(self):
        board_str = " _ "
        for i in range(self.state.data.board_size):
            if i < 10:
                board_str += f" {i} "
            else:
                board_str += f" {i}"

        board_str += "\n"
        for i, row in enumerate(self.state.data.board):
            if i < 10:
                row_str = f" {i} "
            else:
                row_str = f" {i}"
            for val in row:
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
            agent = self.agents[agentIndex]
            action = agent.getAction(self.state)
            self.moveHistory.append((agentIndex, action))
            try:
                if agentIndex == 0:
                    self.state = self.state.generateSuccessor(agentIndex, action)
                    agentIndex = 1
                else:
                    self.state = self.state.generateSuccessor(agentIndex, action)
                    agentIndex = 0
                print_board = True
            except:
                print("invalid move\n")
                print_board = False
                continue

            #TODO: process correctness and game ending
        #TODO: output move history and winning info to a file for TD learning training






                
                    
