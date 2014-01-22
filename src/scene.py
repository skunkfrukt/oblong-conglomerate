import pyglet


class Scene(object):
    def __init__(self):
        pass

    def update(self, dt):
        pass


class TextScene(Scene):
    def __init__(self, next, text, font, speed=10, final_delay=None):
        self.text = text
        self.next = next
        self.speed = speed
        self.font = font
        self.final_delay = final_delay
        self.time = 0
        self.sprites = []

    def setup(self):
        self.time = 0
        self.sprites = self.font.render(self.text)


    def update(self, dt):
        self.time += dt
        if self.final_delay is not None:
            current_delay = self.time - len(self.sprites) / float(self.speed)
            if current_delay >= self.final_delay:
                return 'DONE'

    def draw(self):
        for spr in self.sprites[:int(self.time*self.speed)]:
            spr.draw()


class GameScene(Scene):
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.backgrounds = []
        self.sprites = []

    def setup(self):
        for tset in self.tilemap.tilesets:
            pass

    def update(self, dt):
        pass

    def draw(self):
        for bg in self.backgrounds:
            bg.draw()
        for spr in self.sprites:
            spr.draw()
