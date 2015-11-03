import amity, sys 

print "\twelcome to Amity"
print

object1 = amity.Admin()
list_of_people = {}
list_of_rooms = {}
living_rooms = []
office_rooms = []
switch = False
switch1 = False

#get rooms from the text file
try:

	list_of_rooms = object1.getRooms()
	for x in list_of_rooms:
		if x.upper() == "LIVING" :
			living_rooms = list_of_rooms[x]
		elif x.upper() == "OFFICE":
			office_rooms = list_of_rooms[x]
	#check if their are rooms 
	if living_rooms and office_rooms:
		switch = True
except IOError as e:
	print "I/O error({0}): {1}".format(e.errno, e.strerror)
except ValueError:
    print "Sorry there are not rooms in the file"
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

try:

	while switch:
		option = int(raw_input("please select an option\
			\n 1. enter data  file\
			\n 2. print members in a room\
			\n 8. to quit\
			\n input : "))
		if option == 8:
			break
		elif option == 1:
			list_of_people = object1.getDataFile()
		elif option == 2:
			user_input = raw_input("please enter room name: ")
			room_members = object1.returnRoomMembers(user_input)
			i = 0
			for i in range(len(room_members)):
				if i == 1:
					pass
				else:
					print room_members[i] + " ", 
			break


	if list_of_people:
		switch1 = True
except IOError as e:
	print "I/O error({0}): {1}".format(e.errno, e.strerror)
except ValueError:
    print "You entered Unexpected data."
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise


while switch1:
	#object1.allocateRooms(list_of_people, living_rooms, office_rooms)
	print
	object1.printAllocations()
	object1.printUnAllocated()
	print 
	break

