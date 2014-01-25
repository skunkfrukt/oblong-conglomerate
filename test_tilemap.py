import pyglet
from pyglet.gl import *
from src import tilemap

pyglet.resource.path.append('./data')
pyglet.resource.reindex()

SCALE = 8

class TestWindow(pyglet.window.Window):
    def __init__(self):
        super(TestWindow, self).__init__(64*SCALE, 48*SCALE, caption="\'blong Cong")
        self.map = testmap = tilemap.load('data/m_stage1.json')
        self.sprites = []
        l = self.map.layers[0]
        for n, tileid in enumerate(l.data):
            if tileid > 0:
                img = self.map.tilesets[0][tileid-1]
                x = 4 * (n % l.width)
                y = 44 - 4 * (n // l.width)
                spr = pyglet.sprite.Sprite(img, x, y)
                self.sprites.append(spr)

    def update(self, dt):
        pass

    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        for spr in self.sprites:
            spr.draw()
        '''for i, c in enumerate(self.map.tilesets[0]):
            c.blit((i%8)*4,44-(i//8)*4)'''


w = TestWindow()
glScalef(SCALE, SCALE, SCALE)

#pyglet.clock.schedule(w.update)

pyglet.app.run()