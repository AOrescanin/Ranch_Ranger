import pygame
from entity import Entity
from weapon import Weapon
from bullet import Bullet
from support import import_folder
from settings import *

# **********************************************************************************************************************

class Player(Entity):
    def __init__(self, x, y, groups, obstacle_sprites, object_sprites, create_attack, destroy_attack):
        # general setup
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()

        # player setup
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.import_player_animations()
        self.status = 'down'
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        # player movement
        self.hitbox = self.rect.inflate(0, -24)
        self.obstacle_sprites = obstacle_sprites

        # player stats
        self.stats = {'health': 80, 'speed': 4}
        self.max_stats = {'health': 320, 'speed': 9}
        self.upgrade_cost = {'health': 30, 'speed': 100}
        self.health = self.stats['health']
        self.speed = self.stats['speed']

        # health bar
        self.health_bar_rect = pygame.Rect(16, 16, HEALTH_BAR_WIDTH, BAR_HEIGHT)

        # exp and gems
        self.exp = 0
        self.gems = 0
        self.gem_image = pygame.image.load('assets/shop/gem.png')
        self.ui_font = pygame.font.Font(GAME_FONT, UI_FONT_SIZE)

        # consumables
        self.coffee_box_rect = pygame.Rect(16, HEIGHT - 96, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        self.carrot_box_rect = pygame.Rect(84, HEIGHT - 84, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        self.coffee_count = 0
        self.carrot_count = 0
        self.caffeinated = False
        self.ate_carrot = False
        self.coffee_image = pygame.image.load('assets/consumables/coffee.png')
        self.carrot_image = pygame.image.load('assets/consumables/carrot.png')
        self.coffee_sound = pygame.mixer.Sound('assets/consumables/coffee.wav')
        self.carrot_sound = pygame.mixer.Sound('assets/consumables/carrot.wav')
        self.consumable_font = pygame.font.Font(GAME_FONT, CONSUMABLE_FONT_SIZE)

        # weapons
        self.weapons_list = []
        for weapon in weapon_data.values():
            gun = Weapon(weapon['image'], weapon['position'], weapon['magazine'], weapon['ammo_type'], weapon['damage'],
                         weapon['shooting_cooldown'], weapon['reload_cooldown'], weapon['cost'], weapon['bullet_image'],
                         weapon['shot_sound'], weapon['reload_sound'])
            self.weapons_list.append(gun)

        self.weapon1 = self.weapons_list[0]
        self.weapon2 = self.weapons_list[0]
        self.current_weapon = self.weapon1
        self.bullet_list = []
        self.object_sprites = object_sprites
        self.switch_sound = pygame.mixer.Sound('assets/weapons/switch.wav')
        self.stab_sound = pygame.mixer.Sound('assets/weapons/stab_sound.wav')

        # cool downs
        self.shooting_count = 0
        self.stab_count = 0
        self.reload_count = 0
        self.switch_count = 0
        self.consume_count = 0
        self.stabbing = False
        self.reloading = False
        self.switching = False
        self.consuming = False

    # ******************************************************************************************************************

    def import_player_animations(self):
        player_path = 'assets/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)

    # ******************************************************************************************************************

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.stabbing:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    # ******************************************************************************************************************

    def display(self):
        # convert the health to pixels
        ratio = self.health / self.stats['health']
        current_health_width = self.health_bar_rect.width * ratio
        current_health_rect = self.health_bar_rect.copy()
        current_health_rect.width = current_health_width

        # draw the health bar
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.health_bar_rect)
        pygame.draw.rect(self.display_surface, HEALTH_COLOR, current_health_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.health_bar_rect, LINE_THICKNESS)

        # exp
        exp_text_surface = self.ui_font.render('XP-' + str(int(self.exp)), False, TEXT_COLOR)
        x = WIDTH - 16
        y = 16
        exp_text_rect = exp_text_surface.get_rect(topright=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, exp_text_rect.inflate(16, 16))
        self.display_surface.blit(exp_text_surface, exp_text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, exp_text_rect.inflate(16, 16), LINE_THICKNESS)

        # gems
        gems_text_surface = self.ui_font.render(str(int(self.gems)), False, TEXT_COLOR)
        gems_text_rect = gems_text_surface.get_rect(topright=(x, exp_text_rect.bottomright[1] + 32))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, gems_text_rect.inflate(16, 16))
        self.display_surface.blit(gems_text_surface, gems_text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, gems_text_rect.inflate(16, 16), LINE_THICKNESS)
        self.display_surface.blit(self.gem_image, (gems_text_rect[0] - 100, gems_text_rect[1]))

        # consumables
        pygame.draw.rect(self.display_surface, ITEM_BOX_COLOR, self.coffee_box_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.coffee_box_rect, LINE_THICKNESS)

        if self.coffee_count > 0:
            coffee_count_surface = self.consumable_font.render(str(self.coffee_count), True, TEXT_COLOR)
            coffee_count_rect = coffee_count_surface.get_rect(bottomleft=(20, HEIGHT - 20))
            self.display_surface.blit(self.coffee_image, (16, HEIGHT - 96))
            self.display_surface.blit(coffee_count_surface, coffee_count_rect)

        pygame.draw.rect(self.display_surface, ITEM_BOX_COLOR, self.carrot_box_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.carrot_box_rect, LINE_THICKNESS)

        if self.carrot_count > 0:
            carrot_count_surface = self.consumable_font.render(str(self.carrot_count), True, TEXT_COLOR)
            carrot_count_rect = carrot_count_surface.get_rect(bottomleft=(88, HEIGHT - 8))
            self.display_surface.blit(self.carrot_image, (84, HEIGHT - 84))
            self.display_surface.blit(carrot_count_surface, carrot_count_rect)

        # weapon
        self.current_weapon.draw_weapon(self.display_surface)

        # bullets
        keys = pygame.key.get_pressed()

        for bullet in self.bullet_list:  # offset for bullets player movement
            if keys[pygame.K_a]:
                bullet.x += self.stats['speed']
            if keys[pygame.K_d]:
                bullet.x -= self.stats['speed']

            if keys[pygame.K_w]:
                bullet.y += self.stats['speed']
            if keys[pygame.K_s]:
                bullet.y -= self.stats['speed']

            bullet.shoot(self.display_surface)

            if bullet.off_screen():
                self.bullet_list.remove(bullet)

    # ******************************************************************************************************************

    def input(self):
        # general setup
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # horizontal movement
        if keys[pygame.K_a] and not self.stabbing:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d] and not self.stabbing:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # vertical movement
        if keys[pygame.K_w] and not self.stabbing:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s] and not self.stabbing:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        # shooting
        if pygame.mouse.get_pressed()[0] and self.current_weapon.current_magazine > 0 and not self.stabbing \
                and not self.reloading and not self.switching and not self.consuming and self.shooting_count == 0:
            # shotgun spray
            # if self.current_weapon.ammo_type == 'Buckshot':
            #     self.bullet_list.append(Bullet(HALF_WIDTH, HALF_HEIGHT, mouse_x - 32, mouse_y - 32,
            #                                    self.current_weapon.bullet_image))
            #     self.bullet_list.append(Bullet(HALF_WIDTH, HALF_HEIGHT, mouse_x + 32, mouse_y + 32,
            #                                    self.current_weapon.bullet_image))

            self.bullet_list.append(Bullet(HALF_WIDTH, HALF_HEIGHT, mouse_x, mouse_y, self.current_weapon.bullet_image))
            self.shooting_count = 1
            self.current_weapon.current_magazine -= 1
            self.current_weapon.gun_shot.play()

        # stabbing
        if pygame.mouse.get_pressed()[2] and not self.reloading and not self.switching and not self.consuming \
                and self.stab_count == 0:
            self.create_attack()
            self.stabbing = True
            self.stab_count = 1
            self.stab_sound.play()

        # reloading
        if keys[pygame.K_r] and self.current_weapon.ammo_type != 'Laser' \
                and self.current_weapon.current_magazine < self.current_weapon.magazine \
                and not self.reloading and not self.switching and not self.consuming:
            self.reloading = True
            self.reload_count = 1
            self.current_weapon.reload_sound.play()

        # switching
        if keys[pygame.K_q] and not self.switching and not self.reloading:
            self.switching = True
            self.switch_count = 1

            if self.current_weapon == self.weapon1:
                self.current_weapon = self.weapon2
            else:
                self.current_weapon = self.weapon1

            self.switch_sound.play()

        # consumables
        if keys[pygame.K_c] and self.coffee_count > 0 and not self.consuming and not self.caffeinated:
            self.consuming = True
            self.caffeinated = True
            self.consume_count = 1
            self.coffee_count -= 1
            self.consume_time = pygame.time.get_ticks()
            self.coffee_sound.play()

        if keys[pygame.K_v] and self.carrot_count > 0 and not self.consuming and self.health < self.stats['health']:
            self.consuming = True
            self.ate_carrot = True
            self.consume_count = 1
            self.carrot_count -= 1
            if self.health + CARROT_HEAL <= self.stats['health']:
                self.health += CARROT_HEAL
            else:
                self.health = self.stats['health']

            self.carrot_sound.play()

    # ******************************************************************************************************************

    def cooldown(self):
        # shooting cooldown
        if self.shooting_count >= self.current_weapon.shooting_cooldown:
            self.shooting_count = 0
        elif self.shooting_count > 0:
            self.shooting_count += 1

        # stab cooldown
        if self.stab_count >= STAB_COOLDOWN:
            self.stab_count = 0
            self.stabbing = False
            self.destroy_attack()
        elif self.stab_count > 0:
            self.stab_count += 1

        # reload cooldown
        if self.reload_count >= self.current_weapon.reload_cooldown:
            self.reload_count = 0
            self.reloading = False
            self.current_weapon.current_magazine = self.current_weapon.magazine
        elif self.reload_count > 0:
            self.reload_count += 1

        # switch cooldown
        if self.switch_count >= SWITCH_COOLDOWN:
            self.switch_count = 0
            self.switching = False
        elif self.switch_count > 0:
            self.switch_count += 1

        # consume cooldown
        if self.consume_count >= CONSUME_COOLDOWN:
            self.consume_count = 0
            self.consuming = False
        elif self.consume_count > 0:
            self.consume_count += 1

        # caffeine cooldown
        if self.caffeinated:
            current_time = pygame.time.get_ticks()

            if current_time - self.consume_time >= CAFFEINATED_DURATION:
                self.caffeinated = False

    # ******************************************************************************************************************

    def bullet_hit(self):
        # checking for bullet collisions with objects(lasers can pass through objects)
        if self.current_weapon.ammo_type != 'Laser':
            for sprite in self.object_sprites:
                for bullet in self.bullet_list:
                    x_min = sprite.hitbox[0] - (self.rect.centerx - HALF_WIDTH)
                    x_max = ((sprite.hitbox[0] - (self.rect.centerx - HALF_WIDTH)) + sprite.hitbox[2])
                    y_min = sprite.hitbox[1] - (self.rect.centery - HALF_HEIGHT)
                    y_max = ((sprite.hitbox[1] - (self.rect.centery - HALF_HEIGHT)) + sprite.hitbox[3])
                    if (x_min < bullet.x < x_max) and (y_min < bullet.y < y_max):
                        self.bullet_list.remove(bullet)

    # ******************************************************************************************************************

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    # ******************************************************************************************************************

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    # ******************************************************************************************************************

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    # ******************************************************************************************************************

    def update(self):
        self.get_status()
        self.input()
        if self.caffeinated:
            self.move(self.stats['speed'] * COFFEE_SPEED_BUFF, 'player')
        else:
            self.move(self.stats['speed'], 'player')
        self.cooldown()
        self.bullet_hit()
        self.animate()
