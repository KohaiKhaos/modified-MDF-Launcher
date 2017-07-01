def configParse() :
	config = open("main.cfg","rt",1)
	lines = config.readlines()
	listmods = []
	listpri = []
	listsec = []
	listter = []
	listqua = []
	listqin = []
	try:
		lines.remove("\n")
	except ValueError:
		pass
	for line in lines:
		if line.startswith("//"):
			lines.remove(line)
			
	for x in range(0,len(lines)):
		
		
		if lines[x].startswith("###"): 																		#Option name
			try:
				if listpri != []:
					listpri.append(lines[x+2][:-1]+lines[x+1][:-1])
				else:
					listpri = [lines[x+2][:-1]+lines[x+1][:-1]]
			except IndexError:
				pass
		
		
		if lines[x].startswith("!###:"):																	#Mod names
			if listmods != []:
				listmods.append(lines[x][5:-1])
			else:
				listmods = [lines[x][5:-1]]
				
				
		if lines[x].startswith("#!!!#") or lines[x].startswith("!###!") or lines[x].startswith("!###:") or lines[x].startswith("!!###!!"):
																											#Columns within a block
			if listpri != []:
				if listsec != []:
					listsec.append(listpri)
				else:
					listsec = [listpri]
			listpri = []
			
			
		if lines[x].startswith("!###:") or lines[x].startswith("!###!") or lines[x].startswith("!!###!!"):	#Separate blocks
			if listsec != []:
				if listter != []:
					listter.append(listsec)
				else:
					listter = [listsec]
			listsec = []
			
			
		if lines[x].startswith("!###!") or lines[x].startswith("!!###!!"):									#Separate columns
			if listter != []:
				if listqua != []:
					listqua.append(listter)
				else:
					listqua = [listter]
			listter = []
			
			
		if lines[x].startswith("!!###!!"):																	#Separate pages
			if listmods != []:
				if listqin != []:
					listqin.append(listmods)
				else:
					listqin = [listmods]
			if listqin != []:
				if listqin != []:
					listqin.append(listqua)
				else:
					listqin = [listqua]
			listqua = []
			listmods = []
	return listqin