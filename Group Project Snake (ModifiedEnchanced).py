# Not mine, Edited and modified for study purposes
# Rapid Snake

# Libraries
import pygame
import sys
import pickle
import random
import time
import tkinter as tk
from tkinter import messagebox

# Game Initializing
pygame.init()

# Window size
windowWidth = 520
windowHeight = 570

# Windows Initialization and setup
win = pygame.display.set_mode((windowWidth, windowHeight))  # Main window size
pygame.display.set_caption("Popping Snake")
icon = pygame.image.load("imgs/icon1.png")
pygame.display.set_icon(icon)

# Game speed
clock = pygame.time.Clock()
FPS = 10

# Colors
# Neutrals
white = (255, 255, 255)
black = (0, 0, 0)

# Backgrounds
# reserve color (44, 62, 80)
intro_background = (52, 152, 219)
main_background = (246, 229, 141)
pause_backgrourd = (26, 188, 156)

# Buttons
play_color = (241, 196, 15)
exit_color = (192, 57, 43)
unpause_color = (142, 68, 173)
hover_color = (106, 176, 76)

# Title text color
popping = (19, 15, 64)
snakeT = (255, 255, 255)

# Others
eyeC = (48, 51, 107)
snakeColor = (246, 229, 141)
gridC = (48, 51, 107)
foodC = (186, 220, 88)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Text Font
# Intro Screen
title_font = pygame.font.Font("fonts/BungeeShade-Regular.ttf", 72)
btn_text_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 28)
detail_font = pygame.font.Font("fonts/VastShadow-Regular.ttf", 11)
instruct_font = pygame.font.Font("fonts/Iceland-Regular.ttf", 14)

# Main Screen
score_lenght_font = pygame.font.Font("fonts/Iceland-Regular.ttf", 22)
counter_font = pygame.font.Font("fonts/Monoton-Regular.ttf", 40)
timerT_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 10)
highscore_lastM_font = pygame.font.Font("fonts/Oswald-VariableFont_wght.ttf", 12)

black_font = pygame.font.Font("fonts/Roboto-Black.ttf", 72)
bold_font = pygame.font.Font("fonts/Roboto-Bold.ttf", 48)
light_font = pygame.font.Font("fonts/Roboto-Light.ttf", 34)
medium_font = pygame.font.Font("fonts/Roboto-Medium.ttf", 22)
regular_font = pygame.font.Font("fonts/Roboto-Regular.ttf", 12)
small_font = pygame.font.Font("fonts/Roboto-Black.ttf", 10)

small_black_font = pygame.font.Font("fonts/Roboto-Black.ttf", 48)

# Scoreboard Initialization
scoreboard = pygame.Surface([windowWidth, 50])
scoreboard.fill(black)

# Container size
screenSize = 500
rows = 20

# Snake Game Container
container = pygame.Surface([screenSize, screenSize])
container.fill(black)

# Global Variable Caller
intro = True
flag = None
pause = False
last_move = ["", int(0)]
score = 0


