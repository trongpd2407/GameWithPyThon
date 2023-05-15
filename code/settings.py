# game setup
WIDTH = 1280	
HEIGTH = 720
FPS = 60
TILESIZE = 64

HITBOX_OFFSET = {
	'player': -26,
	'tree_rock': -35,
	'house': -35,
	'grass': -10,
	'invisible': 0}

#ui
BAR_HEIGTH = 20
HP_BAR_WIDTH = 200
MP_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/Font/NormalFont.ttf'
UI_FONT_SIZE = 18
#general color
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HP_COLOR = 'red'
MP_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

#weapons
weapon_data = {
    'sword': {'cooldown': 100, 'dame':15, 'graphic': 'graphics/Weapons/sword/full.png'},
    'lance': {'cooldown': 350, 'dame':25, 'graphic': 'graphics/Weapons/lance/full.png'},
    'axe': {'cooldown': 250 , 'dame':20, 'graphic': 'graphics/Weapons/axe/full.png'},
    'rapier': {'cooldown': 70, 'dame':10, 'graphic': 'graphics/Weapons/rapier/full.png'},
    'sai': {'cooldown': 130, 'dame':15, 'graphic': 'graphics/Weapons/sai/full.png'},
}
#magic
magic_data ={
    'flame' :{'strength':10, 'cost': 20, 'graphic':'graphics/Magic/flame/fire.png' },
    'heal' :{'strength':7, 'cost': 10, 'graphic':'graphics/Magic/heal/heal.png' }
}
#enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3,'cooldown': 400, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 200, 'is_death': 0},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'audio/attack/claw.wav','speed': 4,'cooldown': 300, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 300,'is_death' : 0},
	'spirit': {'health': 120,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 4,'cooldown': 600, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 180,'is_death' : 0},
	'bamboo': {'health': 150,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 3,'cooldown': 200, 'resistance': 3, 'attack_radius': 40, 'notice_radius': 150,'is_death' : 0}}