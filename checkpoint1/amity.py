import os
from random import randint


class Amity(object):

    __living_max = 4
    __office_max = 6

    def __init__(self):
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.file_path, "data")

    def get_data_file(self):
        """ Function that implements logic of getting data from file """
        try:
            self.input = raw_input(
                "Enter data file  i.e. file.txt\n file name : ")
            # appending file name to data path
            self.file_name = os.path.join(self.data_file, self.input)
            return Amity.get_data(self, 2, self.file_name)
        except IOError as e:
            print("Sorry I/O error({0}): {1}".format(e.errno, e.strerror))
            Amity.get_data_file(self)

    def get_rooms(self):
        """ Function that implements logic of getting rooms from file """
        room_file = os.path.join(self.data_file, "rooms.txt")
        return Amity.get_data(self, 1, room_file)

    def get_data(
        self, iterator, fileName
    ):
        """ Function that implements logic of getting data from file """
        self.room = open(fileName, "r")
        self.room_data = self.room.readlines()
        self.rooms = [x.split() for x in self.room_data]
        self.rooms_dic = {}

        for item in self.rooms:
            key = " ".join(item[:iterator])
            value = item[iterator:]
            self.rooms_dic[key] = value
        self.room.close()
        return self.rooms_dic

    def print_allocations(self):
        """ Function to print all allocations of rooms """
        output_file = os.path.join(self.data_file, "output.txt")
        self.output = open(output_file, "r")
        for line in self.output:
            print line
        self.output.close()

    def check_allocations(self):
        """ check for unallocated rooms """
        status_file = os.path.join(self.data_file, "status.txt")
        self.status_file = open(status_file, "r")
        self.status_data = self.status_file.readlines()
        self.status_output = [x[:len(x) - 1] for x in self.status_data]
        return self.status_output

    def print_unallocated(self):
        """ print all un allocated rooms """
        if self.fellows:
            print "Fellows with no office room allocations"
            print self.fellows

        if self.list_of_Yes_fellows:
            print "Staff with no office room allocations"
            print self.list_of_Yes_fellows

        if self.list_of_staff:
            print "Fellows with no living room allocations"
            print self.list_of_staff

    def allocate(
            self, ilist, iallocate, irooms,
            maxi):
        """ function that handles the logic of allocating people to rooms """
        for i in ilist[:]:
            index = irooms[randint(0, len(irooms) - 1)]
            if not iallocate or iallocate.get(index) == None:
                input_increment = [i]
                count = 1
                input_increment.append(count)
                iallocate[index] = input_increment
                ilist.remove(i)
            elif iallocate[index][1] < maxi:
                iallocate[index][1] += 1
                iallocate[index].append(i)
                ilist.remove(i)

    def allocate_rooms(
            self, people, lrooms,
            orooms):
        """ allocate rooms to fellows and staff """
        self.results = self.check_allocations()
        self.list_of_staff = [
            x for x in people if people[x][0].upper() == "STAFF"]
        self.list_of_Yes_fellows = [x for x in people if people[x][
            0].upper() == "FELLOW" and people[x][1].upper() == "Y"]
        self.list_of_No_fellows = [x for x in people if people[x][
            0].upper() == "FELLOW" and people[x][1].upper() == "N"]
        self.fellows = []
        self.fellows = self.list_of_Yes_fellows + self.list_of_No_fellows
        # check if there are rooms that are not yet full
        if len(self.results) == 0:

            self.allocations = {}
            # allocate staff members to rooms
            self.allocate(self.list_of_staff, self.allocations,
                          orooms, self.__office_max)
            # allocate fellows to offices and living rooms
            self.allocate(self.list_of_Yes_fellows,
                          self.allocations, lrooms, self.__living_max)
            # allocate all fellows to office rooms
            self.allocate(self.fellows, self.allocations,
                          orooms, self.__office_max)
            # write to status and output files
            self.write_to_output_files(self.allocations, lrooms, orooms)

        else:

            self.allocations = self.read_from_output_file()
            el_rooms = [x for x in self.results if x in lrooms]
            eo_rooms = [x for x in self.results if x in orooms]
            # allocate staff members to rooms

            self.allocate(self.list_of_staff, self.allocations,
                          eo_rooms, self.__office_max)
            # allocate fellows to offices and living rooms
            self.allocate(self.list_of_Yes_fellows,
                          self.allocations, el_rooms, self.__living_max)
            # allocate all fellows to office rooms
            self.allocate(self.fellows, self.allocations,
                          eo_rooms, self.__office_max)
            # write to status and output files
            self.write_to_output_files(self.allocations, lrooms, orooms)

    def write_to_output_files(
            self, allocations, lrooms,
            orooms):
        output_file = os.path.join(self.data_file, "output.txt")
        status_file = os.path.join(self.data_file, "status.txt")

        self.output = open(output_file, "w")
        self.status = open(status_file, "w")

        allocated_living_rooms = [x[:len(x)] for x in allocations if x[
            : len(x)] in lrooms]
        allocated_office_rooms = [x[:len(x)] for x in allocations if x[
            : len(x)] in orooms]

        for x in allocations:
            if x[: len(x)] in lrooms:
                self.output.write(str(x) + " (LIVING)\n")
                if allocations[x][1] < self.__living_max:
                    self.status.write(x[:len(x)] + "\n")
            else:
                self.output.write(str(x) + " (OFFICE)\n")
                if allocations[x][1] < self.__office_max:
                    self.status.write(x[:len(x)] + "\n")
            for i in range(len(allocations[x])):
                if i != 1:
                    self.output.write(allocations[x][i])
                    self.output.write(", ")
            self.output.write("\n")

        for item in lrooms:
            if not item in allocated_living_rooms:
                self.status.write(item + "\n")
        for item in orooms:
            if not item in allocated_office_rooms:
                self.status.write(item + "\n")
        self.output.close()
        self.status.close()

    def read_from_output_file(self):
        self.output_info = []
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

            self.output_info.append(line)

        i = 0
        while i <= (len(self.output_info) - 1):
            key = self.output_info[i]
            value = self.output_info[i + 1]
            self.output_dic[key] = value
            i += 2
        self.info.close()
        return self.output_dic

    def return_room_members(self, u_input):
        self.room_name = u_input
        result = []
        if self.room_name:
            self.rooms_info = self.read_from_output_file()
            for x in self.rooms_info:
                if x.upper() == self.room_name.upper():
                    result = self.rooms_info[x]
                    break
        return result
