import pyglet
from pyglet.gl import *
from src import tilemap

pyglet.resource.path.append('./data')
pyglet.resource.reindex()

SCALE = 4

class TestWindow(pyglet.window.Window):
    def __init__(self):
        super(TestWindow, self).__init__(64*SCALE, 48*SCALE, caption="\'blong Cong")
        testmap = tilemap.load('data/m_stage1.json')
        self.map, self.mapv = testmap
        self.mapv.setup()

    def update(self, dt):
        pass

    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        try:
            self.mapv.batch.draw()
        except:
            print 'couldn\'t draw tilemap'


w = TestWindow()
glScalef(SCALE, SCALE, SCALE)

pyglet.clock.schedule(w.update)

pyglet.app.run()