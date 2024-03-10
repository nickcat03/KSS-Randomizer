#Everything here is responsible for door randomization

import random
import os 
import json 
from utils import *

door_data = "constants/doors.json"

def randomize_doors(ROM_file):
    #Grab all of the door data and put it in a list
    doors = json.load(open(door_data))
    door_list = list(doors.keys())

    #Initialize blank lists for where all of our door shuffling will go
    #this list will be the final list that will be sent to the ROM
    door_list_randomized = []
    #for keeping track of what door is up next. Start the list with the first door
    door_queue = [door_list[0]]
    #for keeping track of the doors that are already finished
    already_randomized = []
    #two separate lists to sort the door types
    one_way_door_list = []
    two_way_door_list = []

    #temp code
    for i in range(len(door_list)):
        # Select a random door to swap with
        swap_door_index = random.randint(0, len(door_list) - 1)

        # Swap the ROM locations between the current door and the randomly selected door
        doors[door_list[i]]["rom_location"], doors[door_list[swap_door_index]]["rom_location"] = \
            doors[door_list[swap_door_index]]["rom_location"], doors[door_list[i]]["rom_location"]
    
    #write data to rom
    for i in range(len(door_list)):

        rom_location = removeBrackets(doors[door_list[i]]['rom_location'])
        rom_location = int(rom_location, 16)

        for data in doors[door_list[i]]["room_number"]:
            converted_data = hex_string_to_bytes(data)
            writeBytesToFile(ROM_file, converted_data, rom_location, 1)
        for data in doors[door_list[i]]["spawn_coordinates"]:
            converted_data = hex_string_to_bytes(data)
            writeBytesToFile(ROM_file, converted_data, rom_location + 6, 4)


    '''
    #Sort the door types into their own separate lists
    for i in door_list:
            if doors[i]['type'] == 1:
                two_way_door_list.append(i)
            else:
                one_way_door_list.append(i)

    #Now randomize them
    random.shuffle(one_way_door_list)
    random.shuffle(two_way_door_list)


    #However, the doors need to be sorted due to two-way doors needing to be linked
    #Run this loop until we sort through all the doors
    while len(door_queue) > 0:
        #set variable so it's easier to reference
        current_door = door_queue[0]

        if current_door in door_list:
            #set index as variable so it's easier to reference
            current_door_index = door_list.index(current_door)

            #Continue through this loop until we are certain the door has been randomized
            certainly_randomized = False
            while certainly_randomized == False:
                already_checked = 0

                #This is ran for two way doors
                if doors[current_door]['type'] == 1:
                    #If the door is a two way and the two way list is empty, pass it off as checked
                    if len(one_way_door_list) <= 0 or len(two_way_door_list) <= 0:
                        certainly_randomized = True
                    elif not current_door in already_randomized:
                        already_randomized.append(current_door)

                        #Run if the two way door list isn't empty
                        if len(two_way_door_list) > 0:
                            linked_door = find_linked_door(current_door)
                            while two_way_door_list[0] == linked_door:
                                random.shuffle(two_way_door_list)
                            for i in doors[two_way_door_list[0]]['exits']:
                                if not i in already_randomized:
                                    door_queue.append()
                            
                            #Make sure two-way doors link together
                            matching_index = door_list.index(find_linked_door(two_way_door_list[0]))
                            current_linked_door = find_linked_door(current_door)

                            door_list_randomized[current_door_index] = two_way_door_list[0]
                            door_list_randomized[matching_index] = current_linked_door
                            already_randomized.append(matching_index)

                            if current_linked_door in two_way_door_list:
                                two_way_door_list.remove(current_linked_door)
                            del two_way_door_list[0]

                #This is ran for one way doors
                else:
                    if len(one_way_door_list) > 0:
                        for i in doors[one_way_door_list[0]]['exits']:
                            if not i in already_randomized:
                                door_queue.append(i)

                        door_list_randomized[current_door_index] = one_way_door_list[0]
                        del one_way_door_list[0]
                        
        # If the door isn't scheduled to be randomized, mark it as randomized, but don't touch door_list_randomized
        else:
            if not current_door in already_randomized:
                already_randomized.append(current_door)
                for i in doors[current_door]['exits']:
                    if not i in already_randomized:
                        door_queue.append(i)
        
        door_queue.remove(current_door)

        if len(door_queue) <= 0:
            for i in range(len(door_list_randomized)):
                if door_list_randomized[i] == "NULL":
                    already_randomized.remove(door_list[i])
                    print("ERROR: FOUND NULL")
                door_queue.append(door_list[i])
'''







                

    def find_linked_door(string):
        underscore = string.find("_")
        return string[underscore + 1 : len(string)] + "_" + string[0 : underscore]




