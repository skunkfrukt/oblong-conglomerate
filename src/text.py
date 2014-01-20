import pyglet


class Font(object):
    def __init__(self, image_fn, cols, rows, bindings):
        image = pyglet.resource.image(image_fn)
        self.grid = pyglet.image.ImageGrid(image, rows, cols)
        self.bindings = {}
        for k, v in bindings.items():
            self.bindings[k] = self.grid[v]

    def __getitem__(self, index):
        return self.bindings[index]

    def sprite(self, character):
        return pyglet.sprite.Sprite(self[character])

    def render(self, lines):
        sprites = []
        for ln, l in enumerate(lines):
            for cn, c in enumerate(l):
                if c in self.bindings:
                    img = self[c]
                    x = cn * 4 + 2
                    y = 40 - (ln + 1) * 8 + 4
                    spr = pyglet.sprite.Sprite(img, x, y)
                    sprites.append(spr)
        return sprites