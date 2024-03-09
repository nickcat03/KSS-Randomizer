from tkinter import filedialog
from tkinter import *
import random
import os
import sys
import json 
from randomize_doors import * 

#For OS dependencies between Windows and Linux, use if os.name == 'nt'

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Produce random seed number
def getRandomSeed():
	entry_seed_number.delete(0,END) 
	entry_seed_number.insert(END,str(random.randint(0,999999)))

#Function responsible for selecting ROM.
def openROM():
    filepath = filedialog.askopenfilename(filetypes=[("SNES / SFC ROM", (".sfc", ".smc", ".srm", ".swc")), ("All Files", "*")])
    if filepath != '':
        if os.name == 'nt':
            filepath = filepath.replace('/','\\')
        entry_path_to_rom.delete(0,END)
        entry_path_to_rom.insert(END,filepath)

#Open a file dialog and ask for where to put the randomized ROM.
def openDirectory():
    filepath = filedialog.askdirectory(initialdir = os.getcwd())
    if filepath != '':
        if os.name == 'nt':
            filepath = filepath.replace('/','\\')
        entry_path_to_output.delete(0,END)
        entry_path_to_output.insert(END,filepath)


# =========== Start of front end user interface code =================

#Basic window settings
program_window = Tk()
program_window.title("Kirby Super Star GCO Randomizer")
program_window.resizable(False, False)
#program_window.iconbitmap(resource_path("icon.ico"))
program_window["padx"] = 14
program_window["pady"] = 14


#Setup frames
frame_get_rom = Frame(program_window)
frame_get_rom.pack()
frame_seed_number = Frame(program_window)
frame_seed_number.pack()
frame_options = Frame(program_window, borderwidth=2, relief=RIDGE, padx=4, pady=4)
frame_options.pack()
frame_generate_rom = Frame(program_window)
frame_generate_rom.pack()


#File paths...
#Path to ROM
Label(frame_get_rom, text="Path to ROM:").grid(row=0,column=0,sticky=E)

entry_path_to_rom = Entry(frame_get_rom)
entry_path_to_rom.config(width=50)
entry_path_to_rom.grid(row=0,column=1)

get_file_button = Button(frame_get_rom, text="...", command=openROM)
get_file_button.grid(row=0,column=2)

#Output directory
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

#button_image = PhotoImage(file="")
random_seed_button = Button(frame_seed_number, text="?", command=getRandomSeed)
random_seed_button.grid(row=0,column=2)


#Keep the window open
program_window.mainloop()


#img = PhotoImage(file="gcoicon2x.png")
#Label(frame_get_rom, image=img).grid(row=0,column=3,sticky=EW)