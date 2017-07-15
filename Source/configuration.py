import UI_structures as gui
import pickle,gzip
import xml.etree.ElementTree as et

MAIN_CONFIG		=	"main.cfg"
TABLE_CONFIG	=	"table.cfg"
PICKLE_CONFIG	=	"config.bin"
TAB_PICKLE_CONFIG =	"table.bin"
MAIN_XML		=	"main.xml"
TABLE_XML		=	"table.xml"

COMMENTER				=	"//"
PAGE_SEPARATOR			=	"!!###!:"
PAGE_COLUMN_SEPARATOR	=	"!###!"
MOD_SEPARATOR			=	"!###:"
MOD_COLUMN_SEPARATOR	=	"#!!!#"
SWITCH_SEPARATOR		=	"###"

TABLE_PAGE_SEPARATOR	=	"!!###!:"
TABLE_ROW				=	"!###!"
TABLE_COLUMN			=	"#!!!#"
TABLE_SWITCH			=	"###"			#Switches must occur immediately after the column they occur in; rows can get in the middle but that's messy
TABLE_MATRIX			=	"!#!#!"			#Defines default values and disabling of buttons. Does not look pretty

def standardConfigParse(master):
	config = open(MAIN_CONFIG,"rt",1)
	lines = config.readlines()
	pages = []
	
	try:
		lines.remove("\n")
	except ValueError:
		pass
	for line in lines:
		if line.startswith("//"):
			lines.remove(line)

	for x in range(len(lines)):
		if lines[x].startswith(PAGE_SEPARATOR):
			pages.append(gui.switchStandardGUI.addPage(lines[x][7:-1]))
		
		if lines[x].startswith(PAGE_COLUMN_SEPARATOR):
			pages[-1].addColumn()
		
		if lines[x].startswith(MOD_SEPARATOR):
			pages[-1].getLastColumn().addModframe(lines[x][5:-1])
		
		if lines[x].startswith(MOD_COLUMN_SEPARATOR):
			pages[-1].getLastColumn().getLastModframe().addColumn()
			
		if lines[x].startswith(SWITCH_SEPARATOR):
			switch = gui.standardFeatureSwitch()
			for z,ln in enumerate(lines[x+1:x+13],1):
				ln = ln.partition("=")
				if ln[1] == "=":
					lines[x+z] = ln[2]
				else:
					lines[x+z] = ln[0]
			switch.parseSwitch(lines[x+1:x+13])
			pages[-1].getLastColumn().getLastModframe().getLastColumn().addSwitch(switch)
			x = x+12

	return pages

def standardXMLParse():
	file = open(MAIN_XML,"rt",1)
	lines = file.readlines()
	for x in range(len(lines)):
		lines[x] = lines[x].lstrip()
	for line in lines:
		if line.startswith("//"):
			lines.remove(line)
	try:
		lines.remove("\n")
	except ValueError:
		pass
	
	config = et.fromstringlist(lines)
	pages = []
			
	for pg in config:
		pages.append(gui.switchStandardGUI.addPage(pg.get("name")))
		
		for pgcol in pg:
			pages[-1].addColumn()
	
			for mod in pgcol:
				pages[-1].getLastColumn().addModframe(mod.get("name"))
				
				for incol in mod:
					pages[-1].getLastColumn().getLastModframe().addColumn()
					
					for swi in incol:
						switch = gui.standardFeatureSwitch()
						tx = swi.text.splitlines()
						valuepairs = []
						for line in tx:
							line = line.strip()
							line = line.split("=",1)
							line[0] = line[0].strip()
							try:
								line[1] = line[1].strip()
							except:
								line = (line[0],None)
							valuepairs.append(line)
						switch.dictSwitch(dict(valuepairs))
						pages[-1].getLastColumn().getLastModframe().getLastColumn().addSwitch(switch)
	return pages
	
def tabularXMLParse():
	file = open(TABLE_XML,"rt",1)
	lines = file.readlines()
	for x in range(len(lines)):
		lines[x] = lines[x].lstrip()
	for line in lines:
		if line.startswith("//"):
			lines.remove(line)
	try:
		lines.remove("\n")
	except ValueError:
		pass
		
	config = et.fromstringlist(lines)
	pages = []
	
	for pg in config:
		pages.append(gui.tabularStandardGUI.table())
		
		for rowcol in pg:
			if rowcol.tag.lower() is "row":
				label = rowcol.get("label")
				file = rowcol.get("file")
				pages[-1].addCiv(label,file)
			
			elif rowcol.tag.lower() is "column":
				label = rowcol.get("label")
				type = rowcol.get("type")
				caption = rowcol.get("caption")
				pages[-1].addOption(label,type,caption)
				
				for swi in rowcol:
					tx = swi.text.splitlines()
					valuepairs = []
					for line in tx:
						line = line.strip()
						line = line.split("=",1)
						line[0] = line[0].strip()
						try:
							line[1] = line[1].strip()
						except:
							line = (line[0],None)
						valuepairs.append(line)
					pages[-1].addSwitch(dict(valuepairs))
			
			elif rowcol.tag.lower() is "matrix":
				matrix = rowcol.text.slitlines()
	
	
	for page in pages:
		page.populate(matrix)
	return pages
	
def tabularConfigParse():
	config = open(TABLE_CONFIG,"rt",1)
	lines = config.readlines()
	pages = []

	try:
		lines.remove("\n")
	except ValueError:
		pass
	for line in lines:
		if line.startswith("//"):
			lines.remove(line)
	
	for x in range(len(lines)):
		if lines[x].startswith("!!###!:"):
			pages.append(gui.tabularStandardGUI.table())
		
		if lines[x].startswith("!###!"):
			label = lines[x+1].strip()
			file = lines[x+2].strip()
			pages[-1].addCiv(label,file)
			
		if lines[x].startswith("#!!!#"):
			label = lines[x+1].strip()
			type = lines[x+2].strip()
			caption = lines[x+3].strip()
			pages[-1].addOption(label,type,caption)
			
		if lines[x].startswith("###"):
			pages[-1].addSwitch(lines[x+1:x+5])
	
		if lines[x].startswith("!#!#!"):
			z = x+1
			try:
				while not lines[x].startswith("!!###!:"):
					x +=1
			except IndexError:
				pass
			matrix = lines[z:x]
		
		
	for page in pages:
		page.populate(matrix)
	return pages

def saveConfigs(stanConfigs):
	file = gzip.open(PICKLE_CONFIG,"wb")
	for page in stanConfigs:
		pickle.dump(page,file,-1)
	
def loadConfig():
	file = gzip.open(PICKLE_CONFIG,"rb")
	try:
		while True:
			yield pickle.load(file)
	except EOFError:
		raise StopIteration

def saveTableConf(stanConfigs):
	file = gzip.open(TAB_PICKLE_CONFIG,"wb")
	for page in stanConfigs:
		pickle.dump(page,file,-1)
	
def loadTableConf():
	file = gzip.open(TAB_PICKLE_CONFIG,"rb")
	try:
		while True:
			yield pickle.load(file)
	except EOFError:
		raise StopIteration
	
	
	
	
	
	
	