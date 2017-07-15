import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk

import multiprocessing, atexit, logging			#Official modules	
import headerContent as header
import mainContent, configuration, handshake	#Project modules
from logger import log01						#Logger


BACKGROUND_COLOR = "#000"
FOREGROUND_COLOR = "#FFF"

class Application(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,bg=BACKGROUND_COLOR)
		self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
		self.optionWidgets()
		self.createWidgets()

	def optionWidgets(self):
		self.option_add("*Background",BACKGROUND_COLOR)
		self.option_add("*Foreground",FOREGROUND_COLOR)

	def createWidgets(self):
		top=self.winfo_toplevel()
		top.columnconfigure(0,minsize=1000, weight=1)
		top.rowconfigure(0, weight=1)
		top.configure(bg=BACKGROUND_COLOR)
		self.rowconfigure(0, minsize=50)
		self.rowconfigure(1, minsize=50)
		self.rowconfigure(2, minsize=50)
		self.rowconfigure(3, minsize=400, weight=5)
		self.columnconfigure(0, weight=1)
		


		
		#Top row
		log01.debug("Building the top row")
		self.HeaderSet = tk.IntVar()
		
		self.HeaderTabs = HeaderTabs(self)
		self.HeaderTabs.grid(column=0,row=0,sticky=tk.NSEW,pady=5,padx=10)
		
		#Top bar, just below the top buttons
		log01.debug("Building the second row")
		self.HeaderContent = HeaderContent(self)
		self.HeaderContent.grid(column=0,row=1,sticky=tk.NSEW,pady=5,padx=10)
		
		#Second row, just below top bar
		log01.debug("Building the third row")
		self.MainSet = tk.IntVar()
		
		self.MainRow = MainRow(self)
		self.MainRow.grid(column=0,row=2,sticky=tk.NSEW,pady=5,padx=10)
		
		#Main content
		log01.debug("Building the main content")
		self.Main = MainFrame(self)
		self.Main.grid(column=0,row=3,sticky=tk.NSEW,padx=10)
		
###############################################################################


class HeaderTabs(tk.Frame):
	def __init__(self,master=None):
		self.frame = tk.Frame.__init__(self, master,bg=BACKGROUND_COLOR)
		self.master = master
		self.createWidgets()
		
	def createWidgets(self):
		self.HeaderSet = tk.IntVar()
		self.columnconfigure(0,minsize=50)
		self.columnconfigure(1,minsize=50)
		self.columnconfigure(2,minsize=50)
		
		self.buttonlist = ["MDF","Utilities","Profiles"]
		for x,name in enumerate(self.buttonlist,0) :
			#self.button = tk.Radiobutton(self,text=name,value=x,variable=self.master.HeaderSet,indicatoron=0,selectcolor=BACKGROUND_COLOR)
			self.button = tk.Button(self,text=name,command=lambda a=x: self.redrawButtons(a))
			self.button.grid(column=x,row=0,sticky=tk.NW,padx=10,ipadx=5)
			self.buttonlist[x] = self.button
			
		
		
	def redrawButtons(self,x):
		for b in self.buttonlist:
			b.configure(relief="raised")
		self.buttonlist[x].configure(relief="sunken")
		self.master.HeaderSet.set(x)

		
###############################################################################
		
class HeaderContent(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,class_='HeaderContent')
		self.master = master
		self.createWidgets()
		self.observer()
	
	def createWidgets(self)	:
		self.columnconfigure(0,minsize=50)
		self.rowconfigure(0,minsize=50)
		self.mdf = header.mdfBar(self)
		self.util = header.utilitiesBar(self)
		self.prof = header.profilesBar(self)
		
		self.mdf.grid(column=0,row=0,sticky=tk.NW)
		
	def observer(self) :
		self.master.HeaderSet.trace("w",self.redraw)

	def redraw(self,a,b,c):
		self.mdf.grid_remove()
		self.util.grid_remove()
		self.prof.grid_remove()
		if self.master.HeaderSet.get() == 0 :
			log01.debug("Second Row: Drawing MDF launcher options")
			self.mdf.grid(column=0,row=0,sticky=tk.NW)
		elif self.master.HeaderSet.get() == 1 :
			log01.debug("Second Row: Drawing utility launchers")
			self.util.grid(column=0,row=0,sticky=tk.NW)
		elif self.master.HeaderSet.get() == 2 :
			log01.debug("Second Row: Drawing profile options")
			self.prof.grid(column=0,row=0,sticky=tk.NW)

		
###############################################################################
		
class MainRow(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,class_='MainRow',bg=BACKGROUND_COLOR)
		self.master = master
		self.createWidgets()
		
	def createWidgets(self):
		for x in range(0,9):
			self.columnconfigure(x,minsize=50)
			
		self.buttonlist = ["Init","Settings","Mods","Civs","Invaders","Creatures","Dwarf","Kobold","Orc","Worldgen"]
		for x,name in enumerate(self.buttonlist) :
			#self.button = tk.Radiobutton(self,text=name,value=x,variable=self.master.MainSet,indicatoron=0,selectcolor=BACKGROUND_COLOR)
			self.button = tk.Button(self,text=name,command=lambda a=x: self.redrawButtons(a))
			self.button.grid(column=x,row=0,sticky=tk.NW,padx=10,ipadx=5)
			self.buttonlist[x] = self.button
			
	def redrawButtons(self,x):
		for b in self.buttonlist:
			b.configure(relief="raised")
		self.buttonlist[x].configure(relief="sunken")
		self.master.MainSet.set(x)

