import pyglet
from pyglet.gl import *
from pyglet.window import key
from src import knightexpert, shapes

SCALE = 8

class W(pyglet.window.Window):
    def __init__(self):
        super(W, self).__init__(64*SCALE,48*SCALE,caption='KnightExpert')
        self.ke = knightexpert.KnightExpert()
        self.kev = knightexpert.KnightExpertView(self.ke)
        self.kec = knightexpert.KnightExpertController(self.ke)

    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.kev.update_sprite_position(shapes.Vect(0,0))
        self.kev.drawable.draw()

def update(dt):
    pass

def update_model(dt):
    w.ke.start_move(dt)
    w.ke.finish_move()

w = W()
glScalef(SCALE, SCALE, SCALE)

w.push_handlers(w.kec.keys)

@w.event
def on_key_press(symbol, modifiers):
    w.kec.on_key_press(symbol, modifiers)

@w.event
def on_key_release(symbol, modifiers):
    w.kec.on_key_release(symbol, modifiers)

pyglet.clock.schedule(update)
pyglet.clock.schedule_interval(update_model, 0.02)
pyglet.app.run()