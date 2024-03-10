#Everything here is responsible for door randomization

import copy
import random
import os 
import json 
from utils import *

DOOR_DATA = "constants/doors.json"
ROOM_DATA = "constants/rooms.json"


def randomize_doors(ROM_file):

    def remove_available_door_from_sub_lists(chosen_door):
        if chosen_door in available_one_way_doors:
            available_one_way_doors.remove(chosen_door)

        if chosen_door in available_two_way_doors:
            available_two_way_doors.remove(chosen_door)

        if chosen_door in available_dead_end_one_way_doors:
            available_dead_end_one_way_doors.remove(chosen_door)

        if chosen_door in available_dead_end_two_way_doors:
            available_dead_end_two_way_doors.remove(chosen_door)

    #Grab all of the door data and put it in a dict
    DOORS = json.load(open(DOOR_DATA))
    #Generate keys list of all the door names so we have a way of indexing the DOORS dict if needed
    DOOR_LIST = list(DOORS.keys())

    #Do the same thing with the room data.
    #Room data is basically what doors are in which rooms
    ROOMS = json.load(open(ROOM_DATA))
    ROOM_LIST = list(ROOMS.keys())

    #Make a copy of the DOORS list. Doors will be deleted from this list as they are used.
    available_doors = copy.deepcopy(DOORS)

    #Split one way doors and two way doors into separate lists so they can be chosen based on current door type
    #Also do this with dead end doors, which will require 4 lists to sort them all.
    #These two lists will be for standard doors.
    available_one_way_doors = []
    available_two_way_doors = []

    #Dead end doors are doors that lead to a room with no way to progress further.
    #These are mostly bonus rooms which have chests in them and lead to nowhere else.
    available_dead_end_one_way_doors = []
    available_dead_end_two_way_doors = []

    '''
    #Sort every single door into these four lists
    for door_name in DOOR_LIST:

        #Find how many exits the next room has
        doors_in_next_room = DOORS[door_name]['next_room'][0]
        #Find if the door is linked to another door
        linked_to = DOORS[current_door]["linked_to"]

        #If door is linked to another door
        if linked_to:
            #If the next room the door leads into has one or less exit...
            if len(ROOMS[doors_in_next_room]['doors']) <= 1:
                available_dead_end_two_way_doors.append(door_name)
            #If the next room has more than one exit...
            else:
                available_two_way_doors.append(door_name)
        #If door is a one way door
        else:
            #If the next room has no exits (literally just the final room)
            if len(ROOMS[doors_in_next_room]['doors']) <= 0:
                available_dead_end_one_way_doors.append(door_name)
            #If the next room has more than zero exit...
            else:
                available_one_way_doors.append(door_name)
    '''

    #sort with no dead end checks
    for door_name, i in available_doors.items():
        if "linked_to" in i and i["linked_to"]:
            available_two_way_doors.append(door_name)
        else:
            available_one_way_doors.append(door_name)
    
    
    #This dictionary will be the finalized list of randomized doors
    doors_randomized = copy.deepcopy(DOORS)

    #This list determines what door will be randomized next, based on the next room of the previous door.
    #This is so all rooms are accessible.
    #Set the first door to be the first one in the queue.
    door_queue = [DOOR_LIST[0]]

    #List for keeping track of what rooms we already queued up.
    visited_rooms = set()

    #This list is used for keeping track of doors that were linked together instead of randomized.
    #If they were already linked, they need to be skipped in the for loop.
    is_linked = set()

    #This is the main randomization loop
    #Run this list until there are no more doors available
    while len(door_queue) > 0:

        #Set our current door. Mainly for code readability.
        current_door = door_queue[0]

        #If this door was already linked manually, skip the door
        if current_door in is_linked:
            door_queue.remove(current_door)
            continue

        #Find the door the current door is linked to
        linked_to = DOORS[current_door]["linked_to"]

        #Select a random door
        #Note: Do an if for "if total random" once this option is added, so that all doors can be chosen
        if linked_to:
            #Convert this to a string instead of a list element
            linked_to = linked_to[0]

            random_door = linked_to

            current_room = DOORS[current_door]["in_room"][0]
            random_current_room = DOORS[random_door]["in_room"][0]

            #Make sure that we do NOT select the door the current door is linked to.
            #Doing this can result in a door that takes you back to its entrance.

            #Also, if it is a two way, don't link with a door in the same room or else it will loop inside the room.
            while random_door == linked_to or current_room == random_current_room:
                random_door = random.choice(list((available_two_way_doors)))
                random_current_room = DOORS[random_door]["in_room"][0]
        elif not linked_to:
            random_door = random.choice(list((available_one_way_doors)))
            
        #Randomize the door
        print(f"{current_door} overwriting {random_door}")
        doors_randomized[current_door] = available_doors[random_door]
        remove_available_door_from_sub_lists(random_door)
        del available_doors[random_door]

        #Get what the next room will be when entering this door.
        random_next_room = DOORS[random_door]["next_room"][0]

        #If we have not yet queued up this room, add the doors in this room to the queue.
        if random_next_room not in visited_rooms:
            #Add future doors into the queue based on the upcoming room.
            for door in ROOMS[random_next_room]["doors"]:
                door_queue.append(door)
                #Add this room to the visited rooms list so it isn't checked again
                visited_rooms.add(random_next_room)
 
        #Check if the current door is normally a two-way door
        if linked_to:
            '''
            -Using a different variable name for linked_to because this part can get confusing
            -We will be writing the linked door data of the current door to the linked door
             data of the random door we got. This way the doors lead back to each other in-game.
            '''
            #The door linked to the current door we have in the loop
            door_data_to_write = linked_to
            #The door linked to the door we randomly rolled earlier
            door_data_to_edit = DOORS[random_door]["linked_to"][0]

            print(f"{door_data_to_edit} overwriting {door_data_to_write} (by link)")

            #Write the door data
            doors_randomized[door_data_to_edit] = available_doors[door_data_to_write]

            #Add the door we wrote to to the linked door list so we are sure not to overwrite it
            is_linked.add(door_data_to_edit)
            remove_available_door_from_sub_lists(door_data_to_write)
            del available_doors[door_data_to_write]

        #We are done working with this door, remove it from the queue
        door_queue.remove(current_door)

    #print(doors_randomized)


    # Randomization loop has ended
    # Start writing data to ROM

    door_list_randomized = list(doors_randomized.keys())

    for i in range(len(DOOR_LIST)):

        #Take the ROM location that we randomized
        rom_location = remove_brackets(doors_randomized[door_list_randomized[i]]['rom_location'])
        rom_location = int(rom_location, 16)

        #Write all of the data in the static strings into the new ROM locations
        for data in DOORS[DOOR_LIST[i]]["room_number"]:
            converted_data = hex_string_to_bytes(data)
            writeBytesToFile(ROM_file, converted_data, rom_location, 1)
        for data in DOORS[DOOR_LIST[i]]["spawn_coordinates"]:
            converted_data = hex_string_to_bytes(data)
            writeBytesToFile(ROM_file, converted_data, rom_location + 6, 4)