#!/usr/bin/env python

# Import statements
import inspect
import sys
import os




# Program: a4.py

# Programmer Name: Richard Mangerie

# Last Updated: 06/10/2017

# Program Overview: this program displays or updates contents of an album database

# Detailed Description: a database file is traversed and the contents of the database are added to a dictionary
#                       this dictionary is then traversed and specific contents of the dictionary are either
#                       displayed or removed
#                       the contents of the dictionary are then traversed and used to update the original database file

# Code Structure: there are eight methods in total:
#                       make_album(), make_database(), remove_endline(),
#                       list_artists(), list_albums_tracklists(), delete_album(), add_album(), and usage_msg()
#                 there are three methods used to access or mutate the database:
#                       make_album(), make_database() and remove_endline()
#                 the user specifies a parameter to the program, which will call one of four method:
#                       list_artists(), delete_album(), add_album(), or usage_msg()
#                 there is one helper method for list_artists(), called list_albums_tracklists()         







# The global dictionary of artists and years

# artists_and_years: { key = string: artist name, value = dictionary: { key = string: release year, value = dictionary:
#                    { key = string: album name, value = list: (tracklist) } } }

# artists_and_years: { artist name : { release year : { album name : ( tracklist ) } } }

artists_and_years = dict()

# Global variable for the database filename
filename = ""








# Method make_album(): will make an album from the supplied database file db

# Arguments: None

# Preconditions: global string filename has to contain a valid album database filename

# Postconditions: global dictionary artists_and_years will contain a new key and value
#                 NOTE: This new key-value could be contained within one of the nested dictionaries of artists_and_years

def make_album():

    # Global variable that contains all artist and album information
    global artists_and_years

    # Global variable that contains the filename of the output database
    global filename

    # Method variables
    artist_name = ""
    year_and_album = ""
    release_year = ""
    album_name = ""
    track_list = list()

    # Opening the file specified by string filename
    db = open(filename)

    # Using the file db as the input
    with db as input:

        # Empty list
        sections = list()
        # Empty string
        sect = ''

        # Getting every line in input
        for line in input:
            # If the line is not a newline
            if line != '\n':
                # Add the line to the string sect
                sect += line
            # If the line is a newline
            else:
                # Append the current section to the list sections
                sections.append(sect)
                # Empty the string sect
                sect = ''
        # If at the end of the file, make sure that the last section is appended
        sections.append(sect)

        # Making a temporary variable for sections, since the main one will be mutated
        temp_sections = sections

    # Iterator, set to 0
    i = 0

    # For each section in the list temp_sections
    for section in temp_sections:
        # Making a list for each line within the list sections (nested list)
        sections[i] = section.split('\n')
        i = i + 1

    # Going through each section in the list sections
    for section in sections:

        # Iterator, set to 0
        i = 0

        # Strings that will contain artist information
        artist_name = ""
        year_and_album = ""
        album_name = ""
        release_year = ""
        track_list = []

        # Going through each artist attribute per section
        for attr in section:

            # If the iterator is at 0, that line is the artist
            if i == 0:
                artist_name = attr
            # If the iterator is at 0, that line is the year and album
            elif i == 1:
                year_and_album = attr
                # Splitting the year and album into two separate values
                year_and_album = year_and_album.split(" ", 1)
                # Putting the year and album name in their own variables
                release_year = year_and_album[0]
                album_name = year_and_album[1]
            # If the iterator is at any other value, that line is a track in the album
            else:
                # Getting the current track
                track = attr.replace("-", "", 1)  # Stripping the track of its leading dash
                # Appending the current track to the list track_list
                track_list.append(track)

            i = i + 1

        # Removing any blank values in the list track_list
        track_list = filter(None, track_list)

        # If the current artist is already in the dictionary, append the album information to that artist
        if artists_and_years.has_key(artist_name):

            # A dictionary of the years and the albums of that year
            years_and_albums = artists_and_years.get(artist_name)

            # If the release year already exists for the artist
            if years_and_albums.has_key(release_year):

                # A dictionary of the albums and tracklists of that year
                albums_and_tracklists = years_and_albums.get(release_year)
                # Adding the current album to the release year dictioary
                albums_and_tracklists.update({album_name: track_list})

            # If the release year does not exist for the artist
            else:

                # Adding the current album as a sole value for the release year
                years_and_albums.update({release_year: {album_name: track_list}})

        # If the current artist is not in the dictionary,
        # make a new artist key and make the value the album information
        else:
            artists_and_years[artist_name] = {release_year: {album_name: track_list}}

    # Closing the database file
    db.close()







