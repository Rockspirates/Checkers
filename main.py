import pygame
import numpy as np
from graphics import *

run = True
firstClick = True
prev_row, prev_col = -1, -1
legal_moves = []
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
                    firstClick = True
                    move(prev_row, prev_col, row, col, legal_moves)
                else:
                    firstClick = False
                    prev_row, prev_col = row, col
                    legal_moves = showLegalMoves(positions, row, col)

    pygame.display.flip()