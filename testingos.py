# Not mine, Edited and modified for study purposes
# Rapid Snake

# Libraries
import sys
import random
import time
import tkinter as tk
from tkinter import messagebox
import pygame

# Game Initializing
pygame.init()

# Window size
windowWidth = 520
windowHeight = 570

# Windows Initialization and setup
win = pygame.display.set_mode((windowWidth, windowHeight))  # Main window size
pygame.display.set_caption("Rapid Snake")
icon = pygame.image.load(r"C:\Users\Patricia Ann De Asis\Desktop\python\imgs\icon1.png")
pygame.display.set_icon(icon)

# Game speed
clock = pygame.time.Clock()
FPS = 10

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
snakeColor = (255, 255, 0)

# Text Font
black_font = pygame.font.Font(r"C:\Users\Patricia Ann De Asis\Desktop\python\fonts\Roboto-Black.ttf", 72)
bold_font = pygame.font.Font(r"C:\Users\Patricia Ann De Asis\Desktop\python\fonts\Roboto-Bold.ttf", 48)
light_font = pygame.font.Font(r"C:\Users\Patricia Ann De Asis\Desktop\python\fonts\Roboto-Light.ttf", 34)
medium_font = pygame.font.Font(r"C:\Users\Patricia Ann De Asis\Desktop\python\fonts\Roboto-Medium.ttf", 21)
regular_font = pygame.font.Font(r"C:\Users\Patricia Ann De Asis\Desktop\python\fonts\Roboto-Regular.ttf", 11)

# Scoreboard Initialization
scoreboard = pygame.Surface([windowWidth, 50])
scoreboard.fill((0, 0, 0))

# Container size
screenSize = 500
rows = 20

# Snake Game Container
container = pygame.Surface([screenSize, screenSize])
container.fill((127, 127, 127))


class Cubes(object):
    rows = 20
    width = 500

    def __init__(self, start, directX=1, directY=0, color=snakeColor):
        self.pos = start
        self.directX = 1
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
            pygame.draw.circle(surface, green, circleMid, radius)
            pygame.draw.circle(surface, green, centerMid, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cubes(pos)
        self.body.append(self.head)
        self.directX = 0
        self.directY = 1

    # Snake Controls section
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()
            # Loop through dictionary of event keys
            for key in keys:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    if self.directX == 1:
                        pass
                    else:
                        self.directX = -1
                        self.directY = 0
                        # This a dictionary of current head position and also where the cubes going to turn
                        self.turns[self.head.pos[:]] = [self.directX, self.directY]

                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    if self.directX == -1:
                        pass
                    else:
                        self.directX = 1
                        self.directY = 0
                        # This a dictionary of current head position and also where the cubes going to turn
                        self.turns[self.head.pos[:]] = [self.directX, self.directY]

                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    if self.directY == 1:
                        pass
                    else:
                        self.directX = 0
                        self.directY = -1
                        # This a dictionary of current head position and also where the cubes going to turn
                        self.turns[self.head.pos[:]] = [self.directX, self.directY]

                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    if self.directY == -1:
                        pass
                    else:
                        self.directX = 0
                        self.directY = 1
                        # This a dictionary of current head position and also where the cubes going to turn
                        self.turns[self.head.pos[:]] = [self.directX, self.directY]

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
        var = self.head == Cubes(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.directX = 0
        self.directY = 1
        pass

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

    def __init__(self, X, Y):
        width = windowWidth
        height = windowHeight
        self.size = pygame.Surface([100, 40])
        self.text = pygame.font.Font
        self.rect = self.size.get_rect()
        self.rect.center = (X, Y)

    def draw(self, color):
        self.size.fill(color)
        win.blit(self.size, (self.rect.x, self.rect.y))


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
        pygame.draw.line(surface, black, (x, 60), (x, current_width + 60), 1)
        pygame.draw.line(surface, black, (10, y), (current_width + 10, y), 1)


def redraw_window(surface):
    global rows, screenSize, snake, food
    # what surface going to be filled
    surface.fill(white)
    # Casting the scoreboard and container into window
    win.blit(scoreboard, (0, 0))
    win.blit(container, (10, 60))
    snake.draw(surface)
    food.draw(surface)
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


def main_intro():
    global black_font, bold_font, medium_font, regular_font, light_font

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        win.fill(white)
        message1, messageLoc1 = text_object("Rapid", black_font, red)
        messageLoc1.center = ((windowWidth / 2 - 100), 200)
        message2, messageLoc2 = text_object("Snake", black_font, green)
        messageLoc2.center = ((windowWidth / 2 + 100), 200)
        detail1, detailLoc1 = text_object("This is a enhance version of snake game that has been"
                                          "already enhance by us", regular_font, black)
        detailLoc1.center = ((windowWidth / 2), (windowHeight / 2 + 50))
        play_game = Button((windowWidth / 2 - 100), 400)
        exit_game = Button((windowWidth / 2 + 100), 400)
        win.blit(message1, messageLoc1)
        win.blit(message2, messageLoc2)
        play_game.draw(red)
        exit_game.draw(green)
        win.blit(detail1, detailLoc1)
        pygame.display.update()
        clock.tick(8)


def main():
    global rows, snake, food, win, flag

    # Passing the Snake(object) to snake variable
    snake = Snake(snakeColor, (10, 10))
    # Passing the Cubes(object) to snack variable
    food = Cubes(random_snack(rows, snake), color=blue)

    flag = False
    # Main loop to load the animations and logic
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # pygame.time.delay is a limiter to maintain the performance of computer
        pygame.time.delay(50)
        clock.tick(FPS)
        snake.move()
        # Checking if the head of the snake is in the food current location
        if snake.body[0].pos == food.pos:
            # Add another cube into the body
            snake.addCube()
            # Spawn another food
            food = Cubes(random_snack(rows, snake), color=blue)

        # Check the current length of the snake for score counting
        for x in range(len(snake.body)):
            # Collision checker if the head hit itself
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                # Show score into the console
                print('Score: ', len(snake.body))
                # Call message box function
                message_box("You lose!", "Try again")
                # Call reset function
                snake.reset((10, 10))
                break
        # Calling the redraw_window to update the game
        redraw_window(win)
        # Update the screen and fill the window
        pygame.display.flip()
        # Second update for assurance purpose
        pygame.display.update()

    pass


main_intro()
main()
