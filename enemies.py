from blittable_object import BlittableObject
import pygame
from pygame.locals import *
import random


class Enemy(BlittableObject) :

    IMAGE = "images/enemy.png"
    SPEED = 5
    
    def __init__(self, surface, game_level):
        BlittableObject.__init__(self, surface)
        self.set_image(Enemy.IMAGE)
        self.set_speed(game_level)
        self.set_pos()
        
    def set_speed(self, game_level):
        game_mod = 1 + (game_level-1) * 0.2
        self.horiVelocity = int(Enemy.SPEED * self.scale * game_mod) 
        self.vertVelocity = int(random.randint(1, Enemy.SPEED) * self.scale)
    
    def set_pos(self):
        self.rect.topleft = (self.surf_width * random.randint(0, 1), random.randint(0,self.surf_height))
    
    #These are the rebound functions
    def reverseH(self):
        self.horiVelocity = - self.horiVelocity
    def reverseV(self):
        self.vertVelocity = - self.vertVelocity 
    
    # stops the enemies from leaving the screen   
    def boundary(self):
        if  (self.rect.left >= self.surf_width - self.rect.width and self.horiVelocity > 0 or 
                self.rect.left <= 0 and self.horiVelocity < 0):
            self.reverseH()
        if (self.rect.bottom <= self.rect.height and self.vertVelocity < 0 or
                self.rect.bottom >= self.surf_height  and self.vertVelocity > 0):
            self.reverseV()
    
    #causes collisions with items within the screen to cause a rebound        
    def itemCollider(self, collidables):
        destination = self.rect.move(self.horiVelocity, 0) 
        collideX = destination.collidelist(collidables)
        if collideX != -1:
            self.reverseH()
        destination = self.rect.move(0, self.vertVelocity) 
        collideY = destination.collidelist(collidables)
        if collideY != -1:
            self.reverseV()
    
    def update(self, collidables):
        self.boundary()
        self.itemCollider(collidables)
        self.rect=self.rect.move(self.horiVelocity, self.vertVelocity)

    def die(self):
        pass
