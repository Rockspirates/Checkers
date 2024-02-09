import pygame
import numpy as np
pygame.init()

#aspects of the game window
screenwidth = 800
screenheight = 800

#size of each grid in the board
squarewidth = screenwidth // 8

#default positions of the coins
positions = [-1,0,-1,0,-1,0,-1,0,0,-1,0,-1,0,-1,0,-1,-1,0,-1,0,-1,0,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,-1,1,-1,1,-1,-1,1,-1,1,-1,1,-1,1,1,-1,1,-1,1,-1,1,-1]

win = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption("Checkers")

black_standard = pygame.image.load('sprites/black-checker/standard.png')
black_King = pygame.image.load('sprites/black-checker/king-me.png')
red_standard = pygame.image.load('sprites/red-checker/standard.png')
red_King = pygame.image.load('sprites/red-checker/king-me.png')

# BLUE = (255,255,240)
# RED = (173,216,230)

BLUE = (255,255,240)
RED = (120,144,156)

def drawsquare(row, column):
    if (7*row + column) % 2 == 0:
        colour = RED
        pygame.draw.rect(win, colour, (column*squarewidth, row*squarewidth, squarewidth, squarewidth))
    else:
        colour = BLUE
        pygame.draw.rect(win, colour, (column*squarewidth, row*squarewidth, squarewidth, squarewidth))

# f : (row, col) -> {red_standard, black_standard, red_King, black_King}
def drawpieces(row, col):
    factor = 0.9 # factor is adjust the width, height of sprites
    factor1 = 10 # factor1 is to adjust the y-cordinates of centre of sprites
    factor2 = 5 # factor2 is specially for red_King to adjust its centre
    index = 8*row + col
    if positions[index] == 0:
        img = pygame.transform.scale(red_standard, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth, row*squarewidth + factor1))

    elif positions[index] == 1:
        img = pygame.transform.scale(black_standard, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth, row*squarewidth + factor1))
    
    elif positions[index] == 2:
        img = pygame.transform.scale(red_King, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth + factor2, row*squarewidth + factor2))
    
    elif positions[index] == 3:
        img = pygame.transform.scale(black_King, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth, row*squarewidth + factor1))

# updates the board
def drawboard():
    for i in range(8):
        for j in range(8):
            drawsquare(i,j)
            drawpieces(i,j)
    pygame.display.update()

run = True

while run:
    drawboard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


