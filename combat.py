import random
import json


# Classes
class Fighter:
    def __init__(self, name="Fighter", health=0, attack=0):
        self.name = name
        self.max_health = health
        self.base_attack = attack
        self.health = self.max_health
        self.attack = self.base_attack
    
    def __str__(self):
        return self.name
    
    def is_alive(self) -> bool:
        if self.health < 0:
            self.health = 0
        return self.health > 0
        
    def hit_target(self) -> bool:
        return 15 < random.randint(1, 100)
    
    def crit_hit(self) -> bool:
        return 1 == random.randint(1, 10)
    
    def get_hit(self, damage):
        self.health -= damage
        self.is_alive()
    
    
class Player(Fighter):
    
    def __init__(self):
        health = self.load_health()
        super().__init__(name="You", health=health, attack=5)
        self.inventory = {
            "Weapon": None,
            "Consumables": []
        }
        self.backend_inventory = {
            "Weapon": None,
            "Consumables": []
        }
    
    def load_health(self):
        with open("PlayerStats.json", "r") as fp:
            Stats = json.load(fp)
            return Stats["Player"]["Health"]
    
    def hit(self, foe):
        crit = False
        
        if self.is_alive():
            if self.hit_target():
                damage = int(self.attack * random.uniform(0.9, 1.1))
                if self.crit_hit():
                    crit = True
                    damage = int(damage * 1.5)
                foe.get_hit(damage)
                print(f"{self.name} hit {foe} for {damage} damage")
                if crit is True:
                    print("Its a critical hit!")
                if self.backend_inventory["Weapon"]:
                    weapon = self.backend_inventory["Weapon"]
                    self.break_weapon(weapon)
            else:
                print(f"{self.name} missed!")
    
    def weapon_broken(self, weapon) -> bool:
        return weapon.break_chance > random.randint(0, 99)
    
    def break_weapon(self, weapon):
        if self.weapon_broken(weapon):
            print("Oh no! Your weapon broke!")
            self.attack -= weapon.attack
            self.inventory["Weapon"] = None
            self.backend_inventory["Weapon"] = None
    
    def equip_weapon(self, weapon):
        self.inventory["Weapon"] = weapon.name
        self.backend_inventory["Weapon"] = weapon
        self.update_stats(weapon)
    
    def add_consumable(self, food):
        self.inventory["Consumables"].append(food.name)
        self.backend_inventory["Consumables"].append(food)
    
    def eat(self, food):
        food.consume()
        print(f"You consumed a {food}")
        if food.healing > 0:
            print(f"\t +{food.healing} Hp \n\t Hp = {Player.health}")
        if food.atk_bonus > 0:
            print(f"\t +{food.atk_bonus} attack")
        self.inventory["Consumables"].remove(food.name)
        self.backend_inventory["Consumables"].remove(food)
    
    def update_stats(self, weapon):
        self.attack += weapon.attack


class Consumables:
    def __init__(self, name="Name", healing=0, atk_bonus=0):
        self.healing = healing
        self.atk_bonus = atk_bonus
        self.name = name
    
    def __str__(self):
        return self.name
    
    def consume(self):
        if self.healing > 0:
            Player.health += self.healing
            if Player.health > Player.max_health:
                Player.health = Player.max_health
        if self.atk_bonus > 0:
            Player.attack += self.atk_bonus


class HealingPotion(Consumables):
    def __init__(self):
        super().__init__("Healing Potion", 50)


class LesserHealingPotion(Consumables):
    def __init__(self):
        super().__init__("Lesser Healing Potion", 25)


class RagePotion(Consumables):
    def __init__(self):
        super().__init__(name="Rage Potion", atk_bonus=5)


class Weapons:
    def __init__(self, name="Name", attack=0, break_chance=0):
        self.attack = attack
        self.break_chance = break_chance
        self.name = name
    
    def __str__(self):
        return self.name


class Stick(Weapons):
    def __init__(self):
        super().__init__("Stick", 20, 25)


class Sword(Weapons):
    def __init__(self):
        super().__init__("Sword", 40, 10)


