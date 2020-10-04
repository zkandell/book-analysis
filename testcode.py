import bookanalysis as an

#p = "ParagraphTest.txt"
p = 'pg63189.txt'
s = "1661-0.txt"

#phist = an.makewordfreqhist(an.gutenbergtrim(open(p,encoding='utf8')))
#phist = an.loadanalysis(open(p))
shist = an.makehistogramfromfilename(s)

phist = an.makewordfreqhist(an.bookintosentences(an.gutenbergtrim(an.makefulltextlist(open(p,encoding='utf8')))))
#shist = an.makewordfreqhist(an.bookintosentences(an.gutenbergtrim(an.makefulltextlist(open(s,encoding='utf8')))))

textcomp = an.comparewordfreq(phist,shist)

print("Most frequent words used only in Highwayman of the Void:",an.sortdictval(textcomp['anotb'], True)[:10])
print("Most frequent words used only in The Adventures of Sherlock Holmes:",an.sortdictval(textcomp['bnota'], True)[:10])
print("Words used far more often in Highwayman of the Void:",an.sortdictval(textcomp['aoverb'], True)[:10])
print("Words used far more often in The Adventures of Sherlock Holmes:",an.sortdictval(textcomp['bovera'], True)[:10])

##an.saveanalysis("pg63189",phist)

#p = "ParagraphTest.txt"

#ptemp = an.makefulltextlist(open(p,encoding='utf8'))

#plist = an.gutenbergtrim(ptemp)

#ppara = an.makeparagraphlist(plist)

#biglist = an.bookintosentences(plist)
#print(biglist)