# Method make_database(): will form the new database of albums

# Arguments: None

# Preconditions: global string filename has to contain a valid album database filename

# Postconditions: the database file specified by global string filename will be updated

def make_database():

    # Global variable
    global filename

    # The temp filename
    temp_filename = "temp_albums.db"

    # Opening the file temp_filename and writing over the values in it
    temp_file = open(temp_filename, "w")

    # Global variable that contains all artist and album information
    global artists_and_years

    # Getting a list of the artists
    artists = artists_and_years.keys()

    # Going through each artist
    for a in artists:

        # Setting the variable artist to a: the current artist
        artist = a

        # Getting the years and albums dictionary for the current artist
        years_and_albums = artists_and_years.get(artist)

        # Getting a list of each release year
        years = years_and_albums.keys()

        # Going through each release year
        for y in years:

            # Setting the variable year to y: the current release year
            year = y

            # Getting the albums and tracklists dictionary for the current release year
            albums_and_tracklists = years_and_albums.get(year)

            # Getting a list of each album per year
            albums = albums_and_tracklists.keys()

            # Going through each album
            for a in albums:

                # Setting the variable album to a: the current album
                album = a

                # Getting the tracklist for the current album
                tracklist = albums_and_tracklists.get(album)

                # Writing the current artist name to the database
                temp_file.write(artist + "\n")
                # Writing the current year and album name to the database
                temp_file.write(year + " " + album + "\n")

                # Iterator, set to 0
                n = 0

                # Going through each track in the tracklist
                for t in tracklist:

                    # Setting the variable track to t: the current track
                    track = t

                    # Increasing the iterator by 1
                    n = n + 1

                    # If n is the same value as the length of the list, we are at the end of this album
                    if n == len(tracklist):

                        # Write the current track to the database with a preceding dash
                        temp_file.write("-" + track + "\n\n")  # Two newlines to space out albums

                    # If n is a different value than the length of the list, we are still within the tracklist
                    else:

                        # Write the current track to the database with a preceding dash and a newline
                        temp_file.write("-" + track + "\n")

    # Closing the tempfile
    temp_file.close()

    # Calling the method to remove the last line from the database
    remove_endline()

    # Replacing the main database with the temporary database
    os.rename(temp_filename, filename)









# Method remove_endline(): Removes the endline from the temp database file due to an extra unwanted newline that is
#                          produced at the end of the temp database

# Arguments: None

# Preconditions: global string filename has to contain a valid album database filename
#                and a file with the name temp_albums.db must exist

# Postconditions: the database file specified by global string filename will be updated

def remove_endline():

    # Getting the name of the temporary database
    temp_filename = "temp_albums.db"

    # Reading text from the temp database
    read_temp = open(temp_filename)

    # Getting all of the lines of the temp database
    lines = read_temp.readlines()

    # Closing the temp database
    read_temp.close()

    # Reopening the temp database, this time writing to it
    write_temp = open(temp_filename, 'w+')

    # Writing all of the lines to the database except for the last one
    write_temp.writelines([item for item in lines[:-1]])

    # Closing the temp database
    write_temp.close()








# Method list_artists(): will list the artists in the database

# Arguments: string caller, which will be empty if and argument is not passed to the method

# Preconditions: the passed argument caller has to be a string
#                and global string filename has to contain a valid album database filename

# Postconditions: the method list_albums_tracklists will be called with passed parameters
#                 string artist_name and string caller or the method make_database() will be called

