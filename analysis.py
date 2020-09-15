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
    # Takes the file and makes a list where each item is a line of text - allows finer control over going through each line later than file.seek()
    lines = []
    for line in file:
        lines.append(line)
    return lines

def gutenbergstartendtrim(book):
    # If the book comes from Project Gutenberg, this function will attempt to trim off data that doesn't belong to the book
    b = makefulltextlist(book) # Turn the file into a list of lines
    start = None # Initialize start and end variables as None - will be set in the for loop
    end = None
    title = None
    for i in range(len(b)): # Loop through all the lines in the book
        line = b[i].strip()
        if line.startswith("Title: "): # Get the title of the book
            title = line[7:].strip()
            print(title)
        if line.lower().startswith(str(title).lower()): # Find the first line with the title, which is generally where the book itself starts; this line is complex/finicky because of inconsistent title capitalization
            start = i
            continue
        if line.startswith("End of the Project Gutenberg EBook"): # Stop just short of this line, which is always the end of the story
            end = i
            break
    
    if start == None: start = 0
    if end == None: end = len(b) # If this doesn't come from Project Gutenberg, setting these variable will cause the function to just return the entire document unaltered
    # print(start,end)
    trimmedbook = b[start:end]
    return trimmedbook

def makewordfreqhist(lineslist):
    # Takes in a list containing all lines of a book, then constructs a histogram of word frequency and word count
    wordfreqhist = { } # Create the empty dictionary that will be returned at the end
    wordabscount = { } # This will include the number of times every word is used in the text
    wordrelcount = { } # The previous dictionary, but with all values divided by the total word count of the text, to get a relative measure of how frequent words are
    count = 0
    for i in range(len(lineslist)): # Run through every line of text in the list
        line = lineslist[i] # Get the line from the list
        line = cleanline(line) # Clean the line (remove white space, lowercase all letters, strip out punctuation)
        wordlist = line.split() # Split the line into individual words
        for b in wordlist: # Run through every word on the line
            wordabscount[b] = wordabscount.get(b,0)+1 # Increment count, add to dictionary if not seen already
            count += 1 # Get total word count

    for word in wordabscount:
        wordrelcount[word] = wordabscount[word]/count
        
    wordfreqhist["wordcount"] = count
    wordfreqhist["wordabscount"] = wordabscount
    wordfreqhist["wordrelcount"] = wordrelcount
    
    return wordfreqhist

# def comparewordfreq(a,b):
    # a and b are dictionaries containing the relative word frequency for two different texts
    


name = input("Enter file (without extension):")
if len(name)<1 or name == "r":name = "romeo"
if name == "p":name = "pg63189"
if name == "s":name = "1661-0"
filename = name + ".txt"
xfile = open(filename) # Typical file opening

# alllines = gutenbergstartendtrim(xfile) # Turn the text file into a list for processing
# makewordfreqhist(alllines)

test = gutenbergstartendtrim(xfile)
testdict = makewordfreqhist(test)
print(testdict)