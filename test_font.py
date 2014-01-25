import pyglet
from pyglet.gl import *
from src import text, scene

SCALE = 8

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

    '(': 16*3+0,
    ')': 16*3+1,
    '[': 16*3+2,
    ']': 16*3+3,
    '{': 16*3+4,
    '}': 16*3+5,
    '_': 16*3+6,
    '\\': 16*3+7,
    '|': 16*3+8,
    '&': 16*3+9,
    '+': 16*3+10,
    '-': 16*3+11,
    '*': 16*3+12,
    '/': 16*3+13,
    '"': 16*3+14,
    '\'': 16*3+15,

    '=': 16*2+0,
    '<': 16*2+1,
    '>': 16*2+2,

    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9
}

class TestWindow(pyglet.window.Window):
    def __init__(self):
        super(TestWindow, self).__init__(64*SCALE,48*SCALE)
        self.f = text.Font('data/font.png', 16, 6, f_bindings)
        self.time = 0
        text1 = [
            "the kingdom is",
            "in shambles.",
            "never were the",
            "cries for a",
            "hero so great."
        ]
        text2 = [
            "you have read",
            "like two dozen",
            "stories about",
            "gallant knights",
            "and champions."
        ]
        text3 = [
            "it falls on you",
            "to deliver this",
            "land from evil",
            "and inevitable",
            "   distraction."
        ]
        title_text = [
            "+------o------+",
            "THE QUEST FOR |",
            "THE      OBLONG",
            "|  CONGLOMERATE",
            "+------x------+"
        ]

        scene1 = scene.TextScene(None, text1, self.f, final_delay=2)
        scene2 = scene.TextScene(None, text2, self.f, final_delay=2)
        scene3 = scene.TextScene(None, text3, self.f, final_delay=2)
        scene4 = scene.TextScene(None, title_text, self.f)

        scene1.next = scene2
        scene2.next = scene3
        scene3.next = scene4
        scene4.next = None  #TODO First gameplay scene

        self.scene = scene1
        self.scene.setup()

    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.scene.draw()

    def update(self, dt):
        self.time += dt
        if self.scene.update(dt) == 'DONE':
            self.scene.next.setup()
            self.scene = self.scene.next

w = TestWindow()
glScalef(SCALE, SCALE, SCALE)
pyglet.clock.schedule(w.update)

pyglet.app.run()
