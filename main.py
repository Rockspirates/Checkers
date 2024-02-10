import pygame
import numpy as np
from graphics import *

run = True
firstClick = True
prev_row, prev_col = -1, -1
legal_moves = []
currentTurn = True
continuation = False
cont_index = -1
drawboard()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked_pos = getSquareFromClick(pygame.mouse.get_pos())
                row, col = clicked_pos
                if not firstClick:
                    if continuation:
                        continuation = False
                    firstClick = True
                    if positions[row*8+col] == (not currentTurn):
                        drawboard()
                        continue
                    elif positions[row*8+col] == currentTurn:
                        legal_moves = showLegalMoves(positions, row, col)
                        prev_row, prev_col = row, col
                        firstClick = False
                        continue
                    flag = move(prev_row, prev_col, row, col, legal_moves)
                    if flag == 0:
                        if currentTurn:
                            currentTurn = False                 
                        else:
                            currentTurn = True
                    elif flag == 1:
                        continuation = True
                        print("continuation is true now!")
                        cont_index = 8*row + col
                        continue
                    elif flag == -1:
                        continue

                else:
                    if continuation:
                        if row*8 + col == cont_index:
                            firstClick = False
                        else: 
                            continue
                    prev_row, prev_col = row, col
                    legal_moves = showLegalMoves(positions, row, col)
                    if positions[row*8+col] == currentTurn:
                        firstClick = False
                    else:
                        continue
                    prev_row, prev_col = row, col

    pygame.display.flip()