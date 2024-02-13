import pygame
import numpy as np
from graphics2 import *

run = True # for the while loop
red_turn = True
blue_turn = False
turn_counter = True
kill_bit = False
setmode = False
kill_streak = False
coins_moves = []
red_coins_moves = []
blue_coins_moves = []
set_positions = []
red_set_positions = []
blue_set_positions = []
prev_col_g, prev_row_g = -1, -1
prev_row, prev_col = -1, -1
drawboard()

turnon = True
while run:
    # If you want to quit in middle, just close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if red_turn and turnon:
            red_coins_moves, kill_bit = getlegalcoins(positions, True, prev_row_g, prev_col_g)
            turnon = False
            if not len(red_coins_moves) :
                prev_row_g = -1
                red_turn = False
                turnon = True
            print(red_coins_moves, kill_bit)
        elif not red_turn and turnon:
            blue_coins_moves, kill_bit = getlegalcoins(positions, False, prev_row_g, prev_col_g)
            turnon = False
            if not len(blue_coins_moves):
                prev_row_g = -1
                red_turn = True
                turnon = True
            print(blue_coins_moves, kill_bit)

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 1:
                clicked_pos = getSquareFromClick(pygame.mouse.get_pos())
                row, col = clicked_pos
            index = 8*row + col 
            if setmode:
                if red_turn:
                    set_positions = red_set_positions
                else:
                    set_positions = blue_set_positions
                for i in set_positions:
                    if i == index:
                        prev_index = 8*prev_row + prev_col
                        capture_coin(prev_index, index)
                        setmode = False
                        kill_streak = kill_bit
                        if kill_streak:
                            prev_row_g = row
                            prev_col_g = col
                            turnon = True
                        else: 
                            prev_row_g = -1
                            if red_turn:
                                red_turn = False
                            else:
                                red_turn = True
                            turnon = True
                        break
                
                if setmode:
                    if red_turn:
                        red_set_positions = []
                    else:
                        blue_set_positions = []
                    set_positions = []
                    drawboard()
                    setmode = False
                else:
                    continue
            moves = []
            if red_turn:
                coins_moves = red_coins_moves
            else:
                coins_moves = blue_coins_moves
            for obj in coins_moves:
                if obj == index:
                    moves = deepcopy(coins_moves[obj])
                    break
            if len(moves):
                if kill_bit:
                    if red_turn: 
                        red_set_positions = display_kill_moves(row, col, moves)
                    else:
                        blue_set_positions = display_kill_moves(row, col, moves)
                else:
                    if red_turn:
                        red_set_positions = display_normal_moves(row, col, moves)
                    else:
                        blue_set_positions = display_normal_moves(row, col, moves)
                prev_row = row
                prev_col = col
                setmode = True
        
                    
            
                        
            

                
                





