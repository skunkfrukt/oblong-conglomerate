import pyglet


class Scene(object):
    def __init__(self):
        pass

    def update(self, dt):
        pass


class TextScene(Scene):
    def __init__(self, text, font, next):
        self.text = text
        self.next = next
        self.time = 0

    def update(self, dt):
        self.time += dt
        self.update_text()

    def update_text(self):
        pass


class GameScene(Scene):
    def __init__(self, tilemap, ):
        pass
