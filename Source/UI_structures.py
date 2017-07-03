#UI_structures.py


class standardFeatureSwitch:	#A multipurpose class that can be read in and out from a standard library file
	def __init__(self):
		self.name				#The name of the feature controlled
		self.type				#The type of switch present in the GUI. bool for on/off, an integer range ##:## for spinbuttons
								#Menu for the external interface of a menu, and menubutton for menu choices

		self.caption			#A caption that appears when the mouse hovers over the switch on the GUI
		self.values				#The current/default value that the UI takes in when reading this object

		self.filetype			#The type of file the feature interacts with. Possibilities are raw, dfhack, and init

								#Prefix flags that are "on" are followed by "[", prefix flags that are "off" are followed by "!"
		self.onPrefixes				#Iff switch is on, flag is on, and vice versa.
		self.offPrefixes		#Iff switch is on, flag is off, and vice versa.

								#Specialized lines, changes editor behavior
		self.controlOnString	#Instead of switching "[" and "!", if these elements are present the editor will swap out
		self.controlOffString	#these two strings for one another as needed. Lines still have to be prefixed and the prefix 
								#cannot be changed by this, but it still has uses.
								#Note: due to how these options work, any lines that do not have the prefix followed by *exactly*
								#the same line as one of these two will not be edited

		self.numberpos			#Specialized: Allows spinbuttons to select which number in a line to affect, indices start at 0,
								#and only distinct numbers are accounted for, not individual characters

		self.switchtype			#How specific can the files this tag is in be narrowed down?
								# 2 means you can list all of the specific files it will ever be found in
								# 1 means you can list the prefix of all files it will ever be found in (like "creature_")
								# 0 or any other value means that you cannot specify the file, and will need to seach all files for it
		self.target				#The list of specific files or file prefixes specified for switchtype.
		
		
################################################################################


class InvalidConstruction(Exception):
	def __init__():
		print("The GUI you are attempting to load failed due to a formatting error in its construction")

class switchStandardGUI:
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
#	pagecolumn.addModframe(modname)
#	pagecolumn.getModframes()
#	modframe.addColumn()
#	modframe.getColumns()
#	innercolumn.addSwitch(data)
#	innercolumn.getSwitches()
#	switch.getData()
#	switch.changeValue(newValue)

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
		
	class innercolumn:
		def __init__(self,master):
			self.master = master
			self.switches = []
		def getSwitches(self):
			for x in self.switches:
				yield x
		def addSwitch(self,data):
			self.switches.append(switchStandardGUI.switch(self,data)
		
	class modframe:
		def __init__(self,master,modname):
			self.master = master
			self.modname = modname
			self.innercols = []
		def getColumns(self):
			for x in self.innercols:
				yield x
		def addColumn(self,name):
			self.innercols.append(switchStandardGUI.innercolumn(self,name))
		
	class pagecolumn:
		def __init__(self,master):
			self.master = master
			self.modframes = []
		def getModframes(self):
			for x in self.modframes:
				yield x
		def addModframe(self):
			self.modframes.append(switchStandardGUI.modframe(self,modname))
		
	class page:
		def __init__(self,master,name):
			self.master = master
			self.name = name
			self.columns = []
		def getColumns(self):
			for x in self.columns:
				yield x
		def addColumn(self):
			self.columns.append(switchStandardGUI.pagecolumn(self))
	
	
	def addpage(master,name):
		return switchStandardGUI.page(master,name)
		
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


class menu_top:					#A multipurpose class that can be read in and out from a standard library file
	def __init__(self):
		self.name				#The name of the feature controlled
		self.type				#The type of switch present in the GUI. bool for on/off, an integer range ##:## for spinbuttons
								#Menu for the external interface of a menu, and menubutton for menu choices

		self.caption			#A caption that appears when the mouse hovers over the switch on the GUI
		self.values				#The current/default value that the UI takes in when reading this object

		self.filetype			#The type of file the feature interacts with. Possibilities are raw, dfhack, and init

class menu_item:
	def __init__(self):
		self.trueValue			#If the menu_top's value matches this, this menu_item is treated as true

								#Prefix flags that are "on" are followed by "[", prefix flags that are "off" are followed by "!"
		self.onPrefixes				#Iff switch is on, flag is on, and vice versa.
		self.offPrefixes		#Iff switch is on, flag is off, and vice versa.

								#Specialized lines, changes editor behavior
		self.controlOnString	#Instead of switching "[" and "!", if these elements are present the editor will swap out
		self.controlOffString	#these two strings for one another as needed. Lines still have to be prefixed and the prefix 
								#cannot be changed by this, but it still has uses.
								#Note: due to how these options work, any lines that do not have the prefix followed by *exactly*
								#the same line as one of these two will not be edited

		self.numberpos			#Specialized: Allows spinbuttons to select which number in a line to affect, indices start at 0,
								#and only distinct numbers are accounted for, not individual characters

		self.switchtype			#How specific can the files this tag is in be narrowed down?
								# 2 means you can list all of the specific files it will ever be found in
								# 1 means you can list the prefix of all files it will ever be found in (like "creature_")
								# 0 or any other value means that you cannot specify the file, and will need to seach all files for it
		self.target				#The list of specific files or file prefixes specified for switchtype.

		
################################################################################
	
	
class tabularStandardGUI():
#Usage
#
#
#Instance methods
#table.getRows()
#table.getColumns()
#table.addRow(name)
#table.addColumn(name)
#column.menu.getMenuItems()
#column.menu.addMenuItem(item)
#menuitem.getData()
#menuitem.changeValue()


	class table:
		def __init__(self,master):
			self.master = master
			self.rows = []
			self.columns = []
			self.matrix = []
		def getRows():
			for x in self.rows:
				yield x
		def getColumns():
			for x in self.columns:
				yield x
		def addRow(name):
			self.rows.append(tabularStandardGUI.row(self,name)
		def addColumn(name):
			self.rows.append(tabularStandardGUI.columns(self,name)
		def populateTable()
			for y in self.rows:
				self.matrix.append = []
				for x in self.columns:
					self.matrix[y].append = tabularStandardGUI.menu_real(self,item,y,x)

	class row:
		def __init__(self,master,name):
			self.master = master
			self.name = name
	
	class column:
		def __init__(self,master,name):
			self.master = master
			self.name = name
			self.menu = tabularStandardGUI.columnmenu(self)
	
	class columnmenu:
		def __init__(self,master,data):
			if not type(data) is menu_top:
				raise InvalidConstruction
			self.master = master
			self.data = data
			self.items = []
		def getMenuItems():
			for x in self.items
				yield x
		def addMenuItem(item):
			self.items.append(tabularStandardGUI.menuitem(self,item)
			
	class menuitem:
		def __init__(self,master,data):
			if not type(data) is menu_item:
				raise InvalidConstruction
			self.master = master
			self.data = data
		def getData(self):
			return self.data
			
	class menu_real(tabularStandardGUI.columnmenu):
		def __init__(self,master,y,x)
			self.master = master
			self.name = y.name + "_" + x.name
			self.data = x.data
			self.items = x.items
		def getValue():
			return self.data.values
		def setValue(newValue):
			self.data.values = newValue