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
        self.ke.hitbox += Vect(4, 4)
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
        stage_width = 256
        screen_width = 64
        player_position = self.ke.hitbox.x
        screen_offset = int(-max(min(player_position - 32, stage_width - screen_width), 0))
        self.mapv.update_sprite_position(Vect(x=screen_offset))
        try:
            self.mapv.batch.draw()
        except:
            print 'couldn\'t draw tilemap'
        self.kev.update_sprite_position(Vect(screen_offset,0))
        self.kev.drawable.draw()


w = TestWindow()
glScalef(SCALE, SCALE, SCALE)

def mupdate(dt):
    w.ke.start_move(dt)
    delta = w.ke.velocity * dt
    rows = range(int(w.ke.hitbox.bottom // w.map.tileheight),
            int(w.ke.hitbox.top // w.map.tileheight) + 1)
    if delta.x < 0:
        cols = range(int((w.ke.hitbox.left - 1) // w.map.tilewidth),
                int((w.ke.hitbox.left + delta.x) // w.map.tilewidth) - 1, -1)
    elif delta.x > 0:
        cols = range(int((w.ke.hitbox.right + 1) // w.map.tilewidth),
                int((w.ke.hitbox.right + delta.x) // w.map.tilewidth) + 1)
    else:
        cols = []
    candidates_x = [(col, row) for col in cols for row in rows]
    hit_x = w.map.find_obstacle(candidates_x)
    if hit_x:
        w.ke.velocity = Vect(0, w.ke.velocity.y)
        if delta.x < 0:
            delta = Vect(hit_x.right + 1 - w.ke.hitbox.left, delta.y)
        elif delta.x > 0:
            delta = Vect(hit_x.left - 1 - w.ke.hitbox.right, delta.y)
    cols = range(int((w.ke.hitbox.left + delta.x) // w.map.tilewidth),
            int((w.ke.hitbox.right + delta.x) // w.map.tilewidth) + 1)
    if delta.y < 0:
        rows = range(int((w.ke.hitbox.bottom - 1) // w.map.tileheight),
                int((w.ke.hitbox.bottom + delta.y) // w.map.tileheight) - 1, -1)
    elif delta.y > 0:
        rows = range(int((w.ke.hitbox.top + 1) // w.map.tileheight),
                int((w.ke.hitbox.top + delta.y) // w.map.tileheight) + 1)
    candidates_y = [(col, row) for row in rows for col in cols]
    hit_y = w.map.find_obstacle(candidates_y)
    if hit_y:
        w.ke.velocity = Vect(w.ke.velocity.x, 0)
        if delta.y < 0:
            delta = Vect(delta.x, hit_y.top + 1 - w.ke.hitbox.bottom)
            if delta.x == 0:
                w.ke.state = 'idle'
            else:
                w.ke.state = 'walking'
        elif delta.y > 0:
            delta = Vect(delta.x, hit_y.bottom - 1 - w.ke.hitbox.top)
    w.ke.hitbox += delta


w.push_handlers(w.kec.keys)

@w.event
def on_key_press(symbol, modifiers):
    w.kec.on_key_press(symbol, modifiers)

@w.event
def on_key_release(symbol, modifiers):
    w.kec.on_key_release(symbol, modifiers)

pyglet.clock.schedule_interval(mupdate, 0.02)
pyglet.app.run()