from random import randint

class Admin(object):

	__living_max = 4
	__office_max = 6


	"""docstring for Person"""
	def __init__(self):
		pass

	"""
	Function that implements logic of getting data from file

	"""
	def getDataFile(self):
		self.input = raw_input("Enter data file  i.e. file.txt\n input : ")
		self.file_name = "data/" + self.input
		return Admin.getData(self, 2, self.file_name)

	"""
	Function that implements logic of getting rooms from file

	"""
	def getRooms(self):
		return Admin.getData(self,1,"data/rooms.txt")

	"""
	Function that implements logic of getting data from file

	"""
	def getData(self, iterator, fileName):
		self.room = open(fileName, "r")
		self.roomData = self.room.readlines()
		self.rooms = [  x.split() for x in self.roomData ]
		self.rooms_dic = {}

		for item in self.rooms:
			key = " ".join(item[:iterator])
			value = item[iterator:]
			self.rooms_dic[key] = value
		self.room.close()
		return self.rooms_dic
	

	""" 
	allocate rooms to fellows and staff 

	"""
	def allocateRooms(self, people, lrooms, orooms):
		
		self.allocations = {}
		count = 0
		self.list_of_staff = [ x for x in people if people[x][0].upper() == "STAFF"]
		self.list_of_Yes_fellows = [ x for x in people if people[x][0].upper() == "FELLOW" and people[x][1].upper() == "Y"]
		self.list_of_No_fellows = [ x for x in people if people[x][0].upper() == "FELLOW" and people[x][1].upper() == "N"]
		self.fellows = self.list_of_Yes_fellows + self.list_of_No_fellows 
		
		#allocate staff members to rooms
		self.allocate(self.list_of_staff, self.allocations, orooms, self.__office_max)
		#allocate fellows to offices and living rooms
		self.allocate(self.list_of_Yes_fellows, self.allocations, lrooms, self.__living_max)
		#allocate all fellows to office rooms
		self.allocate(self.fellows, self.allocations, orooms, self.__office_max)

		self.output = open("data/output.txt", "w")
		for x in self.allocations:	
			if x[: len(x)] in lrooms:
				self.output.write(str(x) + " (LIVING)\n")
			else:
				self.output.write(str(x) + " (OFFICE)\n")
			for i in range(len(self.allocations[x])) :
				if i != 1 :
					self.output.write(self.allocations[x][i])
					self.output.write(", ")
			self.output.write("\n")
		self.output.close()


	"""
	Function to print all allocations of rooms

	"""
	def printAllocations(self):
		self.output = open("data/output.txt", "r")
		for line in self.output:	
			print line
		self.output.close()


	"""check for allocated rooms"""
	def checkAllocations(self):
		self.statusFile = open("data/status.txt", "r")
		self.status_data = self.statusFile.readlines()
		self.statusOutput = [  x.split() for x in self.status_data ]
		self.status_dic = {}

		for item in self.statusOutput:
			key = " ".join(item[0:2])
			value = item[2:]
			self.status_dic[key] = value
		self.statusFile.close()
		print self.status_dic




	"""print all un allocated rooms"""
	def printUnAllocated(self):
		if self.fellows:
			print "Fellows with no office room allocations"
			print self.fellows
			print

		if self.list_of_Yes_fellows:
			print "Staff with no office room allocations"
			print self.list_of_Yes_fellows
			print

		if self.list_of_staff:
			print "Fellows with no living room allocations"
			print self.list_of_staff
			print

	"""
	function that handles the logic of 
	allocating people to rooms
	"""
	def allocate(self, ilist, iallocate, irooms, maxi):
		for i in ilist[:] :
			index = irooms[randint(0,len(irooms) - 1)]
			if not iallocate or iallocate.get(index) == None :
				inputA = [i]
				count = 1
				inputA.append(count)
				iallocate[index] = inputA
				ilist.remove(i)
			elif iallocate[index][1] < maxi :
				iallocate[index][1] += 1
				iallocate[index].append(i)
				ilist.remove(i)