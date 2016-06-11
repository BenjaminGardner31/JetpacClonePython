from pygame.mixer import Sound
from blittable_object import BlittableObject
import random

class Collectables(BlittableObject) :

    SHIP_PART ='sounds/part.ogg'
    FUEL = 'sounds/fuel.ogg'
    FALL_VELOCITY = 3

    def __init__(self, surface) :
        '''
        fuel_image    : str             - fuel collectable
        part_images   : [str]           - part collectables
        velocity      : int             - how fast is collectable dropping?
        state         : int             - moving? resting? collected?
        collidables   : [Rect]          - things to bump into
        parts_dropped : int             - how many parts dropped so far?
        fuel_dropped  : int             - how many fuel cells dropped?
        item_type     : int             - is current item a part or fuel?
        '''
        BlittableObject.__init__(self, surface)
        self.fall_velocity = int(Collectables.FALL_VELOCITY * self.scale)
        self.collidables = None
        self.next_item = 0
        self.velocity = 0
        self.falling = True
        self.items = (('images/rocket_part_2.png', Collectables.SHIP_PART),
                      ('images/rocket_part_3.png', Collectables.SHIP_PART),
                      ('images/rocket_part_4.png', Collectables.SHIP_PART),
                      ('images/Fuel.png', Collectables.FUEL),
                      ('images/Fuel.png', Collectables.FUEL),
                      ('images/Fuel.png', Collectables.FUEL),
                      ('images/Fuel.png', Collectables.FUEL))
        self.spawn()

    def update(self, platforms) :
        #decide what to do next
        self.collidables = platforms
        if self.falling :
            self.drop()

    def draw(self) :
        #blit collectable item to screen
        if self.next_item <= len(self.items) :
            BlittableObject.draw(self)
        
    def spawn(self) :
        #create the next item
        self.set_image(self.items[self.next_item][0])
        self.item_dropped()
        self.next_item += 1
    
    def item_dropped(self):
        start_x = random.randint(10, self.surf_width - self.rect.width - 10)
        self.rect.bottomleft = (start_x, 0)
        self.falling = True
        self.velocity = self.fall_velocity
    
    def drop(self) :
        #collectable item falling, checking for collisions and adjusting velocity 
        self.velocity = self.fall_velocity
        bump = False
        destination = self.rect.move(0,self.velocity)
        collider = destination.collidelist(self.collidables)
        if collider != -1 :
            self.velocity = self.collidables[collider].top - self.rect.bottom
            bump = True
        elif destination.bottom > self.surf_height :
            self.velocity = self.surf_height - self.rect.bottom
            bump = True
        self.rect = self.rect.move(0,self.velocity)
        if bump :
            self.velocity = 0
            self.falling = False

    def collect(self) :
        #let player collect item
        if self.next_item < len(self.items):
            self.sound = self.set_sound(self.items[self.next_item-1][1])
            self.sound.play()
            self.spawn()
        else:
            self.next_item += 1
            
        
        



        


        
