import os
import random
import sys
from random import randint

import pygame

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
FPS = 30
N = 15


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Boom them all- 2')
install_bomb = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb2.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - self.rect[2])
        self.rect.y = random.randrange(WINDOW_HEIGHT - self.rect[3])
        while pygame.sprite.spritecollideany(self, install_bomb):
            self.rect.x = random.randrange(WINDOW_WIDTH - self.rect[2])
            self.rect.y = random.randrange(WINDOW_HEIGHT - self.rect[3])
        self.add(install_bomb)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = load_image("boom.png")


all_sprites = pygame.sprite.Group()

for _ in range(N):
    Bomb()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('black')
    all_sprites.update(event)
    all_sprites.draw(screen)
    pygame.mouse.set_visible(True)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
