import random
import json
open("saveStore", "r+")
running = True
previous_room = None
coordinates = [0, 0, 0]
inventory = {

}


# classes
class Player:
    def __init__(self, health=100, attack=5):
        self.max_health = health
        self.base_attack = attack
        self.health = self.max_health
        self.attack = self.base_attack
        self.name = "You"

    def __str__(self):
        return self.name

    def is_alive(self) -> bool:
        if self.health < 0:
            self.health = 0
        return self.health > 0

    def hit(self, foe):
        if self.is_alive():
            damage = self.attack
            foe.get_hit(damage)
            print(f"{self.name} hit {foe} for {damage} damage")
            print(f"\t {foe} Hp = {foe.health}")
            try:
                self.break_weapon(inventory["Weapon"])
            except KeyError:
                return

    def get_hit(self, damage):
        self.health -= damage
        self.is_alive()

    def weapon_broken(self, weapon) -> bool:
        return weapon.break_chance > random.randint(0, 99)

    def break_weapon(self, weapon):
        if self.weapon_broken(weapon):
            print("Oh no! Your weapon broke!")
            self.attack -= weapon.attack
            del inventory["Weapon"]

    def equip_weapon(self, weapon):
        inventory["Weapon"] = weapon
        self.update_stats(weapon)

    def update_stats(self, weapon):
        self.attack += weapon.attack


class Weapons:
    def __init__(self, attack=0, break_chance=0):
        self.attack = attack
        self.break_chance = break_chance


class Stick(Weapons):
    def __init__(self):
        super().__init__(20, 25)


class Sword(Weapons):
    def __init__(self):
        super().__init__(40, 100)


class Enemy(Player):
	def __init__(self, name, health, attack):
		super().__init__(health, attack)
		self.name = name

	def __str__(self):
		return self.name


class Goblin(Enemy):
	def __init__(self):
		super().__init__("Goblin", 50, random.randint(1, 40))


class Battle:
	def __init__(self, boss=False):
		self.boss = boss

	def fight(self, foe):

		while Player.is_alive() and foe.is_alive():
			self.print_stats(Player)
			self.print_stats(Goblin)
			move = input("Attack (A) \n Run (R)\n").upper()
			if move not in ("A", "R"):
				print("Please enter a valid move")
			else:
				if move == "A":
					Player.hit(foe)
					if foe.is_alive():
						foe.hit(Player)
					self.print_stats(Player)
					continue
				if move == "R":
					if self.run_from_batte():
						break
					else:
						continue
		if not foe.is_alive():
			print("**You successfully beat your opponent!** \n")
		if not Player.is_alive():
			print("**You died:(** \n")

	def print_stats(self, entity):
		print(f"{entity} stats: \n \t Hp = {entity.health} \n \t Attack = {entity.attack} \n")

	def run_from_batte(self) -> bool:
		if self.boss is True:
			print("Cant run from a boss battle!")
			return False
		else:
			runaway_chance = random.randint(1, 5)
			if runaway_chance != 1:
				print("You ran away from battle!")
				return True
			else:
				print("You tried to run away but were unsuccessful")
				return False


class BossBattle(Battle):
	def __init__(self):
		super().__init__(boss=True)


class Game:
	def __init__(self):
		self.pickup_weapon()

	def pickup_weapon(self):
		pickup = input("Do you want to pick up weapon (y/n) \n")
		if pickup == "y":
			Player.equip_weapon(Sword)
		fight = input("Do you want to fight Goblin (y/n) \n")
		if fight == "y":
			BossBattle.fight(foe=Goblin)


Stick = Stick()
Sword = Sword()
Goblin = Goblin()
Player = Player()
Battle = Battle()
BossBattle = BossBattle()
Game = Game()

