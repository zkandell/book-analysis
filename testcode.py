import bookanalysis as an

p = "pg63189.txt"
s = "1661-0.txt"

phist = an.makewordfreqhist(an.gutenbergtrim(open(p,encoding='utf8')))
shist = an.makehistogramfromfilename(s)

textcomp = an.comparewordfreq(phist,shist)

print("Most frequent words used only in Highwayman of the Void:",an.sortdictval(textcomp['anotb'], True)[:10])
print("Most frequent words used only in The Adventures of Sherlock Holmes:",an.sortdictval(textcomp['bnota'], True)[:10])
print("Words used far more often in Highwayman of the Void:",an.sortdictval(textcomp['aoverb'], True)[:10])
print("Words used far more often in The Adventures of Sherlock Holmes:",an.sortdictval(textcomp['bovera'], True)[:10])

an.saveanalysis("pg63189",phist)

print(an.gutenbergtrim(5))