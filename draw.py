# A simple drawing program using python and pygame.
# Author: Paulus Lahur

# System-related library.
# More info: https://docs.python.org/3/library/sys.html
import sys

# Pygame library.
# More info: https://www.pygame.org/wiki/GettingStarted
import pygame

# Define basic colors in RGB (Red Green Blue) format.
# The value is integer ranging from 0 to 255 (ie. 256 levels).
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)

# Define screen size in terms of pixel count.
SCREEN_SIZE_X = 640
SCREEN_SIZE_Y = 480
SCREEN_SIZE = (SCREEN_SIZE_X, SCREEN_SIZE_Y)
SCREEN_CENTER = (SCREEN_SIZE_X // 2, SCREEN_SIZE_Y // 2)

# Initialize pygame
pygame.init()

# Set window title 
pygame.display.set_caption("Draw")

# Now set up the screen
screen = pygame.display.set_mode(SCREEN_SIZE)

# Fill the screen with color (the default is black).
screen.fill(WHITE)

# Some initialization.
is_running = True
is_drawing = False
xprev, yprev = None, None

# Run pygame continuously until the status "is_running" turns False.
while is_running:

    # Monitor all events going on in the window.
    for event in pygame.event.get():

        # If one of the events is closing the window, 
        # set the status "is_running" to False,
        # so that we get out of this while loop
        if event.type == pygame.QUIT:
            is_running = False

        # When the mouse button is pressed down, start drawing.
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_drawing = True
            x, y = event.pos
            # Draw circle at the start of the drawing
            pygame.draw.circle(screen, RED, (x, y), 2, 2)
            xprev, yprev = x, y

        # When the mouse button is released, stop drawing
        if event.type == pygame.MOUSEBUTTONUP:
            is_drawing = False
            xprev, yprev = None, None

        # When the mouse is moved while its button is pressed down,
        # keep drawing.
        if (event.type == pygame.MOUSEMOTION) and is_drawing:
            x, y = event.pos
            if (xprev != None) and (yprev != None):
                # Draw lines instead of circles to make sure the drawing 
                # is continuous. A line connects previous mouse location
                # to the current one.
                pygame.draw.line(screen, RED, (xprev, yprev), (x, y), 4)
            xprev, yprev = x, y

        # If one of the keys is pressed
        if event.type == pygame.KEYDOWN:
            # If the key "DELETE" is pressed
            if event.key == pygame.K_DELETE:
                screen.fill(WHITE)

    # Put the drawing into display
    pygame.display.flip()

pygame.quit()
sys.exit()
