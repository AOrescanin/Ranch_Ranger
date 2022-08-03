import pygame
import sys
from button import Button
from level import Level
from settings import *

# **********************************************************************************************************************

class Start:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load('assets/menu/menu_background.png').convert_alpha()
        self.text_font = pygame.font.Font(GAME_FONT, MENU_FONT_SIZE)
        self.click_sound = pygame.mixer.Sound('assets/menu/click.wav')
        self.play_sound = pygame.mixer.Sound('assets/menu/play.wav')

        # main menu setup
        self.menu_font = pygame.font.Font(GAME_FONT, TITLE_FONT_SIZE)
        self.menu_title_text = self.menu_font.render('RANCH RANGER', False, TEXT_COLOR)
        self.menu_title_rect = self.menu_title_text.get_rect(center=(TILE_SIZE * 5, TILE_SIZE))

        self.play_button = Button(button_image=pygame.image.load('assets/menu/button.png'),
                                  position=(TILE_SIZE * 5, TILE_SIZE * 3),
                                  button_font=self.text_font, base_color=MENU_TEXT_COLOR,
                                  highlight_color=COLOR_SELECTED, text_input='PLAY', type='menu')
        self.controls_button = Button(button_image=pygame.image.load('assets/menu/button.png'),
                               position=(TILE_SIZE * 5, TILE_SIZE * 5),
                               button_font=self.text_font, base_color=MENU_TEXT_COLOR,
                               highlight_color=COLOR_SELECTED, text_input='CONTROLS', type='menu')
        self.quit_button = Button(button_image=pygame.image.load('assets/menu/button.png'),
                                  position=(TILE_SIZE * 5, TILE_SIZE * 7),
                                  button_font=self.text_font, base_color=MENU_TEXT_COLOR,
                                  highlight_color=COLOR_SELECTED, text_input='QUIT', type='menu')

        # controls menu setup
        self.controls_title_text = self.menu_font.render('CONTROLS', False, TEXT_COLOR)
        self.controls_title_rect = self.controls_title_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE / 2))

        self.up_control_text = self.text_font.render('MOVE UP:      W', False, MENU_TEXT_COLOR)
        self.up_control_rect = self.up_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 1.6))
        self.left_control_text = self.text_font.render('MOVE LEFT:    A', False, MENU_TEXT_COLOR)
        self.left_control_rect = self.left_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 2.2))
        self.down_control_text = self.text_font.render('MOVE DOWN:    S', False, MENU_TEXT_COLOR)
        self.down_control_rect = self.down_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 2.8))
        self.right_control_text = self.text_font.render('MOVE RIGHT:   D', False, MENU_TEXT_COLOR)
        self.right_control_rect = self.right_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 3.4))

        self.shoot_control_text = self.text_font.render('SHOOT:        LEFT-CLICK', False, MENU_TEXT_COLOR)
        self.shoot_control_rect = self.shoot_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 4))
        self.reload_control_text = self.text_font.render('RELOAD:       R', False, MENU_TEXT_COLOR)
        self.reload_control_rect = self.reload_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 4.6))
        self.switch_control_text = self.text_font.render('SWITCH:       Q', False, MENU_TEXT_COLOR)
        self.switch_control_rect = self.switch_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 5.2))
        self.stab_control_text = self.text_font.render('MELEE:        RIGHT-CLICK', False, MENU_TEXT_COLOR)
        self.stab_control_rect = self.stab_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 5.8))
        self.drink_control_text = self.text_font.render('DRINK:        C', False, MENU_TEXT_COLOR)
        self.drink_control_rect = self.drink_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 6.4))
        self.eat_control_text = self.text_font.render('EAT:          V', False, MENU_TEXT_COLOR)
        self.eat_control_rect = self.eat_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 7))

        self.upgrade_menu_control_text = self.text_font.render('UPGRADE MENU: U', False, MENU_TEXT_COLOR)
        self.upgrade_menu_control_rect = self.upgrade_menu_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 7.6))
        self.upgrade_mvmt_control_text = self.text_font.render('UPGRADE MVMT: <- ->', False, MENU_TEXT_COLOR)
        self.upgrade_mvmt_control_rect = self.upgrade_mvmt_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 8.2))
        self.upgrade_control_text = self.text_font.render('UPGRADE:      SPACE', False, MENU_TEXT_COLOR)
        self.upgrade_control_rect = self.upgrade_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 8.8))
        self.shop_menu_control_text = self.text_font.render('SHOP MENU:    I', False, MENU_TEXT_COLOR)
        self.shop_menu_control_rect = self.shop_menu_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 9.4))
        self.buy_control_text = self.text_font.render('BUY:          CLICK', False, MENU_TEXT_COLOR)
        self.buy_control_rect = self.buy_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 10))
        self.back_control_text = self.text_font.render('BACK:         ESC', False, MENU_TEXT_COLOR)
        self.back_control_rect = self.back_control_text.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 10.6))

        # game over setup
        self.round_font = pygame.font.Font(GAME_FONT, UI_FONT_SIZE)
        self.game_over_font = pygame.font.Font(GAME_FONT, GAME_OVER_FONT_SIZE)
        self.game_over_text = self.game_over_font.render('GAME OVER', False, HEALTH_COLOR)
        self.game_over_text_rect = self.game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))

        self.play_again_button = Button(button_image=pygame.image.load('assets/menu/button.png'),
                                        position=(WIDTH/4, HEIGHT * 0.75),
                                        button_font=self.text_font, base_color=MENU_TEXT_COLOR,
                                        highlight_color=COLOR_SELECTED, text_input='PLAY AGAIN', type='menu')
        self.menu_button = Button(button_image=pygame.image.load('assets/menu/button.png'),
                                  position=(WIDTH / 2, HEIGHT * 0.75),
                                  button_font=self.text_font, base_color=MENU_TEXT_COLOR,
                                  highlight_color=COLOR_SELECTED, text_input='MAIN MENU', type='menu')
        self.quit_game_button = Button(button_image=pygame.image.load('assets/menu/button.png'),
                                       position=(WIDTH * 0.75, HEIGHT * 0.75),
                                       button_font=self.text_font, base_color=MENU_TEXT_COLOR,
                                       highlight_color=COLOR_SELECTED, text_input='QUIT', type='menu')

        self.play_sound = pygame.mixer.Sound('assets/menu/play.wav')

    # ******************************************************************************************************************

    def main_menu(self):
        # general setup
        pygame.display.set_caption('Main Menu')

        # draw the elements
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.menu_title_text, self.menu_title_rect)

        # loop for main menu
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for buttons in [self.play_button, self.controls_button, self.quit_button]:
                buttons.highlight_color_change(mouse_pos)
                buttons.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.check_input(mouse_pos):
                        self.play_sound.play()
                        self.play()
                    if self.controls_button.check_input(mouse_pos):
                        self.click_sound.play()
                        self.controls_menu()
                    if self.quit_button.check_input(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    # ******************************************************************************************************************

    def play(self):
        # general setup
        pygame.display.set_caption('Ranch Ranger')
        clock = pygame.time.Clock()
        level = Level()

        # game loop
        while True:
            if level.player.health <= 0:
                self.game_over(level.round)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        level.toggle_upgrade_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        level.toggle_shop_menu()

            level.run()
            pygame.display.update()
            clock.tick(FPS)

    # ******************************************************************************************************************

    def controls_menu(self):
        # general setup
        pygame.display.set_caption('Controls')

        # draw the elements
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.controls_title_text, self.controls_title_rect)
        self.screen.blit(self.up_control_text, self.up_control_rect)
        self.screen.blit(self.left_control_text, self.left_control_rect)
        self.screen.blit(self.down_control_text, self.down_control_rect)
        self.screen.blit(self.right_control_text, self.right_control_rect)
        self.screen.blit(self.shoot_control_text, self.shoot_control_rect)
        self.screen.blit(self.reload_control_text, self.reload_control_rect)
        self.screen.blit(self.switch_control_text, self.switch_control_rect)
        self.screen.blit(self.stab_control_text, self.stab_control_rect)
        self.screen.blit(self.drink_control_text, self.drink_control_rect)
        self.screen.blit(self.eat_control_text, self.eat_control_rect)
        self.screen.blit(self.upgrade_menu_control_text, self.upgrade_menu_control_rect)
        self.screen.blit(self.upgrade_mvmt_control_text, self.upgrade_mvmt_control_rect)
        self.screen.blit(self.upgrade_control_text, self.upgrade_control_rect)
        self.screen.blit(self.shop_menu_control_text, self.shop_menu_control_rect)
        self.screen.blit(self.buy_control_text, self.buy_control_rect)
        self.screen.blit(self.back_control_text, self.back_control_rect)

        # loop for options menu
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.click_sound.play()
                        self.main_menu()

            pygame.display.update()

    # ******************************************************************************************************************

    def game_over(self, round_num):
        # general setup
        pygame.display.set_caption('GAME OVER')
        round_text = self.round_font.render('YOU MADE IT TO ROUND ' + str(round_num - 1), False, HEALTH_COLOR)
        round_text_rect = round_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        # draw the elements
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.game_over_text, self.game_over_text_rect)
        self.screen.blit(round_text, round_text_rect)

        # loop for game over screen
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for buttons in [self.play_again_button, self.menu_button, self.quit_game_button]:
                buttons.highlight_color_change(mouse_pos)
                buttons.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_again_button.check_input(mouse_pos):
                        self.play_sound.play()
                        self.play()
                    if self.menu_button.check_input(mouse_pos):
                        self.click_sound.play()
                        self.main_menu()
                    if self.quit_game_button.check_input(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

# **********************************************************************************************************************

if __name__ == '__main__':
    start = Start()
    start.main_menu()
