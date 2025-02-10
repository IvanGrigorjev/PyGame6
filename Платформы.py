import os
import random
import sys
from random import randint

import pygame

WINDOW_SIZE = W, H = 500, 500
FPS = 60

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Платформы')


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


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 10), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, "grey", (0, 0, 50, 10))
        self.rect = pygame.Rect(pos[0], pos[1], 50, 10)
        self.add(platforms)

    def update(self, *args):
        pass


class Character(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        self.image.fill(pygame.Color("blue"))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, *args):
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect = self.rect.move(0, 1)
        else:
            if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_LEFT:
                self.rect = self.rect.move(-1, 0)
            if args and args[0].type == pygame.KEYDOWN and args[0].key == pygame.K_RIGHT:
                self.rect = self.rect.move(1, 0)


all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True

character = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            Platform(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            if not character:
                character = Character(event.pos)
            else:
                character.rect.x = event.pos[0]
                character.rect.y = event.pos[1]

    screen.fill('black')
    all_sprites.update(event)
    all_sprites.draw(screen)
    pygame.mouse.set_visible(True)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
