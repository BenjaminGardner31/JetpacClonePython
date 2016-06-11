from blittable_object import BlittableObject

class Player(BlittableObject):

    PLAYER_IMAGE = 'images/jetpac_hero_base.png'
    FLYING_PLAYER_IMAGE = 'images/jetpac_hero_boost.png' 
    HIT_PLAYER_IMAGE = "images/jetpac_hero_base_hit.png"
    HIT_FLYING_PLAYER_IMAGE = "images/jetpac_hero_boost_hit.png"
    UP_SPEED = 16 
    SIDE_SPEED = 8
    DOWN_SPEED = 5
    START_LIVES = 3  #The number of lives to be set at the beginning of each level.
    ANIMATION_LENGTH = 20
    
    def __init__(self, surface):
        BlittableObject.__init__(self, surface)
        self.up_speed = int(Player.UP_SPEED * self.scale)
        self.side_speed = int(Player.SIDE_SPEED * self.scale)
        self.down_speed = int(Player.DOWN_SPEED * self.scale)
        self.set_image(Player.PLAYER_IMAGE)
        self.rect.bottomleft = (self.surf_width/2, self.surf_height)
        self.velocity = [0, self.down_speed]
        self.image_ref = 0
        self.orientation = 0
        #Loads all of images initially to allow quick and easy switching during update.
        self.image_list = [[self.load_image(Player.PLAYER_IMAGE, self.rect.size),
                            self.load_image(Player.FLYING_PLAYER_IMAGE, self.rect.size)],
                            [self.image_flip(self.load_image(Player.PLAYER_IMAGE, self.rect.size), True, False),
                             self.image_flip(self.load_image(Player.FLYING_PLAYER_IMAGE, self.rect.size), True, False)]]
        self.hit_image_list = [[self.load_image(Player.HIT_PLAYER_IMAGE, self.rect.size),
                            self.load_image(Player.HIT_FLYING_PLAYER_IMAGE, self.rect.size)],
                            [self.image_flip(self.load_image(Player.HIT_PLAYER_IMAGE, self.rect.size), True, False),
                             self.image_flip(self.load_image(Player.HIT_FLYING_PLAYER_IMAGE, self.rect.size), True, False)]]
        self.lives = Player.START_LIVES
        self.hit_animation_timer = 0


    def move_player(self,button_dict):
        if button_dict["Up"]:
            self.velocity[1] -= self.up_speed
        if button_dict["Left"]:
            self.velocity[0] -= self.side_speed
            self.orientation = 1
        if button_dict["Right"]:
            self.velocity[0] += self.side_speed
            self.orientation = 0

    def update(self, platforms, enemies, collectable, ship):
        """check for collsion with platform from up or down
        set the correct image for the play """
        
        self.image_controller()
        destination = self.platform_collision(platforms)

        #check for collsion with platform from the sides
        destination = self.screen_collision(destination)
        
        #collide with collectibles
        if collectable:
            self.collectable_collision(collectable, ship)
        if enemies:
            is_dead = self.enemy_collision(enemies)
        self.rect = destination
        self.velocity = [0, self.down_speed]
        return is_dead

    def image_controller(self):
        if self.hit_animation_timer and self.hit_animation_timer % 6 == 0:
            if self.velocity[1] < 0:
                self.image_ref = 1
            else:
                self.image_ref = 0
            self.image = self.hit_image_list[self.orientation][self.image_ref]  
        elif  not self.hit_animation_timer or self.hit_animation_timer % 3 == 0:
            if self.velocity[1] < 0:
                self.image_ref = 1
            else:
                self.image_ref = 0
            self.image = self.image_list[self.orientation][self.image_ref]        
        if self.hit_animation_timer:
            self.hit_animation_timer -= 1
        
    def platform_collision(self, platforms):
        destination = self.rect.move(0, self.velocity[1])
        collide_y = destination.collidelist(platforms)
        if collide_y != -1:
            #collision from above
            if self.velocity[1] > 0:    
                destination.bottom = platforms[collide_y].top
            #collision from below
            elif self.velocity[1] < 0:
                destination.top = platforms[collide_y].bottom
        
        destination = destination.move(self.velocity[0], 0)
        collide_x = destination.collidelist(platforms)
        if collide_x != -1:
            #if we are moving right
            if self.velocity[0] > 0:
                destination.right = platforms[collide_x].left
            #if we are moving left
            elif self.velocity[0] < 0:
                destination.left = platforms[collide_x].right
        return destination
        
    def screen_collision(self, destination):
        #check if player hits bottom surface
        if destination.bottom > self.surf_height:
            destination.bottom = self.surf_height
        #check if player hits the top surface
        if destination.top < 0:
            destination.top = 0
        #checks if player hits left surface
        if destination.left < 0:
            destination.left = 0
        #checks if player hits right surface
        if destination.right > self.surf_width:
            destination.right = self.surf_width
        return destination
            
    def collectable_collision(self, collectable, ship):
        if self.rect.colliderect(collectable):
            collectable.collect()
            ship.use_collectable()
    
    def enemy_collision(self, enemies):
        for i in enemies:
            if self.rect.colliderect(i.rect):
                self.lives -= 1
                self.sound = self.set_sound("sounds/hit.ogg")
                self.sound.play()
                if self.lives == 0 : 
                    #returns True to screen as the game has been lost.
                    return True
                enemies.remove(i)
                self.hit_animation_timer = Player.ANIMATION_LENGTH
