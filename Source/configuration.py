import UI_structures as gui
import pickle,gzip

MAIN_CONFIG		=	"main.cfg"
TABLE_CONFIG	=	"table.cfg"
PICKLE_CONFIG	=	"config.bin"
TAB_PICKLE_CONFIG =	"table.bin"

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
			switch.parseSwitch(lines[x+1:x+13])
			pages[-1].getLastColumn().getLastModframe().getLastColumn().addSwitch(switch)
			x = x+12

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
	print(stanConfigs)
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
	
	
	
	
	
	
	