#Responsible for front-end UI and receiving user input

from tkinter import filedialog
from tkinter import *
import binascii
import random
import os
import sys
import shutil
import json 
from randomize_doors import * 

#Produce random seed number
def getRandomSeed():
	entry_seed_number.delete(0,END) 
	entry_seed_number.insert(END,str(random.randint(0,999999)))

#Function responsible for selecting ROM.
def openROM():
    filepath = filedialog.askopenfilename(filetypes=[("SNES / SFC ROM", (".sfc", ".smc", ".srm", ".swc")), ("All Files", "*")])
    if filepath != '':
        #filepath = convert_file_path_format(filepath)
        entry_path_to_rom.delete(0,END)
        entry_path_to_rom.insert(END,filepath)

#Open a file dialog and ask for where to put the randomized ROM.
def openDirectory():
    filepath = filedialog.askdirectory(initialdir = os.getcwd())
    if filepath != '':
        #filepath = convert_file_path_format(filepath)
        entry_path_to_output.delete(0,END)
        entry_path_to_output.insert(END,filepath)

def checkMirrorSettings(mirrorSetting):
	if mirrorSetting == "Don't Randomize":
		check_randomize_spoilerlog.deselect()
		check_randomize_spoilerlog.config(state=DISABLED)
	else:
		check_randomize_spoilerlog.config(state=NORMAL)
          
#Double check if everything is good to go before pulling the trigger.
def validateSettings():
	is_valid = True
	ROM_version = ""

	#if os.path.isfile("JSON\items.json") == False:
		#is_valid = False
		#warning_label.config(text="Error: items.json not found!", fg="#FF0000")
		
	#if os.path.isfile("constants/doors.json") == False:
	#	is_valid = False
	#	warning_label.config(text="Error: mirrors.json not found!", fg="#FF0000")
		
	#if os.path.isfile("JSON\minibosses.json") == False:
		#is_valid = False
		#warning_label.config(text="Error: minibosses.json not found!", fg="#FF0000")
	
	try:
		optionSeedNumber = int(entry_seed_number.get())
	except ValueError:
		is_valid = False
		warning_label.config(text="Error: The seed must only contain numbers.", fg="#FF0000")
	
	outputdir = entry_path_to_output.get()
	inputrom = entry_path_to_rom.get()

	if outputdir == "":
		is_valid = False
		warning_label.config(text="Error: No output directory specified.", fg="#FF0000")
	elif os.path.isdir(outputdir) == False:
		is_valid = False
		warning_label.config(text="Error: Output directory does not exist.", fg="#FF0000")

	if inputrom == "":
		is_valid = False
		warning_label.config(text="Error: No input ROM specified.", fg="#FF0000")
	elif os.path.isfile(inputrom) == False:
		is_valid = False
		warning_label.config(text="Error: Input ROM does not exist.", fg="#FF0000")
	else:
		#Start check of internal ROM header to see what type of ROM is being read
		filecheck = open(inputrom,'rb')
		
        #ROM header location
		filecheck.seek(0x7FC0)
		header_read = filecheck.read(18)

        #Check if a KSS ROM is being read
		if header_read != b'KIRBY SUPER DELUXE':
			warning_label.config(text="Error: File given is not a valid Kirby Super Star ROM.", fg="#FF0000")
        #If its KSS, check what KSS version it is
		else:
			#Location for region and revision data
			filecheck.seek(0x7FD9)
			version_read = filecheck.read(3)
			#Convert the hex read to a string so its easier to check
			version_read = binascii.hexlify(version_read).decode()
			
			#Determine game version. 
			#XX33YY ; XX = Region ; YY = Revision (33 does not change)
			match version_read:
				case "013300":
					ROM_version = "ENG"
				case "003300":
					ROM_version = "JP0"
				case "003301":
					ROM_version = "JP1"
				case "003302":
					# 003302 is JP 1.2, but since 1.1 and 1.2 share the same ROM locations, they will be grouped together
					ROM_version = "JP1"
				case _:
					pass

        #If everything is good to go, start ROM generation
		if ROM_version != "" and is_valid:
			#Put proper game title abbreviation based on region
			if ROM_version == "ENG":
				game_title = "KSS"
			else:
				game_title = "SDX"
			outputrom = outputdir + "/" + game_title + " GCO Randomizer " + str(optionSeedNumber) + ".sfc"
			#outputrom = convert_file_path_format(outputrom)
			generate_ROM(inputrom, outputrom, ROM_version)
			

