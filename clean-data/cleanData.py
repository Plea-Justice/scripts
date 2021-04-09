# -*- coding: utf-8 -*-
import csv
import pprint
from collections import OrderedDict

# here lies the names of the files that the cleaner will be pertaining to.
# file_name_in is case sensitive, while file_name_out & file_name_out_deleted
# are output files that you may name however you'd like.
file_name_in = "Grant-102519.csv"
file_name_out = "output_Grant-102519.csv"
file_name_out_deleted = "output_Grant-102519_deleted_rows.csv"

# unique ID variable names differ from one experiment to another. change the
# character strings following ID_beginning and ID_end to fit accordingly.
ID_beginning = "Q99_1"
ID_end = "SONA_end"

# change this value to 1 if the data is from within participants (2 rows)
# change this value to 0 if the data is for other survey flows (3 rows)
is_WithinParticipants = 0

#==============================================================================
# modifiable variables are above, functions and the main code are below
#==============================================================================

def check_unique_header(header_list):
    """
    Summary:
        Takes in the header found in the CSV and checks all elements if they are
        unique. Used for checking if data on multiple rows can be combined via
        unique entries in a dictionary.
    Returns:
        A list of duplicate elements within the header; an empty list (false)
    """
    dupeList = []
    if (len(set(header_list)) != len(header_list)):
        for each in header_list:
            if header_list.count(each) > 1 and each not in dupeList:
                dupeList.append(each)
    return dupeList

def converge_data(dictionary, csv_row, header):
    """
    Summary:
        takes a specific row in the CSV and uses the header to update the
        dictionary via matching the LinkID.
    Returns:
        None. the dictionary is edited with updated combined data entries.
    """
    if dictionary.get(csv_row[LinkID]) == None: # create the LinkID entry if its not there
        dictionary[csv_row[LinkID]] = OrderedDict()
        for index, each in enumerate(header):
            # populate each LinkID with all items in the headers
            dictionary[csv_row[LinkID]][header[index]] = csv_row[index]
    else: # populate it with specific conditions, starting with unconditional copy
        for index, each in enumerate(line):
            if dictionary[csv_row[LinkID]][header[index]] == "": # unconditional copy
                dictionary[csv_row[LinkID]][header[index]] = csv_row[index]

            if index == email and len(csv_row[index]) > 1:
                # if not (csv_row[email] == "" or csv_row[email == ","]):
                # print("2 " + dictionary[csv_row[LinkID]][header[index]] +" : " +  csv_row[index])
                dictionary[csv_row[LinkID]][header[index]] = csv_row[index].split(",")[0]

            elif index == duration: # sum of the durations
                dictionary[csv_row[LinkID]][header[index]] = str(int(csv_row[index]) +\
                int(dictionary[csv_row[LinkID]][header[index]]))

def write_output_file(output_file_name, dictionary, header1, header2, header3):
    """
    Summary:
        creates a .csv file with the given output_file_name with the dictionary.
        The dictionary is typically populated with updated participant data.
    Returns:
        None
    """
    with open(output_file_name,"w", newline='\n', encoding='utf-8') as outfile:
        csvwriter = csv.writer(outfile, quotechar='"', delimiter=',',
        quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
        csvwriter.writerow(header1)
        csvwriter.writerow(header2)
        if not is_WithinParticipants:
            csvwriter.writerow(header3)
        for each_LinkID in dictionary:
            csvwriter.writerow(dictionary[each_LinkID].values())

#==============================================================================
# functions are above, main code and opening the file is below
#==============================================================================

with open(file_name_in,"r", newline='\n', encoding='utf-8') as file:
    csvreader = csv.reader(file, quotechar='"', delimiter=',',
    quoting=csv.QUOTE_ALL, skipinitialspace=True)

    header = next(csvreader)            # list of headers
    content = next(csvreader)           # list of the actual content
    if not is_WithinParticipants:
        importID = next(csvreader)      # list of variable names as importIDs
    else:
        importID = 0

    dupeList = check_unique_header(header)
    if dupeList is True:
        print("The following items in the Header are not uniquely named:")
        for each in dupeList:
            print(each)
        print("dupeList:")
        print(dupeList)
        print("Because all header items are not unique,\n"
        "the cleaned data is vertically misaligned.")

    participants = OrderedDict() # map of LinkID -to> data
    invalid_rows = OrderedDict() # map of LinkID -to> data but 123456 as a test ID

    # important indexes:
        # duration: sum of all 3 or 2 durations (depending how data was split)
        # email:    column containing the email; making sure the email makes sense
        # LinkID:      match other rows of LinkID (unique value for each participant)
        # ID_1
        # and ID_2: both of these refer to the unique ID entered at the
        #           beginning and end of the experiment, respectively
    duration = header.index("Duration (in seconds)")
    email = header.index("email")
    LinkID = header.index("LinkID")
    ID_1 = header.index(ID_beginning)
    ID_2 = header.index(ID_end)

    for line in csvreader:
        if line[ID_1] == "123456" or line[ID_2] == "123456":
            converge_data(invalid_rows, line, header)
        else:
            converge_data(participants, line, header)

    # if line[SONA_end] != line[Q99_1]:
    #     temp = [line[SONA_end], line[Q99_1], line[LinkID]]
    #     print("the following SONA_end and Q99_1 are mismatched", temp)
    # print("")
            # if participants[line[LinkID]][each] == "":
            #     participants[line[LinkID]][each] = line[index]
    # commented segment tries to detect mismatch of SONA_end and Q99_1

write_output_file(file_name_out, participants, header, content, importID)
if bool(invalid_rows) is not False:
    write_output_file(file_name_out_deleted, invalid_rows, header, content, importID)
# pprint.pprint(participants)
