import pygame

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



# updates the board

# MS1: Imports the sprites
black_standard = pygame.image.load('sprites/black-checker/standard.png')
black_King = pygame.image.load('sprites/black-checker/king-me.png')
red_standard = pygame.image.load('sprites/red-checker/standard.png')
red_King = pygame.image.load('sprites/red-checker/king-me.png')


# BLUE = (255,255,240)
# RED = (173,216,230)

BLUE = (255,255,240)
DARK_BLUE = (209, 229, 244)
RED = (120,144,156)
DARK_RED = (32, 51, 84)

def drawsquare(row, column):
    if (7*row + column) % 2 == 1:
        colour = RED
        pygame.draw.rect(win, colour, (column*squarewidth, row*squarewidth, squarewidth, squarewidth))
    else:
        colour = BLUE
        pygame.draw.rect(win, colour, (column*squarewidth, row*squarewidth, squarewidth, squarewidth))
# f : (row, col) -> {red_standard, black_standard, red_King, black_King}
def drawpieces(row, col):
    factor = 0.9 # factor is adjust the width, height of sprites
    factor1 = 9 # factor1 is to adjust the y-cordinates of centre of sprites
    factor2 = 5 # factor2 is specially for red_King to adjust its centre
    factorx = 1
    index = 8*row + col
    if positions[index] == 0:
        img = pygame.transform.smoothscale(red_standard, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth+factorx, row*squarewidth + factor1))

    elif positions[index] == 1:
        img = pygame.transform.smoothscale(black_standard, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth+factorx, row*squarewidth + factor1))
    
    elif positions[index] == 2:
        img = pygame.transform.smoothscale(red_King, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth + factor2, row*squarewidth + factor2))
    
    elif positions[index] == 3:
        img = pygame.transform.smoothscale(black_King, (squarewidth*factor, squarewidth*factor))
        win.blit(img, (col*squarewidth, row*squarewidth + factor1))


# draws the legal clear square which a piece can jump to (when)
# you click a piece, it can show you where you can possibly land up
def drawLegalSquare(row, col):
    circle_radius = squarewidth // 6  # Smaller radius for the circle
    darker_color = DARK_BLUE if ((7*row + col) % 2 == 0) else DARK_RED
    center_x = col * squarewidth + squarewidth // 2
    center_y = row * squarewidth + squarewidth // 2
    pygame.draw.circle(win, darker_color, (center_x, center_y), circle_radius)

# this indicates all the pieces which would be captured when
# you jump over them
def drawCaptureSquare(row, col): # row and col only
    center_x = col * squarewidth + squarewidth // 2
    center_y = row * squarewidth + squarewidth // 2

    circle_radius = squarewidth // 2.0 # Further increased radius for the hollow circle
    border_width = 5  # Increased width of the border for the hollow circle
    darker_color = DARK_BLUE if ((7*row + col) % 2 == 0) else DARK_RED
    
    # Draw hollow circle which shows the captured square
    pygame.draw.circle(win, darker_color, (center_x, center_y), circle_radius, border_width)


"""
7 indicates the south-west direction
-7 indicates the north-east direction
9 indicates the south-east direction
-9 indicates the north-west direction



"""
numsToEdges = []
for i in range(64):
    numsToEdges.append(dict())
for row in range(8):
    for col in range(8):
        numNorth = row
        numSouth = 7-row
        numWest = col
        numEast = 7 - col
        numsToEdges[row*8 + col] = {
            7: min(numSouth, numWest),
            -7: min(numNorth, numEast),
            9: min(numSouth, numEast),
            -9: min(numNorth, numWest)
        }
def findMoves(board, row, col, dir):
    moves = list()
    index = 8*row + col
    index += dir
    findBlank = False
    i = 0
    move = -1
    first = True
    val = numsToEdges[row*8 + col][dir]
    while i != val:
        i+=1
        if board[index] == 1:
            if first:
                first = False
            index+=dir
            if not findBlank:
                findBlank = True
                continue
            else:
                if move != -1:
                    moves.append((move, dir))
        if board[index] == -1:
            if first:
                moves.append((index, dir))
                break
            if findBlank:
                findBlank = False
                move = index
                index += dir
            else:
                if move != -1:
                    moves.append((move, dir))
    return moves

def generateLegalMoves(board, row, col):

    moves = []
    index = 8*row+col
    if board[index] == 0: # RED'S TURN, GOES FROM TOP TO BOTTOM
        for dir in [7, 9]:
            moves.extend(findMoves(board, row, col, dir))
    else: # BLACKS'S TURN, GOES FROM BOTTOM TO TOP
        for dir in [-7, -9]:
            moves.extend(findMoves(board, row, col, dir))
    return moves

def move(prev_row, prev_col, row, col, moves):
    index = 8*row + col
    if index not in [x[0] for x in moves]:
        drawboard()
        return
    temp = positions[prev_row*8+prev_col]
    positions[prev_row*8+prev_col] = positions[row*8+col]
    positions[row*8+col] = temp
    curr_index = prev_row*8+prev_col
    final_index = row*8+col
    diff = final_index - curr_index
    if diff < 0:
        mult = -1
    else:
        mult = 1
    if abs(diff)%7 == 0:
        dir_abs = 7
    else:
        dir_abs = 9
    move_dir = mult*dir_abs
    while curr_index != final_index-move_dir:
        curr_index+=move_dir
        positions[curr_index] = -1

    drawboard()
    pass

def showLegalMoves(board, row, col):
    drawboard()
    moves = generateLegalMoves(board, row, col)
    for move in moves:
        target_square, move_dir = move
        if move_dir + (8*row+col) == target_square:
            drawLegalSquare(target_square//8, target_square%8)
            continue
        curr_index = row*8 + col
        a = True
        while curr_index != target_square:
            curr_index += move_dir
            if a:
                drawCaptureSquare(curr_index//8, curr_index%8)
                a = False
            else:
                drawLegalSquare(curr_index//8, curr_index%8)
                a = True
        drawLegalSquare(target_square//8, target_square%8)
    return moves
def getSquareFromClick(pos):
    x, y = pos
    row = y // squarewidth
    col = x // squarewidth
    return row, col

def drawboard():
    for i in range(8):
        for j in range(8):
            drawsquare(i,j)
            drawpieces(i,j)
            # if i == 3 or i == 4:
            #     drawLegalSquare(i, j)
    pygame.display.update()