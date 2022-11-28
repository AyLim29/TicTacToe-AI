from tictactoe import TicTacToe, TTT_State, UTTT_State
from constants import *

def main():
    state = UTTT_State([TTT_State([], [], True) for i in range(8)]+ [TTT_State([1,3], [5,8], True)], [i for i in range(9)], force_valid=True)
    render(state)
    # while True:
        
    #     pass
    # pass

def render(state: UTTT_State):
    small_games = state.small_games
    for game_row in range(3):
        for small_game_row in range(3):
            line = ''
            for game_col in range(3):
                game = game_row*3 + game_col
                o_posit = small_games[game].o_posit
                x_posit = small_games[game].x_posit
                
                # Excract rows:
                for i in range(3):
                    cell = small_game_row * 3 + i
                    if cell in o_posit:
                        line += 'O'
                    elif cell in x_posit:
                        line += 'X'
                    else:
                        line += '-'
                    if i != 2:
                        line += ' | '
                line += '      '
            print(line)
            if small_game_row != 2:
                print('---------      ---------      ---------')
        
        print('\n')
        
if __name__ == "__main__":
    main()
