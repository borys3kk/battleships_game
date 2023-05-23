import pygame as pg

class Button:
    def __init__(self, text, x, y, color,width,height):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont("comicsans", 40)
        text = font.render(self.text, True, (0,0,0))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False