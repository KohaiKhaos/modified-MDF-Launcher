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
				#varname = self.content.modname + "_" + swinfo.name
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
					control.display = tk.StringVar()
					control.configure(state='readonly',textvariable = control.display)
					control.bind('<<ComboboxSelected>>', control.select_clear())
					control['values'] = []
					label.grid(row=y,column=x,padx=10,sticky=tk.W)
					control.grid(row=y,column=x+1,sticky=tk.W)
					
				elif swinfo.type == "listitem":
					currlist = list(control['values'])
					currlist.append(swinfo.name)
					control['values'] = currlist
					control.values = control['values']
					print(swinfo.values)
					if swinfo.values == "1":
						try:
							control.current(len(currlist)-1)
						except tk.TclError:
							pass
				
				if not swinfo.type == "listitem":
					self.switchlist.append(control)

				
	def getSwitchVals(self):
		for switch in self.switchlist:
			if type(switch) != ttk.Combobox:
				yield switch.var.get()
			else:
				for choice in switch.values:
					if choice == switch.display.get():
						yield "1"
					else:
						yield "0"
		raise StopIteration

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

				
				
				
				
def tableSwitch(self,swi):		#Reminder, realSwitch is the top-level button
	control = None				#It contains a list of the switches it messes with, a 1-member bool or a multi-member menu
	if swi.type == "bool":	#Only one switch in swi.switches
		control = tk.Checkbutton(self)
		control.var = tk.IntVar()
		control.configure(variable=control.var)
		control.configure(selectcolor=defaultSelectColor,activebackground=defaultActiveBackground)
		if swi.default == "1":
			control.select()
		if swi.default == "0":
			control:deselect()
	elif swi.type == "list":	#Multiple members in swi.switches
		control = ttk.Combobox(self)
		control.var = tk.StringVar()
		control.configure(state='readonly',textvariable = control.var)
		control.bind('<<ComboboxSelected>>', control.select_clear())
		control['values'] = []
		for opt in swi.switches :
			currlist = list(control['values'])
			currlist.append(opt.values)
			control['values'] = currlist
			control.values = control['values']
			if opt.values == swi.default:
				try:
					control.current(len(currlist)-1)
				except tk.TclError:
					pass
	if swi.disabled == "1":
		control.configure(state=tk.DISABLED)
	return control
				
class standardTabularFrame(tk.Frame):
	def __init__(self, master, table):
		self.frame = tk.Frame.__init__(self, master, class_='standardPageFrame')
		self.master = master
		self.table = table
		self.switchlist = []
		self.createWidgets()
	
	def createWidgets(self):
		label1 = tk.Label(self,text = self.table.name)
		label1.grid()
		for y,columnhead in enumerate(self.table.getColumn()):
			label = tk.Label(self,text=columnhead.label)
			label.grid(row=0,column=y+1)
			
		for x,rowhead in enumerate(self.table.getRow()):
			label = tk.Label(self,text=rowhead.label)
			label.grid(row=x+1,column=0)
			
		for x,y,switch in self.table.getSingleSwitch():
			try:
				makeswitch = tableSwitch(self,switch)
				makeswitch.grid(row=y+1,column=x+1,ipadx=0,ipady=0,padx=5,pady=5,sticky=tk.N)
				self.switchlist.append(makeswitch)
			except AttributeError:
				pass
				
	def getSwitchVals(self):
		for switch in self.switchlist:
			if type(switch) != ttk.Combobox:
				yield switch.var.get()
			else:
				for choice in switch.values:
					if choice == switch.display.get():
						yield "1"
					else:
						yield "0"
		raise StopIteration
	

	
	
	
	
	