"""
 _______           __ ______ __                __               
|   |   |.-----.--|  |      |  |--.-----.----.|  |--.-----.----.
|       ||  _  |  _  |   ---|     |  -__|  __||    <|  -__|   _|
|__|_|__||_____|_____|______|__|__|_____|____||__|__|_____|__|  
                                            v1.0.0.0 by JTSage

Main Program

(c) 2021 JTSage.  MIT License.
"""

from tkinter import * # pylint: disable=unused-wildcard-import
from tkinter import ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import os
import lib.mod_checker_lib as mod_checker_lib
from lib.mod_checker_data import knownScriptOnlyMods, knownConflicts


mainConfigFile = ""
masterLog      = []
changeables    = {
	"mainConfigFile" : ""
}


# 
#  _______ _______ _____ __   _      _  _  _ _____ __   _ ______   _____  _  _  _
#  |  |  | |_____|   |   | \  |      |  |  |   |   | \  | |     \ |     | |  |  |
#  |  |  | |     | __|__ |  \_|      |__|__| __|__ |  \_| |_____/ |_____| |__|__|
#                                                                                
# 

root = Tk()
root.title("FS19 Mod Checker")
root.minsize(650, 500)


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save Log", command=lambda: mod_checker_lib.save_log(masterLog))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=lambda: about())
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


mainIconImage = PhotoImage(file = os.path.join(mod_checker_lib.resource_path("./lib/"), 'mcicon.png'))
root.iconphoto(False, mainIconImage)

n = ttk.Notebook(root)

tabConfig   = ttk.Frame(n, padding=(9,9,9,9)) # Config Tab
tabBroken   = ttk.Frame(n, padding=(9,9,9,9)) # Broken Mods / Files Tab
tabMissing  = ttk.Frame(n, padding=(9,9,9,9)) # Missing Mods Tab
tabConflict = ttk.Frame(n, padding=(9,9,9,9)) # Conflicts Tab
tabInactive = ttk.Frame(n, padding=(9,9,9,9)) # Inactive Mods Tab
tabUnused   = ttk.Frame(n, padding=(9,9,9,9)) # Active but Unused Mods Tab

n.add(tabConfig,   text='Configuration')
n.add(tabBroken,   text='Broken Mods')
n.add(tabMissing,  text='Missing Mods')
n.add(tabConflict, text='Possible Conflicts')
n.add(tabInactive, text='Inactive Mods')
n.add(tabUnused,   text='Active, Un-Used Mods')

n.pack(expand = 1, pady = (5,0), padx = 5, fill = "both")

root.update()



# 
#  _______  _____  __   _ _______ _____  ______      _______ _______ ______ 
#  |       |     | | \  | |______   |   |  ____         |    |_____| |_____]
#  |_____  |_____| |  \_| |       __|__ |_____|         |    |     | |_____]
#                                                                           
# 

tabConfig.columnconfigure(0, weight=1)
tabConfig.columnconfigure(1, minsize=root.winfo_width()/2)

ttk.Label(tabConfig, text="First, you need to point Mod Checker to your gameSettings.xml file" ).grid(column=0, columnspan=2, row=0, pady=6, sticky=(W,E))

ttk.Button(tabConfig, text="Load Settings", command=lambda: mod_checker_lib.load_main_config(changeables)).grid(column=0, row=1, columnspan=2, sticky=(W, E))

changeables["mainFileLabel"] = ttk.Label(tabConfig, text="Game Settings File: [not set]" )
changeables["mainFileLabel"].grid(column=0, columnspan=2, row=2, pady=6, sticky=(W,E))

ttk.Label(tabConfig, text="Next, click \"Check Mods\" to scan your collection" ).grid(column=0, columnspan=2, row=3, pady=6, sticky=(W,E))

processButton = ttk.Button(tabConfig, text="Check Mods", command=lambda: mod_checker_lib.process_files(masterLog, changeables))
processButton.state(['disabled'])
processButton.grid(column=0, row=4, columnspan=2, sticky=(W, E))

changeables["processButton"] = processButton

ttk.Label(tabConfig, text="Mods Found").grid(column=0, row=5, sticky=(E))
ttk.Label(tabConfig, text="Broken Mods").grid(column=0, row=6, sticky=(E))
ttk.Label(tabConfig, text="Folders Found").grid(column=0, row=7, sticky=(E))
ttk.Label(tabConfig, text="Missing Mods").grid(column=0, row=8, sticky=(E))

