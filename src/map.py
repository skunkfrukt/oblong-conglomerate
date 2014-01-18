import json


class TileMap(object):
    def __init__(self, json_obj):
        self.layers = [TileMapLayer(a) for a in json_obs['layers']]
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


class TileSet(object):
    def __init__(self, json_obj):
        self.name = json_obj['name']
        self.tilewidth = json_obj['tilewidth']
        self.tileheight = json_obj['tileheight']
        self.image = json_obj['image']
        self.transparentcolor = json_obj['transparentcolor']
        self.spacing = json_obj['spacing']
        self.imagewidth = json_obj['imagewidth']
        self.imageheight = json_obj['imageheight']
        self.firstgid = json_obj['firstgid']
        self.margin = json_obj['margin']
        self.properties = json_obj['properties']
