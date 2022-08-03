import pygame
from entity import Entity
from support import import_folder
from settings import *

# **********************************************************************************************************************

class Enemy(Entity):
    def __init__(self, type, pos, groups):
        # general setup
        super().__init__(groups)

        # graphics
        self.status = 'move'
        self.path = f'assets/enemy/{type}/move/0.png'
        self.image = pygame.image.load(self.path).convert_alpha()

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # stats
        self.type = type
        enemy_stats = enemy_data[self.type]
        self.health = enemy_stats['health']
        self.speed = enemy_stats['speed']
        self.damage = enemy_stats['damage']
        self.exp = enemy_stats['exp']
        self.gems = enemy_stats['gems']
        self.attack_radius = enemy_stats['attack_radius']
        self.notice_radius = 4096
        self.attack_type = 'slash'
        self.resistance = 3

        # cooldown
        self.can_attack = True

    # ******************************************************************************************************************

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius:
            self.status = 'attack'
        else:
            self.status = 'move'

    # ******************************************************************************************************************

    def get_player_distance_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    # ******************************************************************************************************************

    def actions(self, player):
        if self.status == 'attack' and self.can_attack:
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
            player.health -= self.damage
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]

    # ******************************************************************************************************************

    def cooldowns(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()

            if current_time - self.attack_time >= 1000:
                self.can_attack = True

    # ******************************************************************************************************************

    def update(self):
        self.move(self.speed, 'enemy')
        self.cooldowns()

    # ******************************************************************************************************************

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
