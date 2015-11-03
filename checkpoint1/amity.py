import os
from random import randint

class Admin(object):

	__living_max = 4
	__office_max = 6	
	


	"""docstring for Person"""
	def __init__(self):
		self.file_path = os.path.dirname(os.path.abspath(__file__))
		self.data_file = os.path.join(self.file_path, "data")

	"""
	Function that implements logic of getting data from file

	"""
	def getDataFile(self):
		self.input = raw_input("Enter data file  i.e. file.txt\n file name : ")
		self.file_name = "data/" + self.input
		return Admin.getData(self, 2, self.file_name)

	"""
	Function that implements logic of getting rooms from file

	"""
	def getRooms(self):
		room_file = os.path.join(self.data_file, "rooms.txt")
		return Admin.getData(self,1,room_file)

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
	Function to print all allocations of rooms

	"""
	def printAllocations(self):
		output_file = os.path.join(self.data_file, "output.txt")		
		self.output = open(output_file, "r")
		for line in self.output:	
			print line
		self.output.close()


	"""check for unallocated rooms"""
	def checkAllocations(self):
		status_file = os.path.join(self.data_file, "status.txt")
		self.statusFile = open(status_file, "r")
		self.status_data = self.statusFile.readlines()
		self.statusOutput = [  x[:len(x) - 1] for x in self.status_data ]
		return self.statusOutput
		

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

	""" 
	allocate rooms to fellows and staff 
	"""
	def allocateRooms(self, people, lrooms, orooms):
		self.results = self.checkAllocations()
		self.list_of_staff = [ x for x in people if people[x][0].upper() == "STAFF"]
		self.list_of_Yes_fellows = [ x for x in people if people[x][0].upper() == "FELLOW" and people[x][1].upper() == "Y"]
		self.list_of_No_fellows = [ x for x in people if people[x][0].upper() == "FELLOW" and people[x][1].upper() == "N"]
		self.fellows = self.list_of_Yes_fellows + self.list_of_No_fellows 
		#check if there are rooms that are not yet full
		if len(self.results) == 0:

			self.allocations = {}			
			#allocate staff members to rooms
			self.allocate(self.list_of_staff, self.allocations, orooms, self.__office_max)
			#allocate fellows to offices and living rooms
			self.allocate(self.list_of_Yes_fellows, self.allocations, lrooms, self.__living_max)
			#allocate all fellows to office rooms
			self.allocate(self.fellows, self.allocations, orooms, self.__office_max)
			#write to status and output files 
			self.writeToOutputFiles(self.allocations, lrooms, orooms)

		else:

			self.allocations = self.readFromOutputFile()
			el_rooms = [x for x in self.results if x in lrooms]
			eo_rooms = [x for x in self.results if x in orooms]
			#allocate staff members to rooms

			self.allocate(self.list_of_staff, self.allocations, eo_rooms, self.__office_max)
			#allocate fellows to offices and living rooms
			self.allocate(self.list_of_Yes_fellows, self.allocations, el_rooms, self.__living_max)
			#allocate all fellows to office rooms
			self.allocate(self.fellows, self.allocations, eo_rooms, self.__office_max)
			#write to status and output files 
			self.writeToOutputFiles(self.allocations, lrooms, orooms)

			
		


	def writeToOutputFiles(self, allocations, lrooms, orooms):
		output_file = os.path.join(self.data_file, "output.txt")
		status_file = os.path.join(self.data_file, "status.txt")

		self.output = open(output_file, "w")
		self.status = open(status_file, "w")

		Allocated_living_rooms = [x[:len(x)] for x in allocations if x[: len(x)] in lrooms]
		Allocated_office_rooms = [x[:len(x)] for x in allocations if x[: len(x)] in orooms]

		for x in allocations:	
			if x[: len(x)] in lrooms:
				self.output.write(str(x) + " (LIVING)\n")
				if allocations[x][1] < self.__living_max: 
					self.status.write(x[:len(x)] + "\n")
			else:
				self.output.write(str(x) + " (OFFICE)\n")
				if allocations[x][1] < self.__office_max: 
					self.status.write(x[:len(x)] + "\n")
			for i in range(len(allocations[x])) :
				if i != 1 :
					self.output.write(allocations[x][i])
					self.output.write(", ")
			self.output.write("\n")

		for item in lrooms:
			if not item in Allocated_living_rooms:
				self.status.write(item + "\n")
		for item in orooms:
			if not item in Allocated_office_rooms:
				self.status.write(item + "\n")
		self.output.close()
		self.status.close()
		

	def readFromOutputFile(self):
		self.outputInfo = []
		self.output_dic = {}
		output_file = os.path.join(self.data_file, "output.txt")
		self.info = open(output_file, "r")
		for line in self.info:
			line = line.strip()
			if line.find("(LIVING)") != -1:
				line = line.replace("(LIVING)", "")
				line = line.strip()
			elif line.find("(OFFICE)") != -1:
				line = line.replace("(OFFICE)", "")
				line = line.strip()
			else:
				line = line.strip(",")
				line = line.split(', ')
				count = len(line)
				line.insert(1, count)

			self.outputInfo.append(line)

		i = 0
		while i <= (len(self.outputInfo) - 1):
			key = self.outputInfo[i]
			value = self.outputInfo[i + 1]
			self.output_dic[key] = value
			i += 2
		self.info.close()
		return self.output_dic

	def returnRoomMembers(self, u_input):
		self.room_name = u_input
		result = []
		if self.room_name:
			self.rooms_info = self.readFromOutputFile()
			for x in self.rooms_info:
				if x.upper() == self.room_name.upper():
					result = self.rooms_info[x]
					break
		return result
		