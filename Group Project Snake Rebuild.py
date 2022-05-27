# CTTO
# Group Project Snake Rebuild

# Libraries
# import os
import random
import time
import tkinter as tk
from tkinter import messagebox
import pygame

# Game Initialize
pygame.init()
ranNum = ["-1", "0", "1"]
starting = [int(x) for x in ranNum]

# Global Variable Single Call
width = 500
rows = 20
win = pygame.display.set_mode((width, width))
icon = pygame.image.load("imgs\bgpic1.png")

# Time and FPS Section
clock = pygame.time.Clock()
FPS = 10

# Color Section
black = (0, 0, 0)
white = (255, 255, 255)
snakeColor = (255, 255, 0)
snakeFood = (255, 0, 45)
grid = (0, 0, 0)
bgColor = (127, 255, 127)

# Color Button Section
red = (255, 0, 0)
clickedRed = (127, 0, 0)

green = (0, 255, 0)
clickedGreen = (0, 127, 0)

# Game Fonts
largeFont = pygame.font.Font('fonts\\Courier Prime Bold.ttf', 52)
mediumFont = pygame.font.Font('fonts\\Courier Prime.ttf', 15)
smallFont = pygame.font.Font('fonts\\Courier Prime.ttf', 11)

# Pause variable
pause = False


class Cubes(object):
    rows = 20
    w = 500

    def __init__(self, start, color=snakeColor):
        self.pos = start
        self.directX = random.choice(starting)
        self.directY = random.choice(starting)
        self.color = color

    def move(self, directX, directY):
        self.directX = directX
        self.directY = directY
        self.pos = (self.pos[0] + self.directX, self.pos[1] + self.directY)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circlemid = (i * dis + centre - radius, j * dis + 8)
            centermid = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (255, 0, 0), circlemid, radius)
            pygame.draw.circle(surface, (255, 0, 0), centermid, radius)


class Snakes(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cubes(pos)
        self.body.append(self.head)
        self.directX = 0
        self.directY = 1

    @property
    def move(self):
        global pause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    if self.directX == 1:
                        pass
                    else:
                        self.directX = -1
                        self.directY = 0
                        self.turns[self.head.pos[:]] = [self.directX, self.directY]

                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    if self.directY == 1:
                        pass
                    else:
                        self.directX = 0
                        self.directY = -1
                        self.turns[self.head.pos[:]] = [self.directX, self.directY]

                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    if self.directX == -1:
                        pass
                    else:
                        self.directX = 1
                        self.directY = 0
                        self.turns[self.head.pos[:]] = [self.directX, self.directY]

                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    if self.directY == -1:
                        pass
                    else:
                        self.directX = 0
                        self.directY = 1
                        self.turns[self.head.pos[:]] = [self.directX, self.directY]

                if keys[pygame.K_ESCAPE] or keys[pygame.K_p]:
                    if not pause:
                        pass
                    else:
                        pause = True

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.directX == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.directX == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.directY == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.directY == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.directX, c.directY)

    def reset(self, pos):
        self.head = Cubes(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.directX = random.choice(starting)
        self.directY = random.choice(starting)

    def addcube(self):
        tail = self.body[-1]
        dx, dy = tail.directX, tail.directY

        if dx == 1 and dy == 0:
            self.body.append(Cubes((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cubes((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cubes((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cubes((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].directX = dx
        self.body[-1].directY = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def DrawGrid(current_width, row, surface):
    sizeBetween = current_width // row

    x = 0
    y = 0
    for l in range(row):
        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface, grid, (x, 0), (x, current_width))
        pygame.draw.line(surface, grid, (0, y), (current_width, y))


def redraw_window(surface):
    global rows, width, s, snack
    surface.fill(bgColor)
    s.draw(surface)
    snack.draw(surface)
    DrawGrid(width, rows, surface)
    pygame.display.update()


def random_snack(row, item):
    positions = item.body

    while True:
        x = random.randrange(row)
        y = random.randrange(row)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def text_object(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_menu(text, size):
    global largeFont
    text_surf, text_rect = text_object(text, largeFont)
    text_rect.center = ((width / 2), (width / 2))
    win.blit(text_surf, text_rect)

    pygame.display.update()

    main()


def button(text, x, y, w, h, iB, aB, action=None):
    global width, mediumFont
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(win, aB, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()

    else:
        pygame.draw.rect(win, iB, (x, y, w, h))

    text_surf, text_rect = text_object(text, mediumFont)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    win.blit(text_surf, text_rect)


def Unpause():
    global pause
    pause = False


def paused():
    global width, smallFont, mediumFont, largeFont, pause
    pygame.display.set_caption("Snake Saga")

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.fill(bgColor)
        TextSurf, TextRect = text_object("SNAKE SAGA", largeFont)
        TextRect.center = ((width / 2), 200)
        win.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_object("PAUSE GAME", mediumFont)
        TextRect.center = ((width / 2), 290)
        win.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_object("Game has been Pause take your time.", smallFont)
        TextRect.center = ((width / 2), 300)
        win.blit(TextSurf, TextRect)

        button("CONTINUES", 125, 350, 100, 25, red, clickedRed, Unpause)
        button("QUIT", 325, 350, 50, 25, green, clickedGreen, quitgame)

        pygame.display.update()
        time.sleep(300)


def quitgame():
    pygame.quit()
    quit()


def Intro():
    global width, smallFont, mediumFont, largeFont
    pygame.display.set_caption("Snake Saga")

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.fill(bgColor)
        TextSurf, TextRect = text_object("SNAKE SAGA", largeFont)
        TextRect.center = ((width / 2), 200)
        win.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_object("The objective of this game is to eat the apple.", smallFont)
        TextRect.center = ((width / 2), 290)
        win.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_object("The more apple you eat the longer you are.", smallFont)
        TextRect.center = ((width / 2), 300)
        win.blit(TextSurf, TextRect)

        button("PLAY", 125, 350, 50, 25, red, clickedRed, main)
        button("QUIT", 325, 350, 50, 25, green, clickedGreen, quitgame)

        pygame.display.update()
        clock.tick(15)


def main():
    global width, rows, s, snack, win, pause
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Snake Saga")
    s = Snakes(snakeColor, (10, 10))
    snack = Cubes(random_snack(rows, s), color=snakeFood)

    flag = True

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()
                quit()

        pygame.time.delay(50)
        clock.tick(FPS)
        s.move
        if s.body[0].pos == snack.pos:
            s.addcube()

            snack = Cubes(random_snack(rows, s), color=snakeFood)

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                message_box('Your Score', len(s.body))
                message_box('You Lost!', 'Your ran to your self. Play Again..')
                s.reset((10, 10))
                break

        redraw_window(win)

    pass


Intro()
main()
