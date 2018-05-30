import xml.etree.ElementTree as Et
import os
import pandas as pd
from utility import deaccent
from pathlib import Path
from collections import Counter


def proieltbs(treebank, artcounter):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            for sentence in division:
                alltokesinsent = sentence.findall(".*[@form]")
                # Loops through every word.
                for token in alltokesinsent:
                    # Create lists of words or letters.
                    if token.get('lemma') == 'ὁ':
                        if token.get('part-of-speech') == 'S-':
                            pos = 'Article'
                        else:
                            pos = 'Pronoun'
                        artcounter[pos] += 1
    return artcounter


def perseustbs(treebank, artcounter):
    froot = treebank.getroot()
    for body in froot:
        for sentence in body:
            allwordsinsent = sentence.findall(".*[@form]")
            # Loops through every word.
            for word in allwordsinsent:
                # Create lists of words or letters.
                if word.get('lemma') == 'ὁ':
                    if word.get('postag')[0] == 'l':
                        pos = 'Article'
                    else:
                        pos = 'Pronoun'
                    artcounter[pos] += 1
    return artcounter


treebankFolder = '/home/chris/Desktop/Treebanks/'
os.chdir(treebankFolder)
indir = os.listdir(treebankFolder)
artCounter = Counter()

for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = Et.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            artCounter = proieltbs(tb, artCounter)
        else:
            artCounter = perseustbs(tb, artCounter)
print(artCounter)
