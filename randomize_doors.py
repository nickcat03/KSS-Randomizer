#Everything here is responsible for door randomization

import copy
import random
import os 
import json 
from utils import *

DOOR_DATA = resource_path("constants/doors.json")
ROOM_DATA = resource_path("constants/rooms.json")


def randomize_doors(ROM_file):

    def sort_door_sub_lists():
        #Sort every single door into these four lists
        for door_name in DOOR_LIST:

            #Find how many exits the next room has
            next_room = DOORS[door_name]['next_room'][0]
            #Find if the door is linked to another door
            linked_to = DOORS[door_name]["linked_to"]

            #If door is linked to another door
            if linked_to:
                #If the next room the door leads into has more than one exit...
                if len(ROOMS[next_room]['doors']) > 1:
                    available_two_way_doors.append(door_name)
                #If the next room has one or less exit...
                else:
                    available_dead_end_two_way_doors.append(door_name)
            #If door is a one way door
            else:
                #If the next room has more than zero exit...
                if len(ROOMS[next_room]['doors']) > 0:
                    available_one_way_doors.append(door_name)
                #If the next room has no exits (literally just the final room)
                else:
                    available_dead_end_one_way_doors.append(door_name)   
        return

    def remove_available_door_from_sub_lists(chosen_door):
        print("Door to be removed:", chosen_door)
        if chosen_door in available_one_way_doors:
            available_one_way_doors.remove(chosen_door)

        if chosen_door in available_two_way_doors:
            available_two_way_doors.remove(chosen_door)

        if chosen_door in available_dead_end_one_way_doors:
            available_dead_end_one_way_doors.remove(chosen_door)

        if chosen_door in available_dead_end_two_way_doors:
            available_dead_end_two_way_doors.remove(chosen_door)
        
        return

    def generate_queue(door_data):

        temp_queue = []

        #Get what the next room will be when entering this door.
        random_next_room = DOORS[door_data]["next_room"][0]

        #If we have not yet queued up this room, add the doors in this room to the queue.
        if random_next_room not in rooms_queued:
            #Add future doors into the queue based on the upcoming room.
            for door in ROOMS[random_next_room]["doors"]:
                temp_queue.append(door)

            #Add this room to the visited rooms list so it isn't checked again
            rooms_queued.add(random_next_room)

            #Shuffle the doors we added so they aren't in a predictable order
            random.shuffle(temp_queue)

            #Add this shuffled list to the start of the actual door queue
            door_queue.extend(temp_queue)
        return

    #Grab all of the door data and put it in a dict
    DOORS = json.load(open(DOOR_DATA))
    #Generate keys list of all the door names so we have a way of indexing the DOORS dict if needed
    DOOR_LIST = list(DOORS.keys())

    #Do the same thing with the room data.
    #Room data is basically what doors are in which rooms
    ROOMS = json.load(open(ROOM_DATA))
    ROOM_LIST = list(ROOMS.keys())

    #Make a copy of the DOORS list. Doors will be deleted from this list as they are used.
    #available_doors = copy.deepcopy(DOORS)
    available_doors_in_room = copy.deepcopy(ROOMS)

    #Split one way doors and two way doors into separate lists so they can be chosen based on current door type
    #Also do this with dead end doors, which will require 4 lists to sort every single type.
    #These two lists will be for standard doors.
    available_one_way_doors = []
    available_two_way_doors = []

    #Dead end doors are doors that lead to a room with no way to progress further.
    #These are mostly bonus rooms which have chests in them and lead to nowhere else.
    available_dead_end_one_way_doors = []
    available_dead_end_two_way_doors = []

    sort_door_sub_lists()
    
    #This dictionary will be the finalized list of randomized doors
    doors_randomized = copy.deepcopy(DOORS)

    #This list determines what door will be randomized next, based on the next room of the previous door.
    #This is so all rooms are accessible.
    #Set the first door to be the first one in the queue.
    door_queue = [DOOR_LIST[0]]

    #List for keeping track of what rooms we already queued up.
    rooms_queued = set()

    #Keep track of all the rooms that have been linked so far.
    #The purpose of this list is to make sure that rooms don't loop around into each other.
    visited_rooms = set()
    all_rooms_visited = False

    #This list is used for keeping track of doors that were linked together instead of randomized.
    #If they were already linked, they need to be skipped in the for loop.
    already_processed = set()

    #This is the main randomization loop
    #Run this list until there are no more doors available
    while len(door_queue) > 0:

        #Set our current door. Mainly for code readability.
        current_door = door_queue[0]

        #If this door was already linked manually, skip the door
        if current_door in already_processed:
            door_queue.remove(current_door)
            continue

        #print("Available One Way doors:", available_one_way_doors)
        #print("Available two way doors:", available_two_way_doors)
        #print("Available dead end one ways:", available_dead_end_one_way_doors)
        #print("Available dead end two ways:", available_dead_end_two_way_doors)

        print("Current door in queue:", current_door)

        #print(rooms_queued)

        #Find the door the current door is linked to
        linked_to = DOORS[current_door]["linked_to"]

        #Find the current room and next room of the current door we are rolling for
        current_room = DOORS[current_door]["in_room"][0]
        next_room = DOORS[current_door]["next_room"][0]

        #Select a random door
        #Note: Do an if for "if total random" once this option is added, so that all doors can be chosen
        #Run this code if the current door is a two way door
        if linked_to:
            #Convert this to a string instead of a list element
            linked_to = linked_to[0]

            #Set up some variables for this upcoming while loop
            continue_checks = True
            infinite_loop_check = 0

            #Get all available two way doors and allow them to be chosen
            doors_to_choose_from = available_two_way_doors.copy()

            '''
            Check how many exits are available in the next upcoming room.
            If there is more than one exit in the room, choose from any two way door.
            If there is less than 2 exits (no branching paths in the room), only choose a non dead end two way door.
            If there are no more two way doors to choose from, combine the list so we aren't stuck without a door.
            '''
            #removed from the if for now, but if it plays nice I may add it back: len(available_doors_in_room[current_room]["doors"]) > 2 or 
            if len(available_two_way_doors) <= 0:
                #Add the dead end doors to the list of doors to be chosen
                doors_to_choose_from.extend(available_dead_end_two_way_doors)

                print("Less than one door in room", current_room)
            print(doors_to_choose_from)

            '''
            This while loop will make sure a new door is chosen under the following conditions: 
            1. Make sure that we do NOT select the door the current door is linked to. Doing this can result in a door that takes you back to its entrance.
            2. Do not set the randomly generated door as the current door. Otherwise nothing will have been randomized.
            3. Don't link with a door in the same room or else it may cause a loop inside the room.
            4. Don't connect to a room that we have already went to unless all rooms have been visited.
            '''
            while continue_checks:
                random_door = random.choice(list((doors_to_choose_from)))
                random_door_room = DOORS[random_door]["in_room"][0]

                #Check if all conditions apply
                if random_door != linked_to and random_door != current_door and random_door_room != next_room and (random_door_room not in visited_rooms or all_rooms_visited):
                    #If all of these checks pass, break out of the loop with the current door we rolled
                    continue_checks = False 
                else:
                    infinite_loop_check += 1

                #If we never end up finding a suitable door after 10 attempts, we will reset everything and run the randomizer again.
                #Normally this will only happen if we are stuck with a very small number of doors and cannot do anything else.
                if infinite_loop_check >= 10:
                    print("Infinite loop detected, aborting current randomization and trying again.")
                    return "ERROR"

        #Run this code if the current door is a one way door
        elif not linked_to:
            random_door = random.choice(list((available_one_way_doors)))

        #Because this door is being randomized, remove it from the doors available in the given room
        #This is so that a door is always guaranteed to be a non dead end if its the last door to be randomized in the room
        #print("Current room:", current_room)
        print("Removing", current_door, "from", current_room)
        available_doors_in_room[current_room]["doors"].remove(current_door)
            
        #After finalizing the randomization, apply the changes into the randomized dict.
        print(f"{current_door} overwriting {random_door}")
        doors_randomized[current_door] = DOORS[random_door]
        remove_available_door_from_sub_lists(random_door)

        #If things start to not work as intended, consider changing this to random_door instead
        #That may be the more logical approach.
        #(Do the same for the generate_queue function below as well)
        #Based on the next room of the current door, get the next doors in the queue
        generate_queue(current_door)
 
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
            doors_randomized[door_data_to_edit] = DOORS[door_data_to_write]

            #Add the door we wrote to to the processed list so we are sure not to overwrite it
            #Normally it would be more efficient to delete it from the queue, but it is more than likely the linked door is not a part of the queue yet.
            already_processed.add(door_data_to_edit)
            remove_available_door_from_sub_lists(door_data_to_write)

            #Remove the linked door that we just overwrote from the room dict so we know that the door is no longer available in the given room
            linked_room_of_random_door = DOORS[door_data_to_edit]["in_room"][0]
            print("Removing", door_data_to_edit, "from", linked_room_of_random_door, "(from link)")
            available_doors_in_room[linked_room_of_random_door]["doors"].remove(door_data_to_edit)

            #Based on the next room of the current door, get the next doors in the queue
            generate_queue(door_data_to_edit)

        #We are done working with this door, remove it from the queue
        door_queue.remove(current_door)

        #Failsafe in case for whatever reason our current door is repeated in the queue. Make sure not to overwrite it if it has already been written to.
        already_processed.add(current_door)

        #If the current room has yet to be visited, add the room to the visited rooms list
        if current_room not in visited_rooms:
            visited_rooms.add(current_room)

        #If all the rooms visited is the same length as the room list, mark all rooms visited as true
        if len(visited_rooms) >= len(ROOMS):
            print("ALL ROOMS VISITED")
            all_rooms_visited = True

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

    return "PASS"