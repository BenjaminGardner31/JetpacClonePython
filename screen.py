from menu import Menu
from player import Player
from platforms import Platforms
from ship import Ship
from collectables import Collectables
from blittable_object import BlittableObject
from enemies import Enemy
from pygame.font import Font
from pygame.mixer import music
import random

#Storing the RGB value of white, to be used for text
WHITE = (255,255,255)

"""
The Screen class is the main controller of what is updated
and shown on the screen. It inherits from BlittableObject as some of
the image methods are useful.
"""
class Screen(BlittableObject) :

    #list of backgrounds for different levels
    BACKGROUND = ("images/background_1.png", "images/background_2.png", "images/background_3.png",
                    "images/background_4.png", "images/background_5.png")
    DEATH_SCENE = "images/death_scene.png"
    NUM_ENEMIES_PER_LEVEL = 2
    GAME_MUSIC = 'sounds/bubliki.ogg'
    PLATFORM_LOCATIONS = (  ((0.1, 0.5), (0.7, 0.5), (0.4, 0.25)),
                            ((0.1, 0.3), (0.4, 0.55), (0.7, 0.3)),
                            ((0.1, 0.25), (0.4, 0.45), (0.7, 0.65)),
                            ((0.1, 0.5), (0.4, 0.25), (0.7, 0.5)),
                            ((0.1, 0.65), (0.4, 0.45), (0.7, 0.25)) )
    
    def __init__(self, canvas, quit_program):
        BlittableObject.__init__(self, canvas)
        self.reset()
        #stores the method to completely quit the game, so Menu can call it when needed
        self.quit_program = quit_program
        self.menu_toggle()
        #set up a store for the state of important keys, this is managed by the update handler in main.py
        self.key_register={"Left":False,"Up":False,"Right":False,"Shoot":False}
    
    """"This code would allow us to set the game in multiple ways dependings on the variables passed
    default resets the game to basically empty and to level 1."""
    def reset(self, running = False, player = None, ship = None, platforms = None, 
                    platform_rects = None, enemies = None, collectables = None,
                    game_level = 1):
        """This allows the backgrounds to loop no matter how many levels are completed
        (5 should be enough though)."""
        image_ref = (game_level-1) % 5
        self.set_image(Screen.BACKGROUND[image_ref], self.surface.get_size())  
        self.running = running
        self.menu = False
        self.player = player
        self.ship = ship
        self.platforms = platforms
        self.platform_rects = platform_rects
        self.enemies = enemies
        self.collectables = collectables
        self.game_over = False
        self.game_won = False
        self.game_level = game_level
        self.font = Font(None, self.surf_height/20)
    
    #This method controls what happens when a new game or level is started
    def new_game(self, game_level = 1):
        running = True
        platforms = []
        for i in Screen.PLATFORM_LOCATIONS[(game_level-1) % 5]:
            platforms.append(Platforms(self.surface, *i))
        platform_rects = [i.rect for i in platforms]
        player = Player(self.surface)
        collectables = Collectables(self.surface)
        ship = Ship(self.surface)
        enemies = []
        self.reset(running, player, ship, platforms, platform_rects, enemies, collectables, game_level)
        if game_level == 1 :
            music.load(Screen.GAME_MUSIC)
            music.play(-1)
    
    #This controls what happens when the game is lost
    def lost(self):
        music.stop()
        self.running = False
        self.image = self.load_image(Screen.DEATH_SCENE, self.rect.size)
    
    #This controls what happens when the game is won.
    def win(self):
        game_level = self.game_level + 1
        self.new_game(game_level)
	
    """Draw checks if parts of the game should be drawn or not and calls
    their draw methods, also draws background and info text."""
    def draw(self):
        self.surface.blit(self.image, (0,0))
        if self.running:
            if self.platforms:
                for i in self.platforms:
                    i.draw()
            if self.ship:
                self.ship.draw()
            if not self.ship.all_collected():
                if self.enemies:
                    for i in self.enemies:
                        i.draw()
                if self.collectables:
                    self.collectables.draw()
                if self.player :
                    self.player.draw()
            lives_string = "Lives Remaining: {}".format(self.player.lives)
            level_string = "Level: {}".format(self.game_level)
            lives_text = self.font.render(lives_string, 1, WHITE)
            level_text = self.font.render(level_string, 1, WHITE)
            lives_text_size = self.font.size(lives_string)
            lives_text_pos = (self.surf_width - int(lives_text_size[0] * 1.2),
                              int(lives_text_size[1] * 1.2))
            level_text_size = self.font.size(level_string)
            level_text_pos = (int(level_text_size[0] * 0.2), int(level_text_size[1] * 1.2))
            self.surface.blit(lives_text, lives_text_pos)
            self.surface.blit(level_text, level_text_pos)
        if self.menu:
            self.menu.draw()   
    
    #checks what needs to be updated and calls their update functions
    def update(self):
        if self.game_over:
            self.lost()
        if self.game_won:
            self.win()
        if self.running and not self.menu:
            if not self.ship.all_collected():
                #ensures there are always enough enemies on screen
                if self.enemies != None: 
                    exp_num_enemies = self.game_level * Screen.NUM_ENEMIES_PER_LEVEL
                    while len(self.enemies) < exp_num_enemies:
                        self.enemies.append(Enemy(self.surface, self.game_level))
                    for i in self.enemies:
                        i.update(self.platform_rects)
                if self.collectables:
                    self.collectables.update(self.platform_rects)
                if self.player:
                    self.player.move_player(self.key_register)
                    self.game_over = self.player.update(self.platform_rects, self.enemies, 
                                                        self.collectables, self.ship)
                    if self.game_over:
                        self.sound = self.set_sound("sounds/gameover.ogg")
                        self.sound.play()
            if self.ship:
                self.game_won = self.ship.update()    
        else:
            pass
    
    def menu_toggle(self):
        if not self.menu:
            self.menu = Menu(self, self.surface)
        else:
            self.menu = False
    
    def mouse_handler(self, pos):
        if self.menu:
            self.menu.mouse_handler(pos)
        elif self.game_over:
           self.reset()
           self.menu_toggle()

