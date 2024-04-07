#Responsible for front-end UI and receiving user input

from tkinter import filedialog
from tkinter import *
import binascii
import random
import os
import sys
import shutil
import json 
from randomization_scripts.randomize_doors import * 
from randomization_scripts.randomize_chests import *

#initializing strings for text output. Blank for now because they will change depending on the selected language
seed_error = ""
no_input_rom = ""
input_nonexistent = ""
invalid_rom = ""
randomize_success = ""

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

def check_door_randomization():
	if randomize_doors_var.get() == 0:
		door_randomization_type.config(state="disabled")
		randomize_save_doors.config(state="disabled")
		randomize_ability_doors.config(state="disabled")
		randomize_switch_puzzle.config(state="disabled")
	else:
		door_randomization_type.config(state="normal")
		randomize_save_doors.config(state="normal")
		randomize_ability_doors.config(state="normal")
		check_door_settings(door_check.get())

def check_door_settings(selection):
	if selection == "Two-Way Doors Only" or selection == "片側ドアのみ":
		randomize_switch_puzzle.config(state="disabled")
	else:
		randomize_switch_puzzle.config(state="normal")

def update_language():
	global door_randomization_type, language, seed_error, no_input_rom, input_nonexistent, invalid_rom, randomize_success
	language = language_var.get()

	# OptionMenu widgets need to be completely destroyed and recreated in order for them to use the new labels properly
	door_randomization_type.destroy()

	# Assign all text in this if statement
	if language == "English":
		rom_path["text"] = "Path to ROM:"
		output_path["text"] = "Output Path:"
		seed_label["text"] = "Seed:"
		randomize_doors_select["text"] = "Randomize Doors:"
		door_options_list = ["Two-Way Doors Only", "Shuffle By Type", "Total Random"]
		randomize_save_doors["text"] = "Randomize Save Doors"
		randomize_ability_doors["text"] = "Randomize Ability Rooms"
		randomize_switch_puzzle["text"] = "Randomize Switch Puzzle"
		generate_button["text"] = "Generate ROM"
		warning_label["text"] = "Please view the ReadMe for more information on settings."
		status_label["text"] = "Kirby Super Star Great Cave Offensive Randomizer"
		seed_error = "Error: The seed must only contain numbers."
		no_input_rom = "Error: No input ROM specified."
		input_nonexistent = "Error: Input ROM does not exist."
		invalid_rom = "Error: File given is not a valid Kirby Super Star ROM."
		randomize_success = "ROM randomized. Enjoy your game!"
	
	elif language == "Japanese":
		rom_path["text"] = "ROMへのパス:"
		output_path["text"] = "出力パス:"
		seed_label["text"] = "シード:"
		randomize_doors_select["text"] = "ドアのランダム化："
		door_options_list = ["片側ドアのみ", "タイプ別にシャッフル", "完全ランダム"]
		randomize_save_doors["text"] = "セーブドアのランダム化"
		randomize_ability_doors["text"] = "コピー部屋のランダム化"
		randomize_switch_puzzle["text"] = "ランダムスイッチパズル"
		generate_button["text"] = "ROMの生成"
		warning_label["text"] = "設定の詳細についてはReadMeをご覧ください。"
		status_label["text"] = "星のカービィスーパーデラックス洞窟大作戦ランダマイザー"
		seed_error = "エラー： シードには数字のみを含める必要があります。"
		no_input_rom = "エラー： 入力ROMが指定されていません。"
		input_nonexistent = "エラー： 入力ROMが存在しません。"
		invalid_rom = "エラー： 指定されたファイルは有効な星のカービィのROMではありません。"
		randomize_success = "ROMランダム化。ゲームをお楽しみください!"

    # Recreate all OptionMenu elements
	door_randomization_type = OptionMenu(frame_options1, door_check, *door_options_list, command=check_door_settings)
	door_randomization_type.configure(width=19)
	door_randomization_type.grid(row=1, column=0, sticky=W)
	door_check.set(door_options_list[0])
	check_door_randomization()
	warning_label.config(fg="#000000")
          
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
		warning_label.config(text=seed_error, fg="#FF0000")
	
	outputdir = entry_path_to_output.get()
	inputrom = entry_path_to_rom.get()

	if outputdir == "":
		is_valid = False
		warning_label.config(text=no_input_rom, fg="#FF0000")
	elif os.path.isdir(outputdir) == False:
		is_valid = False
		warning_label.config(text=input_nonexistent, fg="#FF0000")

	if inputrom == "":
		is_valid = False
		warning_label.config(text=no_input_rom, fg="#FF0000")
	elif os.path.isfile(inputrom) == False:
		is_valid = False
		warning_label.config(text=input_nonexistent, fg="#FF0000")
	else:
		#Start check of internal ROM header to see what type of ROM is being read
		filecheck = open(inputrom,'rb')
		
        #ROM header location
		filecheck.seek(0x7FC0)
		header_read = filecheck.read(18)

        #Check if a KSS ROM is being read
		if header_read != b'KIRBY SUPER DELUXE':
			warning_label.config(text=invalid_rom, fg="#FF0000")
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
				#case "003300":
				#	ROM_version = "JP0"
				case "003301":
					ROM_version = "JP1"
				case "003302":
					# 003302 is JP 1.2, but since 1.1 and 1.2 share the same ROM locations, they will be grouped together
					ROM_version = "JP1"
				case _:
					is_valid = False
					warning_label.config(text=invalid_rom, fg="#FF0000")

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
	is_randomizing_doors = randomize_doors_var.get()
	door_randomization_method = door_check.get()
	
	shutil.copyfile(original_ROM, randomized_ROM)
	KSS_ROM = open(randomized_ROM, 'rb+')
	
	if is_randomizing_doors:
		save_doors = save_doors_var.get()
		ability_doors = ability_doors_var.get()
		switch_puzzle = switch_puzzle_var.get()

		#This option should be disabled by default if only two way doors are being randomized
		if door_randomization_method == "Two-Way Doors Only" or door_randomization_method == "片側ドアのみ":
			switch_puzzle = False

		random.seed(seed_number)
		print("Seed:", seed_number)
		iterations = 0
		check_if_pass = "ERROR"
		while check_if_pass == "ERROR":
			iterations += 1
			check_if_pass = randomize_doors(KSS_ROM, ROM_version, door_randomization_method, save_doors, ability_doors, switch_puzzle)
		print("Done. Iterated through door generation", iterations, "times.")

	randomize_treasures(KSS_ROM, ROM_version)
	
	warning_label.config(text=randomize_success, fg="#000000")


