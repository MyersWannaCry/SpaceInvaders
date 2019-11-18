import pygame as pg


class Button:
    def __init__(self, rect, command):
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size).convert()
        self.image.fill((255, 0, 0))
        self.function = command

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.function()

    def draw(self, surf):
        surf.blit(self.image, self.rect)


def button_was_pressed():
    print('button_was_pressed')


screen = pg.display.set_mode((800, 600))
done = False
btn = Button(rect=(50, 50, 105, 25), command=button_was_pressed)

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        btn.get_event(event)
    btn.draw(screen)
    pg.display.update()