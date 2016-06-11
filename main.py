import pygame, sys
from pygame.locals import *
from screen import Screen

#Function that takes the events and decides what to do with them
def event_handler(main_screen, event):
    if event.type == KEYDOWN:
        if event.key == K_UP or event.key == K_w:
            main_screen.key_register["Up"] = True
        elif event.key == K_RIGHT or event.key == K_d:
            main_screen.key_register["Right"] = True
        elif event.key == K_LEFT or event.key == K_a:    
            main_screen.key_register["Left"] = True  
        elif event.key == K_SPACE:
            main_screen.key_register["Shoot"] = True
    elif event.type == KEYUP:
        if event.key == K_ESCAPE :
            main_screen.menu_toggle()
        elif event.key == K_UP or event.key == K_w:
            main_screen.key_register["Up"] = False
        elif event.key == K_RIGHT or event.key == K_d:
            main_screen.key_register["Right"] = False
        elif event.key == K_LEFT or event.key == K_a:    
            main_screen.key_register["Left"] = False
    elif event.type == MOUSEBUTTONUP:
        main_screen.mouse_handler(pygame.mouse.get_pos())
    else:
        pass

#This gets called to quit the game, called from the menu only currently.    
def quit_program():
    pygame.quit()
    sys.exit()

pygame.init()
FPS = 30
pygame.display.init()
pygame.display.set_mode((0,0), pygame.FULLSCREEN)
CANVAS = pygame.display.get_surface()
fpsClock = pygame.time.Clock()
pygame.display.set_caption('Jetpac: from "{} Python".format("Monty")')
main_screen = Screen(CANVAS, quit_program)

while True :
    """
    This while loop is the main game processor
    it passes all of the events from the event stack
    to the event_handler
    Then updates and draws all parts of the game
    """
    for event in pygame.event.get():
        event_handler(main_screen, event)
    main_screen.update()
    main_screen.draw()
    pygame.display.update()
    fpsClock.tick(FPS)
