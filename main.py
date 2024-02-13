import pygame
import numpy as np
from graphics import *

run = True
firstClick = True
prev_row, prev_col = -1, -1
legal_moves = []
currentTurn = True

prev_kill = False
kill_row, kill_col = -1, -1

drawboard()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked_pos = getSquareFromClick(pygame.mouse.get_pos())
                row, col = clicked_pos
                # Sets the Opponent and Me Variables
                if currentTurn:
                    opp = 0
                    me = 1
                else:
                    opp = 1
                    me = 0

                # Handles the Second Click
                if not firstClick:
                    if positions[row*8 + col] == opp:
                        firstClick = True
                        drawboard()
                        continue
                    firstClick = True

                    # If I misclick and click my own piece again,
                    if positions[row*8+col] == currentTurn:
                        legal_moves = showLegalMoves(positions, row, col, prev_kill, kill_row, kill_col)
                        prev_row, prev_col = row, col
                        firstClick = False
                        continue

                    flag = move(prev_row, prev_col, row, col, legal_moves)
                    if flag == 0:
                        if currentTurn:
                            currentTurn = False                 
                        else:
                            currentTurn = True
                        prev_kill = False
                        kill_row, kill_col = -1, -1

                    elif flag == -1:
                        firstClick = True
                        drawboard()
                        continue

                    elif flag == 1:
                        prev_kill = True


                else:
                    if positions[row*8 + col] == -1 or positions[row*8 + col] == opp:
                        drawboard()
                        continue
                    if not prev_kill:
                        prev_row, prev_col = row, col
                    else:
                        prev_row, prev_col = kill_row, kill_col
                    legal_moves = showLegalMoves(positions, row, col, prev_kill, kill_row, kill_col)
                    firstClick = False

    pygame.display.flip()