def generate_ROM(original_ROM, randomized_ROM, ROM_version):
	seed_number = entry_seed_number.get()
	
	shutil.copyfile(original_ROM, randomized_ROM)
	KSS_ROM = open(randomized_ROM, 'rb+')
	
	random.seed(seed_number)
	print("Seed:", seed_number)
	iterations = 0
	check_if_pass = "ERROR"
	while check_if_pass == "ERROR":
		iterations += 1
		check_if_pass = randomize_doors(KSS_ROM, ROM_version)
	
	print("Done. Iterated through door generation", iterations, "times.")
	warning_label.config(text="ROM randomized. Enjoy your game!", fg="#000000")


# =========== Start of front end user interface code =================

#Basic window settings
random.seed()

tk = Tk()
tk.title("Kirby Super Star GCO Randomizer")
tk.resizable(False, False)

#tk.iconbitmap(resource_path("katamrando.ico"))

tk["padx"] = 14
tk["pady"] = 14

mirrorcheck = StringVar()
mirrorspoiler = IntVar()
itemcheck = StringVar()
minibosscheck = StringVar()
abilitycheck = StringVar()
musiccheck = StringVar()
palettecheck = IntVar()

mirrorcheck.set("Two-Way Doors Only")
itemcheck.set("Don't Randomize")
minibosscheck.set("Don't Randomize")
abilitycheck.set("Don't Randomize")
musiccheck.set("Don't Randomize")

language_var = StringVar()
language_var.set("English")  # Set default language

#Set up our frames.
frame_get_rom = Frame(tk)
frame_get_rom.pack()
frame_seed_number = Frame(tk)
frame_seed_number.pack()
# Create a container frame for frame_options1 and frame_options2
frame_options_container = Frame(tk)
frame_options_container.pack()

frame_options1 = Frame(frame_options_container, borderwidth=0, relief=RIDGE, padx=4, pady=4)
frame_options1.pack(side=LEFT, fill=BOTH, expand=True)  # Set side to LEFT to position it on the left, and fill=BOTH to make it expand horizontally

frame_options2 = Frame(frame_options_container, borderwidth=0, relief=RIDGE, padx=4, pady=4)
frame_options2.pack(side=LEFT, fill=BOTH, expand=True)  # Set side to LEFT to position it on the left, and fill=BOTH to make it expand horizontally

# Position frame_generate_rom at the bottom of frame_options_container
frame_generate_rom = Frame(tk)

frame_generate_rom.pack(side=BOTTOM, pady=10)  # Set side to BOTTOM and fill to X to position it at the bottom and make it expand horizontally, add some padding for aesthetic

#File paths section.
Label(frame_get_rom, text="Path to ROM:").grid(row=0,column=0,sticky=E)

entry_path_to_rom = Entry(frame_get_rom)
entry_path_to_rom.config(width=50)
entry_path_to_rom.grid(row=0,column=1)

get_file_button = Button(frame_get_rom, text="...", command=openROM)
get_file_button.grid(row=0,column=2)

Label(frame_get_rom, text="Output Path:").grid(row=1,column=0,sticky=E)

entry_path_to_output = Entry(frame_get_rom)
entry_path_to_output.config(width=50)
entry_path_to_output.grid(row=1,column=1)

get_directory_button = Button(frame_get_rom, text="...", command=openDirectory)
get_directory_button.grid(row=1,column=2)

#Random seed section.
Label(frame_seed_number, text="Seed:").grid(row=0,column=0,sticky=E,pady=6)

