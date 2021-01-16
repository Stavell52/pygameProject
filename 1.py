import os
import sys
import random

import pygame


pygame.init()
size = width, height = 450, 620
screen = pygame.display.set_mode(size)
fps = 200


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Правила игры:',
                  '      1. Цель игры – вырастить цветок.',
                  '      2. Есть 3 этапа роста.',
                  '      3. Для завершения каждого этапа нужно:',
                  '         5 капелек и 5 солнышек.',
                  '      4. Для сбора капелек или солнышек нужно',
                  '         нажать на соответствующий символ.',
                  '      5. Для возврата на главный экран – нажать',
                  '         клавишу «пробел».',
                  '      Enjoy yourself!']
    fon = pygame.transform.scale(load_image('fon.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 25)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def menu_screen():
    global level, grouth
    fon = pygame.transform.scale(load_image('fon.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    image_pot = load_image('pot.png')
    screen.blit(image_pot, (175, 390))
    pygame.draw.rect(screen, '#b5d8ef', (100, 510, 100, 89), width=0)
    image_drop = load_image('drop.png')
    screen.blit(image_drop, (100, 510))
    pygame.draw.circle(screen, '#efd8b5', (302, 559), 50, width=0)
    image_sun = load_image('sun.png')
    screen.blit(image_sun, (250, 500))
    if not grouth:
        image_flower = load_image('flower0.png')
        screen.blit(image_flower, (175, 270))
    elif grouth == 1:
        image_flower = load_image('flower1.png')
        screen.blit(image_flower, (185, 100))
    elif grouth == 2:
        image_flower = load_image('flower2.png')
        screen.blit(image_flower, (175, 117))
    elif grouth == 3:
        image_flower = load_image('flower3.png')
        screen.blit(image_flower, (135, 10))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (100 <= event.pos[0] <= 200) and (510 <= event.pos[1] <
                                                     600):
                    level = 1
                    return
                if (250 <= event.pos[0] <= 350) and (510 <= event.pos[1] <=
                                                     622):
                    level = 2
                    return
        pygame.display.flip()
        clock.tick(fps)


class Pot(pygame.sprite.Sprite):
    image = load_image('pot.png')

    def __init__(self):
        super().__init__(pot_sprite)
        self.image = Pot.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = 175, 530

    def update(self, pos):
        if pos:
            x, y = pos
            x = x - self.rect.x
            y = y - self.rect.y
            self.rect = self.rect.move(x - 50, y - 44)


class Drop(pygame.sprite.Sprite):
    image = load_image("drop1.png")

    def __init__(self):
        super().__init__(drop_sprites)
        self.image = Drop.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randint(0, 401)
        self.rect.y = 0

    def update(self, pot):
        global kol_drop
        if not pygame.sprite.collide_mask(self, pot):
            self.rect = self.rect.move(0, 1)
        else:
            pygame.sprite.spritecollide(pot, drop_sprites, True)
            kol_drop += 1


def level1():
    global level, drop_sprites, pot_sprite
    drop_sprites = pygame.sprite.Group()
    pot_sprite = pygame.sprite.Group()
    pot = Pot()
    pos = ()
    k = 0
    moving = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == 32:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                moving = True
                pos = event.pos
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if moving:
                    pos = ()
                    moving = False
        screen.fill('#b5d8ef')
        if k % 150 == 0:
            Drop()
        k += 1
        drop_sprites.draw(screen)
        pot_sprite.draw(screen)
        drop_sprites.update(pot)
        pot_sprite.update(pos)
        pygame.display.flip()
        clock.tick(fps)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'cloud': load_image('cloud.png'),
    'empty': load_image('empty.png'),
    'sun': load_image('sun2.png')
}
player_image = load_image('pot2.png')
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, player, index):
        global kol_sun
        if pygame.sprite.collide_mask(self, player):
            if self.tile_type == 'sun':
                pygame.sprite.spritecollide(player, tiles_group, True)
                kol_sun += 1
            elif self.tile_type == 'cloud':
                index[0] *= -1
                index[1] *= -1
                player_group.update(index)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, index):
        self.rect = self.rect.move(index)


def generate_level(level_view):
    new_player, x, y = None, None, None
    for y in range(len(level_view)):
        for x in range(len(level_view[y])):
            if level_view[y][x] == '.':
                Tile('empty', x, y)
            elif level_view[y][x] == '#':
                Tile('cloud', x, y)
            elif level_view[y][x] == '*':
                Tile('sun', x, y)
            elif level_view[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def level2():
    global tiles_group, player_group, all_sprites
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player, level_x, level_y = generate_level(load_level('level2.txt'))
    index = (0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    return
                elif event.key == 1073741903:
                    index = [tile_width, 0]
                elif event.key == 1073741904:
                    index = [-tile_width, 0]
                elif event.key == 1073741905:
                    index = [0, tile_height]
                elif event.key == 1073741906:
                    index = [0, -tile_height]
        screen.fill('#b5d8ef')
        all_sprites.draw(screen)
        player_group.update(index)
        tiles_group.update(player, index)
        index = (0, 0)
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    clock = pygame.time.Clock()
    drop_sprites = pygame.sprite.Group()
    pot_sprite = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    flower_sprites = pygame.sprite.Group()
    running = True
    level = 0
    kol_drop = 0
    kol_sun = 0
    grouth = 0
    start_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not level:
            menu_screen()
            screen.fill('black')
        elif level == 1:
            kol_drop = 0
            level1()
            level = 0
        elif level == 2:
            kol_sun = 0
            level2()
            level = 0
        if kol_drop >= 5 and kol_sun >= 5:
            kol_drop = 0
            kol_sun = 0
            grouth += 1
        if grouth == 4:
            running = False
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()