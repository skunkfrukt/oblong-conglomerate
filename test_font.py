import pyglet
from src import text

f_bindings = {
    'a': 16*5+0,
    'b': 16*5+1,
    'c': 16*5+2,
    'd': 16*5+3,
    'e': 16*5+4,
    'f': 16*5+5,
    'g': 16*5+6,
    'h': 16*5+7,
    'i': 16*5+8,
    'j': 16*5+9,
    'k': 16*5+10,
    'l': 16*5+11,
    'm': 16*5+12,
    'n': 16*5+13,
    'o': 16*5+14,
    'p': 16*5+15,
    'q': 16*4+0,
    'r': 16*4+1,
    's': 16*4+2,
    't': 16*4+3,
    'u': 16*4+4,
    'v': 16*4+5,
    'w': 16*4+6,
    'x': 16*4+7,
    'y': 16*4+8,
    'z': 16*4+9,
    '.': 16*4+10,
    ',': 16*4+11,
    ':': 16*4+12,
    ';': 16*4+13,
    '!': 16*4+14,
    '?': 16*4+15,
    '0': 16*3+0,
    '1': 16*3+1,
    '2': 16*3+2,
    '3': 16*3+3,
    '4': 16*3+4,
    '5': 16*3+5,
    '6': 16*3+6,
    '7': 16*3+7,
    '8': 16*3+8,
    '9': 16*3+9,
    '+': 16*3+10,
    '-': 16*3+11,
    '*': 16*3+12,
    '/': 16*3+13,
    '"': 16*3+14,
    '\'': 16*3+15,
    '(': 16*2+0,
    ')': 16*2+1,
    '[': 16*2+2,
    ']': 16*2+3,
    '{': 16*2+4,
    '}': 16*2+5,
    '_': 16*2+6,
    '\\': 16*2+7,
    '|': 16*2+8,
    '&': 16*2+9,
    ' ': 16*2+10,
    ' ': 16*2+11,
    ' ': 16*2+12,
    ' ': 16*2+13,
    ' ': 16*2+14,
    ' ': 16*2+15,
}

class TestWindow(pyglet.window.Window):
    def __init__(self):
        super(TestWindow, self).__init__(64,48)
        self.f = text.Font('data/font.png', 16, 6, f_bindings)
        self.time = 0
        self.text = [
            "to be or not",
            "to be that is",
            "the question",
            " +-/ *",
            "sort of"
        ]
        self.sprites = self.f.render(self.text)

    def on_draw(self):
        self.clear()
        i = int(self.time*5)
        for s in self.sprites[:i]:
            s.draw()

    def update(self, dt):
        self.time += dt

w = TestWindow()
pyglet.clock.schedule(w.update)

pyglet.app.run()
