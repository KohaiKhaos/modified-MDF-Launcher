from UI_structures import standardFeatureSwitch
from multiprocessing import Process, Pipe
from time import sleep
from cacheManager import hashManager as hashManager
from cacheManager import cacheManager as cacheManager
from cacheManager import NoCache,NoHash,WrongHash
from logger import log02
import hashlib, os, operator, string, re


CACHEFILE	= "cache.bin"
HASHFILE	= "hashes.sha"

TOO_MANY_FALSES = str.maketrans("!{}","[[]")

RAWS_FOLDER = "Dwarf Fortress/raw/objects/"
INIT_FOLDER = None
INIT_FILES = []
HACK_FOLDER = None
HACK_FILES = []

def Manage(pipe):
	log02.info("Waiting for jobs")
	jobs = []
	while True:
		rawjobs = []
		hackjobs = []
		initjobs = []
		if pipe.poll(None):					#Poll the pipe, wait for something to arrive
			sleep(1)						#If there is, wait a second to let more in
			while pipe.poll():				#Now keep grabbing stuff till it's empty
				jobs.append(pipe.recv())	#Get an object from the launcher, woot woot, gotta see what it is next
		for job in jobs:
			if type(job) == standardFeatureSwitch:	#It's a switch, time to edit files
				if job.filetype == "raw":
					rawjobs.append(job)
				if job.filetype == "hack":
					hackjobs.append(job)
				if job.filetype == "init":
					initjobs.append(job)
			if type(job) == str:					#It's an order, let's do what it says
				pass
				if job == "startup":
					log02.info("Starting up file manager, settings things up")
					cachedfiles = []
					with os.scandir(RAWS_FOLDER) as dir:
						for file in dir:
							if file.is_file(follow_symlinks=False):
								cachedfiles.append(RAWS_FOLDER + file.name)
					cachedfiles.extend(INIT_FILES)
					if not os.access(HASHFILE,os.F_OK) or not os.access(CACHEFILE,os.F_OK):
						log02.warning("There's no hash file set up; creating a new one from scratch")
						hashManager.hashAllFiles(cachedfiles,HASHFILE)					
					if not os.access(CACHEFILE,os.F_OK):
						log02.warning("There's no cache file set up; creating a new one from scratch")
						cacheManager.cacheAllFiles(cachedfiles,CACHEFILE)
				if job == "shutdown":
					log02.info("Shutting down file manager, running the last pass through.")
					rawManager.manage(rawjobs)
					hackManager.manage(hackjobs)
					initManager.manage(initjobs)
					log02.info("Last jobs done, sending clear and exiting")
					pipe.send("Cleared")
					pipe.close()
					multiprocessing.terminate()
		rawManager.manage(rawjobs)
		hackManager.manage(hackjobs)
		initManager.manage(initjobs)



def checkHashCache(filename):
	try:
		try:
			log02.debug("Comparing the hash for %s",filename)
			hashManager.hashFileCompare(filename,HASHFILE)
		except NoHash: #Raised if there is no hash for this file
			log02.warning("No hash found for %s, creating one",filename)
			hashManager.hashFileWrite(filename,HASHFILE)
		except WrongHash: #Raised if the hashes are inconsistent
			log02.warning("Hash for %s is incorrect, replacing it and recaching it",filename)
			cache = cacheManager.cacheReplace(filename,CACHEFILE)
		cache = cacheManager.cacheFileGet(filename,CACHEFILE)
	except NoCache: #Raised if there is no cache for this file
		cache = cacheManager.cacheFile(filename,CACHEFILE)
		log02.warning("No cache found for %s, creating one",filename)
	return cache
		

