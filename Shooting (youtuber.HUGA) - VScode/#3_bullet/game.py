import pygame
from setting import *
from player import Player

class Game:

    def __init__(self):
        self.screen = pygame.display.get_surface()

        #グループの作成
        self.create_group()

        #自機
        player = Player(self.player_group, 300, 500)

        #背景
        self.pre_bg_img = pygame.image.load('assets/img/background/bg.png')
        self.bg_img = pygame.transform.scale(self.pre_bg_img, (screen_width, screen_height))
        self.bg_y = 0
        self.scroll_speed = 0.5

    def create_group(self):
        self.player_group = pygame.sprite.GroupSingle()

    def scroll_bg(self):
        self.bg_y = (self.bg_y + self.scroll_speed) % screen_height
        self.screen.blit(self.bg_img, (0, self.bg_y - screen_height))
        self.screen.blit(self.bg_img, (0, self.bg_y))

    def run(self):
        self.scroll_bg()

        #グループの描画と更新
        self.player_group.draw(self.screen)
        self.player_group.update()