class Cubes(object):
    rows = 20
    width = 500

    def __init__(self, start, directX=1, directY=0, color=snakeColor):
        self.pos = start
        self.directX = 0
        self.directY = 0
        self.color = color

    def move(self, directX, directY):
        self.directX = directX
        self.directY = directY
        self.pos = (self.pos[0] + self.directX, self.pos[1] + self.directY)

    def draw(self, surface, eye=False):
        # Calculation to figure it out the distance of a row
        distance = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        # Drawing the rectangle with specific location of grid
        pygame.draw.rect(surface, self.color, (i * distance + 11, j * distance + 61,
                                               distance - 2, distance - 2))
        if eye:
            center = distance // 2
            radius = 3
            circleMid = (i * distance + 10 + center - radius, j * distance + 68)
            centerMid = (i * distance + 10 + distance - radius * 2, j * distance + 68)
            pygame.draw.circle(surface, eyeC, circleMid, radius)
            pygame.draw.circle(surface, eyeC, centerMid, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.press = False
        self.color = color
        self.head = Cubes(pos)
        self.body.append(self.head)
        self.directX = 0
        self.directY = 0

    # Snake Controls section
    def move(self):
        global flag, pause, first_move, last_move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Loop through dictionary of event keys
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE] and not pause and len(self.body) > 1:
                    pause = True
                    if pause:
                        last_move = ["PAUSE", 0]
                        Pause()
                    else:
                        pass

                if keys[pygame.K_p] and not pause and len(self.body) > 1:
                    pause = True
                    if pause:
                        last_move = ["PAUSE", 0]
                        Pause()
                    else:
                        pass

                if keys[pygame.K_LEFT] or keys[pygame.K_a] and not self.directX == 1:
                    self.directX = -1
                    self.directY = 0
                    self.turns[self.head.pos[:]] = [self.directX, self.directY]
                    last_move = ["LEFT", 1]

                if keys[pygame.K_RIGHT] or keys[pygame.K_d] and not self.directX == -1:
                    self.directX = 1
                    self.directY = 0
                    # This a dictionary of current head position and also where the cubes going to turn
                    self.turns[self.head.pos[:]] = [self.directX, self.directY]
                    last_move = ["RIGHT", 1]

                if keys[pygame.K_UP] or keys[pygame.K_w] and not self.directY == 1:
                    self.directX = 0
                    self.directY = -1
                    # This a dictionary of current head position and also where the cubes going to turn
                    self.turns[self.head.pos[:]] = [self.directX, self.directY]
                    last_move = ["UP", 1]

                if keys[pygame.K_DOWN] or keys[pygame.K_s] and not self.directY == -1:
                    self.directX = 0
                    self.directY = 1
                    # This a dictionary of current head position and also where the cubes going to turn
                    self.turns[self.head.pos[:]] = [self.directX, self.directY]
                    last_move = ["DOWN", 1]

        # Actually moving the cubes according to input
        for i, c in enumerate(self.body):
            # Passing the position X and Y from "c" variable into variable "p"
            p = c.pos[:]
            # Checking if position is in turns then we're going to move
            if p in self.turns:
                # We're grabbing the current position
                turn = self.turns[p]
                # Giving the position "X" and position "Y" into Cube class object
                c.move(turn[0], turn[1])
                # Checking the current length of list or the last object in list
                if i == len(self.body) - 1:
                    # Deleting the last turns to clear the path movers so that if we run into their
                    # again it will not automatically move to last turn in that area
                    self.turns.pop(p)
            # Checking if the snake hit the border
            else:
                # logic: if X position is equal to -1(left) and position is less than 0(end border left)
                if c.directX == -1 and c.pos[0] <= 0:
                    # then we are going to send it to the other side of the map(right side)
                    # c.pos value will be c.row(20)-1(19) and same "Y" position
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.directX == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.directY == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.directY == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    # If not then keep moving it into new position
                    c.move(c.directX, c.directY)

    def reset(self, pos):
        global last_move, start_time, elapse_time
        self.head = Cubes(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.directX = 0
        self.directY = 0
        last_move = ["", 0]
        start_time = time.time()

    def addCube(self):
        # Counting the current length of the snake reverse
        tail = self.body[-1]
        directX = tail.directX
        directY = tail.directY

        # Checking the direction we're heading
        if directX == 1 and directY == 0:
            # Appending the new cube into the last position of last cube according to move
            self.body.append(Cubes((tail.pos[0] - 1, tail.pos[1])))
        elif directX == -1 and directY == 0:
            self.body.append(Cubes((tail.pos[0] + 1, tail.pos[1])))
        elif directY == 1 and directX == 0:
            self.body.append(Cubes((tail.pos[0], tail.pos[1] - 1)))
        elif directY == -1 and directX == 0:
            self.body.append(Cubes((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].directX = directX
        self.body[-1].directY = directY

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


class Button(object):
    global windowWidth, windowHeight

    def __init__(self, posBox, text_input, color, identifier):
        # Passing variables
        self.posBox = posBox
        self.color = color
        self.identify = identifier
        # Button rectangle
        self.size = pygame.Rect(self.posBox, (150, 40))
        # Button text
        self.text_input = text_input
        self.text = btn_text_font.render(self.text_input, True, self.color)
        self.text_rect = self.text.get_rect(center=self.size.center)

    def hoverButton(self, position):
        if position[0] not in range(self.size.left, self.size.right) or position[1] not in range(
                self.size.top, self.size.bottom):
            self.text = btn_text_font.render(self.text_input, True, black)
        else:
            self.text = btn_text_font.render(self.text_input, True, self.color)

    def checkInput(self, position, typed):
        global intro, flag
        if position[0] in range(self.size.left, self.size.right) and position[1] in range(self.size.top,
                                                                                          self.size.bottom):
            if not typed == 1:
                pygame.quit()
                sys.exit()
            else:
                intro = False
                time.sleep(.25)
                flag = True
                pass

    def draw(self, btnColor):
        pygame.draw.rect(win, btnColor, self.size, border_radius=10)
        win.blit(self.text, self.text_rect)


def draw_grid(current_width, row, surface):
    # Gap between rows and column box
    sizeBetween = current_width / row

    x = 10  # X location where we're going to draw the lines of grid X
    y = 60  # Y location where we're going to draw the lines of grid Y

    # Loop of where lines going to be drawn depend on what calculated gap between
    # l = length
    for l in range(row):
        x = x + int(sizeBetween)
        y = y + int(sizeBetween)

        # Pygame line draw pygame.draw.line(surface, color, start, end, thickness)
        # surface = where to draw
        # color = color of lines
        # start = where the starting point
        # end = where the end point
        # thickness = line thickness by pixel
        pygame.draw.line(surface, gridC, (x, 60), (x, current_width + 60), 1)
        pygame.draw.line(surface, gridC, (10, y), (current_width + 10, y), 1)


def redraw_window(surface, new_time):
    global rows, screenSize, snake, food, score, last_move, highscore

    # Scoreboard text/location
    score_text, scoreLoc1 = text_object("Score: " + str(score[1]), score_lenght_font, white)
    snake_lenght, scoreLoc2 = text_object("Lenght: " + str(score[0]), score_lenght_font, white)
    scoreLoc1.topleft = (15, 2)
    scoreLoc2.topleft = (5, 22)

    # Timer text/location
    timer_text1, timerLoc1 = text_object("TIMER", timerT_font, snakeColor)
    timerLoc1.midtop = (windowWidth / 2, 1)
    timer_text2, timerLoc2 = text_object(str(new_time), counter_font, white)
    timerLoc2.midtop = (windowWidth / 2, 0)

    # Player Moves
    moves_text, moveLoc = text_object("Last move: " + str(last_move[0]) + " " + str(last_move[1]), highscore_lastM_font, white)
    moveLoc.topright = (windowWidth, 2)

    # High Score text/location
    high_text, high_loc = text_object("Highscore: COMING SOON", highscore_lastM_font, snakeColor)
    high_loc.bottomright = (windowWidth, 45)

    # what surface going to be filled
    surface.fill(main_background)

    # Casting the scoreboard and container into window
    win.blit(scoreboard, (0, 0))
    win.blit(container, (10, 60))
    snake.draw(surface)
    food.draw(surface)
    win.blit(score_text, scoreLoc1)
    win.blit(snake_lenght, scoreLoc2)
    win.blit(timer_text1, timerLoc1)
    win.blit(timer_text2, timerLoc2)
    win.blit(high_text, high_loc)
    win.blit(moves_text, moveLoc)

    # Displaying the grid into window with screen size desire, rows, and where to put(surface)
    draw_grid(screenSize, rows, surface)

    # Update the screen to load the applied objects
    pygame.display.update()


def random_snack(row, item):
    position = item.body

    while True:
        x = random.randrange(row)
        y = random.randrange(row)
        # Checking the filtered length of the snake location so that we didn't accidentally put the food inside the
        # snake body
        if len(list(filter(lambda z: z.pos == (x, y), position))) > 0:
            continue
        else:
            break

    return x, y


# Defining the text as object and its components
def text_object(text, font, color):
    # Passing the font format into text_surface with 3 parameters
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# main_text object fetcher
def main_text(text, font, color):
    text_surf, text_rect = text_object(text, font, color)
    text_rect.center = ((windowWidth / 2), (windowHeight / 2))
    win.blit(text_surf, text_rect)

    pygame.display.update()
    main()


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def Pause():
    global pause, flag, start_time, elapse_time

    win.fill(pause_backgrourd)
    print("Game is paused")
    unpause_game = Button((windowWidth / 2 - 170, 400), "PLAY", snakeColor, "Play button clicked")
    exit_game = Button((windowWidth / 2 + 21, 400), "QUIT", snakeColor, "Quit button clicked")

    while pause:
        start_time = time.time() - elapse_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_p] or keys[pygame.K_ESCAPE]:
                    print("Unpause", + pause)
                    pause = False
                    time.sleep(0)
                    pass
                else:
                    print("Invalid Input")
        clock.tick(30)
        pygame.display.update()


def main_intro():
    global black_font, bold_font, medium_font, regular_font, light_font, windowWidth, windowHeight, intro
    play_game = Button((windowWidth / 2 - 170, 450), "PLAY", hover_color, "Play button clicked")
    exit_game = Button((windowWidth / 2 + 21, 450), "QUIT", hover_color, "Quit button clicked")

    message1, messageLoc1 = text_object("POPPING", title_font, popping)
    messageLoc1.midtop = ((windowWidth / 2 - 40), 80)
    message2, messageLoc2 = text_object("SNAKE", title_font, snakeT)
    messageLoc2.topleft = ((windowWidth / 2 - 40), 120)

    detail1, detailLoc1 = text_object("This is a enhance version of snake game", detail_font, black)
    detail2, detailLoc2 = text_object(" that has beenalready enhance by us", detail_font, black)
    detailLoc1.midtop = ((windowWidth / 2), 250)
    detailLoc2.midtop = ((windowWidth / 2), 260)

    instruct1, intructLoc1 = text_object("To control the snake use the \"WASD\" or \"ARROW KEYS\" to move",
                                         instruct_font, black)
    instruct2, intructLoc2 = text_object("and \"ESP\" to pause the game.", instruct_font, black)
    intructLoc1.midtop = ((windowWidth / 2), 310)
    intructLoc2.midtop = ((windowWidth / 2), 320)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                play_game.checkInput(pygame.mouse.get_pos(), 1)
                exit_game.checkInput(pygame.mouse.get_pos(), 0)

        win.fill(intro_background)
        win.blit(message1, messageLoc1)
        win.blit(message2, messageLoc2)
        play_game.draw(play_color)
        play_game.hoverButton(pygame.mouse.get_pos())
        exit_game.draw(exit_color)
        exit_game.hoverButton(pygame.mouse.get_pos())
        win.blit(detail1, detailLoc1)
        win.blit(detail2, detailLoc2)
        win.blit(instruct1, intructLoc1)
        win.blit(instruct2, intructLoc2)
        pygame.display.update()
        clock.tick(30)


def main():
    global rows, snake, food, win, flag, intro, score, time_limit, elapse_time, start_time, highscore

    time_limit = 8
    start_time = time.time()
    score = [0, 0]
    comparing = float(0.0)
    add = 0
    # Passing the Snake(object) to snake variable
    snake = Snake(snakeColor, (10, 10))
    # Passing the Cubes(object) to snack variable
    food = Cubes(random_snack(rows, snake), color=foodC)

    # Main loop to load the animations and logic
    while flag and not intro:
        updated_timer = 8
        elapse_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # pygame.time.delay is a limiter to maintain the performance of computer
        clock.tick(FPS)
        snake.move()

        # Starting the actual time counting upon user first move
        if not last_move[1] == 1:
            start_time = time.time()

        # Checking if the head of the snake is in the food current location
        if snake.body[0].pos == food.pos:
            # Add another cube into the body
            snake.addCube()
            # Spawn another food
            food = Cubes(random_snack(rows, snake), color=foodC)
            add = 0
            start_time = time.time()

            if len(snake.body) % 2 == 0:
                add += int(len(snake.body) + 2 + score[1])
                score = [len(snake.body), add]
                add = 0
            else:
                add += int(len(snake.body) + score[1])
                score = [len(snake.body), add]
                add = 0

            if len(snake.body) % 15 == comparing:
                comparing = float(0.1)
                if comparing == float(0.1):
                    time_limit = time_limit - 1
                    print("yes")
            comparing = float(0.0)

        # Check the current length of the snake for score counting
        for x in range(len(snake.body)):
            # Collision checker if the head hit itself
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                # Call message box function
                message_box("You lose!", "Score: " + str(score[1]) + " Lenght: " + str(score[0]))
                # Call reset function
                score = [0, 0]
                snake.reset((10, 10))
                break

        for x in range(len(snake.body)):
            if last_move[1] == 1 and len(snake.body) >= 1 and not updated_timer == 0:
                updated_timer = time_limit - int(elapse_time)
                if elapse_time > time_limit:
                    snake.body.pop()
                    score[0] = len(snake.body)
                    start_time = time.time()

                # print(len(snake.body))
                if elapse_time > time_limit and len(snake.body) == 0:
                    # Show score into the console
                    print('Score: ', score[0], score[1])
                    # Call message box function
                    message_box("You lose!", "Score: " + str(score[1]) + " Lenght: " + str(score[0]))
                    # Call reset function
                    score = [0, 0]
                    snake.reset((10, 10))
                    break

        # Calling the redraw_window to update the game
        redraw_window(win, updated_timer)
        # Second update for assurance purpose
        pygame.display.update()

    pass


main_intro()
main()
