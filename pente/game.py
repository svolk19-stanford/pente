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


class Actions:
  
    @staticmethod
    def getPossibleActions():
        possible = []

        #TODO: create possible actions given gamestate

        return possible

    @staticmethod
    def getSuccessor(action):
        #TODO: return successor state given action
        return

class GameStateData:

  def __init__(self, board, prevState=None):
    """
    Generates a new data packet by copying information from its predecessor.
    """
    self.board = board
    self.score = 0
    self.num_player_1_captures = 0
    self.num_player_2_captures = 0
    self.turn = 0 # begin with player 1 turn

    if prevState != None:
        self.board_size = 19
        self.board = prevState.board
        self.score = prevState.score
        self.num_player_1_captures = prevState.num_player_1_captures
        self.num_player_2_captures = prevState.num_player_2_captures
        self.turn = prevState.turn

class Game:
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, first_turn=0, board_size=19, captures_to_win=5, run_len_to_win=5):
        self.board = [[0 for i in range(board_size)] for j in range(board_size)]
        self.first_turn = first_turn
        self.board_size = board_size
        self.gameOver = False
        self.captures_to_win = captures_to_win
        self.run_len_to_win = run_len_to_win
        self.moveHistory = []

    def move(self, agent_index, move:tuple):
        try:
            assert(move[0] < self.board_size)
            assert(move[1] < self.board_size)
            assert(self.board[move[1]][move[0]] == 0)
            self.board[move[1]][move[0]] = agent_index + 1        
        except:
            raise Exception("Invalid move")

    def __str__(self):
        board_str = " _ "
        for i in range(self.board_size):
            if i < 10:
                board_str += f" {i} "
            else:
                board_str += f" {i}"

        board_str += "\n"
        for i, row in enumerate(self.board):
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



                
                    
