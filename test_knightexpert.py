import pyglet
from pyglet.gl import *
from src import knightexpert, shapes

SCALE = 8

class W(pyglet.window.Window):
    def __init__(self):
        super(W, self).__init__(64*SCALE,48*SCALE,caption='KnightExpert')
        self.ke = knightexpert.KnightExpert()
        self.kev = knightexpert.KnightExpertView(self.ke)

    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.kev.update_sprite_position(shapes.Vect(0,0))
        self.kev.drawable.draw()

def update(dt):
    pass

def update_model(dt):
    w.ke.start_move(shapes.Vect(1,0))
    w.ke.finish_move()

w = W()
glScalef(SCALE, SCALE, SCALE)

pyglet.clock.schedule(update)
pyglet.clock.schedule_interval(update_model, 0.02)
pyglet.app.run()