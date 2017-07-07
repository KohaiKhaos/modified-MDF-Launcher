#file: mainContent.py

import tkinter as tk
import ttk

defaultSelectColor = "#444"
defaultActiveBackground ="#555"


class modFrame(tk.LabelFrame):
	def __init__(self,master,content):

		self.frame = tk.LabelFrame.__init__(self,master,class_='modFrame')
		self.master = master
		self.content = content
		self.switchlist = []
		self.createSwitches()
	
	def createSwitches(self):
		for x,column in enumerate(self.content.getColumns()):
			for y,switch in enumerate(column.getSwitches()):
				swinfo = switch.getData()
				varname = self.content.modname + "_" + swinfo.name
				if swinfo.type == "bool":
					control = tk.Checkbutton(self,text=swinfo.name)
					control.var = tk.IntVar()
					control.configure(variable=control.var)
					control.configure(selectcolor=defaultSelectColor,activebackground=defaultActiveBackground)
					control.grid(row=y,column=x*2,columnspan=2,sticky=tk.W)
					if swinfo.values == "1":
						control.select()
					if swinfo.values == "0":
						control:deselect()
				
				elif swinfo.type[0].isdigit():
					a=0
					try:
						while swinfo.type[a].isdigit():
							a = a+1
						fro = int(swinfo.type[0:a])
						b = a+1 #x is a : at this point if formatting is correct
						while swinfo.type[b].isdigit():
							b = b+1
					except IndexError:
						pass
					too = int(swinfo.type[a+1:b])
					label = tk.Label(self,text=swinfo.name)
					control = tk.Spinbox(self,from_=fro,to=too,width=8)
					control.var = tk.StringVar()
					control.configure(textvariable=control.var)
					label.grid(row=y,column=x,sticky=tk.W)
					control.grid(row=y,column=x+1,sticky=tk.W)
					control.delete(0, control.index(tk.END))
					control.insert(0, swinfo.values)
				
				elif swinfo.type == "list":
					#control = tk.Menubutton(self)
					label = tk.Label(self,text=swinfo.name)
					control = ttk.Combobox(self)
					control.var = tk.StringVar()
					control.configure(state='readonly',textvariable = control.var)
					control.bind('<<ComboboxSelected>>', control.select_clear())
					control['values'] = []
					label.grid(row=y,column=x,padx=10,sticky=tk.W)
					control.grid(row=y,column=x+1,sticky=tk.W)
					
					
				elif swinfo.type == "listitem":
					currlist = []
					for vals in control['values']:
						currlist.append(vals)
					currlist.append(swinfo.name)
					control['values'] = currlist
					if swinfo.values == "1":
						try:
							control.current(len(currlist)-1)
						except tk.TclError:
							pass
				
				if not swinfo.type == "listitem":
					self.switchlist.append(control)
				
	def getSwitchVals(self):
		for switch in self.switchlist:
			yield(switch.var.get())
			
				
class standardPageFrame(tk.Frame):
	def __init__(self, master, content):
		self.frame = tk.Frame.__init__(self, master, class_='standardPageFrame')
		self.master = master
		self.content = content
		self.modframelist = []
		self.createWidgets()
	
	def createWidgets(self):
		label1 = tk.Label(self,text = self.content.name)
		label1.grid()
		x = 0
		z = 0
		for y,column in enumerate(self.content.getColumns()):
			for x,modframe in enumerate(column.getModframes()):
				makeframe = modFrame(self,modframe)
				makeframe.configure(text=modframe.modname)
				span = max([1,4//len(column.modframes)])
				makeframe.grid(row=x*span+1,column=y,rowspan=span,ipadx=10,ipady=5,padx=5,pady=10,sticky=tk.N)
				self.modframelist.append(makeframe)
				
	def getSwitchVals(self):
		for modframe in self.modframelist:
			for value in modframe.getSwitchVals():
				yield value