from tictactoe import TicTacToe, UltimateTicTacToe, TTT_State, UTTT_State
from constants import *
from minimax import Minimax
import os
import math
import time

def main():
    # state = UTTT_State([TTT_State([], [], True) for i in range(8)]+ [TTT_State([1,3], [5,8], True)], [i for i in range(9)], force_valid=True)
    # render(state)
    env = UltimateTicTacToe()
    ai = Minimax(env, O)
    max_depth = 6
    
    state = env.init_posit
    render(state, env)
    turn = X
    while True:
        if turn == X:     
            sg = input("Input Small Game: ")
            cell = input("Input cell: ")
            move = (int(sg), int(cell))
            if not env.check_valid_move(state, move):
                print("Invalid Move")
                time.sleep(0.2)
                continue
            state = env.apply_move(state, move, turn)
            render(state, env)
        else: # Minimax Move:
            #TODO Async Ai is thinking...
            print("thinking...")
            value, move = ai.alpha_beta(state, max_depth, -math.inf, math.inf, O)
            state = env.apply_move(state, move, turn)
            render(state, env, [move])
            print(value)
            
        turn *= -1 
        
        win = env.check_win(state)
        if win != NO_WIN:
            if win == DRAW:
                print("Game Drawed")
            elif win == X:
                print("X won")
            elif win == O:
                print("O won")
            break

def render(state: UTTT_State, env: UltimateTicTacToe, highlight = []):
    class Colours:
        prefix = "\033["
        magenta = f"{prefix}35m"
        cyan = f"{prefix}36m"
        reset = f"{prefix}0m"
        blue = f"{prefix}34m"
        red = f"{prefix}31m"
        green = f"{prefix}32m"
        
    #TODO Render large X/O when small game is won
    small_games = state.small_games
    for game_row in range(3):
        for small_game_row in range(3):
            line = ''
            for game_col in range(3):
                game = game_row*3 + game_col
                o_posit = small_games[game].o_posit
                x_posit = small_games[game].x_posit
                
                ttt_env = env.TTT_env
                
                if ttt_env.check_win(small_games[game]) == X:
                    line += large_X[2 * small_game_row]
                    if game_col != 2: 
                        line += '      '
                    continue
                elif ttt_env.check_win(small_games[game]) == O:
                    line += large_O[2 * small_game_row]
                    if game_col != 2: 
                        line += '      '
                    continue
                
                if game in state.valid_games:
                    line += Colours.blue
                
                # Extract cols:
                for i in range(3):
                    cell = small_game_row * 3 + i
                    if (game, cell) in highlight:
                        line += Colours.red
                        
                    if cell in o_posit:
                        line += 'O'
                    elif cell in x_posit:
                        line += 'X'
                    else:
                        line += '-'
                    
                    if (game, cell) in highlight:
                        if game in state.valid_games:
                            line += Colours.blue
                        else:
                            line += Colours.reset
                            
                    if i != 2:
                        line += ' | '
                        
                if game in state.valid_games:
                    line += Colours.reset
                    
                line += '      '
            print(line)
            
            if small_game_row != 2:
                line = ''
                for game_col in range(3):
                    game = game_row*3 + game_col
                    o_posit = small_games[game].o_posit
                    x_posit = small_games[game].x_posit
                    
                    if game in state.valid_games:
                        line += Colours.blue
                    
                    if ttt_env.check_win(small_games[game]) == X:
                        line += large_X[2 * small_game_row + 1]
                    elif ttt_env.check_win(small_games[game]) == O:
                        line += large_O[2 * small_game_row + 1]
                    else:
                        line += '---------'
                        
                    if game in state.valid_games:
                        line += Colours.reset
                        
                    if game_col != 2:
                        line += '      '
                print(line)
        
        print('\n')
        
if __name__ == "__main__":
    os.system('color')  # enable coloured terminal output
    main()
