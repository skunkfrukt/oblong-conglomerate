import pyglet
from shapes import *


class KnightExpert(object):
    """ Model class for the player character. """

    def __init__(self):
        self.hitbox = Rect(0, 0, 4, 7)
        self.nextbox = self.hitbox
        self.velocity = Vect(0,0)
        self.moving = False
        self.moved = False
        self.grounded = True
        self.jumping = False

    def start_move(self, delta):
        self.nextbox += delta
        self.moving = True

    def finish_move(self):
        self.hitbox = self.nextbox
        moving = False
        moved = True

    @property
    def position(self):
        return self.hitbox.position


class KnightExpertView(object):
    """ View class for the player character. """

    def __init__(self, model):
        self.model = model

        spritesheet = pyglet.resource.image('data/s_knightexpert.png')
        grid = pyglet.image.ImageGrid(spritesheet, 4, 4)
        self.animations = {
            'idle': grid[0]
        }
        self.current_animation = None
        self.sprite = pyglet.sprite.Sprite(self.animations['idle'])
        self.sprite_offset = Vect(-2, 0)

    def choose_animation(self):
        next_animation = 'idle'
        if self.current_animation != next_animation:
            self.sprite.image = self.animations[next_animation]
            self.current_animation = next_animation

    def update_sprite_position(self, screen_offset):
        self.sprite.position = self.model.position + screen_offset

    @property
    def drawable(self):
        return self.sprite


class KnightExpertController(object):
    def __init__(self, model):
        self.model = model