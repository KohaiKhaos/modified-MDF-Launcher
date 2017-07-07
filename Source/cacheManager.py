import pickle, hashlib, gzip
import tempfile as tf

#Cache management
class cacheManager:

	class prefixObj:
		def __init__(self,prefix=None,line=None,position=None,):
			self.prefix = prefix.strip()
			self.lines = []					#A list of raw linecounts
			self.pos = []					#A list of file positions to the beginning of lines, as per file.tell()
			self.lines.append(line)
			self.pos.append(position)
		def __lt__(self,other):
			return self.prefix < other.prefix
		def addPos(self,line,position):
			if not type(line) in [list,tuple]:
				self.lines.append(line)
			else:
				self.lines.extend(line)
				
			if not type(position) in [list,tuple]:
				self.pos.append(position)
			else:
				self.pos.extend(position)
				
		def getPos(self):
			return (self.lines, self.pos)
	
	
	class prefixCache:		#Defines the locations of all the of the prefixes in 1 file
		def __init__(self,fileName=None):
			self.fileName = fileName
			self.prefixes = []
		def __iter__(self):
			for x in len(self.line):
				yield self,fileNames[x],self.lines[x],self.pos[x],self.prefix[x]

		def addPrefix(self,prefix,linenum,position):
			self.prefixes.append(cacheManager.prefixObj(prefix,linenum,position))
			
		def compress(self):
			if self.prefixes != [] and self.prefixes != None:
				self.prefixes.sort()
				for x in range(1,len(self.prefixes)):
					try:
						while self.prefixes[x].prefix == self.prefixes[x-1].prefix:	#If two adjacent prefixes match
							self.prefixes[x-1].addPos(self.prefixes[x].getPos()[0] , self.prefixes[x].getPos()[1])			#Add the position data from the latter list to the first
							self.prefixes.pop(x)									#And remove the latter from the list
					except IndexError:												#Then check again until you get a different prefix
						pass
		
		def findPrefix(self,prestring):
			self.prefixes.sort()
			prestring = prestring.strip()
			lower = 0
			upper = len(self.prefixes)-1
			while True:
				p = (lower + upper)//2
				#print(p," ",self.prefixes[p].prefix)
				if lower > upper:
					raise IndexError
				if self.prefixes[p].prefix == prestring:
					#print("Found a match")
					return self.prefixes[p].getPos()
				elif prestring < self.prefixes[p].prefix:
					upper = p-1
					continue
				elif prestring > self.prefixes[p].prefix:
					lower = p+1
					continue

			
	def getCache(filename):
		cache = cacheManager.prefixCache(filename)
		file = open(filename,"r",1)
		pos = file.tell()
		fulline = file.readline()
		linenum = 0
		while fulline != "":
			linenum += 1
			line = fulline.strip()
			if not line.startswith("[") and line != "\n" and line != "":
				try:
					index = max(line.find("["), line.find("{"), line.find("!"))
					if index == -1:
						pos = file.tell()
						fulline = file.readline()
						continue
					prefix = line[:index]
					cache.addPrefix(prefix,linenum,pos)
				except IndexError:
					pass
			pos = file.tell()
			fulline = file.readline()
		file.close()
		return cache
			
	def cacheAllFiles(filenames,cachefile):
		caches = []
		for filename in filenames:
			print(filename)
			cache = cacheManager.getCache(filename)
			cache.compress()
			caches.append(cache)
		cp = gzip.open(cachefile,"wb",1)
		for c in caches:
			pickle.dump(c,cp)
		cp.close()
	
	def cacheFile(filename,cachefile):
		cache = cacheManager.getCache(filename)
		cache.compress()
		cp = gzip.open(cachefile,"ab",1)
		pickle.dump(cache,cp)
		cp.close()
		return cache
	
	def cacheReplace(filename,cachefile):
		cachef = gzip.open(cachefile,"rb",1)
		caches = []
		newcache = cacheManager.getCache(filename)
		newcache.compress()
		try:
			while True:
				oldcache = pickle.load(cachef)
				if newcache.fileName == oldcache.fileName:
					oldcache = newcache
				caches.append(oldcache)
		except EOFError:
			pass
		cachef.close()
		cachef = gzip.open(cachefile,"wb",1)
		for cache in caches:
			pickle.dump(cache,cachef,-1)
			
	def cacheFileGet(filename,cache):
		file = gzip.open(cache,"rb",1)
		try:
			while True:
				cacheitem = pickle.load(file)
				if cacheitem.fileName == filename:
					return cacheitem
		except EOFError:
			raise NoCache



#Hash management
class hashManager:
	class hashlist:
		def __init__(self,fileName,hash):
			self.fileName = fileName
			self.hash = hash
		
	def hashGet(filename):
		file = open(filename,"r",1)
		contents = file.readlines()
		file.close()
		h = hashlib.sha256()
		for line in contents:
			h.update(line.encode('utf-8'))
		return h.hexdigest()
	
	def hashAllFiles(files,dest):
		file = open(dest,"wb")
		for filename in files:
			hash = hashManager.hashlist(filename,hashManager.hashGet(filename))
			pickle.dump(hash,file,-1)
		file.close()
	
	def hashFileWrite(filename,dest):
		hash = hashManager.hashlist(filename,hashManager.hashGet(filename))
		file = open(dest,"ab")
		pickle.dump(hash,file,-1)
		file.close()
		
	def hashReplace(newhash,hashfile):
		hashf = open(hashfile,"rb+")
		hashes = []
		try:
			while True:
				rechash = pickle.load(hashf)
				if newhash.fileName == rechash.fileName:
					rechash = newhash
				hashes.append(rechash)
		except EOFError:
			hashf.close()
			hashf = open(hashfile,"wb")
		for hash in hashes:
			pickle.dump(hash,hashf,-1)
		

	def hashFileCompare(filename,hashes):			#Returns 1 if it finds the associated hash and it matches the current file hash
													#Returns 0 if it cannot find an associated hash or if the recorded hash and current hash differ
		hash = hashManager.hashlist(None,None)
		recHash = None
		file = open(hashes,"rb",1)
		while True:
			try:
				recHash = pickle.load(file)
				if recHash.fileName == filename:
					break
			except EOFError:
				file.close()
				print("File not found")
				raise NoHash
		file.close()
		currHash = hashManager.hashlist(filename,hashManager.hashGet(filename))
		if recHash.hash == currHash.hash:
			return 1
		else:
			print(filename, "\nWrong hash: ",recHash.hash,"\nWith: ",currHash.hash)
			hashManager.hashReplace(currHash,hashes)
			raise WrongHash
			
			
class NoHash(Exception):
	pass
class WrongHash(Exception):
	pass
class NoCache(Exception):
	pass