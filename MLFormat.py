import xml.etree.ElementTree as ET
from collections import Counter
import os
import pandas as pd


def proieltbs(treebank):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            for sentence in division:
                alltokesinsent = sentence.findall('token')
                for token in alltokesinsent:
                    if token.get('lemma') == 'ὁ':
                        mlformatlist = []
                        #Here we need to find which number value in alltokesinsent the article is. Then we can
                        #move down to the while loop and subtract 7 from that and add the elements of that word
                        #to the list and go forward from there.
                        form = token.get('form')
                        lemma = token.get('lemma')
                        morph = token.get('morphology')
                        mlformatlist.extend([form, lemma, morph])
                        i = -7
                        while i < 14:
                            nextwordid = articleid + i
                            if
                            form =

#                        while sentence[i].get('empty-token-sort'):
 #                           i -= 1


os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')

for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            proieltbs(tb)
        if tbroot.tag == 'treebank':
            perseustbs(tb)

#df = pd.DataFrame.from_dict(artPos, orient='index')

#outname = 'NewArtDistance.csv'
#outdir = '/home/chris/Desktop'
#outpath = os.path.join(outdir, outname)
#df.to_csv(outpath)

#print(artPos)