entry_seed_number = Entry(frame_seed_number)
entry_seed_number.config(width=10)
entry_seed_number.grid(row=0,column=1,sticky=E)
entry_seed_number.insert(END,str(random.randint(0,999999)))

random_seed_button = Button(frame_seed_number, text="?", command=getRandomSeed)
random_seed_button.grid(row=0,column=2)

#Options section.

randomize_doors = Checkbutton(frame_options1, text="Randomize Doors")
randomize_doors.grid(row=0, column=0, sticky=W)

check_randomize_mirrors = OptionMenu(frame_options1, mirrorcheck, "Two-Way Doors Only", "Shuffle By Type", "Total Random", command=checkMirrorSettings)
check_randomize_mirrors.configure(width=19)
check_randomize_mirrors.grid(row=1, column=0, sticky=W)

# Checkboxes for randomization settings
randomize_save_doors = Checkbutton(frame_options1, text="Randomize Save Doors")
randomize_save_doors.grid(row=2, column=0, sticky=W)

randomize_ability_doors = Checkbutton(frame_options1, text="Randomize Ability Doors")
randomize_ability_doors.grid(row=3, column=0, sticky=W)

randomize_switch_puzzle = Checkbutton(frame_options1, text="Randomize Switch Puzzle")
randomize_switch_puzzle.grid(row=4, column=0, sticky=W)

#Chest content
Label(frame_options2, text="Chests Contents:").grid(row=2, column=0, sticky=E)
check_randomize_items = OptionMenu(frame_options2, itemcheck, "Don't Randomize", "Shuffle Chests")
check_randomize_items.configure(width=19)
check_randomize_items.grid(row=2, column=1, sticky=W)

Label(frame_options2, text="Treasure Gold Value:").grid(row=3, column=0, sticky=E)
check_randomize_miniboss = OptionMenu(frame_options2, minibosscheck, "Don't Randomize", "Shuffle Values", "Randomize Values")
check_randomize_miniboss.configure(width=19)
check_randomize_miniboss.grid(row=3, column=1, sticky=W)


Label(frame_options2, text="Minibosses:").grid(row=4, column=0, sticky=E)
check_randomize_stands = OptionMenu(frame_options2, abilitycheck, "Don't Randomize", "Shuffle Minibosses", "Randomize Minibosses")
check_randomize_stands.configure(width=19)
check_randomize_stands.grid(row=4, column=1, sticky=W)

check_randomize_palettes = Checkbutton(frame_options2, text="Randomize Kirby Colors", variable=palettecheck)
check_randomize_palettes.grid(row=5, column=0, columnspan=2)

Label(frame_options2, text="Ability Statues:").grid(row=6, column=0, sticky=E)
check_randomize_stands = OptionMenu(frame_options2, abilitycheck, "Don't Randomize", "Shuffle Abilities", "Randomize Abilities")
check_randomize_stands.configure(width=19)
check_randomize_stands.grid(row=6, column=1, sticky=W)

Label(frame_options2, text="Music:").grid(row=7, column=0, sticky=E)
check_randomize_music = OptionMenu(frame_options2, musiccheck, "Don't Randomize", "Shuffle Music", "Randomize Music")
check_randomize_music.configure(width=19)
check_randomize_music.grid(row=7, column=1, sticky=W)

#Generate ROM section.
generate_button = Button(frame_generate_rom, text="Generate ROM",command=validateSettings)
generate_button.grid(row=0, pady=6)

warning_label = Label(frame_generate_rom, text="Please view the readme for more information on settings.")
warning_label.grid(row=1)

Label(frame_generate_rom, text="Kirby Super Star GCO Randomizer").grid(row=2)

english_radio = Radiobutton(frame_generate_rom, text="English", variable=language_var, value="English").grid(row=3, sticky=W)
japanese_radio = Radiobutton(frame_generate_rom, text="日本語", variable=language_var, value="Japanese").grid(row=3, sticky=E)

tk.mainloop()


#img = PhotoImage(file="gcoicon2x.png")
#Label(frame_get_rom, image=img).grid(row=0,column=3,sticky=EW)