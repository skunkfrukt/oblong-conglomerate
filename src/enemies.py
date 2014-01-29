import pyglet

class VerdantGunk(object):
    def __init__(self, x=0, y=0, patrolrange=None, waittime=0, startdirection=None):
        self.hitbox = Rect(x, y, 4, 2)
        self.oozespeed = 5
        self.patrolrange = patrolrange
        self.maxwaittime = waittime
        self.currentwaittime = 0
        self.direction = startdirection
        if self.direction is None:
            self.velocity = Vect()
        else:
            self.velocity = self.direction * self.oozespeed

    def update(self, dt):
        if self.velocity.x == 0:
            self.currentwaittime += dt
            if self.currentwaittime >= self.maxwaittime:
                self.currentwaittime = 0
                self.directon *= -1
                self.velocity = self.directon * self.oozespeed
        else:
            newbox = self.hitbox + self.velocity * dt
            if self.velocity.x < 0 and int(newbox.left) not in self.patrolrange:
                self.velocity = Vect()
                newbox.left = self.patrolrange[0]
            elif self.velocity.x > 0 and int(newbox.right - 1) not in self.patrolrange:
                self.velocity = Vect()
                newbox.right = self.patrolrange[-1]
            self.hitbox = newbox


class VerdantGunkView(object):
    def __init__(self, model):
        self.model = model
        self.sprite_offset = Vect()
        self.image = pyglet.resource.image('data/s_verdantgunk.png')

    def setup(self):
        self.sprite = pyglet.sprite.Sprite(self.image, self.model.x, self.model.y)

    def update_sprite(self, screen_offset):
        self.sprite.position = self.model.hitbox.position + self.sprite_offset + screen_offset