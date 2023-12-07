from Master import main
import random
from Master import coordinates
# # (0, 0, 0): Room.Spawn,


# # This creates a file to use as a Map files
def create_file():
    with open('GameMapCords.txt', 'w') as file:
        file.write("Hello World\n")


# # This adds a string to the file that I created
def append_file(text):
    with open("GameMapCords.txt", "a") as file:
        file.write(text)


# # This clears everything in the file
def clear_file():
    with open("GameMapCords.txt", "w"):
        pass


# # This reads the content of the file and returns it
def read_file():
    try:
        with open("GameMapCords.txt", "r")as file:
            content = file.read()
            # #print(content)
    except FileNotFoundError:
        print("File could not be found")
    except Exception as e:
        print(f"An error occurred: {e}")
    return content


# # This generates rooms to be used in the file
def generate_map():
    map_coordinates_list = []

    for _ in range(random.randint(2, 6)):
        map_coordinates = [0, 0, 0]

        i = random.randint(1, 4)
        if i == 1:
            map_coordinates[0] += 1
        elif i == 2:
            map_coordinates[0] -= 1
        elif i == 3:
            map_coordinates[1] += 1
        elif i == 4:
            map_coordinates[1] -= 1

        map_coordinates_list.append(map_coordinates)

    new_list = [[0, 0, 0]] + map_coordinates_list
    return new_list


# # This removes any duplicates in the generation
def remove_duplicates(original_list):
    unique_list = []
    for coordinate in original_list:
        if coordinate not in unique_list:
            unique_list.append(coordinate)
    return unique_list


# # This adds the identification to the room EG: [0, 0, 0,] -> ([0, 0, 0]: Room.Spawn)
def add_room(gen_coordinates):
    if gen_coordinates == [0, 0, 0]:
        new_tuple = (tuple(gen_coordinates), "Room.Spawn")
    else:
        new_tuple = (tuple(gen_coordinates), "Room.Crossroad")

    formatted_result = f"[{[new_tuple][0][0]}: {[new_tuple][0][1]}]"
    return formatted_result


# # This adds everything generated to the textfile
def add_to_text_file():
    gen_lis = remove_duplicates(generate_map())
    for x in range(len(gen_lis)):
        append_file(add_room(gen_lis[x]))
        if x < len(gen_lis) - 1:
            append_file("\n")
        elif x > len(gen_lis):
            clear_file()


# # This processes the file form one big string to a list
def process_file():
    file = read_file()
    coords = file.split("\n")
    return coords


clear_file()
add_to_text_file()

process = process_file()
# #print(process[1])
# #main()
