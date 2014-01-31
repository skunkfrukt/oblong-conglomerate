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
    def __init__(self, tilemap, tilemapview, hero_position, override_properties={}, nextdir=None):
        self.nextdir = nextdir
        self.tilemap = tilemap
        self.tilemap.properties.update(override_properties)
        print self.tilemap.properties['offscreen_obstacles']
        self.tilemapview = tilemapview
        self.hero = knightexpert.KnightExpert()
        self.initial_hero_position = hero_position
        self.hero.hitbox.position = hero_position
        self.heroview = knightexpert.KnightExpertView(self.hero)
        self.herocontroller = knightexpert.KnightExpertController(self.hero)
        self.npcs = []
        self.npcviews = []

    def setup(self):
        self.tilemap.setup()
        self.tilemapview.setup()
        for npc in self.npcs:
            npc.setup()
        for npcv in self.npcviews:
            npcv.setup()

    def respawn(self):
        self.hero.hitbox.position = self.initial_hero_position

    def mupdate(self, dt):
        if any([self.hero.hitbox.left >= self.tilemap.pxwidth and self.nextdir == 'r',
                self.hero.hitbox.right < 0 and self.nextdir == 'l',
                self.hero.hitbox.bottom >= self.tilemap.pxheight and self.nextdir == 't',
                self.hero.hitbox.top < 0 and self.nextdir == 'b']):
            return 'next'
        elif self.hero.hitbox.top < 0:
            print 'THOU DIEST'
            self.respawn()
        elif self.hero.talking:
            for npc in self.npcs:
                if npc.hitbox & self.hero.hitbox and npc.can_talk:
                    return 'next'
        self.hero.start_move(dt)
        delta = self.hero.velocity * dt
        herobox = self.hero.hitbox
        tmap = self.tilemap
        ladder_rows = range(tmap.row_at_px(herobox.bottom),
                tmap.row_at_px(herobox.top)+1)
        ladder_cols = range(tmap.col_at_px(herobox.left),
                tmap.col_at_px(herobox.right)+1)
        ladder_candidates = [(col, row) for col in ladder_cols for row in ladder_rows]
        self.hero.can_climb = any([tmap.ladder_at(*cell) for cell in ladder_candidates])
        if not self.hero.can_climb:
            self.hero.unclimb()
        rows = range(tmap.row_at_px(herobox.bottom),
                tmap.row_at_px(herobox.top) + 1)
        if delta.x < 0:
            cols = range(tmap.col_at_px(herobox.left - 1),
                    tmap.col_at_px(herobox.left + delta.x) - 1, -1)
        elif delta.x > 0:
            cols = range(tmap.col_at_px(herobox.right + 1),
                    tmap.col_at_px(herobox.right + delta.x) + 1)
        else:
            cols = []
        candidates_x = [(col, row) for col in cols for row in rows]
        hit_x = self.tilemap.find_obstacle(candidates_x)
        if hit_x:
            self.hero.velocity = Vect(0, self.hero.velocity.y)
            if delta.x < 0:
                delta = Vect(hit_x.right + 1 - herobox.left, delta.y)
            elif delta.x > 0:
                delta = Vect(hit_x.left - 1 - herobox.right, delta.y)
        cols = range(tmap.col_at_px(herobox.left + delta.x),
                tmap.col_at_px(herobox.right + delta.x) + 1)
        if delta.y < 0:
            rows = range(tmap.row_at_px(herobox.bottom - 1),
                    tmap.row_at_px(herobox.bottom + delta.y) - 1, -1)
        elif delta.y > 0:
            rows = range(tmap.row_at_px(herobox.top + 1),
                    tmap.row_at_px(herobox.top + delta.y) + 1)
        candidates_y = [(col, row) for row in rows for col in cols]
        hit_y = self.tilemap.find_obstacle(candidates_y)
        if hit_y:
            '''if not (self.hero.climbing and tmap.ladder_at(
                    tmap.col_at_px(hit_y.left), tmap.row_at_px(hit_y.bottom))):'''
            self.hero.velocity = Vect(self.hero.velocity.x, 0)
            if delta.y < 0:
                delta = Vect(delta.x, hit_y.top + 1 - herobox.bottom)
                if delta.x == 0:
                    self.hero.state = 'idle'
                else:
                    self.hero.state = 'walking'
            elif delta.y > 0:
                delta = Vect(delta.x, hit_y.bottom - 1 - herobox.top)
        self.hero.hitbox += delta

    def vupdate(self):
        player_position = self.hero.hitbox.x
        screen_offset = int(-max(min(player_position - 32, self.tilemap.pxwidth - 64), 0))
        self.tilemapview.update_sprite_position(Vect(x=screen_offset))
        for npcv in self.npcviews:
            npcv.update_sprite(Vect(x=screen_offset))
        self.heroview.update_sprite_position(Vect(screen_offset,0))

    def draw(self):
        self.tilemapview.batch.draw()
        for npcv in self.npcviews:
            npcv.drawable.draw()
        self.heroview.drawable.draw()

    def on_key_press(self, symbol, modifiers):
        self.herocontroller.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.herocontroller.on_key_release(symbol, modifiers)
