import pyglet
from pyglet.gl import *
from src import tilemap, scene, text
from pyglet.window import key
from src import knightexpert, collider
from src.shapes import *
import json

pyglet.resource.path.append('./data')
pyglet.resource.reindex()

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

font = text.Font('data/font.png', 16, 6, f_bindings)
texts_raw = json.load(pyglet.resource.file('data/texts.json'))['texts']
texts = {}
for t in texts_raw:
    texts[t['name']] = t['text']

opening_1 = scene.TextScene(None, texts['opening-1'], font)
opening_2 = scene.TextScene(None, texts['opening-2'], font)
opening_3 = scene.TextScene(None, texts['opening-3'], font)
title = scene.TextScene(None, texts['title'], font)
town_0 = scene.GameScene(*tilemap.load('data/m_town.json'), hero_position=Vect(100, 4), nextdir='r')
stage1_0 = scene.GameScene(*tilemap.load('data/m_stage1.json'), hero_position=Vect(4, 4), nextdir='r')
intermission1_2_0 = scene.TextScene(None, texts['intermission-1to2'], font)
stage2_0 = scene.GameScene(*tilemap.load('data/m_stage2.json'), hero_position=Vect(4, 36), nextdir='t')
intermission2_3_0 = scene.TextScene(None, texts['intermission-2to3'], font)
stage3_0 = scene.GameScene(*tilemap.load('data/m_stage3.json'), hero_position=Vect(244, 8), nextdir='b')
intermission3_2_1 = scene.TextScene(None, texts['intermission-3to2+'], font)
stage2_1 = scene.GameScene(*tilemap.load('data/m_stage2_n.json'), hero_position=Vect(248, 48), nextdir='l')
intermission2_1_1 = scene.TextScene(None, texts['intermission-2+to1+'], font)
stage1_1 = scene.GameScene(*tilemap.load('data/m_stage1_n.json'), hero_position=Vect(248, 36), nextdir='l')
town_1 = scene.GameScene(*tilemap.load('data/m_town_n.json'), hero_position=Vect(248, 4), nextdir='r')
stage1_2 = scene.GameScene(*tilemap.load('data/m_stage1_n.json'), hero_position=Vect(4, 4), nextdir='r')
intermission1_2_2 = scene.TextScene(None, texts['intermission-1++to2++'], font)
stage2_2 = scene.GameScene(*tilemap.load('data/m_stage2_n.json'), hero_position=Vect(4, 36), nextdir='t')
intermission2_3_2 = scene.TextScene(None, texts['intermission-2++to3++'], font)
stage3_2 = scene.GameScene(*tilemap.load('data/m_stage3_n.json'), hero_position=Vect(244, 8), nextdir='b')
stage2_3 = scene.GameScene(*tilemap.load('data/m_stage2.json'), hero_position=Vect(248, 48), nextdir='l')
stage1_3 = scene.GameScene(*tilemap.load('data/m_stage1.json'), hero_position=Vect(248, 36), nextdir='l')
triumphant_return = scene.TextScene(None, texts['triumphant-return'], font)
town_2 = scene.GameScene(*tilemap.load('data/m_town.json'), hero_position=Vect(248, 4))
goodending_0 = scene.TextScene(None, texts['goodEnding-0'], font)
goodending_1 = scene.TextScene(None, texts['goodEnding-1'], font)
goodending_2 = scene.TextScene(None, texts['goodEnding-2'], font)
goodending_3 = scene.TextScene(None, texts['goodEnding-3'], font)
anyending_0 = scene.TextScene(None, texts['anyEnding-0'], font)
anyending_1 = scene.TextScene(None, texts['anyEnding-1'], font)
dotdotdot = scene.TextScene(None, texts['dotDotDot'], font)
anyending_2 = scene.TextScene(None, texts['anyEnding-2'], font)
credits_0 = scene.TextScene(None, texts['credits-0'], font)
credits_1 = scene.TextScene(None, texts['credits-1'], font)

SCENES = [opening_1, opening_2, opening_3, title,
        town_0, stage1_0, intermission1_2_0, stage2_0, intermission2_3_0, stage3_0,
        intermission3_2_1, stage2_1, intermission2_1_1, stage1_1,
        town_1, stage1_2, intermission1_2_2, stage2_2, intermission2_3_2, stage3_2,
        stage2_3, stage1_3, triumphant_return, town_2,
        goodending_0, goodending_1, goodending_2, goodending_3,
        anyending_0, anyending_1, dotdotdot, anyending_2,
        credits_0, credits_1]

class TestWindow(pyglet.window.Window):
    def __init__(self):
        super(TestWindow, self).__init__(64*SCALE, 48*SCALE, caption="\'blong Cong")
        testmap = tilemap.load('data/m_stage1.json')
        map, mapv = testmap
        self.scene = SCENES.pop(0)
        self.scene.setup()

    def mupdate(self, dt):
        if self.scene.mupdate(dt) == 'next':
            self.scene = SCENES.pop(0)
            self.scene.setup()

    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.scene.vupdate()
        self.scene.draw()

    def on_key_press(self, symbol, modifiers):
        self.scene.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.scene.on_key_release(symbol, modifiers)


w = TestWindow()
glScalef(SCALE, SCALE, SCALE)



pyglet.clock.schedule_interval(w.mupdate, 0.02)
pyglet.app.run()