changeables["modLabels"] = {
	"found"   : ttk.Label(tabConfig, text="0", font='Helvetica 18 bold'),
	"broke"   : ttk.Label(tabConfig, text="0", font='Helvetica 18 bold'),
	"folder"  : ttk.Label(tabConfig, text="0", font='Helvetica 18 bold'),
	"missing" : ttk.Label(tabConfig, text="0", font='Helvetica 18 bold')
}
changeables["modLabels"]["found"].grid(column=1, row=5, sticky=(W))
changeables["modLabels"]["broke"].grid(column=1, row=6, sticky=(W))
changeables["modLabels"]["folder"].grid(column=1, row=7, sticky=(W))
changeables["modLabels"]["missing"].grid(column=1, row=8, sticky=(W))


for child in tabConfig.winfo_children(): 
	child.grid_configure(padx=5, pady=5)



# 
#  ______   ______  _____  _     _ _______ __   _      _______  _____  ______  _______
#  |_____] |_____/ |     | |____/  |______ | \  |      |  |  | |     | |     \ |______
#  |_____] |    \_ |_____| |    \_ |______ |  \_|      |  |  | |_____| |_____/ ______|
#                                                                                     
# 

ttk.Label(tabBroken, text="Broken Mods", font='Helvetica 12 bold').pack()
ttk.Label(tabBroken, text="These mods have been detected to be a possible problem.  ZIP Files or Folders with any non-alphanumeric character other than \"_\" will not be loaded by the game.  Mods that are not compressed as a ZIP file cannot be used in multiplayer games.  Finally, the mod folder should only contain mods, no other files.  Below, there is a list of problem files, and a suggested solution", wraplength = 600).pack(fill='x')



brokenCanvas    = Canvas(tabBroken)
brokenCanvasVSB = ttk.Scrollbar(tabBroken, orient="vertical", command=brokenCanvas.yview)
brokenFrame     = ttk.Frame(brokenCanvas, border=1, padding=(30,0))

brokenFrame.bind(
    "<Configure>",
    lambda e: brokenCanvas.configure(
        scrollregion=brokenCanvas.bbox("all")
    )
)

brokenCanvas.create_window((0, 0), window=brokenFrame, anchor="nw")

brokenCanvas.configure(yscrollcommand=brokenCanvasVSB.set)

brokenCanvas.pack(side="left", fill="both", expand=True)
brokenCanvasVSB.pack(side="right", fill="y")

def bf_on_mousewheel(event):
	brokenCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

def bf_bound_to_mousewheel(event):
    brokenCanvas.bind_all("<MouseWheel>", bf_on_mousewheel)

def bf_unbound_to_mousewheel(event):
    brokenCanvas.unbind_all("<MouseWheel>")

brokenFrame.bind('<Enter>', bf_bound_to_mousewheel)
brokenFrame.bind('<Leave>', bf_unbound_to_mousewheel)

# brokenTreeCols = ('Name','Type','Problem')

# brokenTree = ttk.Treeview(tabBroken, selectmode='browse', columns=brokenTreeCols, show='headings')
# brokenTree.pack(expand=True, side='left', fill='both', pady=(5,0))

# brokenTreeVSB = ttk.Scrollbar(tabBroken, orient="vertical", command=brokenTree.yview)
# brokenTreeVSB.pack(side='right', fill='y')

# brokenTree.configure(yscrollcommand=brokenTreeVSB.set)

# for col in brokenTreeCols:
# 	brokenTree.heading(col, text=col, command=lambda _col=col: \
# 				 treeview_sort_size_column(brokenTree, _col, False))

changeables["brokenFrame"] = brokenFrame



# 
#  _______ _____ _______ _______ _____ __   _  ______      _______  _____  ______  _______
#  |  |  |   |   |______ |______   |   | \  | |  ____      |  |  | |     | |     \ |______
#  |  |  | __|__ ______| ______| __|__ |  \_| |_____|      |  |  | |_____| |_____/ ______|
#                                                                                         
# 

ttk.Label(tabMissing, text="Missing Mods", font='Helvetica 12 bold').pack()
ttk.Label(tabMissing, text="The scanner failed to find the mods below, however they are referenced in one or more savegames. For mods that have not been purchased, this is usually harmless.  For mods you have purchased, missing the mod file could cost you in-game money.  To correct this, re-download the mod from where you originally got it and place it in the mod folder.", wraplength = 600).pack(fill='x')

missingTreeCols = ('Name','Title','Purchased','Savegame')

missingTree = ttk.Treeview(tabMissing, selectmode='browse', columns=missingTreeCols, show='headings')
missingTree.pack(expand=True, side='left', fill='both', pady=(5,0))

missingTree.column("#3", minwidth=0, width=75, stretch=NO) 
missingTree.column("#4", minwidth=0, width=100, stretch=NO) 

missingTreeVSB = ttk.Scrollbar(tabMissing, orient="vertical", command=missingTree.yview)
missingTreeVSB.pack(side='right', fill='y')

missingTree.configure(yscrollcommand=missingTreeVSB.set)

