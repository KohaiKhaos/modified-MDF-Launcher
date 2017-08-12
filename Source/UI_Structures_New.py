#UI_structures_New.py
#Reimplements the standardardized structures with pythonic data structures at their cores

class standardFeatureSwitch:	#A multipurpose class that can be read in and out from a standard library file
	def __init__(self):
	  self.content = {}
    
  def get(self,tag):
    return self.content[tag]
  
  def set(self,tag,value=none):
    self.content[tag] = value
  
	def parseSwitch(self,textlines):
    for ln in textlines:
      key,val = ln.split("=",2)
      key = key.strip()
      val = val.strip()
      self.content.set(key,val)
		
	def dictSwitch(self,dictionary):
    for key,val in dict.iter(dictionary):
      self.content.set(key,val)

  def fromMenu(menu,options):
    switches = []
    for option in options:
      foo = dict.copy(option)
      foo.update(menu)
      if menu["values"] == option["name"]:
        foo["values"] = "1"
      else
        foo["values"] = "0"
      switches.append(foo)
     return switches
    


class InvalidConstruction(Exception):
	def __init__():
		print("The GUI you are attempting to load failed due to a formatting error in its construction")

class switchStandardGUI:
#
#	[page]	-	>	[pagecolumn]	-	>	[modframe]	-	>	[innercolumn]	-	>	[switch]
#
#Usage
#	Provides a readable format for the basic main content for the MW GUI.
#	Pages are held in a separate array, but this means only *one* array is needed externally.
#	Methods provide a sensible and reliable way to both build the gui and then retrieve information from it.
#
#Callable functions:
#	switchStandardGui.addPage(master,name)
#	switchStandardGui.getPages()
#
#Instance methods:
#	page.addColumn()
#	page.getColumns()
#	page.getLastColumn()
#	pagecolumn.addModframe(modname)
#	pagecolumn.getModframes()
#	pagecolumn.getLastModframe()
#	modframe.addColumn()
#	modframe.getColumns()
#	modframe.getLastColumn()
#	innercolumn.addSwitch(data)
#	innercolumn.getSwitches()
#	switch.getData()
#	switch.changeValue(newValue)

	class page:
		def __init__(self,name,master):
			self.master = master
			self.name = name
			self.columns = []
		def getLastColumn(self):
			return self.columns[-1]
		def getColumns(self):
			for x in self.columns:
				yield x
		def addColumn(self):
			self.columns.append(switchStandardGUI.pagecolumn(self))

			
	class pagecolumn:
		def __init__(self,master):
			self.master = master
			self.modframes = []
		def getLastModframe(self):
			return self.modframes[-1]
		def getModframes(self):
			for x in self.modframes:
				yield x
		def addModframe(self,modname):
			self.modframes.append(switchStandardGUI.modframe(self,modname))

	class modframe:
		def __init__(self,master,modname):
			self.master = master
			self.modname = modname
			self.innercols = []
		def getLastColumn(self):
			return self.innercols[-1]
		def getColumns(self):
			for x in self.innercols:
				yield x
		def addColumn(self):
			self.innercols.append(switchStandardGUI.innercolumn(self))			

	class innercolumn:
		def __init__(self,master):
			self.master = master
			self.switches = []
		def getSwitches(self):
			for x in self.switches:
				yield x
		def addSwitch(self,data):
			self.switches.append(switchStandardGUI.switch(self,data))

			
	class switch:
		def __init__(self, master, data):
			if not type(data) is standardFeatureSwitch:
				raise InvalidConstruction
			self.master = master
			self.data = data
		def getData(self):
			return self.data
		def changeValue(self,nawvalue):
			self.data.value = newvalue
		
	
	def addPage(name,master=None):
		return switchStandardGUI.page(name,master)
		
	def getPages(pagelist):
		if not type(pagelist) is list:
			raise IndexError
		if not type(pagelist[0]) is switchStandardGUI.page:
			raise InvalidConstruction
		for x in pagelist:
			yield x
	
	
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################



class tabularStandardGUI:
	class table:
		def __init__(self,name=None):
			self.name = name
			self.toprow = []
			self.leftcol = []
			self.switchlist = []
			
		def addOption(self,label,type="bool",caption=None):
			self.toprow.append(None)
			self.toprow[-1] = tabularStandardGUI.option(label,type,caption)
			
		def addCiv(self,label,file=None):
			civ = tabularStandardGUI.civilization(label,file)
			self.leftcol.append(civ)
			
		def addSwitch(self,dictionary):
			self.toprow[-1].addSwitch(dictionary)
			
		def populate(self,matrixtext = None):
			self.switchlist = []
			if matrixtext == None:
				for civ in self.leftcol:
					self.switchlist.append([])
					for option in self.toprow:
						swi = tabularStandardGUI.realSwitch(civ.label+option.label,option.type,option.switches,civ.file)
						self.switchlist[-1].append(swi)
			else:
				print(matrixtext)
				for y,civ in enumerate(self.leftcol):
					matrixtext[y] = matrixtext[y].strip()
					words = matrixtext[y].split("|")
					self.switchlist.append([])
					for x,option in enumerate(self.toprow):
						try:
							word = words[x].strip()
							print(word)
							if word[0] == "~":
								default = word[1:]
								disabled = "1"
							else:
								default = word
								disabled = "0"
						except IndexError:
							default = "0"
							disabled = "1"
						swi = tabularStandardGUI.realSwitch(civ.label+option.label,option.type,option.switches,civ.file,default,disabled)
						self.switchlist[-1].append(swi)
		
		def showContents(self):
			print("\t\t", end="")
			for x in self.toprow:
				print(x.label,end="\t\t")
			print("")
			for row,y in enumerate(self.switchlist):
				print(self.leftcol[row].label,end="\t")
				for x in y:
					print(x.name,end="\t\t")
				print("")
		
		def getRow(self):
			for x in self.leftcol:
				yield x
			raise StopIteration
		
		def getColumn(self):
			for x in self.toprow:
				yield x
			raise StopIteration
		
		def getSingleSwitch(self):
			for y,row in enumerate(self.switchlist):
				for x,switch in enumerate(row):
					yield x,y,switch
			raise StopIteration
			
	class option:
		def __init__(self,label,type,caption=None):
			self.label = label
			self.caption = caption	#Mouseover text for the label
			self.type = type	#What type of option it is; bool or list
			self.switches = []	#bool means a single switch, list is a list of switches from which a Combobox is built
			
		def addSwitch(self,dictionary):
			switch = tabularStandardGUI.tableSwitch(dictionary)
			if self.type == "bool":
				self.switches = [switch]
			else:
				self.switches.append(switch)

	class civilization:
		def __init__(self,label,file=None):
			self.label = label
			self.file = file	#What file to go to for this
			
	class tableSwitch:
		def __init__(self,dictionary):
			self.values = dictionary.get("Value")
			self.onPrefixes = dictionary.get("TagOn")
			self.offPrefixes = dictionary.get("TagOff")
			self.controlOnString = dictionary.get("ControlOn")
			self.controlOffString = dictionary.get("ControlOff")
			


	class realSwitch:
		def __init__(self,name,type,switches,file,default,disabled):
			self.name = name
			self.type = type
			self.switches = switches
			self.file = file
			self.default = default
			self.disabled = disabled













