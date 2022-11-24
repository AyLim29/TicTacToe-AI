from constants import *

class TTT_State:
    def __init__(self, o_posit: list[tuple], x_posit: list[tuple], force_valid=True) -> None:
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

class TicTacToe:
    def __init__(self) -> None:
        self.init_posit = TTT_State([], [])
    
    def apply_move(self, state: TTT_State, move: tuple, turn) -> None:
        if move not in state.o_posit and move not in state.x_posit:
            return state
        if turn == X:
                return TTT_State(state.o_posit, state.x_posit + [move], O)
        else:
            return TTT_State(state.o_posit + [move], state.x_posit, X)
    
    def check_win(self, state: TTT_State) -> int:
        # Winning Positions
        horizontal = [[(i, j) for j in range(3)] for i in range(3)]
        vertical = [[(j, i) for j in range(3)] for i in range(3)]
        diagonal = [[(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]]
        
        # Check if x_posit/ o_posit contains winning positions
        for win_pos in horizontal + vertical + diagonal:
            if all(elem in state.x_posit for elem in win_pos):
                return X
            if all(elem in state.o_posit for elem in win_pos):
                return O
            
        # Check Draw
        if len(state.x_posit) + len(state.o_posit) == 9:
            return DRAW
        
        return NO_WIN
    
class UltimateTicTacToe:
    def __init__(self) -> None:
        self.init_posit = [TicTacToe() for _ in range(9)]
    
    
if __name__ == "__main__":
    ttt = TicTacToe()
    print(["DRAW", "X", "NO_WIN", "O"][ttt.check_win(TTT_State([[(j, i) for j in range(3)] for i in range(3)][2], [(1,1)], X))])
    
        