class rawManager:
#
#Functions
# manage(switches)									- Main manager for raws, does all the real work.
# simpleReplace(filepointer,cache,switchdatum)		- Swaps ! and [ in a file, as needed
# numberReplace(filepointer,cache,switchdatum)		- Swaps two numbers with one another in a file, as needed
# controlledReplace(filepointer,cacha,switchdatum) 	- Swaps two specified strings with one another in a file, as needed; takes *all* current switches that need this
#													because it actually overwrites the whole file to avoid any issues with string length or corruption
#													It is also slower to run, so it should not be used senselessly

	def manage(switches):
		log02.info("Managing a bunch of raw edits")
		if switches != []:
			dir = os.scandir(RAWS_FOLDER)
			for file in dir:
				if file.is_file(follow_symlinks=False):
					fp = open(RAWS_FOLDER + file.name,"r+",1)
					cache = checkHashCache(RAWS_FOLDER + file.name) #Check integrity of the cache and  hash on this file
					for switch in switches:
						log02.debug("Performing edits for %s", switch.name.strip())
						type = switch.type.strip()
						if type[0].isdigit():		#Value replacement
							rawManager.numberReplace(fp,cache,switch)
						else:
							rawManager.simpleReplace(fp,cache,switch)
					fp.close()
			dir.close()
	

	def simpleReplace(fp,cache,switch):
		if switch.onPrefixes != "":
			try:
				line,pos = cache.findPrefix(switch.onPrefixes.strip())
			except IndexError:
				pass
			else:
				for p in pos:
					fp.seek(p,0) #Seek to the line the prefix is on
					text = fp.readline() #Seek forward the length of the prefix
					if switch.values == "1":
						text = text.translate(TOO_MANY_FALSES)
					else:
						text = list(text.partition("["))
						if text[1] != "":
							text[1] = "!"
						text = text[0] + text[1] + text[2]
					fp.seek(p,0)
					fp.write(text)

		if switch.offPrefixes != "":
			try:
				line,pos = cache.findPrefix(switch.offPrefixes.strip())
			except IndexError:
				pass
			else:
				for p in pos:
					fp.seek(p,0) #Seek to the line the prefix is on
					text = fp.readline() #Seek forward the length of the prefix
					fp.seek(p,0)
					if switch.values == "0":
						text = text.translate(TOO_MANY_FALSES)
					else:
						text = list(text.partition("["))
						if text[1] != "":
							text[1] = "!"
						text = text[0] + text[1] + text[2]
					fp.write(text)
		
	def controlledReplace(fp,cache,switch):
		if len(switch.controlOnString) == len(switch.controlOffString):
			try:
				line,pos = cache.findPrefix(switch.onPrefixes.strip())
			except IndexError:
				pass
			else:
				for p in pos:
					fp.seek(p,0) #Seek to the line the prefix is on
					text = fp.readline()
					if switch.values == "1":
						text = list(text.partition(switch.controlOffString))
						if text[1] != "":
							text[1] = switch.controlOnString
						text = text[0] + text[1] + text[2]
					else:
						text = list(text.partition(switch.controlOnString))
						if text[1] != "":
							text[1] = switch.controlOffString
						text = text[0] + text[1] + text[2]
					fp.write(text)

			try:
				line,pos = cache.findPrefix(switch.offPrefixes.strip())
			except IndexError:
				pass
			else:
				for p in pos:
					fp.seek(p,0) #Seek to the line the prefix is on
					text = fp.readline()
					if switch.values == "0":
						text = list(text.partition(switch.controlOffString))
						if text[1] != "":
							text[1] = switch.controlOnString
						text = text[0] + text[1] + text[2]
					else:
						text = list(text.partition(switch.controlOnString))
						if text[1] != "":
							text[1] = switch.controlOffString
						text = text[0] + text[1] + text[2]
					fp.write(text)

		else: #If the two control strings are of different length
			content = fp.readlines()
			try:
				line,pos = cache.findPrefix(switch.onPrefixes.strip())
			except IndexError:
				pass			
			else:
				for ln in line:
					text = content[ln]
					if switch.values == "1":
						text = list(text.partition(switch.controlOffString))
						if text[1] != "":
							text[1] = switch.controlOnString
						text = text[0] + text[1] + text[2]
					else:
						text = list(text.partition(switch.controlOnString))
						if text[1] != "":
							text[1] = switch.controlOffString
						text = text[0] + text[1] + text[2]
					content[ln] = text

			try:
				line,pos = cache.findPrefix(switch.offPrefixes.strip())
			except IndexError:
				pass
			else:
				for ln in line:
					text = content[ln]
					if switch.values == "0":
						text = list(text.partition(switch.controlOffString))
						if text[1] != "":
							text[1] = switch.controlOnString
						text = text[0] + text[1] + text[2]
					else:
						text = list(text.partition(switch.controlOnString))
						if text[1] != "":
							text[1] = switch.controlOffString
						text = text[0] + text[1] + text[2]
					content[ln] = text
			fp.seek(0)
			fp.writelines(content)
			fp.truncate()
						
						
			
	def numberReplace(fp,cache,switch):
		try:
			line,pos = cache.findPrefix(switch.onPrefixes.strip())
		except IndexError: #Raised if the prefix isn't in this file, so we can skip it
			pass
		else:
			for p in pos:
				fp.seek(p,0) #Seek to the line the prefix is on
				text = fp.readline()
				txt = re.split(r'(\d+)', text)	#Split text around numbers
				try:
					length = len(txt[switch.numberpos*2-1])
				except IndexError:
					print("Someone did something wrong when they wrote that one")
				if length == len(switch.values):
					fp.seek(p,0)
					txt[switch.numberpos*2-1] = switch.values
					text = ""
					for t in txt:
						text += t
					fp.write(text)
				else:  #We have a problem and need to now load in the entire file to do this write
					content = fp.readlines()
					for ln in line:
						text = content[ln]
						txt = re.split(r'(\d+)', text)	#Split text around numbers
						txt[switch.numberpos*2-1] = switch.values
						text = ""
						for t in txt:
							text += t
						content[ln] = text
					fp.seek(0)
					fp.writelines(content)
					fp.truncate()
			
