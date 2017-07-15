import tkinter as tk
from PIL import Image
from PIL import ImageTk
import subprocess, webbrowser, os

DF_PATH		= "Dwarf Fortress"
SAVE_PATH	= "Dwarf Fortress/data/save"
UTIL_PATH	= "Masterwork Dwarf Fortress/Utilities"
MANUAL_PATH	= "manual.html"

WIKI_URL	= "http://dwarffortresswiki.org/"
FORUM_URL	= "http://www.bay12forums.com/smf/index.php?board=24.0"




class mdfBar(tk.Frame):
	def __init__(self, master=None):
		self.frame = tk.Frame.__init__(self, master,class_='mdfBar')
		self.master=master
		self.createWidgets()
	
	
	def createWidgets(self):
		img = Image.open("../Resources/df-icon.png")
		img = img.resize((35,35),Image.BICUBIC)
		self.DFButton = tk.Button(self,command=self.LaunchDF,height=35,width=37)
		self.DFButton.image = ImageTk.PhotoImage(img)
		self.DFButton.config(image=self.DFButton.image)
		self.DFButton.grid(row=0,column=0)
		
		img = Image.open("../Resources/folder-open.png")
		img = img.resize((17,17),Image.BICUBIC)
		self.FileMenu = tk.Menubutton(self,height=35,width=37,relief="raised")
		self.FileMenu.image = ImageTk.PhotoImage(img)
		self.FileMenu.config(image=self.FileMenu.image,text="Open",compound=tk.TOP)
		self.FileMenu.grid(row=0,column=1)
		self.menu = tk.Menu(self.FileMenu,tearoff=0)
		targ = "file://" + os.path.realpath(DF_PATH)
		self.menu.add_command(label="Dwarf Fortress",command=lambda y=targ: self.OpenFiles(y))
		targ = "file://" + os.path.realpath(SAVE_PATH)
		self.menu.add_command(label="Saves",command=lambda y=targ: self.OpenFiles(y))
		targ = "file://" + os.path.realpath(DF_PATH)
		self.menu.add_command(label="Utilities",command=lambda y=targ: self.OpenFiles(y))
		self.FileMenu.config(menu=self.menu)
		
		img = Image.open("../Resources/book-question.png")
		img = img.resize((17,17),Image.BICUBIC)
		targ = "file://" + os.path.realpath(MANUAL_PATH)
		self.ManualButton = tk.Button(self,height=35,width=37,command=lambda y=targ: self.OpenFiles(y))
		self.ManualButton.image = ImageTk.PhotoImage(img)
		self.ManualButton.config(image=self.ManualButton.image,text="Manual",compound=tk.TOP)
		self.ManualButton.grid(row=0,column=2)
		
		img = Image.open("../Resources/globe--arrow.png")
		img = img.resize((17,17),Image.BICUBIC)
		self.LinkMenu = tk.Menubutton(self,height=35,width=37,relief="raised")
		self.LinkMenu.image = ImageTk.PhotoImage(img)
		self.LinkMenu.config(image=self.LinkMenu.image,text="Links",compound=tk.TOP)
		self.LinkMenu.grid(row=0,column=3)
		self.menu = tk.Menu(self.LinkMenu,tearoff=0)
		targ = WIKI_URL
		self.menu.add_command(label="Wiki",command=lambda y=targ: self.OpenFiles(y))
		targ = FORUM_URL
		self.menu.add_command(label="MW Forum",command=lambda y=targ: self.OpenFiles(y))
		self.LinkMenu.config(menu=self.menu)
		
		img = Image.open("../Resources/information_large.png")
		img = img.resize((17,17),Image.BICUBIC)
		self.InfoButton = tk.Button(self,height=35,width=37)
		self.InfoButton.image = ImageTk.PhotoImage(img)
		self.InfoButton.config(image=self.InfoButton.image,text="About",compound=tk.TOP)
		self.InfoButton.grid(row=0,column=4)
	
	def LaunchDF(self):
		#Launch DF
		p = subprocess.Popen(["Dwarf Fortress/Dwarf Fortress.exe"],
						 	 cwd="Dwarf Fortress",
							 stdout=subprocess.PIPE,
							 stderr=subprocess.STDOUT)
		#Close the program
		self.master.master.quit()

	def OpenFiles(self,target=".."):
		webbrowser.open_new_tab(target)
	

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