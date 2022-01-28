import pygame
import os
import sys

# level = input()
level = 'level1.txt'
if not os.path.isfile('data/' + level):
    print("Такого уровня не существует!!")
    sys.exit()

pygame.init()
pygame.display.set_caption('Перемещение героя')
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, folder='data'):
    fullname = os.path.join(folder, name)
    if not os.path.isfile(fullname):
        sys.exit()

    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.title = 0 if tile_type == 'empty' else 1


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y

        for i in all_sprites:
            if i.rect.x < 0:
                i.rect.x += width
            if i.rect.x > 500:
                i.rect.x -= width
            if i.rect.y < 0:
                i.rect.y += width
            if i.rect.y > 500:
                i.rect.y -= width
        s = pygame.sprite.spritecollideany(self, tiles_group)
        if s.title:
            self.rect.x -= x
            self.rect.y -= y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def splash_screen():
    image = load_image('mario.jpg')
    screen.blit(image, (0, 0))
    pygame.display.flip()


tile_images = {'wall': load_image('box.png'),
               'empty': load_image('grass.png')}
player_image = load_image('mar.png')
tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player, level_x, level_y = generate_level(load_level(level))
splash_screen()
camera = Camera()
for sprite in all_sprites:
    camera.apply(sprite)
running = True
start_game = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and start_game:
            screen.fill((0, 0, 0))
            pygame.display.flip()
            start_game = False
        if event.type == pygame.KEYDOWN and not start_game:
            if event.key == pygame.K_RIGHT:
                player.update(50, 0)
            if event.key == pygame.K_LEFT:
                player.update(-50, 0)
            if event.key == pygame.K_DOWN:
                player.update(0, 50)
            if event.key == pygame.K_UP:
                player.update(0, -50)

    if not start_game:
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
