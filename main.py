import random
import json
open("saveStore", "r+")
running = True
previous_room = None
coordinates = [0, 0, 0]
inventory = {

}


# classes
class Items:

    class Stick:
        damage = 20
        break_chance = 25


class EnemyContainer:

    class Thing:
        damage = random.randint(1, 40)

class Room:

    class Spawn:
        move_options = ["NORTH"]
        enemy_chance = 0
        loot_chance = 0
        dialogues = [
            "Welcome",
            "Hello"
        ]

    class Crossroad:
        move_options = ["NORTH", "SOUTH", "EAST", "WEST"]
        enemy_chance = 15
        loot_chance = 15
        dialogues = [
            "You find yourself in a 4-way corridor",
            "w"
        ]

    class ChestDeadEnd:
        move_options = previous_room
        enemy_chance = 0
        loot_chance = 100
        dialogues = [
            "You find an empty room with a chest"
        ]

    class NSHallway:
        move_options = ["NORTH", "SOUTH"]
        enemy_chance = 15
        loot_chance = 5
        dialogues = [
            "You are in a hallway."
        ]

    class EWHallway:
        move_options = ["EAST", "WEST"]
        enemy_chance = 15
        loot_chance = 5
        dialogues = [
            "You are in a hallway."
        ]

    class Boss:
        move_options = []
        enemy_chance = 100
        enemies = [EnemyContainer.Thing]

        loot_chance = 100
        dialogues = [
            "big boss"
        ]
# map
# noinspection PyDictCreation
game_map = {
    (0, 0, 0): Room.Spawn,
    (0, 1, 0): Room.Crossroad,
    (1, 1, 0): Room.Crossroad,
    (0, 2, 0): Room.Boss
}


# eughhguh huughhh guhh hguuhhghh
def enter_room():
    new_room = game_map[tuple(coordinates)]
    return new_room


# var
current_room = enter_room()


# true or false for enemy or loot, returns true or false (e or l spawns)
def roll(enemy, loot):
    e_chance = current_room.enemy_chance
    l_chance = current_room.loot_chance
    rolled = random.randint(0, 100)
    if enemy:
        if e_chance > rolled:
            return True
        else:
            return False
    elif loot:
        if l_chance > rolled:
            return True
        else:
            return False


# creates list of move options in current room
def move_choice_list():
    listed = ""
    for i in current_room.move_options:
        listed += str(current_room.move_options.index(i) + 1) + ": " + str(i) + "\n"
    return listed


def move(mchoice):
    global previous_room
    mchoice = mchoice.upper()
    if mchoice in current_room.move_options:
        previous_room = enter_room()
        if mchoice == "NORTH":
            coordinates[1] += 1
        elif mchoice == "SOUTH":
            coordinates[1] += -1
        elif mchoice == "EAST":
            coordinates[0] += -1
        elif mchoice == "WEST":
            coordinates[0] += 1
        elif mchoice == "DOWN":
            coordinates[2] += -1
        elif mchoice == "UP":
            coordinates[2] += 1
        else:
            print("Invalid Direction! Type the direction you want to move in")


def main():
    global current_room
    global previous_room
    global coordinates
    while True:
        chosen_dialogue = random.choice(current_room.dialogues)
        print(chosen_dialogue)
        print(move_choice_list())
        chosen_move = input("Select direction to move:\n")
        move(chosen_move)

        current_room = enter_room()


main()