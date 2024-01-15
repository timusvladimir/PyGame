import os
import sys

import pygame


#функция загрузка спрайтов
def load_image(name, color_key=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# класс курсора
class Cursor(pygame.sprite.Sprite):
    # инициализация класса
    def __init__(self, group):
        super().__init__(group)
        try:
            self.image = load_image("data\cursor\cursor.gif")
        except:
            print('Не найден графический файл курсора !')
            sys.exit()
        self.rect = self.image.get_rect()


cursor = pygame.sprite.Group()
cur = Cursor(cursor)
