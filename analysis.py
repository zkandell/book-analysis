# Pull in the text file to analyze the words used
import string

name = input("Enter file (without extension):")
if name == "r":name = "romeo"
if name == "p":name = "pg63189"
filename = name + ".txt"
xfile = open(filename)
words = { }
count = 0

def cleanline(line_to_clean):
    temp = line_to_clean.strip() # Get rid of white space
    temp = temp.lower() # Lower case all letters
    temp = temp.translate(str.maketrans("","",string.punctuation))
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

for i, line in enumerate(xfile):
    # words[v] = k.get(v,0)+1
    # print(i,line.strip())
    fixedline = cleanline(line)
    w = fixedline.split()
    for b in w:
        words[b] = words.get(b,0)+1 # Increment count, add to dictionary if not seen already
        count += 1 # Get total word count
    
newfile = open(name + "analysis.txt", "w")
newfile.write(str("Word count: " + str(count)) + "\n")
newfile.write(str(words))
newfile.close