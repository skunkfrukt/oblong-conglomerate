import pyglet
from shapes import *
import knightexpert


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
        self.done = False
        self.sprites = self.font.render(self.text)


    def mupdate(self, dt):
        if self.done:
            return 'next'
        self.time += dt
        if self.final_delay is not None:
            current_delay = self.time - len(self.sprites) / float(self.speed)
            if current_delay >= self.final_delay:
                self.done = True

    def vupdate(self):
        pass

    def draw(self):
        for spr in self.sprites[:int(self.time*self.speed)]:
            spr.draw()

    def on_key_press(self, symbol, modifiers):
        self.done = True

    def on_key_release(self, symbol, modifiers):
        pass


class GameScene(Scene):
    def __init__(self, tilemap, tilemapview, hero_position):
        self.tilemap = tilemap
        self.tilemapview = tilemapview
        self.hero = knightexpert.KnightExpert()
        self.hero.hitbox.position = hero_position
        self.heroview = knightexpert.KnightExpertView(self.hero)
        self.herocontroller = knightexpert.KnightExpertController(self.hero)

    def setup(self):
        self.tilemap.setup()
        self.tilemapview.setup()

    def mupdate(self, dt):
        if self.hero.hitbox.x > 256:
            return 'next'
        self.hero.start_move(dt)
        delta = self.hero.velocity * dt
        rows = range(int(self.hero.hitbox.bottom // self.tilemap.tileheight),
                int(self.hero.hitbox.top // self.tilemap.tileheight) + 1)
        if delta.x < 0:
            cols = range(int((self.hero.hitbox.left - 1) // self.tilemap.tilewidth),
                    int((self.hero.hitbox.left + delta.x) // self.tilemap.tilewidth) - 1, -1)
        elif delta.x > 0:
            cols = range(int((self.hero.hitbox.right + 1) // self.tilemap.tilewidth),
                    int((self.hero.hitbox.right + delta.x) // self.tilemap.tilewidth) + 1)
        else:
            cols = []
        candidates_x = [(col, row) for col in cols for row in rows]
        hit_x = self.tilemap.find_obstacle(candidates_x)
        if hit_x:
            self.hero.velocity = Vect(0, self.hero.velocity.y)
            if delta.x < 0:
                delta = Vect(hit_x.right + 1 - self.hero.hitbox.left, delta.y)
            elif delta.x > 0:
                delta = Vect(hit_x.left - 1 - self.hero.hitbox.right, delta.y)
        cols = range(int((self.hero.hitbox.left + delta.x) // self.tilemap.tilewidth),
                int((self.hero.hitbox.right + delta.x) // self.tilemap.tilewidth) + 1)
        if delta.y < 0:
            rows = range(int((self.hero.hitbox.bottom - 1) // self.tilemap.tileheight),
                    int((self.hero.hitbox.bottom + delta.y) // self.tilemap.tileheight) - 1, -1)
        elif delta.y > 0:
            rows = range(int((self.hero.hitbox.top + 1) // self.tilemap.tileheight),
                    int((self.hero.hitbox.top + delta.y) // self.tilemap.tileheight) + 1)
        candidates_y = [(col, row) for row in rows for col in cols]
        hit_y = self.tilemap.find_obstacle(candidates_y)
        if hit_y:
            self.hero.velocity = Vect(self.hero.velocity.x, 0)
            if delta.y < 0:
                delta = Vect(delta.x, hit_y.top + 1 - self.hero.hitbox.bottom)
                if delta.x == 0:
                    self.hero.state = 'idle'
                else:
                    self.hero.state = 'walking'
            elif delta.y > 0:
                delta = Vect(delta.x, hit_y.bottom - 1 - self.hero.hitbox.top)
        self.hero.hitbox += delta

    def vupdate(self):
        player_position = self.hero.hitbox.x
        screen_offset = int(-max(min(player_position - 32, 256 - 64), 0))
        self.tilemapview.update_sprite_position(Vect(x=screen_offset))
        self.heroview.update_sprite_position(Vect(screen_offset,0))

    def draw(self):
        self.tilemapview.batch.draw()
        self.heroview.drawable.draw()

    def on_key_press(self, symbol, modifiers):
        self.herocontroller.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.herocontroller.on_key_release(symbol, modifiers)
