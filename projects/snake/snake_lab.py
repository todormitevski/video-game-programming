# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *
import time

FPS = 15

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)

# TASK 1 - second worm colors
BLUE      = (    0,  0, 255)
PURPLE  = (  160, 32, 240)

DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

# TASK 2
BLINK_ELEMENT_1_DURATION = 5
BLINK_ELEMENT_1_INTERVAL = 5
BLINK_ELEMENT_2_DURATION = 7

BLINK_COLOR_1 = (255, 255, 0)
BLINK_COLOR_2 = (128, 0, 128)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    second_worm_created = False

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    # TASK 1
    second_worm_created = False
    second_worm_coords = []
    start_time = time.time()


    # TASK 2
    blink_element_1_start_time = time.time()
    blink_element_1_active = False
    blink_element_1_position = getRandomLocation()

    blink_element_2_active = True
    blink_element_2_start_time = time.time()
    blink_element_2_position = getRandomLocation()


    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            # TASK 1 - if first worm's head touches second worm
            if not wormCoords[HEAD] in second_worm_coords:
                del wormCoords[-1] # remove worm's tail segment


        # TASK 1
        if not second_worm_created and time.time() - start_time >= 5:
            startx1 = random.randint(5, CELLWIDTH - 6)
            starty1 = random.randint(5, CELLHEIGHT - 6)
            second_worm_coords = [{'x': startx1,     'y': starty1},
                                  {'x': startx1 - 1, 'y': starty1},
                                  {'x': startx1 - 2, 'y': starty1}]
            second_worm_created = True


        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        
        # TASK 1 - second worm movement
        last_dir = None

        if second_worm_created:
            move_direction = random.choice([UP, DOWN, LEFT, RIGHT])

            if move_direction == UP and last_dir != DOWN:
                new_head = {'x': second_worm_coords[HEAD]['x'], 'y': second_worm_coords[HEAD]['y'] - 1}
                last_dir = UP
            elif move_direction == DOWN and last_dir != UP:
                new_head = {'x': second_worm_coords[HEAD]['x'], 'y': second_worm_coords[HEAD]['y'] + 1}
                last_dir = DOWN
            elif move_direction == LEFT and last_dir != RIGHT:
                new_head = {'x': second_worm_coords[HEAD]['x'] - 1, 'y': second_worm_coords[HEAD]['y']}
                last_dir = LEFT
            elif move_direction == RIGHT and last_dir != LEFT:
                new_head = {'x': second_worm_coords[HEAD]['x'] + 1, 'y': second_worm_coords[HEAD]['y']}
                last_dir = RIGHT
            second_worm_coords.insert(0, new_head)

            # check if the second worm has hit the edge
            if second_worm_coords[HEAD]['x'] == -1 or second_worm_coords[HEAD]['x'] == CELLWIDTH or second_worm_coords[HEAD]['y'] == -1 or second_worm_coords[HEAD]['y'] == CELLHEIGHT:
                second_worm_created = False # delete second worm
            # for secondWormBody in second_worm_coords[1:]:
            #     if secondWormBody['x'] == second_worm_coords[HEAD]['x'] and secondWormBody['y'] == second_worm_coords[HEAD]['y']:
            #         second_worm_created = False

            # TASK 1 - if second worm's head touches first worm
            if second_worm_coords[HEAD] in wormCoords:
                second_worm_coords.insert(0, new_head)
            else:
                del second_worm_coords[-1]


        # TASK 2
        # Check if it's time to activate the first blinking element
        if not blink_element_1_active and time.time() - blink_element_1_start_time >= BLINK_ELEMENT_1_INTERVAL:
            blink_element_1_active = True
            blink_element_1_start_time = time.time()

        # Check if it's time to deactivate the first blinking element
        if blink_element_1_active and time.time() - blink_element_1_start_time >= BLINK_ELEMENT_1_DURATION:
            blink_element_1_active = False

        # Draw the first blinking element if active
        if blink_element_1_active:
            drawBlinkElement(blink_element_1_position, BLINK_COLOR_1)

        # Check if it's time to deactivate the second blinking element
        if blink_element_2_active and time.time() - blink_element_2_start_time >= BLINK_ELEMENT_2_DURATION:
            blink_element_2_active = False

        # Draw the second blinking element if active
        if blink_element_2_active:
            drawBlinkElement(blink_element_2_position, BLINK_COLOR_2)

        
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords, DARKGREEN, GREEN)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)

        # TASK 1
        if second_worm_created:
            drawWorm(second_worm_coords, PURPLE, BLUE)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# TASK 2
def drawBlinkElement(coord, color):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    blinkElementRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, color, blinkElementRect)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    # TASK 2
    additional_points = 0
    if blink_element_1_active and wormCoords[HEAD] == blink_element_1_position:
        additional_points += 3

    if blink_element_2_active and wormCoords[HEAD] == blink_element_2_position:
        additional_points += 3

    total_score = len(wormCoords) - 3 + additional_points

    # Display the total score on the screen
    drawScore(total_score)

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


# TASK 1
def drawWorm(wormCoords, color1, color2):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, color1, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, color2, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()