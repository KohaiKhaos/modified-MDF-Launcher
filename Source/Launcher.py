import tkinter as tk
import mainContent
import configuration

BACKGROUND_COLOR = "#000"
FOREGROUND_COLOR = "#FFF"

class Application(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,bg=BACKGROUND_COLOR)
		self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
		self.optionWidgets()
		self.createWidgets()

	def optionWidgets(self):
		self.option_add("*Background","#000")
		self.option_add("*Foreground","#FFF")

	def createWidgets(self):
		top=self.winfo_toplevel()
		top.columnconfigure(0,minsize=1000, weight=1)
		top.rowconfigure(0,minsize=700, weight=1)
		top.configure(bg=BACKGROUND_COLOR)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=5)
		self.columnconfigure(0, weight=1)
		
		self.option_add('*Radiobutton*background',BACKGROUND_COLOR)
		self.option_add('*Radiobutton*foreground',FOREGROUND_COLOR)
		
		
		#Top row
		self.HeaderSet = tk.IntVar()
		
		self.HeaderTabs = HeaderTabs(self)
		self.HeaderTabs.grid(column=0,row=0,sticky=tk.NW,pady=10,padx=10)
		
		#Top bar, just below the top buttons
		self.HeaderContent = HeaderContent(self)
		self.HeaderContent.grid(column=0,row=1,sticky=tk.NW,pady=10,padx=10)
		
		#Second row, just below top bar
		self.MainSet = tk.IntVar()
		
		self.MainRow = MainRow(self)
		self.MainRow.grid(column=0,row=2,sticky=tk.NW,pady=5,padx=10)
		
		#Main content
		self.Main = MainFrame(self)
		self.Main.grid(column=0,row=3,sticky=tk.NSEW,pady=5,padx=10)

	
	

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
		
		buttonlist = ["MDF","Utilities","Profiles"]
		x=0
		for name in buttonlist :
			self.button = tk.Radiobutton(self,text=name,value=x,variable=self.master.HeaderSet,indicatoron=0,selectcolor=BACKGROUND_COLOR)
			self.button.grid(column=x,row=0,sticky=tk.NW,padx=10,ipadx=5)
			x = x+1
			
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
		self.mdf = mdfBar(self)
		self.util = utilitiesBar(self)
		self.prof = profilesBar(self)
		
		self.mdf.grid(column=0,row=0,sticky=tk.NW)
		
	def observer(self) :
		self.master.HeaderSet.trace("w",self.redraw)

	def redraw(self,a,b,c):
		self.mdf.grid_remove()
		self.util.grid_remove()
		self.prof.grid_remove()
		if self.master.HeaderSet.get() == 0 :
			self.mdf.grid(column=0,row=0,sticky=tk.NW)
		elif self.master.HeaderSet.get() == 1 :
			self.util.grid(column=0,row=0,sticky=tk.NW)
		elif self.master.HeaderSet.get() == 2 :
			self.prof.grid(column=0,row=0,sticky=tk.NW)


class mdfBar(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,class_='mdfBar')
		self.text = tk.Label(self,text="MDF stuff")
		self.text.grid()

class utilitiesBar(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,class_='utilitiesBar')
		self.text = tk.Label(self,text="Utilities stuff")
		self.text.grid()

class profilesBar(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,class_='profilesBar')
		self.text = tk.Label(self,text="Profiles stuff")
		self.text.grid()
		
###############################################################################
		
class MainRow(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,class_='MainRow',bg=BACKGROUND_COLOR)
		self.master = master
		self.createWidgets()
		
	def createWidgets(self):
		for x in range(0,9):
			self.columnconfigure(x,minsize=50)
			
		buttonlist = ["Init","Settings","Mods","Civs","Invaders","Creatures","Dwarf","Kobold","Orc","Worldgen"]
		x=0
		for name in buttonlist :
			self.button = tk.Radiobutton(self,text=name,value=x,variable=self.master.MainSet,indicatoron=0,selectcolor=BACKGROUND_COLOR)
			self.button.grid(column=x,row=0,sticky=tk.NW,padx=10,ipadx=5)
			x = x+1


###############################################################################

class MainFrame(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,class_='MainFrame')
		self.master = master
		self.createWidgets()
		self.observer()
	
	def createWidgets(self):
		self.config = configuration.configParse()
		
		settingsFrames = self.config[0]
		settingsContent = self.config[1]
		self.settings = mainContent.standardPageFrame(self,"Settings",settingsFrames,settingsContent)
		
		modFrames = self.config[2]
		modContent = self.config[3]
		self.mods = mainContent.standardPageFrame(self,"Mods",modFrames,modContent)
		
		civFrames = []
		civContent = [[[]]]
		
		invaFrames = []
		invaContent = [[[]]]
		
		creaFrames = self.config[4]
		creaContent = self.config[5]
		self.creatures = mainContent.standardPageFrame(self,"Creatures",creaFrames,creaContent)
		
		dwarFrames = self.config[6]
		dwarContent = self.config[7]
		self.dwarves = mainContent.standardPageFrame(self,"Dwarves",dwarFrames,dwarContent)
		
		koboFrames = []
		koboContent = [[[]]]
		
		orcFrames = []
		orcContent = [[[]]]
		
		worldFrames = []
		worldcontent = [[[]]]
		
		self.settings.grid()

	def observer(self) :
		self.master.MainSet.trace("w",self.redraw)		
	
	def redraw(self,a,b,c):
		self.settings.grid_remove()
		self.mods.grid_remove()
		self.creatures.grid_remove()
		self.dwarves.grid_remove()
		if self.master.MainSet.get() == 1 :
			self.settings.grid()
		elif self.master.MainSet.get() == 2 :
			self.mods.grid()
		elif self.master.MainSet.get() == 5 :
			self.creatures.grid()
		elif self.master.MainSet.get() == 6 :
			self.dwarves.grid()


###############################################################################

app = Application()
app.master.title('Masterwork Dwarf Fortress')
app.mainloop()




##########################################################################################################
#	[MDF]		[Utilities]		[Profiles]																			Radio buttons
#	[Top bar frame, changeable, controlled by tabs above]
#	[Init]	[Settings]	[Mods]	[Civs]	[Invaders]	[Creatures]	[Dwarf]	[Kobold]	[Orc]	[Worldgen]				Radio buttons
#	[Main section frame, changeable, controlled by tabs above]
#	[Content table]		[Content table]		[Content table]
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
#	
##########################################################################################################