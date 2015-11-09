# implemented importation on different lines
from amity import Amity
import sys

print "\twelcome to Amity"
print

amity_system = Amity()
list_of_rooms = {}
list_of_people = {}
living_rooms = []
office_rooms = []
switch = False


def allocations(amity, living_rooms, office_rooms):
    while True:
        option = int(raw_input("please select an option\
                \n 1. enter data  file\
                \n 2. print members in a room\
                \n 8. to quit\
                \n input : "))
        if option == 8:
            break
        elif option == 1:
            try:
                list_of_people = amity.get_data_file()
            except IOError:
                print("File does not exist")
                list_of_people = amity.get_data_file()
            if list_of_people:
                amity.allocate_rooms(
                    list_of_people, living_rooms, office_rooms)
            amity.print_allocations()
            print
            amity.print_unallocated()
        elif option == 2:
            user_input = raw_input("please enter room name: ")
            room_members = amity.return_room_members(user_input)
            room_members.pop(1)
            if room_members:
                for i in room_members:
                    print i,
                print
            else:
                print("There are no members in the room")


# get rooms from the text file
try:
    list_of_rooms = amity_system.get_rooms()
    for x in list_of_rooms:
        if x.upper() == "LIVING":
            living_rooms = list_of_rooms[x]
        elif x.upper() == "OFFICE":
            office_rooms = list_of_rooms[x]
    # check if their are rooms
    if living_rooms and office_rooms:
        switch = True
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except ValueError:
    print "Sorry there are not rooms in the file"
except:
    print "Unexpected error:", sys.exc_info()[0]

allocations(amity_system, living_rooms, office_rooms)

# get user input
