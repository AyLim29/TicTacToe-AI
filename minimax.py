from tictactoe import TicTacToe, UltimateTicTacToe, TTT_State, UTTT_State
from constants import *
import math

class Minimax:
    def __init__(self, environment: UltimateTicTacToe, max_player: int) -> None:
        self.env = environment
        self.current_state = environment.init_posit
        self.max_player = max_player
        
        # Hyperparameters
        self.look_ahead = 5
        
    
    def minimax(self, state: UTTT_State, depth, player):
        if depth == 0 or self.env.check_win(state) != NO_WIN:
            return self.heuristic(state)
        
        neighbouring_states = self.get_neighbouring_states(state, player)
        
        # Maximize
        if player == self.max_player:
            value = -math.inf
            action = None
            for neighbour, n_action in neighbouring_states:
                neighbour_value = self.minimax(neighbour, depth - 1, -1 * player)
                if value < neighbour_value:
                    value = neighbour_value
                    action = n_action  
            return action
        # Minimize
        else: 
            value = math.inf
            action = None
            for neighbour, n_action in neighbouring_states:
                neighbour_value = self.minimax(neighbour, depth - 1, -1 * player)
                if value > neighbour_value:
                    value = neighbour_value
                    action = n_action  
            return action

    def alpha_beta(self, state: UTTT_State, depth, player):
        pass

    def heuristic(self, state: UTTT_State):
        pass
    
    def get_valid_moves(self, state: UTTT_State):
        valid_moves = []
        env = self.env
        small_games = state.small_games
        for small_game in range(9):
            if env.check_win(small_games[small_game]) != NO_WIN or small_game not in state.valid_games:
                continue
            for cell in range(9):
                if cell in small_games[small_game].o_posit or cell in small_games[small_game].x_posit:
                    continue
                valid_moves.append((small_game, cell))
        return valid_moves
        
    def get_neighbouring_states(self, state: UTTT_State, turn):
        env = self.env
        neighbours = []

        for valid_move in self.get_valid_moves(self, state):
            neighbours.append((env.apply_move(state, valid_move, turn), valid_move))
            
        return neighbours
    