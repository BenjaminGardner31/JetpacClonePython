from blittable_object import BlittableObject

class Platforms(BlittableObject):
    #Platforms only initialise and draw
    IMAGE = "images/platform_template.png"
    PLATFORM_SIZE = (0.2, 0.04)
    
    def __init__(self, canvas, x, y):
        BlittableObject.__init__(self, canvas)
        size = (int(Platforms.PLATFORM_SIZE[0] * self.surf_width),
                int(Platforms.PLATFORM_SIZE[1]*self.surf_height))
        self.set_image(Platforms.IMAGE, size)
        self.rect.topleft = (x * self.surf_width, y * self.surf_height)
        

