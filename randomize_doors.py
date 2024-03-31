import copy
import random
import json
from utils import *

DOOR_DATA = resource_path(convert_file_path_format("constants/doors.json"))
ROOM_DATA = resource_path(convert_file_path_format("constants/rooms.json"))
print("door json:", DOOR_DATA)
print("room json:", ROOM_DATA)

def randomize_doors(ROM_file, ROM_version):

    def check_options():
        to_remove = []
        for door in DOORS:
            special_attributes = DOORS[door]["special"]
            if (("switchpuzzle" in special_attributes and not randomize_switch_puzzle) or
            ("one-way" in special_attributes and not randomize_one_ways) or
            ("save" in special_attributes and not randomize_save_rooms)):
                room = DOORS[door]["in_room"][0]
                print("Removing", door, "from", room)
                if room in ROOMS and door in ROOMS[room]["doors"]:
                    ROOMS[room]["doors"].remove(door)
                to_remove.append(door)

        for door in to_remove:
            if door in DOORS:
                print("deleting", door)
                del DOORS[door]

    def sort_door_sub_lists():
        for door in DOOR_LIST:
            special_attributes = DOORS[door]["special"]
            next_room = DOORS[door]['next_room'][0]

            '''
            Ability is for checking if a room requires a specific ability in order to proceed, with no other way to progress otherwise. Mark it as a dead end if so.
            If a room has one door, put it in dead end list
            If a room has branching paths, put it in pathing door list
            '''

            if "ability" in special_attributes or len(ROOMS[next_room]['doors']) <= 1:
                available_dead_end_doors.append(door)
            else:
                available_pathing_doors.append(door)

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
        print("Adding doors in", random_next_room, "to queue")
        if random_next_room not in rooms_queued:
            for door in ROOMS[random_next_room]["doors"]:
                temp_queue.append(door)
            rooms_queued.add(random_next_room)
            random.shuffle(temp_queue)
            door_queue.extend(temp_queue)

    def get_valid_doors(doors_list, linked_to, current_room, visited_rooms, all_rooms_visited):
        valid_doors = []

        for random_door in doors_list:
            random_door_room = DOORS[random_door]["in_room"][0]
            random_door_next_room = DOORS[random_door]["next_room"][0]
            if (random_door != linked_to
                and random_door_next_room != current_room
                and ((random_door_next_room not in visited_rooms) or all_rooms_visited)): #random_door_room not in visited_rooms and 
                valid_doors.append(random_door)

        return valid_doors

    def write_data_to_ROM():
        for door in DOOR_LIST:
            #print("Writing door data", doors_randomized[door])
            #print("Address being written to:", DOORS[door])
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
    randomize_one_ways = False
    randomize_save_rooms = False

    # Load door and room data
    DOORS = json.load(open(DOOR_DATA))
    ROOMS = json.load(open(ROOM_DATA))

    # Delete doors from lists based on user options
    check_options()

    DOOR_LIST = list(DOORS.keys())
    ROOM_LIST = list(ROOMS.keys())

    # Copy door data for data manipulation
    available_doors_in_room = copy.deepcopy(ROOMS)

    # Initialize door lists
    available_doors = copy.deepcopy(DOOR_LIST)
    available_pathing_doors = []
    available_dead_end_doors = []

    sort_door_sub_lists()

    doors_randomized = copy.deepcopy(DOORS)
    not_processed = copy.deepcopy(DOOR_LIST)
    rooms_queued = set()
    visited_rooms = set()
    already_processed = set()

    def process_door_queue():
        while door_queue:

            current_door = door_queue[0]

            print("Current door in queue:", current_door)

            if current_door in already_processed:
                door_queue.remove(current_door)
                continue

            linked_to = DOORS[current_door]["linked_to"]
            current_room = DOORS[current_door]["in_room"][0]

            linked_to = linked_to[0]
            doors_to_choose_from = []
            
            doors_to_choose_from = get_valid_doors(available_pathing_doors, linked_to, current_room, visited_rooms, False)
            if len(doors_to_choose_from) <= 0:
                doors_to_choose_from = get_valid_doors(available_pathing_doors, linked_to, current_room, visited_rooms, True)

            if len(doors_to_choose_from) <= 0 or len(available_doors_in_room[current_room]["doors"]) > 1:
                doors_to_choose_from.extend(get_valid_doors(available_dead_end_doors, linked_to, current_room, visited_rooms, False))
                if len(doors_to_choose_from) <= 0:
                    doors_to_choose_from.extend(get_valid_doors(available_dead_end_doors, linked_to, current_room, visited_rooms, True))


            if len(doors_to_choose_from) > 0:
                random_door = random.choice(list(doors_to_choose_from))
                print("random door:", random_door)
            else:
                print("No more doors to choose from")
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
                not_processed.remove(door_data_to_edit)
                remove_door_from_sub_lists(door_data_to_write)

                #Remove the linked door from the ROOM list
                linked_room_of_random_door = DOORS[door_data_to_edit]["in_room"][0]
                print(f"{door_data_to_edit} becomes {door_data_to_write} (by link)")
                
                #Custom door data for one way doors are not listed in the room data, so check if the door is there first before removing it.
                if door_data_to_edit in available_doors_in_room[linked_room_of_random_door]["doors"]:
                    available_doors_in_room[linked_room_of_random_door]["doors"].remove(door_data_to_edit)
                else:
                    print(f"{door_data_to_edit} is most likely a custom door, so it was not removed from the list.")

                # This is probably redundant
                linked_door_room = DOORS[door_data_to_edit]["in_room"][0]
                if linked_door_room not in visited_rooms:
                    visited_rooms.add(linked_door_room)

            door_queue.remove(current_door)
            already_processed.add(current_door)
            not_processed.remove(current_door)

            if current_room not in visited_rooms:
                visited_rooms.add(current_room)


    door_queue = [available_doors[0], available_doors[2]]
    process_door_queue()

    print("Available pathing doors:", available_pathing_doors)
    print("Available dead end doors:", available_dead_end_doors)

    if len(already_processed) < len(DOOR_LIST):
        print("Some doors are impossible to access (Randomized", len(already_processed), "out of", len(DOOR_LIST), "doors).")
        return "ERROR"
    else:
        print("Processed", len(already_processed), "doors out of", len(DOOR_LIST), "doors")
        
    # Write data to ROM
    write_data_to_ROM()
    
    return "PASS"