class initManager(rawManager):
	def manage(switches):
		log02.info("Managing a bunch of init edits")
		if switches != []:
			dir =  os.scandir(INIT_FOLDER)
			for file in dir:
				if file.is_file(follow_symlinks=False):
					if file.name in INIT_FILES:
						fp = open(file.name,"r+",1)
						cache = checkHashCache(file) #Check integrity of the cache and  hash on this file
						for switch in switches:
							log02.debug("Performing edits for %s", switch.name.strip())
							if switch.type[0].isdigit:		#Value replacement
								initManager.numberReplace(fp,cache,switch)
							elif switch.controlOnString is "":
								initManager.simpleReplace(fp,cache,switch)
							elif not switch.controlOnString is "" and not switch.controlOffString is "":
								initManager.controlledReplace(fp,cache,swith)
						fp.close()
			dir.close()
		

		

		

class hackManager:
	def manage(switches):
		log02.info("Managing a bunch of DFhack edits")
		if switches != []:
			dir = os.scandir(HACK_FOLDER)
			for file in dir:
				file.is_file(follow_symlinks=False)
				if file.name in HACK_FILES:
					fp = open(file.name,"r+",1)
					for switch in switches:
						log02.debug("Performing edits for %s", switch.name.strip())
						if switch.type[0].isdigit:		#Value replacement
							hackManager.numberReplace(fp,switch)
						else:
							hackManager.hackToggle(fp,switch)
					fp.close()
			dir.close()
				
	def hackToggle(fp,switch):
		contents = fp.readlines()
		for line in contents:
			try:
				line.index(switch.onPrefixes.strip())
			except ValueError:
				pass
			else:
				if switch.values == 1:
					line = line.lstrip("#")
				else:
					line = "#" + line

			try:
				line.index(switch.offPrefixes.strip())
			except ValueError:
				continue
			if switch.values == 0:
				line = line.lstrip("#")
			else:
				line = "#" + line
		fp.seek(0)
		fp.writelines(contents)
		fp.truncate()
	
	def numberReplace(fp,switch):
		contents = fp.readlines()
		for line in content:
			if line.find(fp.onPrefixes.strip()):
				tagnum = 0
				for x,char in enumerate(line):
					if not char.isdigit():	
						left = x
						continue
					tagnum += 1
					while char.isdigit():
						next(line)
					if tagnum == switch.numberpos:
						right = x
						line = line[:left] + switch.values + line[right:]
		fp.seek(0)
		fp.writelines(contents)
		fp.truncate()