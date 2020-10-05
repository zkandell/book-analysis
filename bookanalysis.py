# This file is just defining functions - no actual code is executed here

import string
import re

def saveanalysis(name,hist):
    newfilename = name + "analysis.txt" # Creates a file name for the new file that will be written - string of the file name is returned with the function
    file = open(newfilename, "w") # Creates a new file to write thsi information to
    file.write(str(hist)) # Write the dictionary as a string to a file - sure, it's a basic method, but it works
    file.close # Closes the file
    return newfilename

def loadanalysis(file):
    s = file.read() # Make a string out of the file
    file.close() # Close the file
    hist = eval(s) # Read the text of the string, turning it into a dictionary
    return hist

def cleanline(line):
    temp = line.strip() # Get rid of white space
    temp = temp.lower() # Lower case all letters
    temp = temp.replace("--"," ") # Replace double hyphens with spaces to avoid unexpected compound words
    temp = temp.translate(str.maketrans("","",'!"“”’#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')) # Strip out all punctuation
    return temp

def makeparagraphlist(lines):
    # Takes in a list of strings, turns it into a list of paragraphs
    fullbookstring = "" # Initialize the empty string
    for l in lines: # This puts together a single string containing all text in the book
        fullbookstring = fullbookstring + l # Append that line to the end of the string
    paralist = fullbookstring.split('\n\n') # Two newlines are used to separate paragraphs, so split on those to divide the list into paragraphs
    return paralist

def makesentencelist(paragraph):
    # Takes in a string representing a paragraph, breaks it into sentences
    sentlist = re.split('[.!?]',paragraph) # Splits the book into sentences (can be refined much further)
    for i in range(len(sentlist)): sentlist[i] = sentlist[i].replace('\n',' ') # Replace newlines with spaces to fix formatting issues
    return sentlist

def bookintosentences(lines):
    # Takes in the book as a list of lines, outputs a list where each item is a paragraph containing a list of sentences
    biglist = list() # THE list - we'll add to this later
    plist = makeparagraphlist(lines) # Turn the book into paragraphs
    for p in range(len(plist)): biglist.append(makesentencelist(plist[p])) # Split every paragraph into sentences, then write to the big list
    return biglist

def sortdictval(d,rev):
    # Function to create a sorted list out of a dictionary, sorted by the values, not the keys
    tmp = list() # Create an empty list
    sortlist = list()
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
    for line in file: lines.append(line)
    return lines

def gutenbergtrim(book):
    # If the book came from Project Gutenberg, this function will attempt to trim off data that doesn't belong to the book
    # This function is intended to be used with a list, but it can also take a file handle
    if isinstance(book,list): b = book # If you've passed in a book, then no need to do anything special
    else: 
        try: b = makefulltextlist(book) # Creates a list if the variable type passed in can be made into a list (like dictionaries or files)
        except: return [] # If a list can't be made, then return a blank list
    # Initialize start, end, and title variables as None - will be set in the for loop
    start = None
    end = None
    title = None
    for i in range(len(b)): # Loop through all the lines in the book
        line = b[i].strip() # Strip off the whitespace to simplify text comparison
        if line.startswith("Title: "): title = line[7:].strip() # Get the title of the book
        # Once you've determined the title, find the first line with the title, generally where the book itself starts; this line is finicky to correct for inconsistent capitalization
        if title is not None and line.lower().startswith(title.lower()):
            start = i
            continue
        if line.startswith("End of the Project Gutenberg EBook"): # Stop just short of this line, which is always the end of the story
            end = i
            break
    
    if start == None: start = 0
    if end == None: end = len(b) # If this doesn't come from Project Gutenberg, setting these variable will cause the function to just return the entire document unaltered
    trimmedbook = b[start:end]
    return trimmedbook

def counttwowordphrases(paralist):
    # Goes through the entire book and counts the number of times each two-word phrase is used
    return

def countwords(paralist):
    # Takes in the paragraph list, counts how often each specific word is used
    wordscount = { }
    for i in range(len(paralist)): # Run through every paragraph of text in the book
        lineslist = paralist[i]
        for j in range(len(lineslist)):
            line = lineslist[j] # Get the line from the list
            line = cleanline(line) # Clean the line (remove white space, lowercase all letters, strip out punctuation)
            wordlist = line.split() # Split the line into individual words
            for b in wordlist: wordscount[b] = wordscount.get(b,0)+1 # Increment count, add to dictionary if not seen already
    return wordscount

def getphrasecount(hist):
    # Gets the total word/phrase count from a histogram of individual word/phrase count
    wordcount = 0
    for word in hist: wordcount+=hist[word] # Add the uses of each individual word/phrase to the total count
    return wordcount

def getphrasefreq(hist,count):
    # Turn the word counts into frequency
    relcount = { }
    for word in hist: relcount[word] = hist[word]/count # Divide usage of phrase by total phrases to get frequency, for every phrase in the book
    return relcount

def makewordfreqhist(paralist):
    # Takes in a list output from bookintosentences, spits out a histogram of word frequency
    # Initialize variables
    wordfreqhist = { } # Create the empty dictionary that will be returned at the end
    # Build the dictionary that the function returns
    wordfreqhist['wordabscount'] = countwords(paralist)
    wordfreqhist['wordcount'] = getphrasecount(wordfreqhist['wordabscount'])
    wordfreqhist['wordrelcount'] = getphrasefreq(wordfreqhist['wordabscount'],wordfreqhist['wordcount'])
    
    return wordfreqhist

def xnoty(book_x,book_y):
    # Builds a dictionary with the absolute count of words used in one book and not the other
    histcount_x = book_x['wordabscount'] # Get word counts from the dictionary passed in for each book
    histcount_y = book_y['wordabscount']
    xnotydict = {} # Initialize dictionary we're about to fill up
    for key in histcount_x: # Looping through every entry in x
        if histcount_y.get(key,0) == 0: # If entry in y doesn't appear in x
            xnotydict[key] = histcount_x[key] # Add entry to xnoty dictionary - this notes down the absolute count, not frequency
    return xnotydict

def xovery(book_x,book_y):
    # Builds a dictionary of the relative frequency of all words that appear in both books
    histfreq_x = book_x['wordrelcount']
    histfreq_y = book_y['wordrelcount']
    xoverydict = dict()
    for key in histfreq_x: # Loop through every entry in x
        if histfreq_y.get(key,0) != 0: # Run only if the word is in both dictionaries
            xoverydict[key] = histfreq_x[key]/histfreq_y[key]
    return xoverydict

def comparewordfreq(book_a,book_b):
    # book_a and book_b are the output of makewordfreqhist: dictionaries with word count, absolute counts, and relative frequencies          
    wordfreqcomparison = { } # Create the main dictionary we'll return at the end
    
    # Build histogram of words that are in one book but not the other
    wordfreqcomparison["anotb"] = xnoty(book_a,book_b)
    wordfreqcomparison["bnota"] = xnoty(book_b,book_a)

    # Make two dictionaries of words in both
    wordfreqcomparison["aoverb"] = xovery(book_a,book_b)
    wordfreqcomparison["bovera"] = xovery(book_b,book_a)
    
    return wordfreqcomparison
    
def makehistogramfromfilename(filename):
    # Takes in a string pointing to the file location, returns the histogram
    return makewordfreqhist(bookintosentences(gutenbergtrim(makefulltextlist(open(filename,encoding='utf8'))))) # Look, these functions need to be strung together somehow, and typing them all out every time is annoying