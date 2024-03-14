from constants import *

""" 
The current state of the Tic Tac Toe game
"""
class TTT_State:
    def __init__(self, o_posit: list[int], x_posit: list[int], force_valid=True) -> None:
        if force_valid:
            assert isinstance(o_posit, list), '!!! tried to create State but o_posit is not a list !!!'
            assert isinstance(x_posit, list), '!!! tried to create State but x_posit is not a list !!!'
            for i in o_posit:
                for j in x_posit:
                    assert i != j, '!!! tried to create State but o_posit shares element with x_posit !!!'
        # TODO more assertions
        
        self.o_posit = o_posit
        self.x_posit = x_posit
        self.force_valid = force_valid
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, TTT_State):
            return False
        # Not equal if positions of Os and Xs are different:
        for i in other.o_posit:
            if i not in self.o_posit:
                return False
        for j in other.x_posit:
            if j not in self.o_posit.x_posit:
                return False
        return True
    
    def __hash__(self) -> int:
        return hash((self.x_posit, self.o_posit))
    
    def deepcopy(self):
        return TTT_State(self.o_posit, self.x_posit)

"""
The current state of the ultimate Tic Tac Toe game
"""
class UTTT_State:
    def __init__(self, small_games: list[TTT_State], valid_games: list, force_valid=True) -> None:
        # Assert small_games has 9 games
        self.small_games = small_games
        self.valid_games = valid_games
    
    def __eq__(self, other) -> bool:
        for i in range(9):
            if self.small_games[i] != other.small_games[i]:
                return False
        return True
    
    def __hash__(self) -> int:
        return hash(self.small_games)
    
    def deepcopy(self):
        return UTTT_State(self.small_games, self.valid_games)

"""
Controls the logic of the tic tac toe games
"""
class TicTacToe:
    def __init__(self):
        self.init_posit = TTT_State([], [])
    
    def apply_move(self, state: TTT_State, move: int, turn: int) -> TTT_State:
        if move in state.o_posit or move in state.x_posit:
            return state
        if turn == X:
                return TTT_State(state.o_posit, state.x_posit + [move], O)
        else:
            return TTT_State(state.o_posit + [move], state.x_posit, X)
    
    def check_win(self, state: TTT_State) -> int:
        # Check if x_posit/ o_posit contains winning positions
        #BUG FIX CHECK_WIN 
        for win_pos in HORIZONTAL + VERTICAL + DIAGONAL:
            if all(elem in state.x_posit for elem in win_pos):
                return X
            if all(elem in state.o_posit for elem in win_pos):
                return O
            
        # Check Draw
        if len(state.x_posit) + len(state.o_posit) == 9:
            return DRAW
        
        return NO_WIN

"""
Controls the logic of the ultimate tic tac toe games
"""
class UltimateTicTacToe:
    def __init__(self) -> None:
        self.init_posit = UTTT_State([TTT_State([], [], True) for i in range(9)], [i for i in range(9)], force_valid=True)
        self.TTT_env = TicTacToe()
        
    def apply_move(self, state: UTTT_State, move: tuple[int], turn) -> UTTT_State:
        # move: (small game index, move in small game)
        
        cell = move[1]
        new_state = state.small_games[move[0]].deepcopy()
        new_state = self.TTT_env.apply_move(new_state, move[1], turn)
        new_small_games = state.small_games[0:move[0]] + [new_state] + state.small_games[move[0] + 1:]
        # new_state = UTTT_State(new_small_games, n)
        
        #TODO calculate new valid games
        
        new_valid_games = []
        # Check if the move results in a solved game 
        if self.TTT_env.check_win(new_small_games[move[1]]) != NO_WIN:
            # Check which other small games it can go to::
            for i in range(9):
                if self.TTT_env.check_win(new_small_games[i]) == NO_WIN:
                    new_valid_games.append(i)
        else:
            new_valid_games = [move[1]]
            
        return UTTT_State(new_small_games, new_valid_games)
        
    def check_win(self, state: UTTT_State) -> int:
        small_games = state.small_games
        for positions in HORIZONTAL + VERTICAL + DIAGONAL:
            win_X = True
            win_O = True
            for pos in positions:
                # Check if all pos are X or O
                pos_winner = self.TTT_env.check_win(small_games[pos])
                if pos_winner != X:
                    win_X = False
                if pos_winner != O:
                    win_O = False
            
            if win_X == True:
                return X
            if win_O == True:
                return O
        
        # Check if all are not NO_WIN then
        draw = True
        for i in range(9):
            if self.TTT_env.check_win(small_games[i]) == NO_WIN:
                draw = False
                    
        if draw == True:
            return DRAW
        
        return NO_WIN
    
    def check_valid_move(self, state: UTTT_State, move):
        if move[0] not in range(9) or move[1] not in range(9):
            return False
        if move[0] not in state.valid_games:
            return False
        game = state.small_games[move[0]]
        if move[1] in game.o_posit + game.x_posit:
            return False
        return True
    

    
    
    
if __name__ == "__main__":
    # ttt = TicTacToe()
    # print(["DRAW", "X", "NO_WIN", "O"][ttt.check_win(TTT_State([[(j, i) for j in range(3)] for i in range(3)][2], [(1,1)], X))])
    ttt = TicTacToe()
    state = TTT_State([],[0,4,8])
    print(["DRAW", "X", "NO_WIN", "O"][ttt.check_win(state)])
        
