import pyglet
from pyglet.window import key
from shapes import *


class KnightExpert(object):
    """ Model class for the player character. """

    def __init__(self):
        self.hitbox = Rect(0, 0, 4, 7)
        self.nextbox = self.hitbox
        self.velocity = Vect(0,0)
        self.acceleration = Vect(0,0)
        self.runspeed = 10
        self.moving = False
        self.moved = False
        self.grounded = True
        self.jumping = False
        self.walking = None
        self.stopping = True
        self.direction = 'L'
        self.state = 'idle'

    def start_move(self, dt):
        # self.oldbox = self.hitbox
        if True:  # self.state not in ('walking', 'idle'):
            self.velocity += Vect(0, -120) * dt
        # self.hitbox += self.velocity * dt

    def walk(self, direction):
        if self.state not in ('hurt', 'dead'):
            self.update_lateral_velocity(direction)
        if self.state == 'idle':
            self.state = 'walking'

    def unwalk(self):
        self.walk(None)

    def jump(self):
        if self.state in ('idle', 'walking'):
            self.velocity += Vect(0, 40)
            self.state = 'jumping'
        elif self.state == 'climbing':
            self.state = 'falling'

    def update_lateral_velocity(self, direction):
        if direction == None:
            self.velocity = Vect(0, self.velocity.y)
        elif direction == 'R':
            self.velocity = Vect(self.runspeed, self.velocity.y)
        elif direction == 'L':
            self.velocity = Vect(-self.runspeed, self.velocity.y)

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
        self.sprite.position = self.model.position + self.sprite_offset + screen_offset

    @property
    def drawable(self):
        return self.sprite


class KnightExpertController(object):
    def __init__(self, model):
        self.model = model
        self.current_dominant_lateral_direction = None
        self.keys = key.KeyStateHandler()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.current_dominant_lateral_direction = 'L'
            self.model.walk('L')
        elif symbol == key.RIGHT:
            self.current_dominant_lateral_direction = 'R'
            self.model.walk('R')
        elif symbol == key.SPACE:
            self.model.jump()

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            if self.keys[key.RIGHT]:
                self.current_dominant_lateral_direction = 'R'
                self.model.walk('R')
            else:
                self.model.unwalk()
        elif symbol == key.RIGHT:
            if self.keys[key.LEFT]:
                self.current_dominant_lateral_direction = 'L'
                self.model.walk('L')
            else:
                self.model.unwalk()