def list_artists(caller=""):

    # Global variable
    global artists_and_years

    # Global variable
    global filename

    # Default value
    repeat = True


    # Getting a string "caller" that specifies which method called the current method
    if caller == "":  # Only change the string caller if no variable is passed into the method list_artists
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller = calframe[1][3]

    # Printing only if string caller does not equal "delete_album"
    if caller != "delete_album":
        # Description of what is to be done by this method
        print "Listing chosen album:"

    # Getting a list of the artists
    artists = sorted(artists_and_years.keys())
    # Empty dictionary
    num_and_artist = dict()

    # While the boolean repeat equals true
    while repeat:

        # Iterator, starts at 0
        n = 0


        # Display message
        print "\nAritsts in database, listed alphabetically:"

        # Goes through each artist
        for a in artists:
            # Increasing the iterator
            n = n + 1

            # Printing the iterator and artist number
            print str(n) + ". " + a

            # Placing both the iterator and artist name as a dictionary key:value
            num_and_artist.update({n: a})

        # Getting user input for an artist choice
        artist_choice = raw_input("\nEnter an artist by number (enter q to quit): ")

        # If the user typed in a number
        if artist_choice.isdigit():

            # Set the variable artist_choice as what the user chose
            artist_choice = int(artist_choice)

            # If the user chose a number larger than the number of artists, print a message
            if artist_choice > n:

                print "\nEnter a valid artist number!"

            # If the user chose a number that is a number for an artist, stop the while-loop
            else:

                repeat = False

        # If the user did not type in a number
        else:

            # If the user typed "q", quit the program
            if artist_choice == "q":

                # Making the new database under the filename
                make_database()

                # Return statement, quits the method
                return None

            # If the user did not type a "q", print a message
            else:

                print "\nPlease enter valid input!"

    # Getting the artist name that the user chose
    artist_name = num_and_artist.get(artist_choice)

    # Calling the method list_albums_tracklists with the paraemters artist_name and caller
    list_albums_tracklist(artist_name, caller)

    # Return statement, quits the method
    return None








# Method list_albums_tracklist(): will list the albums for the chosen artist and the tracklist for the chosen album

# Arguments: string artist_name, string caller

# Preconditions: the passed arguments artist_name and caller have to be string
#                and global string filename has to contain a valid album database filename

# Postconditions: the method list_albums() will be called with parameter string caller
#                 -OR-
#                 the method delete_album() will be called with parameters
#                 string artist_name, string release_year, and string album_name
#                 -OR-
#                 the method list_albums_tracklists() will be called with parameters
#                 string artist_name and string caller
#                 -OR-
#                 the method make_database() will be called

def list_albums_tracklist(artist_name, caller):

    # Global variable
    global artists_and_years

    # Global variable
    global filename

    # Default value
    repeat = True

    # Getting the dictionary of years and albums from the global dictionary based on the parameter input
    years_albums = artists_and_years.get(artist_name)

    # Sorting the years and storing them in a list
    years = sorted(years_albums.keys())

    # Local dict
    num_and_years_albums = dict()

    # While the boolean repeat equals true
    while repeat:

        # Iterator, set to 0
        n = 0

        # Display message
        print "\nAlbums for " + artist_name + ", listed chronologically:"

        # Going through each release year for the artist
        for y in years:
            # Getting the albums and tracklists for that year
            albums_tracklists = years_albums[y]

            # Sorting the albums for that year and storing them in a list
            albums = sorted(albums_tracklists.keys())

            # Going through each album for the release year
            for al in albums:
                # Increasing the itertor by 1
                n = n + 1

                # Printing the iterator as a string and the album name
                print str(n) + ". " + al

                # Placing both the iterator and a list of the year and album name as a dictionary key:value
                num_and_years_albums.update({n: [y, al]})

        # If the caller method was delete_album()
        if (caller == "delete_album"):
            # Getting the user's album choice number to delete
            album_choice = raw_input("\nEnter an album by number to delete (enter a to go back to artists menu): ")
        # If the caller method was not delete_album()
        else:
            # Getting the user's album choice number
            album_choice = raw_input("\nEnter an album by number (enter a to go back to artists menu): ")

        # If the user choice is a digit
        if album_choice.isdigit():

            # Convert choice to an int and store it in album_choice
            album_choice = int(album_choice)

            # If the int is greater than the number of choices, print out a message
            if album_choice > n:

                print "\nEnter a valid album number!"

            # If the int is within the number of choices, set repeat to false
            else:

                repeat = False

        # If the user choice is not a digit
        else:

            # If the user input was "a"
            if album_choice == "a":

                # Go back to the list_artists method with parameter caller
                list_artists(caller)
                # Quit the current method
                return None

            # If the user input was not "a", print a message
            else:

                print "\nPlease enter valid input!"

    # Getting the release year and the album list from the dictionary year_album
    year_album = num_and_years_albums.get(album_choice)

    # Getting the release year and album name from the list year_album
    release_year = year_album[0]
    album_name = year_album[1]

    # If the caller method was delete_album()
    if caller == "delete_album":

        # Call delete_album and send artist_name, release_year, and album_name
        delete_album(artist_name, release_year, album_name)

        # Exit out of the method
        return None

    # If the caller method was not delete_album()
    else:

        # Getting the album and tracklist dictionary from the dictionary years_albums
        albums_tracklists = years_albums.get(release_year)

        # Getting the tracklist from the dictionary albums_tracklists
        tracklist = albums_tracklists.get(album_name)

        # Iterator, set to 0
        i = 0

        # Display message
        print "\nTracklist for " + album_name + ":"

        # Going through each track in the tracklist
        for t in tracklist:
            # Increasing the iterator by 1
            i = i + 1

            # Printing the current track in the tracklist
            print str(i) + ". " + t

        # Reset repeat to equal true
        repeat = True

        # While repeat equals true
        while repeat:

            # Getting user input
            menu_choice = raw_input("\nWould you like to return to the albums menu? (y/n): ")

            # If the user choice is a number, print out a message
            if menu_choice.isdigit():

                print "\nPlease enter valid input!"

            # If the user choice is not a number
            else:

                # If the user choice is "y"
                if menu_choice == "y":

                    # Go back to the main list screen with parameters artist_name and caller
                    list_albums_tracklist(artist_name, caller)
                    # Setting repeat to false
                    repeat = False
                    # Exiting the current method
                    return None

                # If the user choice is "n"
                elif menu_choice == "n":

                    # Calling the make_database method and quitting the program
                    make_database()
                    # Exiting the current method
                    return None

                # If the user choice is not "y" or "n", print out a message
                else:

                    print "\nPlease enter valid input!"










