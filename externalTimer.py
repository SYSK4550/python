# Libraries
import time
import pygame

pygame.init()
start_time = time.time()

seconds = int(0)
minutes = int(0)
hours = int(0)


# Main timer
class ExTimer(object):
    def __init__(self, count):
        current_time = time.time()
        self.count = count
