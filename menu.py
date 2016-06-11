from blittable_object import BlittableObject
from pygame import Rect
from pygame.font import Font

BLACK = (0,0,0)

class Menu(BlittableObject):
    '''
    BUTTON_IMAGE    : str               - button image file
    BUTTON_SCALE    : (float,float)     - button image size, relative to screen size
    BUTTON_SPACING  : float             - space between menu buttons, relative to button size
    FONT_MARGIN     : float             - margin around menu fonts, relative to button size
    '''

    BUTTON_IMAGE = "images/menu_button.png"
    BUTTON_SCALE = (0.3, 0.08)
    BUTTON_SPACING = 1.3
    FONT_MARGIN = 0.8
    INITIAL_TEXT_SIZE = 100
    
    def __init__(self, main_screen, surface):
        
        '''
        Dict used for improved readability of code, especially incase we had wanted more options
        button_strings  : [str...]         - text on menu buttons
        button_options  : [function...]    - function to run on button click
        num_buttons     : int              - number of menu items
        button_rects    : [Rect...]        - menu item rectangle boundaries
        button_text     : [Surface...]     - Font surface objects for menu items
        '''

        self.button_string_options = { "game_not_running" : ["New Game", "Quit to Desktop"],
                                        "game_running" : ["Resume Game", "New Game", "Quit to Desktop"]}
        self.button_click_options = { "game_not_running" : [main_screen.new_game, main_screen.quit_program],
                                        "game_running" :[main_screen.menu_toggle, main_screen.new_game, main_screen.quit_program]}
        BlittableObject.__init__(self, surface)
        if main_screen.running:
            running = "game_running"
        else:
            running = "game_not_running"
        self.button_strings = self.button_string_options[running]
        self.button_options = self.button_click_options[running]
        self.num_buttons = len(self.button_options)
        self.button_rects = None
        self.button_text = None
        button_width = int(Menu.BUTTON_SCALE[0] * self.surf_width)
        button_height = int(Menu.BUTTON_SCALE[1] * self.surf_height)
        self.set_image(Menu.BUTTON_IMAGE, (button_width, button_height)) 
        self.rect_setup(button_width, button_height)
    
    def draw(self):
        #blit menu to screen
        for i in range(self.num_buttons):
            self.surface.blit(self.image, self.button_rects[i])
            self.surface.blit(self.button_text[i], self.button_text_pos[i])
            
    def rect_setup(self, button_width, button_height):
        ''' works out menu button positions and font sizes, iterates down
        from a large size so that it finds the largest size that fits the text
        for all the buttons nicely. Preferably the button strings should vary 
        too much in length'''
        surf_midpoint = (int(0.5 * self.surf_width), int( 0.5 * self.surf_height ))
        text_size = Menu.INITIAL_TEXT_SIZE
        font = Font(None, text_size)
        rect_list = []
        for i in range(self.num_buttons):
            button_pos = (surf_midpoint[0] - button_width/2,
                          surf_midpoint[1] + (button_height * (i - self.num_buttons/2)) * Menu.BUTTON_SPACING)
            rect = Rect(button_pos, (button_width, button_height))
            rect_list.append(rect)
            while (font.size(self.button_strings[i])[0] >= (button_width * Menu.FONT_MARGIN) or
                   font.size(self.button_strings[i])[1] >= (button_height * Menu.FONT_MARGIN)):
                text_size -= 1
                font = Font(None, text_size)
        self.button_rects = rect_list
        self.button_text = [font.render(s, 1, BLACK) for s in self.button_strings]
        self.button_text_pos = [(self.button_rects[i].center[0] - self.button_text[i].get_size()[0]/2, 
                                self.button_rects[i].center[1] - self.button_text[i].get_size()[1]/2)
                                for i in range(self.num_buttons)]
        
    def mouse_handler(self, pos):
        #menu item selection
        for i in range(len(self.button_rects)):
            if self.button_rects[i].collidepoint(pos):
                self.button_options[i]()

