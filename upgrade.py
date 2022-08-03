import pygame
from settings import *

# **********************************************************************************************************************

class Upgrade:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_num = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(GAME_FONT, UPGRADE_FONT_SIZE)

        # items
        self.width = WIDTH // 6
        self.height = HEIGHT * 0.8
        self.create_items()

        # selection
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.selection_sound = pygame.mixer.Sound('assets/upgrade/selection_sound.wav')

    # ******************************************************************************************************************

    def input(self):
        keys = pygame.key.get_pressed()

        # movement and selection
        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_num - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.selection_sound.play()
            elif keys[pygame.K_LEFT] and self.selection_index > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.selection_sound.play()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    # ******************************************************************************************************************

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()

            if current_time - self.selection_time >= SELECTION_COOLDOWN:
                self.can_move = True

    # ******************************************************************************************************************

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_num)):
            # horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_num
            left = (item * increment) + (increment - self.width) // 2

            # vertical position
            top = self.display_surface.get_size()[1] * 0.1

            # create object
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    # ******************************************************************************************************************

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)

# **********************************************************************************************************************


class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font
        self.upgrade_sound = pygame.mixer.Sound('assets/upgrade/upgrade_sound.wav')

    # ******************************************************************************************************************

    def display_names(self, surface, name, cost):
        # title
        title_surface = self.font.render(name, False, MENU_TEXT_COLOR)
        title_rect = title_surface.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 16))

        # cost
        cost_surface = self.font.render(str(int(cost)), False, MENU_TEXT_COLOR)
        cost_rect = cost_surface.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,16))

        # draw
        surface.blit(title_surface, title_rect)
        surface.blit(cost_surface, cost_rect)

    # ******************************************************************************************************************

    def display_bar(self, surface, value, max_value):
        # drawing setuo
        top = self.rect.midtop + pygame.math.Vector2(0, 64)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 64)

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 32, 16)

        # draw elements
        pygame.draw.line(surface, MENU_TEXT_COLOR, top, bottom, 4)
        pygame.draw.rect(surface, MENU_TEXT_COLOR, value_rect)

    # ******************************************************************************************************************

    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if player.exp >= player.upgrade_cost[upgrade_attribute] and \
                player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4
            self.upgrade_sound.play()

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]
            self.upgrade_sound.play()

    # ******************************************************************************************************************

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost)
        self.display_bar(surface, value, max_value)
