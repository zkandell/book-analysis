import string

# Defining all the functions I'm using

def saveanalysis(name):
    # Does not actually work - needs to be fixed
    # newfilename = name + "analysis.txt" # Creates a file name for the new file that will be written - string of the file name is returned with the function
    # file = open(newfilename, "w") # Creates a new file to write thsi information to
    # file.write(str("Word count: " + str(count)) + "\n") # Writes the word count to a line
    # file.write(str(words)) # Writes the word frequency dictionary to the second line
    # file.close # Closes the file
    return # newfilename
    
def cleanline(line):
    temp = line.strip() # Get rid of white space
    temp = temp.lower() # Lower case all letters
    temp = temp.replace("--"," ") # Replace double hyphens with spaces to avoid unexpected compound words
    temp = temp.translate(str.maketrans("","",'!"“”#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')) # Strip out all punctuation
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

def gutenbergtrim(book):
    # If the book came from Project Gutenberg, this function will attempt to trim off data that doesn't belong to the book
    b = makefulltextlist(book) # If a file is passed to this function rather than a list of lines, this will create the list
    # Initialize start, end, and title variables as None - will be set in the for loop
    start = None
    end = None
    title = None
    for i in range(len(b)): # Loop through all the lines in the book
        line = b[i].strip() # Strip off the whitespace to simplify text comparison
        if line.startswith("Title: "): # Get the title of the book
            title = line[7:].strip()
        # Once you've determined the title, find the first line with the title, generally where the book itself starts; this line is finicky to correct for inconsistent capitalization
        if title is not None and line.lower().startswith(title.lower()):
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
    # Initialize variables
    wordfreqhist = { } # Create the empty dictionary that will be returned at the end
    wordabscount = { } # This will include the number of times every word is used in the text
    wordrelcount = { } # The previous dictionary, but with all values divided by the total word count of the text, to get a relative measure of how frequent words are
    count = 0
    
    # Count the words
    for i in range(len(lineslist)): # Run through every line of text in the list
        line = lineslist[i] # Get the line from the list
        line = cleanline(line) # Clean the line (remove white space, lowercase all letters, strip out punctuation)
        wordlist = line.split() # Split the line into individual words
        for b in wordlist: # Run through every word on the line
            wordabscount[b] = wordabscount.get(b,0)+1 # Increment count, add to dictionary if not seen already
            count += 1 # Get total word count

    # Turn the word counts into frequency
    for word in wordabscount: # Loop through every entry in the raw word count list
        wordrelcount[word] = wordabscount[word]/count # Divide by word count to get frequency
        
    # Build the dictionary that the function returns
    wordfreqhist["wordcount"] = count
    wordfreqhist["wordabscount"] = wordabscount
    wordfreqhist["wordrelcount"] = wordrelcount
    
    return wordfreqhist

def comparewordfreq(book_a,book_b):
    # book_a and book_b are the output of makewordfreqhist: dictionaries with word count, absolute counts, and relative frequencies
    
    # Pull out each individual dictionary from the inputs
    histcount_a = book_a["wordabscount"]
    histfreq_a = book_a["wordrelcount"]
    histcount_b = book_b["wordabscount"]
    histfreq_b = book_b["wordrelcount"]
    
    
    # Create empty dictionaries that we're going to return later
    anotb = { }
    bnota = { }
    aoverb = { }
    bovera = { }
        
    # The following two sections can be done as a single function that's called twice - for now, I just want it to work
    # Make dictionary of words in a but not in b
    for key in histcount_a: # Looping through every entry in a
        if histcount_b.get(key,0) == 0: # If entry in a doesn't appear in b
            anotb[key] = histcount_a[key] # Add entry to anotb dictionary - this notes down the absolute count, not frequency
    
    # Make dictionary of words in b bun not in a
    for key in histcount_b: # Looping through every entry in b
        if histcount_a.get(key,0) == 0: # If entry in a doesn't appear in a
            bnota[key] = histcount_b[key] # Add entry to bnota dictionary - this notes down the absolute count, not frequency
            
    # Make two dictionaries of words in both; key is word, value is frequency in a divided by frequency in b for aoverb, frequency in b divided by frequency in a for bovera
    for key in histfreq_a: # Loop through every entry in a
        if histfreq_b.get(key,0) != 0: # Run only if the word is in both dictionaries
            aoverb[key] = histfreq_a[key]/histfreq_b[key]
            bovera[key] = histfreq_b[key]/histfreq_a[key]
            
    wordfreqcomparison = { } # Create the main dictionary we'll return at the end
    # Fill up that dictionary
    wordfreqcomparison["anotb"] = anotb
    wordfreqcomparison["bnota"] = bnota
    wordfreqcomparison["aoverb"] = aoverb
    wordfreqcomparison["bovera"] = bovera
    
    return wordfreqcomparison
    
def makehistogramfromfilename(filename):
    # Takes in a string pointing to the file location, returns the histogram
    return makewordfreqhist(gutenbergtrim(makefulltextlist(open(filename)))) # Look, these functions need to be strung together somehow, and typing them all out every time is annoying


p = "pg63189.txt"
s = "1661-0.txt"

phist = makehistogramfromfilename(p)
shist = makehistogramfromfilename(s)

textcomp = comparewordfreq(phist,shist)

print("Most frequent words used only in Highwayman of the Void:",sortdictval(textcomp['anotb'], True)[:10])
print("Most frequent words used only in The Adventures of Sherlock Holmes:",sortdictval(textcomp['bnota'], True)[:10])
print("Words used far more often in Highwayman of the Void:",sortdictval(textcomp['aoverb'], True)[:10])
print("Words used far more often in The Adventures of Sherlock Holmes:",sortdictval(textcomp['bovera'], True)[:10])