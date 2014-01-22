import json
import pyglet

def load(filename):
    f = pyglet.resource.file(filename)
    j = json.load(f)
    return TileMap(j)

class TileMap(object):
    def __init__(self, json_obj):
        self.layers = [TileMapLayer(a) for a in json_obj['layers']]
        self.orientation = json_obj['orientation']
        self.tilewidth = json_obj['tilewidth']
        self.tileheight = json_obj['tileheight']
        self.width = json_obj['width']
        self.height = json_obj['height']
        self.version = json_obj['version']
        self.backgroundcolor = json_obj['backgroundcolor']
        self.tilesets = [TileSet(a) for a in json_obj['tilesets']]
        self.properties = json_obj['properties']


class TileMapLayer(object):
    def __init__(self, json_obj):
        self.opacity = json_obj['opacity']
        self.name = json_obj['name']
        self.width = json_obj['width']
        self.height = json_obj['height']
        self.visible = json_obj['visible']
        self.x = json_obj['x']
        self.y = json_obj['y']
        self.type = json_obj['type']
        self.data = json_obj['data']

    def __getitem__(self, index):
        """ Adjusts for Pyglet's inverted y axis. """
        c = index % self.width
        r = self.height - 1 - index // self.width
        return self.data[r * self.width + c]


class TileSet(object):
    def __init__(self, json_obj):
        self.name = json_obj['name']
        self.tilewidth = json_obj['tilewidth']
        self.tileheight = json_obj['tileheight']
        self.transparentcolor = json_obj['transparentcolor']
        spacing = json_obj['spacing']
        imagewidth = json_obj['imagewidth']
        imageheight = json_obj['imageheight']
        self.firstgid = json_obj['firstgid']
        margin = json_obj['margin']
        self.properties = json_obj['properties']
        self.rows = imageheight / self.tileheight
        self.cols = imagewidth / self.tilewidth
        image = pyglet.resource.image(json_obj['image'])#.get_region(
               # margin, margin, imagewidth-margin, imageheight-margin)
        self.grid = pyglet.image.ImageGrid(image,
                self.rows, self.cols,
                item_width=self.tilewidth, item_height=self.tileheight,
                row_padding=spacing, column_padding=spacing)

    def __getitem__(self, index):
        """ Adjusts for Pyglet's inverted y axis. """
        c = index % self.cols
        r = self.rows - 1 - index // self.cols
        return self.grid[r * self.cols + c]

