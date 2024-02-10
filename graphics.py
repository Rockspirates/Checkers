import pygame
import pygame.gfxdraw
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
    pygame.gfxdraw.filled_circle(win, center_x, center_y, circle_radius, darker_color)

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

You can make sense of these directions by adding them to the index of a cell (row*8+col)

then I find the distance it has from the sides of the board and then find the minimum distance in each direction
then I put the information in the dictionary

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

# This function is used to find the available moves in a particular direction
def findMoves(board, row, col, dir):
    print("Finding moves for index:", row*8+col)
    moves = list() # where I will store the moves. Moves are stored as a tuple containing the FINAL_INDEX, DIRECTION
    index = 8*row + col
    index += dir
    findBlank = False # This is the term which alternates in the diagonal. True when I want to find blank in diag and False when I wanna find Opp piece
    i = 0 # Counter which counts the steps till I reach the edge
    move = -1 # initiate with a NULL Move
    first = True # For the corner case when the blank is the first square encounter which is a valid move
    me = board[row*8+col]
    if not me: # to set the opp and me variable which are later used to identify pieces
        opp = 1
    else:
        opp = 0
    val = numsToEdges[row*8 + col][dir]
    while i != val:
        i+=1
        print(i, index)
        if board[index] == opp:
            print("opponent detected at", index)
            if first:
                first = False
            index+=dir
            if not findBlank:
                findBlank = True
                continue
            else:
                print("Opponent detected when I was trying to detect blank", move)
                if move != -1:
                    moves.append((move, dir))
                break
        if board[index] == -1:
            print("blank detected at", index)
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
                break
        if board[index] == me:
            print("my piece detected at", index)
            if move != -1:
                moves.append((index, dir))
            break
    if move != -1:
        moves.append((move, dir))
    return moves


# This moves uses the last function to generate moves in the appropriate direction considering player
def generateLegalMoves(board, row, col):
    moves = []
    index = 8*row+col
    if board[index] == 0: # RED'S TURN, GOES FROM TOP TO BOTTOM
        for dir in [7, 9]: # Downward Direction Diagonals
            moves.extend(findMoves(board, row, col, dir)) # inserts tuples of the form (FINAL_INDEX, DIRECTION)
    else: # BLACKS'S TURN, GOES FROM BOTTOM TO TOP
        for dir in [-7, -9]: # Upward Direction Diagonals 
            moves.extend(findMoves(board, row, col, dir))
    return moves


# This is the actual function which updates the move. This also checks if the clicked square is in the legal squares or not to prevent illegal moves
# Also updates the positions array in the backend
def move(prev_row, prev_col, row, col, moves):
    index = 8*row + col
    if index not in [x[0] for x in moves]: # checks if the square is in legal moves
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

    drawboard() # Draws the updated positions array on the board
    pass


# Shows the legal moves available to the selectetd piece
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

# Gets the square coordinates from mouse click
def getSquareFromClick(pos):
    x, y = pos
    row = y // squarewidth
    col = x // squarewidth
    return row, col


# Draws the complete board
def drawboard():
    for i in range(8):
        for j in range(8):
            drawsquare(i,j)
            drawpieces(i,j)
    pygame.display.update()