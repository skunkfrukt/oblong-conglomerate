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
        self.runspeed = 20
        self.moving = False
        self.moved = False
        self.grounded = True
        self.jumping = False
        self.walking = None
        self.stopping = True
        self.climbing = False
        self.can_climb = False
        self.talking = False
        self.direction = 'L'
        self.state = 'falling'

    def start_move(self, dt):
        if not self.climbing:
            self.velocity += Vect(0, -120) * dt
        else:
            self.velocity = Vect(0, 30)

    def walk(self, direction):
        if self.state not in ('hurt', 'dead'):
            self.update_lateral_velocity(direction)
        if self.state == 'idle':
            self.state = 'walking'

    def unwalk(self):
        self.walk(None)

    def climb(self):
        if self.can_climb:
            self.climbing = True
            self.state = 'climbing'

    def unclimb(self):
        self.climbing = False
        self.state = 'falling'

    def jump(self):
        if self.state in ('idle', 'walking'):
            self.velocity += Vect(0, 50)
            self.state = 'jumping'
        elif self.state == 'climbing':
            self.unclimb()

    def update_lateral_velocity(self, direction):
        if direction == None:
            self.velocity = Vect(0, self.velocity.y)
        elif direction == 'R':
            self.velocity = Vect(self.runspeed, self.velocity.y)
        elif direction == 'L':
            self.velocity = Vect(-self.runspeed, self.velocity.y)
        if self.climbing:
            self.velocity += Vect(y=30)

    def talk(self):
        self.talking = True

    def untalk(self):
        self.talking = False

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
            'idle': grid[12]
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
        elif symbol == key.UP:
            self.model.talk()
            self.model.climb()

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
        elif symbol == key.UP:
            self.model.untalk()
            self.model.unclimb()

