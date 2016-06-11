from blittable_object import BlittableObject

class Ship(BlittableObject) :  
    '''
    MAX_VELOCITY  : int        - Ship speed limit
    AUDIO_ASCEND  : str        - Blastoff sound file
    '''

    MAX_VELOCITY = 7
    AUDIO_ASCEND = 'sounds/blastoff.ogg'
    FLAME_IMAGE = "images/rocket_flame.png"
        
    def __init__(self, surface) :
        '''
        ship_images  : [str]           - ship buildup stages
        built_parts  : int             - how many ship parts attached?
        fuel         : int             - how many fuel cells inserted?
        velocity     : int             - how fast is ship moving?
        max_velocity : int             - ship speed limit, adjusted to screen
        sound        : Sound           - ship Sound player object
        launchpad    : (int,int)       - where to ground ship
        '''
        BlittableObject.__init__(self, surface)
        self.launchpad = (self.surf_width/2, self.surf_height)
        self.max_velocity = int(Ship.MAX_VELOCITY * self.scale)
        
        #Must agree with the collectable list!!
        self.ship_images = ('images/rocket_stage_1.png',
                             'images/rocket_stage_2.png',
                             'images/rocket_stage_3.png',
                             'images/rocket_completed.png',
                             'images/rocket_fuel_1.png',
                             'images/rocket_fuel_2.png',
                             'images/rocket_fuel_3.png',
                             'images/rocket_fueled.png')        
        self.velocity = 0
        self.sound = None
        self.set_image(self.ship_images[0])
        self.rect.midbottom = self.launchpad
        self.collected_items = 1
        self.takeoff_image = self.load_image(Ship.FLAME_IMAGE, self.rect.size)
        self.takeoff_image_rect = self.takeoff_image.get_rect()
        self.takeoff_image_rect.topleft = self.rect.bottomleft
         
    def update(self) :
        #decide what to do next
        if self.rect.bottom < 0 : #ship has escaped
            self.velocity = 0
            if self.sound != None :
                self.sound.stop()
        elif self.all_collected() :
            if self.rect.bottom == self.surf_height: #play blastoff sound only once
                self.sound = self.set_sound(Ship.AUDIO_ASCEND)
                self.sound.play()
            return self.ascend()
        
    def draw(self):
        #blit to screen
        if not self.rect.bottom < 0 : #ship still on screen
            BlittableObject.draw(self)
            self.surface.blit(self.takeoff_image, self.takeoff_image_rect)
  
    def use_collectable(self) :
        #use collectable from player in ship
        if not self.all_collected():
            self.set_image(self.ship_images[self.collected_items])
            self.rect.midbottom = self.launchpad
            self.collected_items += 1
    
    def ascend(self) :
        #ship blastoff
        self.velocity += (self.max_velocity - self.velocity) * 0.05
        self.rect = self.rect.move(0,-self.velocity)
        self.takeoff_image_rect.topleft = self.rect.bottomleft
        if self.rect.bottom <= 0:
            #returns True if the game is won and the animation is finished
            return True

    def all_collected(self):
        ''' 
            have all parts been collected? 
            all_collected() -> bool
        '''
        return self.collected_items >= len(self.ship_images)
        


        



