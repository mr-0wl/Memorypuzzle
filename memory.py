# Memory Puzzle
# From InventWithPython
# Credit to Al Seigart
# Released under simplified BSD license

import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8 #speed of boxes sliding and cover reveal
BOXSIZE = 40
GAPSIZE 10
BOARDWIDTH = 10
BOARDHEIGHT = 7
assert (BOARDWIDTH * BOARHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs to match'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) /2)

# color in RGB
GRAY = (100,100,100)
NAVYBLUE = (60,60,100)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)

BGCOLOR = NAVYBLUE
LIGHTBCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined"

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption("Memory")

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(Flase)

    firstSelection = None

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True: #main loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) #draw the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            #the mouse is currently over a boxx
            if not revealedBoxes[boxx][boxy]:
                drawHighlightbox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True #set the box as revealed
                if firstSelection == None: #the current box was the first one clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second clicked
                    #check if there is a match between two icons
                    icon1Shape, icon1Color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2Shape, icon2Color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1Shape != icon2Shape or icon1Color != icon2Color:
                        #icons don't match recover both selections
                        pygame.time.wait(1000) #1000 milliseconds == 1 second
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): #check if all pairs found
                        gaemWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        #reset the Board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        #show the fully unrevealed board for a second
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        #replay the start game animation
                        startGameAnimation(mainBoard)
                    firstSelection = None #reset the fisrt selection variable

            #redraw the screen and wait a tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes
