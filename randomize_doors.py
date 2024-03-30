import copy
import random
import json
from utils import *

DOOR_DATA = resource_path(convert_file_path_format("constants/doors.json"))
ROOM_DATA = resource_path(convert_file_path_format("constants/rooms.json"))
print("door json:", DOOR_DATA)
print("room json:", ROOM_DATA)

def randomize_doors(ROM_file, ROM_version):
    def check_allowed_doors():
        # If the user doesn't want switch puzzle doors to be randomized, remove them everywhere
        if not randomize_switch_puzzle:
            DOORS.remove("Tree3_Reset1")
            DOORS.remove("Tree3_Reset2")
            DOORS.remove("Tree3_Reset3")
            DOORS.remove("Reset1_Tree3")
            DOORS.remove("Reset2_Tree3")
            DOORS.remove("Reset3_Tree3")
            ROOMS["Tree_Room3"]["doors"].remove("Tree3_Reset1")
            ROOMS["Tree_Room3"]["doors"].remove("Tree3_Reset2")
            ROOMS["Tree_Room3"]["doors"].remove("Tree3_Reset3")

    def sort_door_sub_lists():
        for door_name in DOOR_LIST:
            next_room = DOORS[door_name]['next_room'][0]
            if len(ROOMS[next_room]['doors']) > 1:
                available_pathing_doors.append(door_name)
            else:
                available_dead_end_doors.append(door_name)

        random.shuffle(available_pathing_doors)
        random.shuffle(available_dead_end_doors)

    def remove_door_from_sub_lists(chosen_door):
        if chosen_door in available_pathing_doors:
            available_pathing_doors.remove(chosen_door)
        if chosen_door in available_dead_end_doors:
            available_dead_end_doors.remove(chosen_door)
        if chosen_door in available_doors:
            available_doors.remove(chosen_door)

    def generate_queue(chosen_door):
        temp_queue = []
        random_next_room = DOORS[chosen_door]["next_room"][0]
        if random_next_room not in rooms_queued:
            for door in ROOMS[random_next_room]["doors"]:
                temp_queue.append(door)
            rooms_queued.add(random_next_room)
            random.shuffle(temp_queue)
            door_queue.extend(temp_queue)

    def write_data_to_ROM():
        for door in DOOR_LIST:
            print("Writing door data", doors_randomized[door])
            print("Address being written to:", DOORS[door])
            door_data = doors_randomized[door]
            rom_locations = DOORS[door]['rom_location'][ROM_version]
            #Most doors have one rom location, but some may have two if they span two tiles
            #Doors that have no rom locations are custom coordinates to link one-way doors
            for rom_location in rom_locations:
                rom_location = int(rom_location, 16)
                for data in door_data["room_number"]:
                    converted_data = hex_string_to_bytes(data, 1)
                    writeBytesToFile(ROM_file, converted_data, rom_location, 1)
                for data in door_data["spawn_coordinates"]:
                    converted_data = hex_string_to_bytes(data, 4)
                    writeBytesToFile(ROM_file, converted_data, rom_location + 6, 4)

    #This will be togglable later, setting to true permanently for testing purposes
    true_random = True
    
    #Will be togglable, this is for switch puzzle doors. They can be a bit weird.
    randomize_switch_puzzle = False

    # Load door and room data
    DOORS = json.load(open(DOOR_DATA))
    ROOMS = json.load(open(ROOM_DATA))

    # Remove any doors from the main DOORS list if they were toggled off by the user
    check_allowed_doors()

    DOOR_LIST = list(DOORS.keys())
    ROOM_LIST = list(ROOMS.keys())

    # Copy door data for manipulation
    available_doors_in_room = copy.deepcopy(ROOMS)

    # Initialize door lists
    available_doors = copy.deepcopy(DOOR_LIST)
    available_pathing_doors = []
    available_dead_end_doors = []

    sort_door_sub_lists()

    doors_randomized = copy.deepcopy(DOORS)
    door_queue = [DOOR_LIST[0]]
    rooms_queued = set()
    visited_rooms = set()
    all_rooms_visited = False
    already_processed = set()

    while door_queue:

        current_door = door_queue[0]

        print("Current door in queue:", current_door)

        if current_door in already_processed:
            door_queue.remove(current_door)
            continue

        linked_to = DOORS[current_door]["linked_to"]
        current_room = DOORS[current_door]["in_room"][0]
        next_room = DOORS[current_door]["next_room"][0]

        linked_to = linked_to[0]
        continue_checks = True
        infinite_loop_check = 0
        doors_to_choose_from = available_pathing_doors.copy()

        if len(available_pathing_doors) <= 0:
            doors_to_choose_from.extend(available_dead_end_doors)

        while continue_checks:
            random_door = random.choice(list(doors_to_choose_from))
            random_door_room = DOORS[random_door]["in_room"][0]

            print("random door:", random_door)

            # and (random_door_room not in visited_rooms or all_rooms_visited)
            if random_door != linked_to and random_door != current_door and random_door_room != next_room and random_door_room != current_room:
                continue_checks = False
            else:
                infinite_loop_check += 1

            if infinite_loop_check >= 10:
                print("Infinite loop detected, aborting current randomization and trying again.")
                return "ERROR"


        available_doors_in_room[current_room]["doors"].remove(current_door)

        print(f"{current_door} becomes {random_door}")
        doors_randomized[current_door] = DOORS[random_door]
        remove_door_from_sub_lists(random_door)
        generate_queue(random_door)

        #Code for linking doors together. Always ran if true random is enabled, or if the door is a two-way door
        if true_random or DOORS[current_door]["special"] != ["one-way"]:
            door_data_to_write = linked_to
            door_data_to_edit = DOORS[random_door]["linked_to"][0]
            doors_randomized[door_data_to_edit] = DOORS[door_data_to_write]
            already_processed.add(door_data_to_edit)
            remove_door_from_sub_lists(door_data_to_write)
            linked_room_of_random_door = DOORS[door_data_to_edit]["in_room"][0]
            print(f"{door_data_to_edit} becomes {door_data_to_write} (by link)")
            
            #Custom door data for one way doors are not listed in the room data, so check if the door is there first before removing it.
            if door_data_to_edit in available_doors_in_room[linked_room_of_random_door]["doors"]:
                available_doors_in_room[linked_room_of_random_door]["doors"].remove(door_data_to_edit)
            else:
                print(f"{door_data_to_edit} is most likely a custom door, so it was not removed from the list.")

            #generate_queue(door_data_to_edit)

        door_queue.remove(current_door)
        already_processed.add(current_door)

        if current_room not in visited_rooms:
            visited_rooms.add(current_room)

        if len(visited_rooms) >= len(ROOMS):
            print("ALL ROOMS VISITED")
            all_rooms_visited = True

        print("processed doors:", already_processed)


    print("Available pathing doors:", available_pathing_doors)
    print("Available dead end doors:", available_dead_end_doors)

    # Write data to ROM
    write_data_to_ROM()
    

    return "PASS"


        # current_door = door_queue[0]

        # print("Current door in queue:", current_door)

        # if current_door in already_processed:
        #     door_queue.remove(current_door)
        #     continue

        # linked_to = DOORS[current_door]["linked_to"]
        # current_room = DOORS[current_door]["in_room"][0]
        # next_room = DOORS[current_door]["next_room"][0]

        # if linked_to:
        #     linked_to = linked_to[0]
        #     continue_checks = True
        #     infinite_loop_check = 0
        #     doors_to_choose_from = available_two_way_doors.copy()

        #     if len(available_two_way_doors) <= 0:
        #         doors_to_choose_from.extend(available_dead_end_two_way_doors)

        #     while continue_checks:
        #         random_door = random.choice(list(doors_to_choose_from))
        #         random_door_room = DOORS[random_door]["in_room"][0]

        #         print("random door:", random_door)

        #         # and (random_door_room not in visited_rooms or all_rooms_visited)
        #         if random_door != linked_to and random_door != current_door and random_door_room != next_room and random_door_room != current_room:
        #             continue_checks = False
        #         else:
        #             infinite_loop_check += 1

        #         if infinite_loop_check >= 10:
        #             print("Infinite loop detected, aborting current randomization and trying again.")
        #             return "ERROR"

        # elif not linked_to:
        #     random_door = random.choice(list(available_one_way_doors))

        # available_doors_in_room[current_room]["doors"].remove(current_door)

        # print(f"{random_door} overwriting {current_door}")
        # doors_randomized[current_door] = DOORS[random_door]
        # remove_available_door_from_sub_lists(random_door)
        # generate_queue(random_door)

        # if linked_to:
        #     door_data_to_write = linked_to
        #     door_data_to_edit = DOORS[random_door]["linked_to"][0]
        #     doors_randomized[door_data_to_edit] = DOORS[door_data_to_write]
        #     already_processed.add(door_data_to_edit)
        #     remove_available_door_from_sub_lists(door_data_to_write)
        #     linked_room_of_random_door = DOORS[door_data_to_edit]["in_room"][0]
        #     print(f"{door_data_to_write} overwriting {door_data_to_edit} (by link)")
        #     available_doors_in_room[linked_room_of_random_door]["doors"].remove(door_data_to_edit)
        #     #generate_queue(door_data_to_edit)

        # door_queue.remove(current_door)
        # already_processed.add(current_door)

        # if current_room not in visited_rooms:
        #     visited_rooms.add(current_room)

        # if len(visited_rooms) >= len(ROOMS):
        #     print("ALL ROOMS VISITED")
        #     all_rooms_visited = True