# Method delete_album(): deletes a specified album from the database

# Arguments: string artist_name, string release_year, string album_name
#            if no arguments are passed, these strings are empty

# Preconditions: the passed arguments artist_name, release_year, and album_name have to be strings
#                and global string filename has to contain a valid album database filename

# Postconditions: the method list_artists() will be called
#                 -OR-
#                 the method make_database() will be called
#                 and a key and value pair from global dictionary artists_and_years will be removed
#                 NOTE: This key and value could be contained within one of the nested dictionaries of artists_and_years

def delete_album(artist_name="", release_year="", album_name=""):

    # The global dictionary
    global artists_and_years

    # If no parameters were sent
    if not artist_name and not release_year and not album_name:

        # Description of what is to be done by this method
        print "Deleting album from database:"

        # Listing the artists and albums in the dictionary
        list_artists()

        # Quitting the method
        return None

    # If parameters were sent
    else:
        # Deleting the album specified
        years_and_albums = artists_and_years.get(artist_name)
        albums_and_tracklists = years_and_albums.get(release_year)
        del albums_and_tracklists[album_name]

        # Making the albums database
        make_database()

        # Confirmation message
        print "\nAlbum deleted from database!"

        # Quitting the method
        return None









# Method add_album(): adds a specified album to the database

# Arguments: None

# Preconditions: the passed arguments artist_name, release_year, and album_name have to be strings
#                and global string filename has to contain a valid album database filename

# Postconditions: the method make_database() will be called
#                 and global dictionary artists_and_years will contain a new key and value
#                 NOTE: This key and value could be contained within one of the nested dictionaries of artists_and_years

