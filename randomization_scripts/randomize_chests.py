import copy
import random
import json
import sys
sys.path.append("..")
from utils import *

CHEST_DATA = resource_path(convert_file_path_format("constants/chests.json"))
print("chest json:", CHEST_DATA)

def randomize_treasures(ROM_file, ROM_version):

    CHESTS = json.load(open(CHEST_DATA))
    CHEST_LIST = list(CHESTS.keys())
    chest_locations_randomized = copy.deepcopy(CHEST_LIST)
    chest_items_randomized = copy.deepcopy(CHEST_LIST)
    chest_gold_randomized = copy.deepcopy(CHEST_LIST)

    #Randomize all the lists
    random.shuffle(chest_locations_randomized)
    random.shuffle(chest_items_randomized)
    random.shuffle(chest_gold_randomized)

    NUMBER_OF_CHESTS = len(CHEST_LIST)

    #All chest data is located in a single spot in ROM, so it can be indexed
    CHEST_DATA_TABLE = 0x0F4B1A

    for i in range(NUMBER_OF_CHESTS):

        writing_to = CHEST_LIST[i]

        #Location randomization (note that this is the location of the chests in the treasure menu)
        location_data = chest_locations_randomized[i]

        print("Overwriting location data", writing_to, "with", location_data)

        rom_location = CHESTS[writing_to]['rom_location'][ROM_version][0]
        rom_location = int(rom_location, 16)
        for data in CHESTS[location_data]["slot_number"]:
            converted_data = hex_string_to_bytes(data, 1)
            write_bytes_to_file(ROM_file, converted_data, rom_location)

        #Item randomization
        item_data = chest_items_randomized[i]

        print("Overwriting location data", writing_to, "with", item_data)

        rom_location = CHEST_DATA_TABLE + 4 + (i * 5)
        for data in CHESTS[item_data]["item_data"]:
            converted_data = hex_string_to_bytes(data, 1)
            write_bytes_to_file(ROM_file, converted_data, rom_location)

        #Gold randomization
        gold_data = chest_gold_randomized[i]

        print("Overwriting location data", writing_to, "with", gold_data)

        rom_location = CHEST_DATA_TABLE + (i * 5)
        for data in CHESTS[gold_data]["gold_amount"]:
            converted_data = hex_string_to_bytes(data, 4)
            write_bytes_to_file(ROM_file, converted_data, rom_location)