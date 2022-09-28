#Parts taken from code written by Paulus Lahur
#Rest written by Mikhail Romadinov

#This is a drawing app with a uiManagement system
#each thing which is drawn (inlcuding freedraw elements) is put into a uiElement which is in turn placed into a uiGroup
# press w on the keyboard to clear the drawings
# press s to open the brush Size Popup (NOT FINISHED YET)

# Have fun :)


# Stuff to be done: 
# make buttons do stuff
# add a .action() function to the uiElems class
# make the mouseLockElem segment have some function
# code for above between lines 129 - 144 ish


from multiprocessing import Manager
from os import getgroups
from re import S
import sys
from turtle import screensize
from matplotlib.pyplot import text 
import pygame
from scipy import interpolate
import numpy

maxBrushSize = 100
minBrushSize = 0.001
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
GREY = (150,150,150)
DEFAULT_COLOUR = RED
DEFAULT_SIZE = 1

# Define screen size in terms of pixel count.
SCREEN_SIZE_X = 640
SCREEN_SIZE_Y = 580
SCREEN_SIZE = (SCREEN_SIZE_X, SCREEN_SIZE_Y)
SCREEN_CENTER = (SCREEN_SIZE_X // 2, SCREEN_SIZE_Y // 2)
TOOLBAR_HEIGHT = 100

# Define mouses

LEFT = 1
RIGHT = 2

def main():
    #init pygame
    pygame.init()

    #set window title
    pygame.display.set_caption("Draw")

    #setup screen
    screen = pygame.display.set_mode(SCREEN_SIZE)

    #Fill screen with white
    screen.fill(WHITE)

    #initialisation
    is_running = True
    emptyGroup = []
    uiGroups = [['drawpanel',emptyGroup,'high',True],['brushSizePopup',emptyGroup,'high',False]]
    uiManager = uiManagement(uiGroups,screen)
    currentView = 'drawpanel'
    tempPoints = []
    is_drawing = False
    mouseLockElem = None
    selectedLayer = 1
    drawCount = 0
    drawColour = DEFAULT_COLOUR
    drawSize = DEFAULT_SIZE
    font = pygame.font.Font('freesansbold.ttf', 15)
    smallerfont = pygame.font.Font('freesansbold.ttf',7)

    uiManager.resetDrawPanel()
    #run pygame until is_running is false
    while is_running:
        #watch all events in the window
        for event in pygame.event.get():
            #reset view prior to render
            screen.fill(WHITE)

            if event.type == pygame.MOUSEMOTION:
                if is_drawing and currentView == 'drawpanel':
                    x,y = event.pos
                    tempPoints.append((x,y))
                
                if mouseLocked:
                    x,y = event.pos
                    mouseLockElem.updateVal((x,y))

            uiGroups = uiManager.getGroups()
            for uiGroup in uiGroups:
                uiGroup.renderElems()
            
            for point in tempPoints:
                pygame.draw.circle(screen,drawColour,point,drawSize)
            
            #input management
            if event.type == pygame.KEYDOWN:
                #Resets drawpanel when backspace/delete pressed back to a white screen
                if (event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE or event.key == pygame.K_w) and currentView == 'drawpanel':
                    uiManager.resetDrawPanel()
                    drawCount=0

                #Opens the size popup
                if event.key == pygame.K_s and currentView == 'drawpanel':

                    uiManager.toggleActivateElement('brushSizePopup')
                    uiManager.resetUIElems('brushSizePopup')
                    x,y = pygame.mouse.get_pos()
                    backElem = uiElem(x-20,y-10,'sizePopupBkgRect',screen,50,120,'rect','bkg',2,GREY,None, active=True)
                    uiManager.addFinElem('brushSizePopup', backElem)

                    textElem = uiElem(x+40,y+5,'sizePopupText',screen,None,None,'text','smallerfont',1,WHITE,None,text='Change Brush Size:',text_colour=WHITE, active=True)
                    uiManager.addFinElem('brushSizePopup', textElem)
                    #textElem = smallerfont.render("Change Brush Size:",True,WHITE,None)
                    #textElemRect = textElem.get_rect()
                    #textElemRect.center = (x+40,y+7)


            
            #Checks for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                overBut = None
                overBut = checkOverButton(uiManager,x,y)
                if not overBut == None:
                    if overBut.action():
                        mouseLockElem = overBut
                        mouseLocked = True
                        overBut.action()
                    else:
                        overBut.action()
                if mouseLockElem == None and currentView == 'drawpanel':
                    is_drawing = True
                else:
                    is_drawing = False
            

            
            if event.type == pygame.MOUSEBUTTONUP:
                
                #applies smoothing and adds 
                if is_drawing:
                    is_drawing = False
                    smoothPoints = smoothDraw(tempPoints)
                    smthpnts = []
                    for ind,point in enumerate(smoothPoints[0]):
                        smthpnts.append([drawColour,point,smoothPoints[1][ind],drawSize])
                    uiManager.addElem('drawpanel', [numpy.mean(smoothPoints[0]), numpy.mean(smoothPoints[1]), 'freedraw-'+str(drawCount),screen,None,None,'freedraw','brush',selectedLayer,drawColour,None,False,None,None,smthpnts,None,None,None,True])
                    drawCount += 1
                    tempPoints = []
                
                if mouseLocked:
                    mouseLockElem = None
                    mouseLocked = False



            # If one of the events is closing the window, 
            # set the status "is_running" to False,
            # so that we get out of this while loop
            elif event.type == pygame.QUIT:
                is_running = False
            
            pygame.display.flip()

    pygame.quit()
    sys.exit()

            

class uiManagement:
    def __init__(self,uiGroups,screen):
        groups = []
        for group in uiGroups:
            grp = uiGroup(group[0],group[1],group[2],group[3])
            groups.append(grp)
        self.uiGroups = groups
        self.screen = screen

    def addElem(self,uiGroupLabel,uiElem):
        """uiGroupLabel refers to the label of the uiGroup in question where the uiElem will be added"""
        #print(self)
        groups = self.getGroups()
        #print(groups)
        for group in groups:
            #print(group.getLabel())
            if group.getLabel() == uiGroupLabel:
                #print('doesthsigooo')
                group.addElem(uiElem)
    
    def addFinElem(self,uiGroupLabel,uiElem):
        #print(self)
        groups = self.getGroups()
        #print(groups)
        for group in groups:
            #print(group.getLabel())
            if group.getLabel() == uiGroupLabel:
                #print('doesthsigooo')
                group.addFinElem(uiElem)
    
    def getGroups(self):
        return self.uiGroups
    
    def resetDrawPanel(self):
        for uiGroup in self.uiGroups:

            print('reset')
            print(uiGroup.getLabel())
            if uiGroup.getLabel() == 'drawpanel':
                uiGroup.resetElements([])
    
    def resetUIElems(self,groupLabel):
        for uiGroup in self.uiGroups:
            if uiGroup.getLabel() == groupLabel:
                uiGroup.resetElements([])
    
    def toggleActivateElement(self,groupLabel,elemLabel = None):
        """Toggle Activate Element toggles the visibility activation of an uielement or uigroup for Rendering"""
        for group in self.uiGroups:
            if group.label == groupLabel:
                if group.active and elemLabel == None:
                    group.active = False
                else:
                    group.active = True
                if not elemLabel == None:
                    for element in group.uiElements:
                        if element.label == elemLabel:
                            if element.active:
                                element.active = False
                            else:
                                element.active = True
    
    #Returns a list of active buttons/interactive ui elements
    def activeButtons(self):
        temp = []
        for group in self.uiGroups:
            if group.active:
                for elem in group.uiElements:
                    if elem.active and (type == 'button' or type == 'interactive'):
                        temp.append(elem)
        return temp



class uiGroup:
    def __init__(self,label,uiElements,priority,active):
        self.label = label
        elmnts = []
        for elem in uiElements:
            elmnts.append(uiElem(elem[0],elem[1],elem[2],elem[3],elem[4],elem[5],elem[6],elem[7],elem[8],elem[9],elem[10],elem[11],elem[12],elem[13],elem[14],elem[15],elem[16],elem[17],elem[18]))
        self.uiElements = elmnts
        self.priority = priority
        self.active = active
    
    def getLabel(self):
        return self.label
    
    def addFinElem(self,elem):
        self.uiElements.append(elem)

    def addElem(self,elem):
        element = uiElem(elem[0],elem[1],elem[2],elem[3],elem[4],elem[5],elem[6],elem[7],elem[8],elem[9],elem[10],elem[11],elem[12],elem[13],elem[14],elem[15],elem[16],elem[17],elem[18])
        self.uiElements.append(element)

    #Renders the ui elements in a uigroup based upon their layer (layer >= 0)
    def renderElems(self):
        """RenderElems renders all the uiElements in a uigroup based upon their layer values where layer >=0"""
        renderOrder = []
        srts = []
        if self.active:
            if not (self.uiElements == None or self.uiElements == []):
                #"yes")
                #print(self.uiElements)
                for elem in self.uiElements:
                    srts.append(elem.getlayer())
                numLayers = numpy.max(srts)
                print(numLayers)
                n = numLayers
                while n >= 0:
                    #print(n)
                    for elem in self.uiElements:
                        #print(elem.getlayer())
                        if elem.getlayer() == n:
                         #   print(elem.label)
                            renderOrder.append(elem)
                    n = n - 1
                #print(renderOrder)
                for elem in renderOrder:
                    #print("rendering")
                    elem.render()
    
    #Resets the ui elements in a uigroup
    def resetElements(self, val):
        self.uiElements = val

class uiElem:

    def __init__(self,x,y,label,screen,height,width,shape,type,layer,colour,bkgcolour=None,followcursor=False,text=None,text_colour=BLACK,points = None,endpoint_left = None,endpoint_right = None, button_action = None, button_link = None, active = False):
        self.x = x
        self.y = y
        self.label = label
        self.screen = screen
        self.height = height
        self.width = width
        self.shape = shape
        self.type = type
        self.layer = layer
        self.colour = colour
        self.bkgcolour = bkgcolour
        self.followcursor=followcursor
        self.text = text
        self.text_colour = text_colour
        self.points = points
        self.endpoint_left = endpoint_left
        self.endpoint_right = endpoint_right
        self.button_action = button_action
        self.button_link = button_link
        self.active = active
        self.locked = False
        if self.shape == 'text':
            self.font = pygame.font.Font('freesansbold.ttf', 15)
            self.smallerfont = pygame.font.Font('freesansbold.ttf',7)
        
    
    def getlayer(self):
        #print(self.layer)
        return self.layer

    def action(self):
        if self.type == 'button':
            if self.button_action == 'lockmouse':
                self.locked = True
                return True



    def render(self):
        if self.active:
            if self.shape == 'rect':
                pygame.draw.rect(self.screen, self.colour, pygame.Rect(self.x,self.y,self.width,self.height),0)
            elif self.shape == 'circle':
                pygame.draw.circle(self.screen,self.colour,(self.x,self.y),self.width,0)
            elif self.shape == 'freedraw':
                for point in self.points:
                    #print(point)
                    pygame.draw.circle(self.screen,point[0],(int(point[1]),int(point[2])),point[3],0)
            elif self.shape == 'text':
                if self.type == 'smallerfont':
                    print("teext")
                    txt = self.smallerfont.render(self.text,True,self.colour,self.bkgcolour)
                    txtRect = txt.get_rect()
                    txtRect.center = (self.x,self.y)
                    self.screen.blit(txt,txtRect)
            elif self.shape == 'line':
                pygame.draw.line(self.screen,self.colour,(self.endpoint_left[0],self.endpoint_left[1]),(self.endpoint_right[0],self.endpoint_right[0]),self.width)


def smoothDraw(points):
    x = []
    y = []
    if len(points)<=3:
        points = []
        points.append([-2,0])
        points.append([0,-2])
        points.append([1,0])
        points.append([0,-1])
    for point in points:
        if point[0]<SCREEN_SIZE_X:
            x.append(int(point[0]))
        else:
            x.append(SCREEN_SIZE_X-1)
        
        if point[1]<SCREEN_SIZE_Y:
            y.append(int(point[1]))
        else:
            y.append(SCREEN_SIZE_Y-1)
    print("x")
    print(x)
    print("y")
    print(y)
    tck, *rest = interpolate.splprep([x,y])
    #if ()
    n = len(x)*50
    u = numpy.linspace(0,1,num=n*4)
    smooth = interpolate.splev(u,tck)
    print("smooth: " + str(smooth))
    return smooth

def checkOverButton(uiManager,x,y):
    actButs = uiManager.activeButtons()
    for but in actButs:
        if but.corn('tl')[0]<=x<=but.corn('br') and but.corn('br')<=y<=but.corn('tl'):
            return but
    return None

if __name__ == '__main__':
    main()