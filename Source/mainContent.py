#file: mainContent.py

import tkinter as tk



defaultSelectColor = "#444"
defaultActiveBackground ="#555"




class contentFrame(tk.LabelFrame):
	def __init__(self, master, title, content):
		self.frame = tk.LabelFrame.__init__(self,master,class_='contentFrame')
		self.master = master
		self.title = title
		self.content = content
		self.createWidgets()
		
	def createWidgets(self):
		for columns in range(0,len(self.content)):
			for index,cont in enumerate(self.content[columns]):
				if cont.startswith("bool"):
					control = tk.Checkbutton(self,text=cont[4:],variable=self.title+ "_" + cont[4:])
					control.configure(selectcolor=defaultSelectColor,activebackground=defaultActiveBackground)
					control.grid(row=index,column=columns)
					
				elif cont[0].isdigit():
					x=0
					while cont[x].isdigit():
						x = x+1
					fro = int(cont[0:x])
					y = x+1 #x is a : at this point if formatting is correct
					while cont[y].isdigit():
						y = y+1
					too = int(cont[x+1:y])
					label = tk.Label(self,text=cont[y:])
					control = tk.Spinbox(self,from_=fro,to=too,width=8)
					label.grid(row=index,column=columns)
					control.grid(row=index,column=columns+1)
					
				elif cont.startswith("listitem"):
					control.menu.add_radiobutton(label=cont[8:], value=cont[8:],variable=control.title)
					
				elif cont.startswith("list"):
					control = tk.Menubutton(self,text="Stuff")
					control.title = tk.StringVar()
					control.configure(textvariable=control.title)
					control.title.set("Default")
					control.menu = tk.Menu(control,tearoff=0)
					control['menu'] = control.menu
					control.grid(row=index,column=columns)
				
	


class standardPageFrame(tk.Frame):
	def __init__(self, master,name,frames,content):
		self.frame = tk.Frame.__init__(self, master,class_='standardPageFrame')
		self.master = master
		self.name = name
		self.frames = frames
		self.content = content
		self.createWidgets()
	
	def createWidgets(self):
		label1 = tk.Label(self,text = self.name)
		label1.grid()
		x = 0
		z = 0
		for framegroups in self.content:
			y = 0
			for frame in self.content[x]:
				content = contentFrame(self,self.frames[z],self.content[x][y])
				content.configure(text=self.frames[z])
				span = max([1,4//len(self.content[x])])
				content.grid(row=y*span+1,column=x,sticky=tk.N,padx=5,pady=10,rowspan=span)
				y = y+1
				z = z+1
			content.columnconfigure(x,minsize=50)
			x = x+1
			
			
class tabularPageFrame(tk.Frame)
	def __init__(self, master,name,options,civs,accessmatrix):
		self.frame = tk.Frame.__init__(self, master,class_='standardPageFrame')
		self.master = master
		self.name = name
		self.options = options
		self.civs = civs
		self.matrix = accessmatrix
		self.createWidgets()
	
	def createWidgets(self):
		label1 = tk.Label(self,text = self.name)
		label1.grid()
		
		for y,c in enumerate(self.civs,1):
			civlabel = tk.Label(self,text = c)
			civlabel.grid(row=y,column=0)
		
		for x,sets in enumerate(self.options,1):
			optlabel = tk.Label(self,text = sets[0])
			optlabel.grid(row=0,column=x)
			for y,c in enumerate(self.civs,1):
				matrixmenu = tk.Menu(self,text="foo")
				matrixmenu.title = tk.StringVar()
				matrixmenu.configure(textvariable=control.title)
				matrixmenu.title.set(sets[1][0])
				matrixmenu.menu = tk.Menu(matrixmenu,tearoff=0)
				matrixmenu['menu'] = matrixmenu.menu
				matrixmenu.grid(row=y,column=x)
				for z,choices in enumerate(sets[1]):
					matrixmenu.menu.add_radiobutton(label=sets[1][z][8:],value=sets[1][z][8:],variable=matrixmenu.title)
				
				