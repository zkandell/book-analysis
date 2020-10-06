import string
import re

def saveanalysis(name,hist):
    newfilename = name + "analysis.txt" # Creates a file name for the new file that will be written - string of the file name is returned with the function
    file = open(newfilename, "w") # Creates a new file to write this information to
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
    for l in lines: fullbookstring = fullbookstring + l # Glue all the lines in the book together into a single string
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

def sortdictval(d,rev=True):
    # Function to create a sorted list out of a dictionary, sorted by the values, not the keys
    tmp = list() # Create an empty list
    sortlist = list()
    for k,v in d.items(): tmp.append((v,k)) # Build a list of tuples, with values in front of keys to allow sorting
    tmp = sorted(tmp, reverse=rev) # Sort the list, with rev determining which order the list is sorted in
    for v,k in tmp: sortlist.append((k,v)) # Reverse all items to get key value pairs in the right order again
    # You return a list, not a dictionary, because lists have order, while dictionaries do not
    return sortlist
    
def makefulltextlist(file): return file.readlines()

def gutenbergtrim(book):
    # If the book came from Project Gutenberg, this function will attempt to trim off data that doesn't belong to the book
    if isinstance(book,list): b = book # If you've passed in a list of all lines in the book, then no need to do anything special
    else: 
        try: b = makefulltextlist(book) # Creates a list if a file is passed into the function
        except: return [] # If a list can't be made, then return a blank list
    start = None # These variables will (in theory) be set in the for loop
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

def getngramfromline(wordlist,i,n):
    # From a list of words, it retrieves a phrase of n words, starting at index i
    ngram = wordlist[i] # Start by grabbing the first word of the ngram
    if n == 1: return ngram # If n is 1, then we're done already
    else:
        for j in range(1,n): ngram = ngram + ' ' + wordlist[i+j] # Run through the rest of n words, adding them to the string
    return ngram # Return the string we just created

def countwordngram(paralist,n):
    # Counts the number of times each n-length word phrase is used; paralist is the list created by bookintosentences, n is the word length of phrases you're interested in tracking
    phrasecount = { }
    for i in range(len(paralist)):
        lineslist = paralist[i] # Run through every paragraph of text in the book, pulling out sentences
        for j in range(len(lineslist)):
            wordlist = cleanline(lineslist[j]).split() # Loop through every sentence, cleaning it up, then splitting it into individual words
            for b in range(len(wordlist)-(n-1)):
                phrase = getngramfromline(wordlist,b,n) # Get the phrase we're looking for
                phrasecount[phrase] = phrasecount.get(phrase,0)+1 # Increment count, add to dictionary if not seen already
    return phrasecount

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
    wordfreqhist = { }
    # Build the dictionary that the function returns
    wordfreqhist['1wordabscount'] = countwordngram(paralist,1)
    wordfreqhist['wordcount'] = getphrasecount(wordfreqhist['1wordabscount'])
    wordfreqhist['1wordrelcount'] = getphrasefreq(wordfreqhist['1wordabscount'],wordfreqhist['wordcount'])
    wordfreqhist['2wordabscount'] = countwordngram(paralist,2)
    wordfreqhist['2wordrelcount'] = getphrasefreq(wordfreqhist['2wordabscount'],getphrasecount(wordfreqhist['2wordabscount']))
    wordfreqhist['3wordabscount'] = countwordngram(paralist,3)
    wordfreqhist['3wordrelcount'] = getphrasefreq(wordfreqhist['3wordabscount'],getphrasecount(wordfreqhist['3wordabscount']))

    return wordfreqhist

def xnoty(histcount_x,histcount_y):
    # Builds a dictionary with the absolute count of words used in one book and not the other
    xnotydict = {} # Initialize dictionary we're about to fill up
    for key in histcount_x: # Looping through every entry in x
        if histcount_y.get(key,0) == 0: xnotydict[key] = histcount_x[key] # If entry in y doesn't appear in x, add the absolute count to the dictionary
    return xnotydict

def xovery(histfreq_x,histfreq_y):
    # Builds a dictionary of the relative frequency of all words that appear in both books
    xoverydict = dict()
    for key in histfreq_x: # Loop through every entry in x
        if histfreq_y.get(key,0) != 0: xoverydict[key] = histfreq_x[key]/histfreq_y[key] # If it's in both dictionaries, record the ratio of the two frequencies
    return xoverydict

def comparewordfreq(book_a,book_b):
    # book_a and book_b are the output of makewordfreqhist: dictionaries with word count, absolute counts, and relative frequencies          
    wordfreqcomparison = { } # Create the main dictionary we'll return at the end
    
    # Build histogram of words that are in one book but not the other
    wordfreqcomparison["anotb"] = xnoty(book_a['1wordabscount'],book_b['1wordabscount'])
    wordfreqcomparison["bnota"] = xnoty(book_b['1wordabscount'],book_a['1wordabscount'])

    # Make two dictionaries of words in both
    wordfreqcomparison["aoverb"] = xovery(book_a['1wordrelcount'],book_b['1wordrelcount'])
    wordfreqcomparison["bovera"] = xovery(book_b['1wordrelcount'],book_a['1wordrelcount'])
    
    return wordfreqcomparison
    
def makehistogramfromfilename(filename):
    # Takes in a string pointing to the file location, returns the histogram
    return makewordfreqhist(bookintosentences(gutenbergtrim(makefulltextlist(open(filename,encoding='utf8'))))) # Look, these functions need to be strung together somehow, and typing them all out every time is annoying