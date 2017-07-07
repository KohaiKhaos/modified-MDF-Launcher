import UI_structures as gui
import pickle,gzip

MAIN_CONFIG		=	"main.cfg"
TABLE_CONFIG	=	"table.cfg"
PICKLE_CONFIG	=	"config.bin"


COMMENTER				=	"//"
PAGE_SEPARATOR			=	"!!###!:"
PAGE_COLUMN_SEPARATOR	=	"!###!"
MOD_SEPARATOR			=	"!###:"
MOD_COLUMN_SEPARATOR	=	"#!!!#"
SWITCH_SEPARATOR		=	"###"


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
			label = line[x+1]
			file = line[x+2]
			pages[-1].addCiv(label,file)
			
		if lines[x].startswith("#!!!#"):
			label = line[x+1]
			type = line[x+2]
			caption = line[x+3]
			pages[-1].addOption(label,type,caption)
			
		if lines[x].startswith("###"):
			pages[-1].addSwitch()
	
	pages.populate()

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
	
	
	
	
	
	
	
	