def add_album():

    # Global dictionary
    global artists_and_years

    # Global variable
    global filename

    # list track_list
    track_list = list()

    # Setting repeat to true
    repeat = True

    # Setting isNotValidYear to true
    isNotValidYear = True

    # Description of what is to be done by this method
    print "Adding album to database:\n"

    # Checking if the album already exists in the database
    while repeat:

        # Getting from user artist_name, album_name, and release_year
        artist_name = raw_input("Artist name: ")
        album_name = raw_input("Album name: ")
        release_year = raw_input("Release year: ")

        while isNotValidYear:

            if release_year.isdigit() != True:

                print "\nPlease enter a valid year!\n"

                release_year = raw_input("Release year: ")

            else:

                isNotValidYear = False

        # If the artist already exists in the database
        if artists_and_years.has_key(artist_name):

            # Dictionary containing release years and albums for the chosen artist
            years_and_albums = artists_and_years.get(artist_name)

            # If the release year for the chosen artist already exists in the database
            if years_and_albums.has_key(release_year):

                # Dictionary containing albums and tracklists for the chosen release year
                albums_and_tracklists = years_and_albums.get(release_year)

                # If the album for the chosen release year already exists in the database
                if albums_and_tracklists.has_key(album_name):

                    # Prompt to the user that the album already exists, then prompt again for an album
                    print "\nThat album has already been entered for that artist!\n"

                # If the album for the chosen release year does not exist in the database,
                # then the album does not exist in the database
                else:

                    repeat = False

            # If the release year for the chosen artist does not exist in the database,
            # then the album does not exist in the database
            else:

                repeat = False

        # If the artist does not exist in the database, then the album does not exist in the database
        else:

            repeat = False

    # Settning the current track to the user input
    current_track = raw_input("\nTrack list (enter -1 to finish):\n")

    # While the current track does not equal "-1
    while (current_track != "-1"):
        # Append the current track to the list track_list
        track_list.append(current_track)

        # Get another track
        current_track = raw_input()

    # If the database already contains the chosen artist
    if artists_and_years.has_key(artist_name):

        # Dictionary containing release years and albums for the chosen artist
        years_and_albums = artists_and_years.get(artist_name)

        # If the database already contains the release year for the chosen artist
        if years_and_albums.has_key(release_year):

            # Dictionary containing albums and tracklists for the chosen release_year
            albums_and_tracklists = years_and_albums.get(release_year)

            # Appending the user-inputted album and tracklist to the chosen release year
            albums_and_tracklists.update({album_name: track_list})

        # If the database does nto contain the release year for the chosen artist
        else:

            # Appending the user-inputted album and tracklist to the chosen artist
            years_and_albums.update({release_year: {album_name: track_list}})

    # If the database does not contain the chosen artist
    else:

        # Appending the user-inputted album and tracklist to the global dictionary, since the artist is a new artist
        artists_and_years.update({artist_name: {release_year: {album_name: track_list}}})

    # Make the database with the new information
    make_database()

    # Confirmation message
    print "\nAlbum added to database!"

    # Quitting the method
    return None








# Method usage_msg(): displays a message on how to use the current program

# Arguments: None

# Preconditions: None

# Postconditions: None

def usage_msg():

    # Description of what is to be done by this method
    print "Usage message:\n"

    # Printing the usage message
    print "How to use cddb:"
    print "\t-l: lists artists, then lists albums by artist based on artist choice, then lists tracks from chosen album"
    print "\t-d: deletes album from database"
    print "\t-a: adds album to database"
    print "\t-h: displays this usage message"
    print "No parameter speicifed or an invalid parameter will automatically display this usage message"

    # Quitting the method
    return None







# Getting the number of arguments during script call
arg_num = len(sys.argv)

# If there is more than one argument, set that as the total display
if arg_num > 1:

    # The user-inputted argument
    arg = str(sys.argv[1])  # Getting the argument from call time

    # If a bad argument or multiple arguments, print usage message
    if (arg != "-l") and (arg != "-d") and (arg != "-a") and (arg != "-h"):
        arg = "-h"
# If no arguments, print usage message
else:
    arg = "-h"


# If the argument is "-h", display the usage messsage
if arg == "-h":

    # Calling the method usage_msg()
    usage_msg()

# If the argument is not "-h"
else:

    #Going through each environment variable
    for v in os.environ:

	#If the current environment variable equals "CDDB"
	if v == 'CDDB':

	   #Set the filename as the value for the environemtn variable CDDB
	   filename = os.environ['CDDB']
    
    #If the filename is blank, then the environemtn variable CDDB did not exist
    if filename == "":
	
	#Setting a default value for the filename, since CDDB did not exist
	filename = "albums.db"

    # Making a dictionary from the album database
    make_album()

    # Executing a specific method based on the program argument
    if arg == "-l":
        list_artists()
    elif arg == "-d":
        delete_album()
    elif arg == "-a":
        add_album()

    # Finished with program execution
    print "\nGoodbye!"
