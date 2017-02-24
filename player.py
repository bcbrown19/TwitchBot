# player objection creation and miscellaneous functions

from random import randint
import sql
from utils import *

RACES = ['human','elf','half-elf','dwarf','half-orc','kender', 'goblin', 'gnome']

CLASSES = ['fighter','mage', 'thief', 'cleric', 'paladin', 'ranger', 'sorcerer'
		'druid', 'peasant', 'bard', 'monk', 'barbarian']

class Player:
	"""docstring for Player"""

	def __init__(self, user, name, race, sex, _class, str, dex, con, wis, int, chr):
		self.user = user
		self.name = name
		self.race = race
		self.sex = sex
		self._class = _class
		self.str = 0 # 4d6 (top 3)
		self.dex = 0
		self.con = 0
		self.wis = 0
		self.int = 0
		self.chr = 0
		self.hp = 0
		self.xp = 0
		self.lvl = 0
		self.religion = None
		self.inventory = []

		# sql.create_player(user, name, race, sex, _class, str, dex, con, wis, wis, int, chr
		
	def calculate_hp(con):
		
		if con == 1:
			con_mod = -3
		elif con <= 3:
			con_mod = -2
		elif con <= 6:
			con_mod = -1
		elif con <= 14:
			con_mod = 0
		elif con == 15:
			con_mod = 1
		elif con >= 16:
			con_mod = 2
		self.hp = 8 + con_mod

	def add_hp(self, pts):
		self.hp += pts

	def is_dead(self):
		if self.hp > 0:
			return False
		else:
			return True

	def calculate_age(race, _class):
		base_age = 0
		num_of_dice = 0
		modifier_die = 0

		if race.lower() == 'human':
			base_age = 15	
			if _class.lower() in ['barbarian', 'thief', 'sorcerer', 'peasant']:
				num_of_dice = 1
				modifier = 4
			elif _class.lower() in ['bard', 'fighter', 'paladin', 'ranger']:
				num_of_dice = 1
				modifier = 6
			elif _class.lower() in ['cleric', 'druid', 'monk', 'wizard']:
				num_of_dice = 2
				modifier = 6

		elif race.lower() == 'dwarf':
			base_age = 40
			if _class.lower() in ['barbarian', 'thief', 'sorcerer', 'peasant']:
				num_of_dice = 3
				modifier = 6
			elif _class.lower() in ['bard', 'fighter', 'paladin', 'ranger']:
				num_of_dice = 5
				modifier = 6
			elif _class.lower() in ['cleric', 'druid', 'monk', 'wizard']:
				num_of_dice = 7
				modifier = 6

		elif race.lower() == 'elf':
			base_age = 110
			if _class.lower() in ['barbarian', 'thief', 'sorcerer', 'peasant']:
				num_of_dice = 4
				modifier = 6
			elif _class.lower() in ['bard', 'fighter', 'paladin', 'ranger']:
				num_of_dice = 6
				modifier = 6
			elif _class.lower() in ['cleric', 'druid', 'monk', 'wizard']:
				num_of_dice = 10
				modifier = 6

		elif race.lower() == 'gnome':
			base_age = 40
			if _class.lower() in ['barbarian', 'thief', 'sorcerer', 'peasant']:
				num_of_dice = 4
				modifier = 6
			elif _class.lower() in ['bard', 'fighter', 'paladin', 'ranger']:
				num_of_dice = 6
				modifier = 6
			elif _class.lower() in ['cleric', 'druid', 'monk', 'wizard']:
				num_of_dice = 9
				modifier = 6

		elif race.lower() == 'half-elf':
			base_age = 20
			if _class.lower() in ['barbarian', 'thief', 'sorcerer', 'peasant']:
				num_of_dice = 1
				modifier = 6
			elif _class.lower() in ['bard', 'fighter', 'paladin', 'ranger']:
				num_of_dice = 2
				modifier = 6
			elif _class.lower() in ['cleric', 'druid', 'monk', 'wizard']:
				num_of_dice = 3
				modifier = 6

		elif race.lower() == 'half-orc':
			base_age = 14
			if _class.lower() in ['barbarian', 'thief', 'sorcerer', 'peasant']:
				num_of_dice = 1
				modifier = 4
			elif _class.lower() in ['bard', 'fighter', 'paladin', 'ranger']:
				num_of_dice = 1
				modifier = 6
			elif _class.lower() in ['cleric', 'druid', 'monk', 'wizard']:
				num_of_dice = 2
				modifier = 6

		elif race.lower() == 'kender':
			base_age = 20
			if _class.lower() in ['barbarian', 'thief', 'sorcerer', 'peasant']:
				num_of_dice = 2
				modifier = 4
			elif _class.lower() in ['bard', 'fighter', 'paladin', 'ranger']:
				num_of_dice = 3
				modifier = 6
			elif _class.lower() in ['cleric', 'druid', 'monk', 'wizard']:
				num_of_dice = 4
				modifier = 6

		elif race.lower() == 'goblin':
			base_age = 14
			num_of_dice = 1
			modifier = 6
