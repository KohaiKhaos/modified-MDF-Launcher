#handshake.py
#All functions and definitions directly relating to passing of information between the main launcher and the file editor are placed  here.

import UI_structures
import fileManager
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
					currentOld = str(data.values)
					currentNew = str(next(newValues))
					if currentOld == currentNew :
						continue
					else:
						data.values = currentNew
						yield data
						
						
#Launches the file manager and gives it a useable pipe
#Returns a pipe for use later
def launchFileManager():
	parent_conn, child_conn = Pipe()
	FM = Process(target=fileManager.Manage, args=(child_conn,), daemon=True)
	FM.start()
	return parent_conn