# Pull in the text file to analyze the words used
import string

# Defining all the functions I'm using
def saveanalysis(name):
    newfilename = name + "analysis.txt" # Creates a file name for the new file that will be written - string of the file name is returned with the function
    file = open(newfilename, "w") # Creates a new file to write thsi information to
    file.write(str("Word count: " + str(count)) + "\n") # Writes the word count to a line
    file.write(str(words)) # Writes the word frequency dictionary to the second line
    file.close # Closes the file
    return newfilename
    
def cleanline(line):
    temp = line.strip() # Get rid of white space
    temp = temp.lower() # Lower case all letters
    temp = temp.translate(str.maketrans("","",string.punctuation)) # Strip out all punctuation
    return temp

def sortdictval(d,rev):
    # Function to create a sorted list out of a dictionary, sorted by the values, not the keys
    # Initialize variables
    tmp = list() # Create an empty list
    sortlist = list() # Create an empty version of the returned list
    
    # Make a temporary list that holds items from the dictionary
    for k,v in d.items(): # Run through every item in the dictionary
        tmp.append((v,k)) # Add a tuple to the list, but in reversed order, putting values before keys
    
    # Sort the list, with rev determining which order the list is sorted in
    tmp = sorted(tmp, reverse=rev)
    
    for v,k in tmp: # Run through all items in tmp
        sortlist.append((k,v)) # Reverse the order to get key value pairs in the right order again

    # You return a list, not a dictionary, because lists have order, while dictionaries do not
    return sortlist
    
def makefulltextlist(file):
    # Takes the file and makes a list where each item is a line of text - allows finer control over going through each line later
    lines = []
    for line in file:
        lines.append(line)
    return lines

name = input("Enter file (without extension):")
if len(name)<1 or name == "r":name = "romeo"
if name == "p":name = "pg63189"
filename = name + ".txt"
xfile = open(filename)
words = { } # Create the dictionary that will eventually have the word histogram
count = 0 # Word count starts at 0, obviously

alllines = makefulltextlist(xfile) # Turn the text file into a list for processing

for i in range(len(alllines)): # Run through every line of text in the list
    line = alllines[i] # Get the line from the list
    line = cleanline(line) # Clean the line (remove white space, lowercase all letters, strip out punctuation)
    wordlist = line.split() # Split the line into individual words
    for b in wordlist: # Run through every word on the line
        words[b] = words.get(b,0)+1 # Increment count, add to dictionary if not seen already
        count += 1 # Get total word count
    
print(alllines)
print(words)
print(count)