for col in missingTreeCols:
	missingTree.heading(col, text=col, command=lambda _col=col: \
				 treeview_sort_size_column(missingTree, _col, False))


changeables["missingTree"] = missingTree



# 
#  _______  _____  __   _ _______        _____ _______ _______      _______  _____  ______  _______
#  |       |     | | \  | |______ |        |   |          |         |  |  | |     | |     \ |______
#  |_____  |_____| |  \_| |       |_____ __|__ |_____     |         |  |  | |_____| |_____/ ______|
#                                                                                                  
# 
ttk.Label(tabConflict, text = "Possible Conflicts", font='Helvetica 12 bold').pack()
ttk.Label(tabConflict, text = "These mods were detected in your mod folder.  In some specific cases, they can cause conflicts with other mods, causing your game to either not work or behave strangely. This display is for informational purposes, and should not be taken a suggestion not to use anything listed here", wraplength=600).pack(fill='x')

ttk.Label(tabConflict, text = "\u2022 " + "This should not be taken as a suggestion that these mods do not work.", anchor='w').pack(pady=(20, 0), padx=(30,0), fill='x')
ttk.Label(tabConflict, text = "\u2022 " + "This is also not intended as a slight against the mod or author.", anchor='w').pack(padx=(30,0), fill='x')
ttk.Label(tabConflict, text = "\u2022 " + "Many (most) times these mods will work as intended.", anchor='w').pack(padx=(30,0), fill='x')
ttk.Label(tabConflict, text = "\u2022 " + "If you do experience in-game problems, this may be a good place to start testing.", anchor='w').pack(pady=(0,10), padx=(30,0), fill='x')

conflictCanvas    = Canvas(tabConflict)
conflictCanvasVSB = ttk.Scrollbar(tabConflict, orient="vertical", command=conflictCanvas.yview)
conflictFrame     = ttk.Frame(conflictCanvas, border=1, padding=(30,0))

conflictFrame.bind(
    "<Configure>",
    lambda e: conflictCanvas.configure(
        scrollregion=conflictCanvas.bbox("all")
    )
)

conflictCanvas.create_window((0, 0), window=conflictFrame, anchor="nw")

conflictCanvas.configure(yscrollcommand=conflictCanvasVSB.set)

conflictCanvas.pack(side="left", fill="both", expand=True)
conflictCanvasVSB.pack(side="right", fill="y")

def cf_on_mousewheel(event):
	conflictCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

def cf_bound_to_mousewheel(event):
    conflictCanvas.bind_all("<MouseWheel>", cf_on_mousewheel)

def cf_unbound_to_mousewheel(event):
    conflictCanvas.unbind_all("<MouseWheel>")

conflictFrame.bind('<Enter>', cf_bound_to_mousewheel)
conflictFrame.bind('<Leave>', cf_unbound_to_mousewheel)


changeables["conflictFrame"] = conflictFrame



# 
#  _____ __   _ _______ _______ _______ _____ _    _ _______      _______  _____  ______  _______
#    |   | \  | |_____| |          |      |    \  /  |______      |  |  | |     | |     \ |______
#  __|__ |  \_| |     | |_____     |    __|__   \/   |______      |  |  | |_____| |_____/ ______|
#                                                                                                
# 
ttk.Label(tabInactive, text="Inactive Mods", font='Helvetica 12 bold').pack()
ttk.Label(tabInactive, text="These mods are not activated in any of your savegames.  If you would like to save space, and perhaps speed up FS19 starting, you could remove some or all of these.", wraplength = 600).pack(fill='x')

inactiveTreeCols = ('Name','Size')

inactiveTree = ttk.Treeview(tabInactive, selectmode='browse', columns=inactiveTreeCols, show='headings')
inactiveTree.pack(expand=True, side='left', fill='both', pady=(5,0))

inactiveTree.column("#2", minwidth=0, width=100, stretch=NO, anchor='e') 

inactiveTreeVSB = ttk.Scrollbar(tabInactive, orient="vertical", command=inactiveTree.yview)
inactiveTreeVSB.pack(side='right', fill='y')

inactiveTree.configure(yscrollcommand=inactiveTreeVSB.set)

for col in inactiveTreeCols:
	inactiveTree.heading(col, text=col, command=lambda _col=col: \
				 treeview_sort_size_column(inactiveTree, _col, False))

changeables["inactiveTree"] = inactiveTree



# 
#  _     _ __   _ _     _ _______ _______ ______       _______  _____  ______  _______
#  |     | | \  | |     | |______ |______ |     \      |  |  | |     | |     \ |______
#  |_____| |  \_| |_____| ______| |______ |_____/      |  |  | |_____| |_____/ ______|
#                                                                                     
# 
ttk.Label(tabUnused, text="Active, Unused Mods", font='Helvetica 12 bold').pack()
ttk.Label(tabUnused, text="These mods are active in a savegame, but do not seem to be in use. If you do not plan on using them, you could possible remove them.  Please note that some script only or pre-requisite mods may appear here by mistake, so please use this list carefully.", wraplength = 600).pack(fill='x')


