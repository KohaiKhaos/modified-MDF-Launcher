import pickle
import hashlib

#Cache management
class cacheManager:
	class prefixCache:
		def __init__(self,fileName):
			self.fileName = fileName
			self.prefixlist = [[]]

	def cacheFileWrite(filename,dest):			#Before calling cacheFile the first time in a run, clear the contents of dest; dest is a binary file
		
		prefixlist = [[]]

		#First, let's read the contents of the file called filename	
		file = open(filename,"r",1)
		contents = file.readlines()
		file.close()
		for linenum,line in enumerate(contents):
			line = line.strip()
			if not line.startswith("[") and line != "\n" and line != "":
				try:
					prefix = line[:line.index("{")]
				except ValueError:
					continue
				if prefixlist == [[]]:
					prefixlist = [[prefix,linenum]]
				else:
					prefixlist.append([prefix,linenum])
			else:
				pass
		
		#Now let's convert that into a useful, short-form cache
		prefixlist.sort()
		for x in range(1,len(prefixlist)):
			try:
				while prefixlist[x][0] == prefixlist[x-1][0]:	#If two adjacent prefixes match
					prefixlist[x-1].append(prefixlist[x][1])	#Add the line number from the latter list to the first
					prefixlist.pop(x)							#And remove the latter from the list
			except IndexError:									#Then check again until you get a different prefix
				pass
		
		#prefixlist now contains a shortened cache
		#So let's make a cache file
		cache = cacheManager.prefixCache(filename)
		cache.prefixlist = prefixlist
		file = open(dest,"ab")
		pickle.dump(cache,file,-1)
		file.close()
	
	def cacheSearch(prefix,cache,rawfile=None):
		cacheContents = []
		file = open(cache,"rb",1)
		try:
			if rawfile == None :			#If there is no rawfile, so all files must be processed
				while True:
					prelist = cacheManager.prefixCache(None)
					prelist = pickle.load(file)
					if cacheContents == []:
						cacheContents = [prelist]
					else:
						cacheContents.append(prelist)
			
			elif type(rawfile) in [list,tuple] :	#If rawfile is a list of files
				while True:
					prelist = cacheManager.prefixCache(None)
					prelist = pickle.load(file)
					if prelist.fileName in rawfile:
						if cacheContents == []:
							cacheContents = [prelist]
						else:
							cacheContents.append(prelist)

			else:									#If rawfile is a single file
				while True:
					prelist = cacheManager.prefixCache(None)
					prelist = pickle.load(file)
					if prelist.fileName is rawfile:
						if cacheContents == []:
							cacheContents = [prelist]
						else:
							cacheContents.append(prelist)
						break

		except EOFError:
			pass
		file.close()
		returnvals = []
		for files in cacheContents:
			for prefixes in files.prefixlist:
				try:
					if prefixes[0] in prefix:
						if returnvals == []:
							returnvals = [files.fileName,prefixes[1:]]
						else:
							returnvals.append(files.fileName,prefixes[1:])
				except IndexError:
					pass
		return returnvals


				
	
	
	
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
		
	def hashFileWrite(filename,dest):
		hash = hashManager.hashlist(filename,hashManager.hashGet(filename))
		file = open(dest,"ab")
		pickle.dump(hash,file,-1)
		file.close()
		
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
				print("File not found")
				return 0
		currHash = hashManager.hashGet(filename)
		print(currHash)
		print(recHash.hash)
		if recHash.hash == currHash:
			return 1
		else:
			return 0