import pygame
from settings import *

# **********************************************************************************************************************

class Weapon:
    def __init__(self, image, pos, magazine, ammo_type, damage, shooting_cooldown, reload_cooldown, cost, bullet_image,
                 shot_sound, reload_sound):
        self.image = pygame.image.load(image).convert_alpha()
        self.pos = pos
        self.magazine = magazine
        self.current_magazine = magazine
        self.ammo_type = ammo_type
        self.damage = damage
        self.shooting_cooldown = shooting_cooldown
        self.reload_cooldown = reload_cooldown
        self.cost = cost
        self.bullet_image = bullet_image
        self.gun_shot = pygame.mixer.Sound(shot_sound)
        self.reload_sound = pygame.mixer.Sound(reload_sound)
        self.font = pygame.font.Font(GAME_FONT, AMMO_FONT_SIZE)

    # ******************************************************************************************************************

    def draw_weapon(self, display):
        ammo_surface = self.font.render(str(self.current_magazine), True, 'Black')  # ADD COLOR TO SETTINGS

        if self.current_magazine > 9:
            ammo_rect = ammo_surface.get_rect(topleft=(self.pos[0] - 128, self.pos[1]))
        else:
            ammo_rect = ammo_surface.get_rect(topleft=(self.pos[0] - 64, self.pos[1]))

        display.blit(self.image, self.pos)

        if self.ammo_type != 'Laser':
            display.blit(ammo_surface, ammo_rect)