class Enemy(Fighter):
    def __init__(self, name, health, attack):
        super().__init__(name, health, attack)
        self.npc = True
    
    def hit(self, foe):
        crit = False
        
        if self.is_alive():
            if self.hit_target():
                damage = int(self.attack * random.uniform(0.9, 1.1))
                if self.crit_hit():
                    crit = True
                    damage = int(damage * 1.5)
                foe.get_hit(damage)
                print(f"{self.name} hit {foe} for {damage} damage")
                if crit is True:
                    print("Its a critical hit!")
            else:
                print(f"{self.name} missed!")


class Goblin(Enemy):
    def __init__(self):
        super().__init__("Goblin", 25, 5)
        
        
class Knight(Enemy):
    def __init__(self):
        super().__init__("Knight", 100, 25)


class Battle:
    def __init__(self, boss=False):
        self.boss = boss
    
    def fight(self, foe):
        self.print_player_stats()
        self.print_stats(foe)
        
        while Player.is_alive() and foe.is_alive():
            move = input(" Attack (A)\n Open inventory (I)\n Run (R)\n").upper()
            if move not in ("A", "I", "R"):
                print("Please enter a valid move")
            else:
                if move == "A":
                    Player.hit(foe)
                    if foe.is_alive():
                        foe.hit(Player)
                    self.print_player_stats()
                    self.print_stats(foe)
                    continue
                if move == "R":
                    if self.run_from_battle():
                        break
                    else:
                        if foe.is_alive():
                            foe.hit(Player)
                            self.print_player_stats()
                            self.print_stats(foe)
                        continue
                if move == "I":
                    self.show_inventory()
                continue
        
        if not foe.is_alive():
            print("**You successfully beat your opponent!** \n")
            self.save_player_health()
        if not Player.is_alive():
            print("**You died:(** \n")
            
    def save_player_health(self):
        with open("PlayerStats.json", "r") as fp:
            Stats = json.load(fp)
        
        Stats["Player"]["Health"] = Player.health
        
        with open("PlayerStats.json", "w") as fp:
            json.dump(Stats, fp)
        
    
    def print_player_stats(self):
        print(f"Your stats: \n \t Hp = {Player.health} \n \t Attack = {Player.attack}")
    
    def print_stats(self, entity):
        print(f"{entity} stats: \n \t Hp = {entity.health}")
        
    def show_inventory(self):
        for (i, item) in enumerate(Player.inventory["Consumables"], start=1):
            print(i, item)
        inventory_input = input("Use Item (Number)\nBack (B)\n").upper()
        try:
            inventory_input = int(inventory_input)
        except ValueError:
            return
        
        while inventory_input not in ["B"] + [*range(0, len(Player.inventory["Consumables"]) + 1)]:
            print("Please enter a valid option")
            inventory_input = input("Use Item (Number)\nBack (B)\n").upper()
        
        if inventory_input in [*range(0, len(Player.inventory["Consumables"]) + 1)]:
            food = Player.backend_inventory["Consumables"][int(inventory_input) - 1]
            Player.eat(food)
        else:
            if inventory_input == "B":
                return
        return
    
    def run_from_battle(self) -> bool:
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


class Mainloop:
    def __init__(self):
        self.pickup_weapon()
        self.pickup_potions()
        self.fight()
    
    def pickup_weapon(self):
        pickup = input("Do you want to pick up weapon (y/n) \n")
        if pickup == "y":
            Player.equip_weapon(Sword)

    def pickup_potions(self):
        potion = input("Do you want a potion (y/n) \n")
        if potion == "y":
            Player.add_consumable(HealingPotion)
            Player.add_consumable(LesserHealingPotion)

    def fight(self):
        fight = input("Do you want to fight Enemy (y/n) \n")
        if fight == "y":
            Battle.fight(foe=Knight)


Fighter = Fighter()
Stick = Stick()
Sword = Sword()
Goblin = Goblin()
Knight = Knight()
Player = Player()
Battle = Battle()
HealingPotion = HealingPotion()
LesserHealingPotion = LesserHealingPotion()
RagePotion = RagePotion()
BossBattle = BossBattle()
Mainloop = Mainloop()
