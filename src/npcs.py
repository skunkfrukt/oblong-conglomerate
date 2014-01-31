import pyglet
from shapes import *

class WiseOldKing(object):
    def __init__(self, x=0, y=0, patrolrange=None, waittime=0, startdirection=None):
        self.hitbox = Rect(x, y, 4, 6)
        self.direction = startdirection
        self.velocity = Vect()
        self.can_talk = True

    def setup(self):
        pass

    def update(self, dt):
        pass

    @property
    def x(self):
        return self.hitbox.left

    @property
    def y(self):
        return self.hitbox.bottom


class WiseOldKingView(object):
    def __init__(self, model):
        self.model = model
        self.sprite_offset = Vect(x=-2)
        self.image = pyglet.image.ImageGrid(pyglet.resource.image('data/s_wiseoldking.png'), 2, 2)[2]

    def setup(self):
        self.sprite = pyglet.sprite.Sprite(self.image, self.model.x, self.model.y)

    def update_sprite(self, screen_offset):
        self.sprite.position = self.model.hitbox.position + self.sprite_offset + screen_offset

    @property
    def drawable(self):
        return self.sprite


class ActualOblongConglomerate(object):
    def __init__(self, x=0, y=0, patrolrange=None, waittime=0, startdirection=None):
        self.hitbox = Rect(x, y, 16, 8)
        self.direction = startdirection
        self.velocity = Vect()
        self.can_talk = True

    def setup(self):
        pass

    def update(self, dt):
        pass

    @property
    def x(self):
        return self.hitbox.left

    @property
    def y(self):
        return self.hitbox.bottom


class ActualOblongConglomerateView(object):
    def __init__(self, model):
        self.model = model
        self.sprite_offset = Vect()
        self.image = pyglet.image.ImageGrid(pyglet.resource.image('data/s_actualoblongconglomerate.png'), 2, 1)[0]

    def setup(self):
        self.sprite = pyglet.sprite.Sprite(self.image, self.model.x, self.model.y)

    def update_sprite(self, screen_offset):
        self.sprite.position = self.model.hitbox.position + self.sprite_offset + screen_offset

    @property
    def drawable(self):
        return self.sprite