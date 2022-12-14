import pygame

# **********************************************************************************************************************

class Knife(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'knife'
        direction = player.status.split('_')[0]

        # graphic
        full_path = f'assets/weapons/pitchfork/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))