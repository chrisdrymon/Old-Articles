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
                        form = token.get('form')
                        morph = token.get('morphology')
                        articlenumber = alltokesinsent.index(token)
                        mlformatlist.extend([form, morph])
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
                        print(mlformatlist)


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

#outname = 'MLFormat.csv'
#outdir = '/home/chris/Desktop'
#outpath = os.path.join(outdir, outname)
#df.to_csv(outpath)

#print(artPos)
