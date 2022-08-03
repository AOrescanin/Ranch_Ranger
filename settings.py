# game setup
WIDTH = 1920
HEIGHT = 1080
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2
MAP_SIZE = 4096
FPS = 60
TILE_SIZE = 64

# ui
LINE_THICKNESS = 4
ITEM_BOX_SIZE = 80
BAR_HEIGHT = 24
HEALTH_BAR_WIDTH = 240

# general colors
UI_BG_COLOR = '#333333'
UI_BORDER_COLOR = '#000009'
TEXT_COLOR = '#eeb462'
HEALTH_COLOR = '#cd7672'
ITEM_BOX_COLOR = '#534666'
MENU_TEXT_COLOR = '#DC8665'
COLOR_SELECTED = '#138086'

# fonts
GAME_FONT = 'assets/font/joystix.ttf'
CONSUMABLE_FONT_SIZE = 16
SHOP_FONT_SIZE = 24
UPGRADE_FONT_SIZE = 32
MENU_FONT_SIZE = 36
UI_FONT_SIZE = 48
TITLE_FONT_SIZE = 56
AMMO_FONT_SIZE = 64
GAME_OVER_FONT_SIZE = 80

# consumables
COFFEE_SPEED_BUFF = 1.3
CAFFEINATED_DURATION = 5000
CARROT_HEAL = 25

# cooldowns
STAB_COOLDOWN = 16
SWITCH_COOLDOWN = 16
CONSUME_COOLDOWN = 64
SELECTION_COOLDOWN = 333

#BULLET
BULLET_SPEED = 20

# weapons
weapon_data = {
	'Revolver': {'image': 'assets/weapons/revolver.png', 'position': (WIDTH - 180, HEIGHT - 85), 'magazine': 6,
				 'ammo_type': 'Normal', 'damage': 10, 'shooting_cooldown': 25, 'reload_cooldown': 200, 'cost': 0,
				 'bullet_image': 'assets/weapons/revolver_bullet.png', 'shot_sound': 'assets/weapons/revolver_shot.wav',
				 'reload_sound': 'assets/weapons/revolver_reload.wav'},
	'Shotgun': {'image': 'assets/weapons/shotgun.png', 'position': (WIDTH - 455, HEIGHT - 85), 'magazine': 7,
				'ammo_type': 'Buckshot', 'damage': 15, 'shooting_cooldown': 60, 'reload_cooldown': 220, 'cost': 25,
				'bullet_image': 'assets/weapons/shotgun_bullet.png','shot_sound': 'assets/weapons/shotgun_shot.wav',
				'reload_sound': 'assets/weapons/shotgun_reload.wav'},
	'Rifle': {'image': 'assets/weapons/rifle.png', 'position': (WIDTH - 525, HEIGHT - 85), 'magazine': 1,
			  'ammo_type': 'FMJ', 'damage': 8, 'shooting_cooldown': 60, 'reload_cooldown': 40, 'cost': 50,
			  'bullet_image': 'assets/weapons/rifle_bullet.png',	'shot_sound': 'assets/weapons/rifle_shot.wav',
			  'reload_sound': 'assets/weapons/rifle_reload.wav'},
	'Assault_Rifle': {'image': 'assets/weapons/ar.png', 'position': (WIDTH - 525, HEIGHT - 155), 'magazine': 30,
					  'ammo_type': 'Normal', 'damage': 12, 'shooting_cooldown': 10, 'reload_cooldown': 160, 'cost': 120,
					  'bullet_image': 'assets/weapons/ar_bullet.png', 'shot_sound': 'assets/weapons/ar_shot.wav',
					  'reload_sound': 'assets/weapons/ar_reload.mp3'},
	'Machine_Gun': {'image': 'assets/weapons/machine_gun.png', 'position': (WIDTH - 535, HEIGHT - 125), 'magazine': 20,
					'ammo_type': 'Normal', 'damage': 10, 'shooting_cooldown': 5, 'reload_cooldown': 140, 'cost': 150,
					'bullet_image': 'assets/weapons/machine_gun_bullet.png', 'shot_sound': 'assets/weapons/gun_shot.mp3',
					'reload_sound': 'assets/weapons/machine_gun_reload.wav'},
	'Rail_Gun': {'image': 'assets/weapons/rail_gun.png', 'position': (WIDTH - 470, HEIGHT - 115), 'magazine': 1000,
				 'ammo_type': 'Laser', 'damage': 25, 'shooting_cooldown': 100, 'reload_cooldown': 1, 'cost': 350,
				 'bullet_image': 'assets/weapons/rail_gun_laser.png', 'shot_sound': 'assets/weapons/rail_gun_shot.wav',
				 'reload_sound': 'assets/weapons/revolver_reload.wav'},
	'Ray_Gun': {'image': 'assets/weapons/ray_gun.png', 'position': (WIDTH - 405, HEIGHT - 140), 'magazine': 1000,
				'ammo_type': 'Laser', 'damage': 8, 'shooting_cooldown': 16, 'reload_cooldown': 1, 'cost': 500,
				'bullet_image': 'assets/weapons/ray_gun_laser.png',	'shot_sound': 'assets/weapons/ray_gun_shot.wav',
				'reload_sound': 'assets/weapons/revolver_reload.wav'}}

# enemies
enemy_data = {
	'normal': {'health': 15, 'speed': 4, 'damage': 15, 'exp': 5, 'gems': 3, 'attack_radius': 80},
	'strong': {'health': 25, 'speed': 3, 'damage': 30, 'exp': 10, 'gems': 5, 'attack_radius': 96},
	'fast': {'health': 10, 'speed': 7, 'damage': 10, 'exp': 7, 'gems': 4, 'attack_radius': 64}
}
