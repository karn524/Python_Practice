import pygame
from setting import *
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, x, y):
        super().__init__(groups)

        #画像
        self.image_list = []
        for i in range(5):
            image = pygame.image.load(f'assets/img/enemy/{i}.png')
            self.image_list.append(image)

        self.index = 0
        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(self.pre_image, (50, 50))
        self.rect = self.image.get_rect(center = (x, y))

        #移動
        move_list = [1, -1]
        self.direction = pygame.math.Vector2((random.choice(move_list), 1))
        self.speed = 1
        self.timer = 0

    def move(self):
        self.timer += 1
        if self.timer > 80:
            self.direction.x *= -1
            self.timer = 0

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def animation(self):
        self.index += 0.15
        if self.index > len(self.image_list):
            self.index = 0

        self.pre_image = self.image_list[int(self.index)]
        self.image = pygame.transform.scale(self.pre_image, (50, 50))

    def check_off_screen(self):
        if self.rect.top > screen_height:
            self.kill()

    def update(self):
        self.move()
        self.check_off_screen()
        self.animation()





