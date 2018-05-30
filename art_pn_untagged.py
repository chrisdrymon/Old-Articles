import xml.etree.ElementTree as Et
import os
import pandas as pd
from utility import deaccent
from pathlib import Path


def proieltbs(treebank, perarticledict, totarticlenumber, allforms):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            for sentence in division:
                alltokesinsent = sentence.findall(".*[@form]")
                # Loops through every word.
                for token in alltokesinsent:
                    # Creates all the values that will go into a single element.
                    if token.get('lemma') == 'ὁ':
                        articlenumber = alltokesinsent.index(token)
                        if source.get('jewish') == 'yes':
                            jewish = 'yes'
                        else:
                            jewish = 'no'
                        mlformatlist = [jewish]
                        nextwordid = articlenumber + 1
                        try:
                            form = deaccent(alltokesinsent[nextwordid].get('form'))
                            mlformatlist.append(form)
                            # Create lists of words or letters.
                            if not deaccent(token.get('form')) in allforms:
                                allforms.append(deaccent(token.get('form')))
                        except IndexError:
                            mlformatlist.append('OOR')
                        if token.get('part-of-speech') == 'S-':
                            fanswer = 'Article'
                        else:
                            fanswer = 'Pronoun'
                        mlformatlist.append(fanswer)
                        perarticledict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1
    returnlist = [perarticledict, totarticlenumber, allforms]
    return returnlist


def perseustbs(treebank, perarticledict, totarticlenumber, allforms):
    froot = treebank.getroot()
    for body in froot:
        for sentence in body:
            allwordsinsent = sentence.findall(".*[@form]")
            # Loops through every word.
            for word in allwordsinsent:
                # Create lists of words or letters.
                if not deaccent(word.get('form')) in allforms:
                    allforms.append(deaccent(word.get('form')))
                # Creates all the values that will go into a single element.
                if word.get('lemma') == 'ὁ':
                    articlenumber = allwordsinsent.index(word)
                    if body.get('jewish') == 'yes':
                        jewish = 'yes'
                    else:
                        jewish = 'no'
                    mlformatlist = [jewish]
                    nextwordid = articlenumber + 1
                    try:
                        form = deaccent(allwordsinsent[nextwordid].get('form'))
                        mlformatlist.append(form)
                    except IndexError:
                        mlformatlist.append('OOR')
                    if word.get('postag')[0] == 'l':
                        fanswer = 'Article'
                    else:
                        fanswer = 'Pronoun'
                    mlformatlist.append(fanswer)
                    perarticledict[totarticlenumber] = mlformatlist
                    totarticlenumber += 1

    returnlist = [perarticledict, totarticlenumber, allforms]
    return returnlist


treebankFolder = '/home/chris/Desktop/Treebanks/'

outTrainPath = Path('/home/chris/Desktop/MLTrain.csv')
outTestPath = Path('/home/chris/Desktop/MLTest.csv')
formListPath = Path('/home/chris/Desktop/Formlist.txt')
ultimateListPath = Path('/home/chris/Desktop/Everythinglist.txt')

os.chdir(treebankFolder)
indir = os.listdir(treebankFolder)

perArticleDict = {}
totArticleNumber = 1
allForms = ['OOR', 'yes', 'no', 'Article', 'Pronoun']

for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = Et.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            returnedList = proieltbs(tb, perArticleDict, totArticleNumber, allForms)
        else:
            returnedList = perseustbs(tb, perArticleDict, totArticleNumber, allForms)
        perArticleDict = returnedList[0]
        totArticleNumber = returnedList[1]
        allForms = returnedList[2]

labelList = ['Jewish', '1Form', 'Answer']
ultimateList = list(set(allForms))
df = pd.DataFrame.from_dict(perArticleDict, orient='index')
df.columns = labelList
df = df.sample(frac=1).reset_index(drop=True)
splitNum = int(df.shape[0]*.8)
dfTrain = df[:splitNum]
dfTest = df[splitNum:]
dfTrain.to_csv(outTrainPath, index=False)
dfTest.to_csv(outTestPath, index=False)
with open(formListPath, "w") as output:
    for s in allForms:
        output.write("%s\n" % s)
with open(ultimateListPath, "w") as output:
    for s in ultimateList:
        output.write("%s\n" % s)
print(len(allForms), 'forms in lemma list.')
print(len(ultimateList), 'entries total in the ultimate list.')
print(len(perArticleDict), 'article entires.')