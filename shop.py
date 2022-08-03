import pygame
from button import Button
from settings import *

# **********************************************************************************************************************

class Shop:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.background = pygame.image.load('assets/shop/shop_background.png').convert_alpha()
        self.bought_sound = pygame.mixer.Sound('assets/shop/bought_sound.wav')
        self.menu_font = pygame.font.Font(GAME_FONT, SHOP_FONT_SIZE)
        self.clock = pygame.time.Clock()

        # buttons
        self.shotgun_button = Button(button_image=pygame.image.load('assets/shop/shotgun_button.png'),
                                     position=(0, 64), button_font=self.menu_font,
                                     base_color=MENU_TEXT_COLOR, highlight_color=COLOR_SELECTED,
                                     text_input=str(self.player.weapons_list[1].cost), type='shop')
        self.rifle_button = Button(button_image=pygame.image.load('assets/shop/rifle_button.png'),
                                   position=(0, HALF_HEIGHT - 108), button_font=self.menu_font,
                                   base_color=MENU_TEXT_COLOR, highlight_color=COLOR_SELECTED,
                                   text_input=str(self.player.weapons_list[2].cost), type='shop')
        self.assault_rifle_button = Button(button_image=pygame.image.load('assets/shop/assault_rifle_button.png'),
                                           position=(0, HEIGHT - 278), button_font=self.menu_font,
                                           base_color=MENU_TEXT_COLOR, highlight_color=COLOR_SELECTED,
                                           text_input=str(self.player.weapons_list[3].cost), type='shop')
        self.machine_gun_button = Button(button_image=pygame.image.load('assets/shop/machine_gun_button.png'),
                                         position=(WIDTH - 592, 64), button_font=self.menu_font,
                                         base_color=MENU_TEXT_COLOR, highlight_color=COLOR_SELECTED,
                                         text_input=str(self.player.weapons_list[4].cost), type='shop')
        self.rail_gun_button = Button(button_image=pygame.image.load('assets/shop/rail_gun_button.png'),
                                      position=(WIDTH - 592, HALF_HEIGHT - 108), button_font=self.menu_font,
                                      base_color=MENU_TEXT_COLOR, highlight_color=COLOR_SELECTED,
                                      text_input=str(self.player.weapons_list[5].cost), type='shop')
        self.ray_gun_button = Button(button_image=pygame.image.load('assets/shop/ray_gun_button.png'),
                                     position=(WIDTH - 592, HEIGHT - 278), button_font=self.menu_font,
                                     base_color=MENU_TEXT_COLOR, highlight_color=COLOR_SELECTED,
                                     text_input=str(self.player.weapons_list[6].cost), type='shop')
        self.coffee_button = Button(button_image=pygame.image.load('assets/shop/coffee_button.png'),
                                    position=(HALF_WIDTH - 40, HALF_HEIGHT - 160), button_font=self.menu_font,
                                    base_color=MENU_TEXT_COLOR, highlight_color=COLOR_SELECTED, text_input='100', type='shop')
        self.carrot_button = Button(button_image=pygame.image.load('assets/shop/carrot_button.png'),
                                    position=(HALF_WIDTH - 40, HALF_HEIGHT + 80), button_font=self.menu_font,
                                    base_color=MENU_TEXT_COLOR, highlight_color=COLOR_SELECTED, text_input='50', type='shop')

    # ******************************************************************************************************************

    def display(self):
        # general setup
        menu_text = self.menu_font.render('SHOP', False, MENU_TEXT_COLOR)
        menu_rect = menu_text.get_rect(center=(HALF_WIDTH, 16))
        mouse_pos = pygame.mouse.get_pos()
        self.display_surface.fill(ITEM_BOX_COLOR)
        self.display_surface.blit(menu_text, menu_rect)

        # update buttons
        for buttons in [self.shotgun_button, self.rifle_button, self.assault_rifle_button, self.machine_gun_button,
                        self.rail_gun_button, self.ray_gun_button, self.coffee_button, self.carrot_button]:
            buttons.highlight_color_change(mouse_pos)
            buttons.update(self.display_surface)

        x = self.display_surface.get_size()[0] - 16
        y = self.display_surface.get_size()[1] - 80
        gems_text_surface = self.player.ui_font.render(str(int(self.player.gems)), False, TEXT_COLOR)
        gems_text_rect = gems_text_surface.get_rect(topright=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, gems_text_rect.inflate(16, 16))
        self.display_surface.blit(gems_text_surface, gems_text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, gems_text_rect.inflate(16, 16), LINE_THICKNESS)
        self.display_surface.blit(self.player.gem_image, (gems_text_rect[0] - 100, gems_text_rect[1]))

        # check for input, ensure player has enough gems and that they don't already have that specific weapon
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.shotgun_button.check_input(mouse_pos):
                    if self.player.gems >= self.player.weapons_list[1].cost \
                            and self.player.weapon1 != self.player.weapons_list[1] \
                            and self.player.weapon2 != self.player.weapons_list[1]:
                        if self.player.current_weapon == self.player.weapon1:
                            self.player.weapon1 = self.player.weapons_list[1]
                        else:
                            self.player.weapon2 = self.player.weapons_list[1]

                        self.player.current_weapon = self.player.weapons_list[1]
                        print('Shotgun bought')
                        self.bought_sound.play()
                        self.player.gems -= self.player.weapons_list[1].cost

                elif self.rifle_button.check_input(mouse_pos):
                    if self.player.gems >= self.player.weapons_list[2].cost \
                            and self.player.weapon1 != self.player.weapons_list[2] \
                            and self.player.weapon2 != self.player.weapons_list[2]:
                        if self.player.current_weapon == self.player.weapon1:
                            self.player.weapon1 = self.player.weapons_list[2]
                        else:
                            self.player.weapon2 = self.player.weapons_list[2]

                        self.player.current_weapon = self.player.weapons_list[2]
                        print('Rifle bought')
                        self.bought_sound.play()
                        self.player.gems -= self.player.weapons_list[2].cost

                elif self.assault_rifle_button.check_input(mouse_pos):
                    if self.player.gems >= self.player.weapons_list[3].cost \
                            and self.player.weapon1 != self.player.weapons_list[3] \
                            and self.player.weapon2 != self.player.weapons_list[3]:
                        if self.player.current_weapon == self.player.weapon1:
                            self.player.weapon1 = self.player.weapons_list[3]
                        else:
                            self.player.weapon2 = self.player.weapons_list[3]

                        self.player.current_weapon = self.player.weapons_list[3]
                        print('Assault rifle bought')
                        self.bought_sound.play()
                        self.player.gems -= self.player.weapons_list[3].cost

                elif self.machine_gun_button.check_input(mouse_pos):
                    if self.player.gems >= self.player.weapons_list[4].cost \
                            and self.player.weapon1 != self.player.weapons_list[4] \
                            and self.player.weapon2 != self.player.weapons_list[4]:
                        if self.player.current_weapon == self.player.weapon1:
                            self.player.weapon1 = self.player.weapons_list[4]
                        else:
                            self.player.weapon2 = self.player.weapons_list[4]

                        self.player.current_weapon = self.player.weapons_list[4]
                        print('Machine gun bought')
                        self.bought_sound.play()
                        self.player.gems -= self.player.weapons_list[4].cost

                elif self.rail_gun_button.check_input(mouse_pos):
                    if self.player.gems >= self.player.weapons_list[5].cost \
                            and self.player.weapon1 != self.player.weapons_list[5] \
                            and self.player.weapon2 != self.player.weapons_list[5]:
                        if self.player.current_weapon == self.player.weapon1:
                            self.player.weapon1 = self.player.weapons_list[5]
                        else:
                            self.player.weapon2 = self.player.weapons_list[5]

                        self.player.current_weapon = self.player.weapons_list[5]
                        print('Rail gun bought')
                        self.bought_sound.play()
                        self.player.gems -= self.player.weapons_list[5].cost

                elif self.ray_gun_button.check_input(mouse_pos):
                    if self.player.gems >= self.player.weapons_list[6].cost \
                            and self.player.weapon1 != self.player.weapons_list[6] \
                            and self.player.weapon2 != self.player.weapons_list[6]:
                        if self.player.current_weapon == self.player.weapon1:
                            self.player.weapon1 = self.player.weapons_list[6]
                        else:
                            self.player.weapon2 = self.player.weapons_list[6]

                        self.player.current_weapon = self.player.weapons_list[6]
                        print('Ray gun bought')
                        self.bought_sound.play()
                        self.player.gems -= self.player.weapons_list[6].cost

                elif self.coffee_button.check_input(mouse_pos):
                    if self.player.gems >= 100:
                        print('coffee bought')
                        self.player.coffee_count += 1
                        self.bought_sound.play()
                        self.player.gems -= 100

                elif self.carrot_button.check_input(mouse_pos):
                    print('carrot bought')
                    if self.player.gems >= 50:
                        self.player.carrot_count += 1
                        self.bought_sound.play()
                        self.player.gems -= 50

        pygame.display.update()
        self.clock.tick(FPS)
