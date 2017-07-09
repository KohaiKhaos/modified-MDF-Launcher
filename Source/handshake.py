#handshake.py
#All functions and definitions directly relating to passing of information between the main launcher and the file editor are placed  here.

import UI_structures as gui
from fileManager import Manage
from multiprocessing import Process, Pipe


#Takes in the page structure and gets its current values, and the new set of values collected upon a page change
#Returns, one at a time, the list of changes to implement.
def compareValues(oldPage,newVals):
	newValues = iter(newVals)
	for column in oldPage.getColumns():
		for mod in column.getModframes():
			for column in mod.getColumns():
				for switch in column.getSwitches():
					data = switch.getData()
					if data.type != "list":						
						currentOld = str(data.values)
						currentNew = str(next(newValues))
						if currentOld == currentNew :
							continue
						else:
							data.values = currentNew
							print(data.name,data.values)
							yield data

def compareTableValues(oldTable,newVals):
	newValues = iter(newVals)
	for x,y,swi in oldTable.getSingleSwitch():
		currentOld = str(swi.switches[0].values)
		currentNew = str(next(newValues))
		if currentOld == currentNew :
						continue
		else:
			swi.switches[0].values = currentNew
			curr = gui.standardFeatureSwitch.fromTablular(swi)
			yield curr

#Launches the file manager and gives it a useable pipe
#Returns a pipe for use later
def launchFileManager():
	parent_conn, child_conn = Pipe()
	FM = Process(None,Manage,"File Manager", args=(child_conn,), daemon=True)
	FM.start()
	return parent_conn