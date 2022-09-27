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
SCREEN_SIZE_Y = 580
SCREEN_SIZE = (SCREEN_SIZE_X, SCREEN_SIZE_Y)
SCREEN_CENTER = (SCREEN_SIZE_X // 2, SCREEN_SIZE_Y // 2)
TOOLBAR_HEIGHT = 100

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
        
        #Buttons for the Toolbar
        class Button:
            def __init__(self, x, y, width, height, color, text=None, text_color = BLACK):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.color = color
                self.text = text
                self.text_color = text_color
            def draw(self, screen):
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
                pygame.draw.react(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
                if self.text:
                    button_font = pygame.font.SysFont("calibri")
                    text_surface = button.font.render(self.text, 1, self.text_color)
                    screen.blit(text_surface, (self.x + self.width/2 - text_surface.get_width()/2)
             def clicked(self, pos):
                x,y = pos
                if not (x >= self.x and x <= self.x + self.width):
                    return False
                if not (y >= self.y and y <= self.y + self.height):
                    return False
                return True
             button_y = SCREEN_SIZE Y - TOOLBAR_HEIGHT/2 - 25
             buttons = [
                 Button(5, button_y, 20, 20, BLACK)
                 Button(30, button_y, 20, 20, RED)
                 Button(55, button_y, 20, 20, BLUE)
                 Button(80, button_y, 20, 20, GREEN)
                 Button(105, button_y, 20, 20, YELLOW)
                 Button(130, button_y, 20, 20, MAGENTA)
                 Button(155, button_y, 20, 20, CYAN)
                 Button(170, button_y, 20, 20, WHITE)
                 Button(195, button_y, 20, 20, WHITE, "Erase", BLACK)
                 Button(220, button_y, 20, 20, WHITE, "Clear", BLACK)
                 Button(245, button_y, 20, 20, BLACK)
             for button in buttons:
                 button.draw(screen)
    # Put the drawing into display
    pygame.display.flip()

pygame.quit()
sys.exit()