unusedTreeCols = ('Name','Title','Savegame','Size')
unusedTree = ttk.Treeview(tabUnused, selectmode='browse', columns=unusedTreeCols, show='headings')
unusedTree.pack(expand=True, side='left', fill='both', pady=(5,0))

unusedTree.column("#3", minwidth=0, width=120, stretch=NO)
unusedTree.column("#4", minwidth=0, width=100, stretch=NO, anchor='e') 

unusedTreeVSB = ttk.Scrollbar(tabUnused, orient="vertical", command=unusedTree.yview)
unusedTreeVSB.pack(side='right', fill='y')

unusedTree.configure(yscrollcommand=unusedTreeVSB.set)

for col in unusedTreeCols:
	unusedTree.heading(col, text=col, command=lambda _col=col: \
				 treeview_sort_size_column(unusedTree, _col, False))

changeables["unusedTree"] = unusedTree



# 
#  _______ ______   _____  _     _ _______
#  |_____| |_____] |     | |     |    |   
#  |     | |_____] |_____| |_____|    |   
#                                         
# 

def about() :
	aboutWindow = Toplevel(root)
  

	aboutWindow.title("About FS19 Mod Checker")
	aboutWindow.geometry("600x460")

	ttk.Label(aboutWindow, text="FS19 Mod Checker", font='Helvetica 18 bold').pack()

	ttk.Label(aboutWindow, text="This little program will take a look at your mod install folder and inform you of the following:", anchor = 'w', wraplength = 600).pack(fill = 'x', pady = 0, padx = (10,0))

	aboutBullets = [
		"If a mod file is named incorrectly and won't load in the game.",
		"If a mod is not properly zipped.",
		"If a mod is used in your save games, but does not appear to be installed.",
		"If a mod is not loaded or used in any of your save games",
		"If a mod is loaded but unused in your save games."
	]

	for thisBullet in aboutBullets:
		ttk.Label(aboutWindow, text="\u2022 " + thisBullet, anchor = 'w', wraplength = 520).pack(fill = 'x', pady = (5,0), padx = (40,0))	

	ttk.Label(aboutWindow, text="This program only offers suggestions, no files on your computer will be altered", font='Helvetica 9 bold', anchor='center', wraplength = 600).pack(fill = 'x', pady=(10,0) )

	MITLicenseText = "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."
	ttk.Label(aboutWindow, text=MITLicenseText, anchor = 'w', wraplength = 560).pack(fill = 'x', pady = (20,0), padx = (20,0))
	
	aboutWindow.bind('<Escape>', lambda x: aboutWindow.destroy())
	aboutWindow.iconphoto(False, mainIconImage)
	aboutWindow.focus_force()



# 
#  _______ _____ ______ _______       _______  _____         ______ __   _ _     _ _______
#  |______   |    ____/ |______          |    |     |       |_____/ | \  | |     | |  |  |
#  ______| __|__ /_____ |______ _____    |    |_____| _____ |    \_ |  \_| |_____| |  |  |
#                                                                                         
# 

def size_to_real_number(text) :
	try :
		num, ext = text.split()

		if ext == "B":
			return float(num)
		if ext == "Kb" :
			return float(num) * 1024
		if ext == "Mb" :
			return float(num) * 1024 * 1024
		if ext == "Gb" :
			return float(num) * 1024 * 1024 * 1024
	
	except ValueError :
		return text

	return text



# 
#  _______  ______ _______ _______       _______  _____   ______ _______
#     |    |_____/ |______ |______       |______ |     | |_____/    |   
#     |    |    \_ |______ |______ _____ ______| |_____| |    \_    |   
#                                                                       
# 

def treeview_sort_size_column(tv, col, reverse):
	if ( col == "Size" ) :
		l = [(size_to_real_number(tv.set(k, col)), k) for k in tv.get_children('')]
	else :
		l = [(tv.set(k, col), k) for k in tv.get_children('')]

	l.sort(reverse=reverse)

	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l): # pylint: disable=unused-variable
		tv.move(k, '', index)

	# reverse sort next time
	tv.heading(col, text=col, command=lambda _col=col: \
				 treeview_sort_size_column(tv, _col, not reverse))




# 
#  _______ _______ _____ __   _              _____   _____   _____ 
#  |  |  | |_____|   |   | \  |      |      |     | |     | |_____]
#  |  |  | |     | __|__ |  \_|      |_____ |_____| |_____| |      
#                                                                  
# 

root.mainloop()
