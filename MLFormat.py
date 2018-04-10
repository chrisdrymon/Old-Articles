import xml.etree.ElementTree as ET
from collections import Counter
import os
import pandas as pd


def proieltbs(treebank, perarticledict, totarticlenumber):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            for sentence in division:
                alltokesinsent = sentence.findall('token')
                for token in alltokesinsent:
                    if token.get('lemma') == 'ὁ':
                        form = token.get('form')
                        morph = token.get('morphology')
                        articlenumber = alltokesinsent.index(token)
                        mlformatlist = [form, morph]
                        i = -7
                        while i < 14:
                            nextwordid = articlenumber + i
                            try:
                                form = alltokesinsent[nextwordid].get('form')
                                lemma = alltokesinsent[nextwordid].get('lemma')
                                morph = alltokesinsent[nextwordid].get('morphology')
                                mlformatlist.extend([form, lemma, morph])
                            except IndexError:
                                mlformatlist.extend([None, None, None])
                            i += 1
                        perarticledict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1
    returnlist = [perarticledict, totarticlenumber]
    return returnlist

os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')
perArticleDict = {}
totArticleNumber = 1
for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            returnedList = proieltbs(tb, perArticleDict, totArticleNumber)
            perArticleDict = returnedList[0]
            totArticleNumber = returnedList[1]
#        if tbroot.tag == 'treebank':
 #           perseustbs(tb, perArticleDict, totArticleNumber)

df = pd.DataFrame.from_dict(perArticleDict, orient='index')
outname = 'MLFormat.csv'
outdir = '/home/chris/Desktop'
outpath = os.path.join(outdir, outname)
df.to_csv(outpath)


