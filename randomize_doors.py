#Everything here is responsible for door randomization

import random
import os 
import json 
from utils import *

door_data = "/constants/doors.json"

def randomize_doors():
    #Grab all of the door data and put it in a list
    doors = json.load(open(door_data))
    door_list = list(doors.keys())


def write_data():
    '''
    Data writes consist of first writing the room number, then the spawn coordinates. This is because they are listed separately in the ROM.
    '''
    for x in range(len(door_list)):
        for y in doors[door_list[x]]["room_number"]:
            #writeBytesToFile(ROM, y, data, 1)
            print(y)
        for z in doors[door_list[x]]["spawn_coordinates"]:
            #writeBytesToFile(ROM, z + 6, data, 2)
            print(z)