# =========== Start of front end user interface code =================

#Basic window settings
random.seed()

tk = Tk()
tk.title("Kirby Super Star GCO Randomizer")
tk.resizable(False, False)

#tk.iconbitmap(resource_path("katamrando.ico"))

tk["padx"] = 14
tk["pady"] = 14

door_check = StringVar()
mirrorspoiler = IntVar()
itemcheck = StringVar()
minibosscheck = StringVar()
abilitycheck = StringVar()
musiccheck = StringVar()
palettecheck = IntVar()
randomize_doors_var = IntVar()
save_doors_var = IntVar()
ability_doors_var = IntVar()
switch_puzzle_var = IntVar()

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

frame_options_container = Frame(tk)
frame_options_container.pack()

frame_options1 = Frame(frame_options_container, borderwidth=0, relief=RIDGE, padx=4, pady=4)
frame_options1.pack(side=LEFT, fill=BOTH, expand=True) 

frame_options2 = Frame(frame_options_container, borderwidth=0, relief=RIDGE, padx=4, pady=4)
frame_options2.pack(side=LEFT, fill=BOTH, expand=True) 

frame_generate_rom = Frame(tk)
frame_generate_rom.pack(pady=10)

frame_language = Frame(tk)
frame_language.pack(side=LEFT)


#File paths section.
rom_path = Label(frame_get_rom, text="Path to ROM:")
rom_path.grid(row=0,column=0,sticky=E)

entry_path_to_rom = Entry(frame_get_rom)
entry_path_to_rom.config(width=50)
entry_path_to_rom.grid(row=0,column=1)

get_file_button = Button(frame_get_rom, text="...", command=openROM)
get_file_button.grid(row=0,column=2)

output_path = Label(frame_get_rom, text="Output Path:")
output_path.grid(row=1,column=0,sticky=E)

entry_path_to_output = Entry(frame_get_rom)
entry_path_to_output.config(width=50)
entry_path_to_output.grid(row=1,column=1)

get_directory_button = Button(frame_get_rom, text="...", command=openDirectory)
get_directory_button.grid(row=1,column=2)

#Random seed section.
seed_label = Label(frame_seed_number, text="Seed:")
seed_label.grid(row=0,column=0,sticky=E,pady=6)

entry_seed_number = Entry(frame_seed_number)
entry_seed_number.config(width=10)
entry_seed_number.grid(row=0,column=1,sticky=E)
entry_seed_number.insert(END,str(random.randint(0,999999)))

random_seed_button = Button(frame_seed_number, text="?", command=getRandomSeed)
random_seed_button.grid(row=0,column=2)

#Options section.
randomize_doors_select = Checkbutton(frame_options1, text="Randomize Doors", variable=randomize_doors_var, command=check_door_randomization)
randomize_doors_select.grid(row=0, column=0, sticky=W)
randomize_doors_select.select()

door_randomization_type = OptionMenu(frame_options1, door_check, "Two-Way Doors Only", command=check_door_settings)
door_randomization_type.configure(width=19)
door_randomization_type.grid(row=1, column=0, sticky=W)

# Checkboxes for randomization settings
randomize_save_doors = Checkbutton(frame_options1, text="Randomize Save Doors", variable=save_doors_var)
randomize_save_doors.grid(row=2, column=0, sticky=W)

randomize_ability_doors = Checkbutton(frame_options1, text="Randomize Ability Doors", variable=ability_doors_var)
randomize_ability_doors.grid(row=3, column=0, sticky=W)
randomize_ability_doors.select()

randomize_switch_puzzle = Checkbutton(frame_options1, text="Randomize Switch Puzzle", variable=switch_puzzle_var, state="disabled")
randomize_switch_puzzle.grid(row=4, column=0, sticky=W)

#Commenting these out until they are actually finished
'''
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
'''

#Generate ROM section.
generate_button = Button(frame_generate_rom, text="Generate ROM",command=validateSettings)
generate_button.grid(row=0, pady=6)

warning_label = Label(frame_generate_rom, text="Please view the ReadMe for more information on settings.")
warning_label.grid(row=1)

status_label = Label(frame_generate_rom, text="Kirby Super Star GCO Randomizer")
status_label.grid(row=2)

english_radio = Radiobutton(frame_language, text="English", variable=language_var, value="English", command=update_language).grid(row=0, column=0)
japanese_radio = Radiobutton(frame_language, text="日本語", variable=language_var, value="Japanese", command=update_language).grid(row=0, column=1)

update_language()
tk.mainloop()

#img = PhotoImage(file="gcoicon2x.png")
#Label(frame_get_rom, image=img).grid(row=0,column=3,sticky=EW)