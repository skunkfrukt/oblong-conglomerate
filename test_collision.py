import pyglet
from pyglet.gl import *
from src import tilemap
from pyglet.window import key
from src import knightexpert, collider
from src.shapes import *

pyglet.resource.path.append('./data')
pyglet.resource.reindex()

SCALE = 4

class TestWindow(pyglet.window.Window):
    def __init__(self):
        super(TestWindow, self).__init__(64*SCALE, 48*SCALE, caption="\'blong Cong")
        testmap = tilemap.load('data/m_stage1.json')
        self.map, self.mapv = testmap
        self.map.setup()
        self.mapv.setup()
        self.ke = knightexpert.KnightExpert()
        self.ke.hitbox += Vect(5, 15)
        self.kev = knightexpert.KnightExpertView(self.ke)
        self.kec = knightexpert.KnightExpertController(self.ke)
        self.things = []
        self.things.extend(self.map.tiles)
        self.things.append(self.ke)

    def update(self, dt):
        pass

    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        placeholder = self.mapv.tileset[24]
        try:
            self.mapv.batch.draw()
        except:
            print 'couldn\'t draw tilemap'
        for t in self.map.tiles:
            placeholder.blit(t.hitbox.x, t.hitbox.y)
        try:
            placeholder.blit(w.ke.oldbox.x, w.ke.oldbox.y)
        except:
            pass
        self.kev.update_sprite_position(Vect(0,0))
        self.kev.drawable.draw()


w = TestWindow()
glScalef(SCALE, SCALE, SCALE)

def update_model(dt):
    w.ke.move(dt)
    collisions = collider.collide(w.things)
    for collision in collisions:
        if w.ke in collision:
            for a in collision:
                if a is not w.ke:
                    other = a
            if w.ke.velocity.x > 0:  # and w.ke.oldbox.right <= other.hitbox.x:
                w.ke.hitbox += Vect(other.hitbox.x - w.ke.hitbox.right - 1, 0)
                w.ke.velocity = Vect(0, w.ke.velocity.y)
            elif w.ke.velocity.x < 0: # and w.ke.oldbox.x >= other.hitbox.right:
                w.ke.hitbox += Vect(other.hitbox.right - w.ke.hitbox.x + 1, 0)
                w.ke.velocity = Vect(0, w.ke.velocity.y)
            if w.ke.velocity.y < 0: #and w.ke.oldbox.y >= other.hitbox.top:
                w.ke.hitbox += Vect(0, other.hitbox.top - w.ke.hitbox.y +1)
                w.ke.velocity = Vect(w.ke.velocity.x, 0)
                w.ke.state = 'idle'


w.push_handlers(w.kec.keys)

@w.event
def on_key_press(symbol, modifiers):
    w.kec.on_key_press(symbol, modifiers)

@w.event
def on_key_release(symbol, modifiers):
    w.kec.on_key_release(symbol, modifiers)

pyglet.clock.schedule_interval(update_model, 0.02)
pyglet.app.run()