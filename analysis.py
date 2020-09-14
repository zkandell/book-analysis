# Pull in the text file to analyze the words used
import string

name = input("Enter file (without extension):")
if name == "r":name = "romeo"
if name == "p":name = "pg63189"
filename = name + ".txt"
xfile = open(filename)
words = { } # Create the dictionary that will eventually have the word histogram
count = 0 # Word count starts at 0, clearly
alllines = list() # Create an empty list for later

def cleanline(line):
    temp = line.strip() # Get rid of white space
    temp = temp.lower() # Lower case all letters
    temp = temp.translate(str.maketrans("","",string.punctuation)) # Strip out all punctuation
    return temp

# Function to create a sorted list out of a dictionary, sorted by the values, not the keys
def sortdictval(d,rev):
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
    
alllines = makefulltextlist(xfile)

for i in range(len(alllines)):
    line = alllines[i]
    fixedline = cleanline(line)
    w = fixedline.split()
    for b in w:
        words[b] = words.get(b,0)+1 # Increment count, add to dictionary if not seen already
        count += 1 # Get total word count
    
print(alllines)
print(words)
print(count)
    
# newfile = open(name + "analysis.txt", "w")
# newfile.write(str("Word count: " + str(count)) + "\n")
# newfile.write(str(words))
# newfile.close