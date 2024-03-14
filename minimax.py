from tictactoe import TicTacToe, UltimateTicTacToe, TTT_State, UTTT_State
from constants import *
import math

class Minimax:
    def __init__(self, environment: UltimateTicTacToe, max_player: int) -> None:
        self.env = environment
        self.current_state = environment.init_posit
        self.max_player = max_player
        
        # Hyperparameters
        self.look_ahead = 7
        
        #TODO calculate number of valid states:
        
    
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

    def alpha_beta(self, state: UTTT_State, depth, alpha, beta, player):
        winner = self.env.check_win(state)
        if winner != NO_WIN:
            # return float(winner * self.max_player), None
            return float(winner * math.inf * self.max_player), None
        if depth == 0:
            return self.heuristic(state), None

        
        neighbouring_states = self.get_neighbouring_states(state, player)
        
        # Maximize
        if player == self.max_player:
            value = -math.inf
            action = None
            for neighbour, n_action in neighbouring_states:
                neighbour_value, _ = self.alpha_beta(neighbour, depth - 1, alpha, beta, -1 * player)
                
                # Set value = max(value, neighbour_value)
                if value < neighbour_value:
                    value = neighbour_value
                    action = n_action  
                
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value, action
        
        # Minimize
        else: 
            value = math.inf
            action = None
            for neighbour, n_action in neighbouring_states:
                neighbour_value, _ = self.alpha_beta(neighbour, depth - 1, alpha, beta, -1 * player)
                
                # Set value = min(value, neighbour_value)
                if value > neighbour_value:
                    value = neighbour_value
                    action = n_action  
                
                if value <= alpha:
                    break
                beta = min(beta, value)
                
            return value, action

    def get_valid_moves(self, state: UTTT_State):
        valid_moves = []
        env = self.env
        ttt_env = env.TTT_env
        
        small_games = state.small_games
        for small_game in range(9):
            if ttt_env.check_win(small_games[small_game]) != NO_WIN or small_game not in state.valid_games:
                continue
            for cell in range(9):
                if cell in small_games[small_game].o_posit or cell in small_games[small_game].x_posit:
                    continue
                valid_moves.append((small_game, cell))
        return valid_moves
        
    def get_neighbouring_states(self, state: UTTT_State, turn):
        env = self.env
        neighbours = []

        for valid_move in self.get_valid_moves(state):
            neighbours.append((env.apply_move(state, valid_move, turn), valid_move))
            
        return neighbours
    
    def heuristic(self, state: UTTT_State) -> float:
        env = self.env
        # +1 for any cells 
        
        # Check if state wins the game
        winner = env.check_win(state)
        if winner != NO_WIN:
            if winner == self.max_player:
                return math.inf
            else: # Draw or other player wins
                return -math.inf
        
        # Heurisitic:
        # Number of small games won
        # Number of dominaiting small games - small games with more tokens than the opponent
        # Number of cells that result in a win
        # Blocking moves - Got for free 
        num_x_won = 0
        num_o_won = 0        
        
        num_dom_x = 0
        num_dom_o = 0
        
        num_win_cells_x = 0
        num_win_cells_o = 0
        for i in range(9):
            # Calculated number of small games won
            winner = env.TTT_env.check_win(state.small_games[i])     
            if winner == X:
                num_x_won += 1
            elif winner == O:
                num_o_won += 1
                
            # # Calculate number of dominating games
            # num_o = len(state.small_games[i].o_posit)
            # num_x = len(state.small_games[i].x_posit)
            # if num_o > num_x:
            #     num_dom_o += 1           
            # elif num_x > num_o:
            #     num_dom_x += 1           
                
            # Calculate number of cells that result in a win
            #TODO add higher weight when in a valid game
            
        for valid_game in state.valid_games: 
            for move in range(9):
                # Iterate through empty cells
                if move not in state.small_games[valid_game].o_posit + state.small_games[valid_game].x_posit:
                    next_state_X = env.TTT_env.apply_move(state.small_games[valid_game], move, X)
                    next_state_O = env.TTT_env.apply_move(state.small_games[valid_game], move, O)
                    winner_X = env.TTT_env.check_win(next_state_X)
                    winner_O = env.TTT_env.check_win(next_state_O)
                    if winner_X == X:
                        num_win_cells_x += 1
                    elif winner_X == O:
                        num_win_cells_o += 1
                    if winner_O == X:
                        num_win_cells_x += 1
                    elif winner_O == O:
                        num_win_cells_o += 1
            
            #TODO number of winning cells in large game
        
        #TODO the turn matters - so num_win_cells_other_player is worth more if it is their turn
        #TODO Prefer winning small games that result in a potential three in a row rather than winning any small game 
        if self.max_player == X:
            return (num_x_won - num_o_won)*10 + (num_win_cells_x - num_win_cells_o)*3
        else:
            return (num_o_won - num_x_won)*10 + (num_win_cells_o - num_win_cells_x)*3