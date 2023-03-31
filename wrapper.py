import pygame as pg

class Wrapper:
    def __init__(self):
        pass
    
    def load_image(self, path, size:tuple((int, int)), rotate=False):
        img = pg.image.load(path)
        img = pg.transform.scale(img, size)

        if rotate:
            img = pg.transform.rotate(img, -90)

        return img