###############################################################################

class MainFrame(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,class_='MainFrame')
		self.master = master
		self.createWidgets()
		self.observer()
		atexit.register(self.config_save)
		atexit.register(self.file_save)
		atexit.register(self.exitStateMents)
	
	def createWidgets(self):
		log01.debug("Loading main config options")
		try:
			self.config = []
			for page in configuration.loadConfig():
				self.config.append(page)
		except IOError:
			#self.config = configuration.standardConfigParse(self)
			self.config = configuration.standardXMLParse()
			
		try:
			self.tableconf = []
			for page in configuration.loadTableConf():
				self.tableconf.append(page)
		except IOError:
			#self.tableconf = configuration.tabularConfigParse()
			self.tableconf = configuration.tabularXMLParse()
		
		initContent = self.config[0]
		self.init = mainContent.standardPageFrame(self,initContent)
		self.init.grid()
		
		settingsContent = self.config[1]
		self.settings = mainContent.standardPageFrame(self,settingsContent)
		self.settings.grid()
		self.settings.grid_remove()
		
		modContent = self.config[2]
		self.mods = mainContent.standardPageFrame(self,modContent)
		self.mods.grid()
		self.mods.grid_remove()
		
		civContent = self.tableconf[0]
		self.civs = mainContent.standardTabularFrame(self,civContent)
		self.civs.grid()
		self.civs.grid_remove()
		
		creatureContent = self.config[3]
		self.creatures = mainContent.standardPageFrame(self,creatureContent)
		self.creatures.grid()
		self.creatures.grid_remove()
		
		dwarfContent = self.config[4]
		self.dwarf = mainContent.standardPageFrame(self,dwarfContent)
		self.dwarf.grid()
		self.dwarf.grid_remove()

	def observer(self) :
		self.master.MainSet.trace("w",self.redraw)		
	
	def redraw(self,a,b,c):
		self.init.grid_remove()
		self.settings.grid_remove()
		self.mods.grid_remove()
		self.civs.grid_remove()
		self.creatures.grid_remove()
		self.dwarf.grid_remove()
		if self.master.MainSet.get() == 0 :
			log01.debug("Main: Drawing init options")
			self.init.grid()
		if self.master.MainSet.get() == 1 :
			log01.debug("Main: Drawing settings options")
			self.settings.grid()
		if self.master.MainSet.get() == 2 :
			log01.debug("Main: Drawing mod options")
			self.mods.grid()
		if self.master.MainSet.get() == 3 :
			log01.debug("Main: Drawing civ options")
			self.civs.grid()
		if self.master.MainSet.get() == 5 :
			log01.debug("Main: Drawing creature options")
			self.creatures.grid()
		if self.master.MainSet.get() == 6 :
			log01.debug("Main: Drawing dwarf options")
			self.dwarf.grid()
		self.file_save()

		
	def exitStateMents(self):
		log01.warning("Saving before exiting")
		
	def file_save(self):
		#Save all edits before you close silly
		log01.info("Applying all edits")
		vals = []
		for value in self.init.getSwitchVals():
			vals.append(value)
		for diffs in handshake.compareValues(self.config[0],vals):
			parent_pipe.send(diffs)

		vals = []
		for value in self.settings.getSwitchVals():
			vals.append(value)
		for diffs in handshake.compareValues(self.config[1],vals):
			parent_pipe.send(diffs)
		vals = []
#		for value in self.civs.getSwitchVals():
#			vals.append(value)
#		for diffs in handshake.compareTableValues(self.tableconf[0],vals):
#			print(diffs)
			
	def config_save(self):
		log01.info("Saving configs to file")
		#configuration.saveConfigs(self.config)
		configuration.saveTableConf(self.tableconf)


###############################################################################


	


	
#Main
if __name__ == '__main__':
	def exit_handler():
		#Say bye
		print("Byebye")
	
	def getClear():
		parent_pipe.send("shutdown")
		parent_pipe.recv()
		
	log01.warning("Starting up")
	log01.debug("Initializing file manager")
	multiprocessing.freeze_support()
	parent_pipe = handshake.launchFileManager()
	parent_pipe.send("startup")
	
	log01.debug("Initializing exit handler")
	atexit.register(exit_handler)
	atexit.register(getClear)
	
	log01.info("Initializing launcher window")
	app = Application()
	app.master.title('Masterwork Dwarf Fortress')
	app.mainloop()
	log01.warning("Shutting down")
	

	
	



##########################################################################################################
#	[MDF]		[Utilities]		[Profiles]																			Radio buttons
#	[Top bar frame, changeable, controlled by tabs above]
#	[Init]	[Settings]	[Mods]	[Civs]	[Invaders]	[Creatures]	[Dwarf]	[Kobold]	[Orc]	[Worldgen]				Radio buttons
#	[Main section frame, changeable, controlled by tabs above]
#	[Content table]		[Content table]		[Content table]
##########################################################################################################