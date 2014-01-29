import json
import pyglet
from shapes import *

def load(filename):
    f = pyglet.resource.file(filename)
    j = json.load(f)
    return parse_tilemap(j)

def parse_tilemap(json_obj):
    tmap = TileMap()
    tmap.layers = [parse_tilelayer(a) for a in json_obj['layers']]
    tmap.orientation = json_obj['orientation']
    tmap.tilewidth = json_obj['tilewidth']
    tmap.tileheight = json_obj['tileheight']
    tmap.width = json_obj['width']
    tmap.height = json_obj['height']
    tmap.version = json_obj['version']
    # tmap.backgroundcolor = json_obj['backgroundcolor']
    tmap.properties = json_obj['properties']
    tmapv = TileMapView(tmap)
    tmapv.tilesets = [parse_tileset(a) for a in json_obj['tilesets']]
    return tmap, tmapv

def parse_tilelayer(json_obj):
    tlay = TileLayer()
    tlay.opacity = json_obj['opacity']
    tlay.name = json_obj['name']
    tlay.width = json_obj['width']
    tlay.height = json_obj['height']
    tlay.visible = json_obj['visible']
    tlay.x = json_obj['x']
    tlay.y = json_obj['y']
    tlay.type = json_obj['type']
    tlay.data = json_obj['data']
    tlay.properties = json_obj['properties']
    return tlay

def parse_tileset(json_obj):
    tset = TileSet()
    tset.name = json_obj['name']
    tset.tilewidth = json_obj['tilewidth']
    tset.tileheight = json_obj['tileheight']
    tset.transparentcolor = json_obj['transparentcolor']
    spacing = json_obj['spacing']
    imagewidth = json_obj['imagewidth']
    imageheight = json_obj['imageheight']
    tset.firstgid = json_obj['firstgid']
    margin = json_obj['margin']
    tset.properties = json_obj['properties']
    tset.rows = imageheight / tset.tileheight
    tset.cols = imagewidth / tset.tilewidth
    image = pyglet.resource.image(json_obj['image'])#.get_region(
           # margin, margin, imagewidth-margin, imageheight-margin)
    tset.grid = pyglet.image.ImageGrid(image,
            tset.rows, tset.cols,
            item_width=tset.tilewidth, item_height=tset.tileheight,
            row_padding=spacing, column_padding=spacing)
    return tset


class TileMap(object):
    def __init__(self):
        self.tiles = []
        self.obstacle = []

    def setup(self):
        self.obstacle = [False] * self.width * self.height
        for lay in self.layers:
            collision_type = lay.properties.get('collision-type', 'void')
            print 'layer', lay.name, 'type', collision_type
            if collision_type == 'block':
                for row in range(lay.height):
                    for col in range(lay.width):
                        index = row * lay.width + col
                        if lay[index] > 0:
                            w = self.tilewidth
                            h = self.tileheight
                            x = col * w
                            y = row * h
                            self.obstacle[index] = True

    def find_obstacle(self, coordinate_list):
        for col, row in coordinate_list:
            if self.obstacle_at(col, row):
                return self.rect_at(col, row)
        return None

    def obstacle_at(self, col, row):
        if col in range(self.width) and row in range(self.height):
            tileindex = row * self.width + col
            return self.obstacle[tileindex]
        else:
            return False  # Handle screen exit.

    def rect_at(self, col, row):
        return Rect(col * self.tilewidth, row * self.tileheight, self.tilewidth, self.tileheight)


class Tile(object):
    def __init__(self, x, y, w, h, collision_type):
        self.hitbox = Rect(x, y, w, h)
        self.collision_type = collision_type


class TileMapView(object):
    def __init__(self, model):
        self.model = model
        self.sprites = []
        self.tilesets = []
        self.tileset = {}

    def index_tiles(self):
        for tset in self.tilesets:
            for index, tile in enumerate(tset):
                self.tileset[tset.firstgid + index] = tile

    def setup(self):
        self.index_tiles()
        self.batch = pyglet.graphics.Batch()
        self.groups = []
        self.sprites = []
        t_w = self.model.tilewidth
        t_h = self.model.tileheight
        for lay in self.model.layers:
            lay_index = len(self.groups)
            self.groups.append(pyglet.graphics.OrderedGroup(lay_index))
            for col in range(lay.width):
                for row in range(lay.height):
                    t_index = row * lay.width + col
                    if lay[t_index] > 0:
                        img = self.tileset[lay[t_index]]
                        x, y = t_w * col, t_h * row
                        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch,
                                group=self.groups[-1])
                        spr.original_position = Vect(spr.x, spr.y)
                        self.sprites.append(spr)

    def update_sprite_position(self, offset):
        for spr in self.sprites:
            spr.position = spr.original_position + offset


class TileLayer(object):
    def __init__(self):
        pass

    def __getitem__(self, index):
        """ Adjusts for Pyglet's inverted y axis. """
        c = index % self.width
        r = self.height - 1 - index // self.width
        return self.data[r * self.width + c]


class TileSet(object):
    def __init__(self):
        pass

    def __getitem__(self, index):
        """ Adjusts for Pyglet's inverted y axis. """
        c = index % self.cols
        r = self.rows - 1 - index // self.cols
        return self.grid[r * self.cols + c]

