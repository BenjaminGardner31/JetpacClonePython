import pygame
from pygame.locals import *
from pygame.mixer import Sound

#Used to assign common values and define repeated functions for all BlittableObjects
class BlittableObject :

    #STANDARD_WIDTH    : float     - original game screen width, for scaling
    STANDARD_WIDTH = 640.0
        
    def __init__(self, surface) :
        '''
		Used to reduce code and setup generic variables
        surface      : Surface         - BlittableObject container
        surf_width   : int             - surface width
        surf_height  : int             - surface height
        image        : Image           - current BlittableObject image
        rect         : Rect            - BlittableObject rectangle
        scale        : float           - screen scale factor
        '''
        self.surface = surface
        self.surf_width, self.surf_height = self.surface.get_size()
        self.scale = self.surf_width/BlittableObject.STANDARD_WIDTH
        self.image = None        
        self.rect = None
         
    def draw(self) :
        #blit BlittableObject to screen
        self.surface.blit(self.image, self.rect)
        
    def set_image(self, image, size = None) :
        ''' 
           load image to scale, generate rect
           
           image    : str       - path to image file
        '''
        self.image = self.load_image(image, size)
        self.rect = self.image.get_rect()
        if not size: 
            w, h = self.image.get_size()
            w = int(w * self.scale) 
            h = int(h * self.scale) 
            self.rect.size = (w, h)
            self.image = self.image_transform((w,h))
        
    def load_image(self, image, size = None):
        '''
            Load image file, in the specified size
            
            image   : str           - image file to load
            size    : (int, int)    - size to scale to
            
            image_transform(image, size) -> Image
        '''
        if size:
            return self.image_transform(size, pygame.image.load(image))
        else:
            return pygame.image.load(image)
    
    def image_transform(self, size, image = None) :
        '''
            scale image to specified size
            
            size    : (int, int)    - size to scale to
            image   : Image         - image object to scale. Defaults to self.image
            
            image_transform(size, image) -> Image
        '''
        new_image = None
        
        if image :
            new_image = pygame.transform.scale(image, size)
        else :
            new_image = pygame.transform.scale(self.image, size)
            self.rect.size = new_image.get_size()
        return new_image
        
    def image_flip(self, image, xbool, ybool) :
        '''
            scale image to specified size
            
            image    : Image    - Image object to flip
            xbool    : bool     - flip left-to-right
            ybool    : bool     - flip up-side-down
            
            image_flip(image, xbool, ybool) -> Image
        '''
        return pygame.transform.flip(image, xbool, ybool)
    
    def set_sound(self, sound):
        '''
            scale image to specified size
            
            sound    : Sound    - Sound object to play
        '''
        return Sound(sound)
        


