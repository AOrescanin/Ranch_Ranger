# import pygame
import sys
from player import Player
from enemy import Enemy
from knife import Knife
from upgrade import Upgrade
from shop import Shop
from tile import Tile
from settings import *
from support import *

# **********************************************************************************************************************

# noinspection PyTypeChecker
class Level:
    def __init__(self):
        # general setup
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.object_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # enemy setup
        self.enemy_list = []

        # sprite setup
        self.create_map()

        # round
        self.round = 1
        self.round_font = pygame.font.Font(GAME_FONT, UI_FONT_SIZE)

        # menus
        self.upgrade = Upgrade(self.player)
        self.shop = Shop(self.player)
        self.u_game_paused = False
        self.i_game_paused = False

    # ******************************************************************************************************************

    def create_map(self):
        # importing graphics
        layouts = {
                'boundary': import_csv_layout('assets/level/map_floorblocks.csv'),  # rename csv files
                'objects': import_csv_layout('assets/level/map_objects.csv'),
        }
        graphics = {
            'objects': import_folder('assets/objects'),
        }

        # grouping graphics
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'objects':
                            surface = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)
                            Tile((x, y), [self.object_sprites], 'object', surface)

        # creating player
        self.player = Player(2448, 1948, [self.visible_sprites], self.obstacle_sprites, self.object_sprites,
                             self.create_attack, self.destroy_attack)

    # ******************************************************************************************************************

    def spawn_enemies(self, round_num):
        spawn_multiplier = 1

        # spawn the 3 types of enemies for the round number
        for i in range(round_num):
            enemy1 = Enemy('fast', (2500 + (128 * spawn_multiplier), 7500), [self.visible_sprites])
            enemy2 = Enemy('normal', (-800, 3000 + (128 * spawn_multiplier)), [self.visible_sprites])
            enemy3 = Enemy('strong', (2000 + (128 * spawn_multiplier), -100), [self.visible_sprites])
            self.enemy_list.append(enemy1)
            self.enemy_list.append(enemy2)
            self.enemy_list.append(enemy3)
            spawn_multiplier += 1

    # ******************************************************************************************************************

    def create_attack(self):
        self.current_attack = Knife(self.player, [self.visible_sprites])

    # ******************************************************************************************************************

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()

        self.current_attack = None

    # ******************************************************************************************************************

    def display_round(self):
        round_text = self.round_font.render(str(self.round - 1), False, HEALTH_COLOR)
        round_text_rect = round_text.get_rect(midtop=(HALF_WIDTH, 16))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, round_text_rect.inflate(16, 16))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, round_text_rect.inflate(16, 16), LINE_THICKNESS)
        self.display_surface.blit(round_text, round_text_rect)

    # ******************************************************************************************************************

    def toggle_upgrade_menu(self):
        self.u_game_paused = not self.u_game_paused

    # ******************************************************************************************************************

    def toggle_shop_menu(self):
        self.i_game_paused = not self.i_game_paused

    # ******************************************************************************************************************

    def enemy_hit(self):
        for enemy in self.enemy_list:
            for bullet in self.player.bullet_list:
                x_min = enemy.hitbox[0] - (self.player.rect.centerx - HALF_WIDTH)
                x_max = ((enemy.hitbox[0] - (self.player.rect.centerx - HALF_WIDTH)) + enemy.hitbox[2])
                y_min = enemy.hitbox[1] - (self.player.rect.centery - HALF_HEIGHT)
                y_max = ((enemy.hitbox[1] - (self.player.rect.centery - HALF_HEIGHT)) + enemy.hitbox[3])

                if (x_min < bullet.x < x_max) and (y_min < bullet.y < y_max):
                    enemy.health -= self.player.current_weapon.damage

                    if enemy.health <= 0:
                        self.visible_sprites.remove(enemy)
                        self.enemy_list.remove(enemy)
                        self.player.exp += enemy.exp
                        self.player.gems += enemy.gems
                        # self.death_sound.play()

                    # allows for rifle and laser weapons to go through enemies
                    if self.player.current_weapon.ammo_type != 'Laser' and self.player.current_weapon.ammo_type != 'FMJ':
                        self.player.bullet_list.remove(bullet)

    # ******************************************************************************************************************

    def run(self):
        # draw the game
        self.visible_sprites.custom_draw(self.player)
        self.player.display()
        self.display_round()

        # toggle menus
        if self.u_game_paused:
            self.upgrade.display()
        elif self.i_game_paused:
            self.shop.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player, self.enemy_list)
            self.enemy_hit()
            if len(self.enemy_list) == 0:
                self.spawn_enemies(self.round)
                self.round += 1


# **********************************************************************************************************************

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surface = pygame.image.load("assets/level/map.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    # ******************************************************************************************************************

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - HALF_WIDTH
        self.offset.y = player.rect.centery - HALF_HEIGHT

        # drawing the floor
        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_position)

        # offsetting the graphics to the player
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    # ******************************************************************************************************************

    def enemy_update(self, player, enemy_list):
        for enemy in enemy_list:
            enemy.enemy_update(player)
