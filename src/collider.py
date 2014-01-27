import itertools

def collide(colliders):
    spatial_hash = {}
    collisions = set()
    for collider in colliders:
        for x in range(int(collider.hitbox.x), int(collider.hitbox.right), 4):
            hash = x >> 2
            if hash not in spatial_hash:
                spatial_hash[hash] = []
            spatial_hash[hash].append(collider)
        for area in spatial_hash.values():
            combos = itertools.combinations(area, 2)
            hits = filter(lambda x: x[0].hitbox & x[1].hitbox, combos)
            collisions |= set(hits)
    return collisions