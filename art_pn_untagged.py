import xml.etree.ElementTree as Et
import os
import pandas as pd
from utility import deaccent
from pathlib import Path


def proieltbs(treebank, perarticledict, perpronoundict, totarticlenumber, allforms):
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
                        artform = deaccent(token.get('form'))
                        if artform not in allforms:
                            allforms.append(artform)
                        if source.get('jewish') == 'yes':
                            jewish = 'yes'
                        else:
                            jewish = 'no'
                        mlformatlist = [jewish]
                        nextwordid = articlenumber + 1
                        try:
                            form = deaccent(alltokesinsent[nextwordid].get('form'))
                            mlformatlist.append(form)
                            if form not in allforms and not form == '':
                                allforms.append(form)
                        except IndexError:
                            mlformatlist.append('OOR')
                        if token.get('part-of-speech') == 'S-':
                            mlformatlist.append(0)
                            perarticledict[totarticlenumber] = mlformatlist
                        else:
                            mlformatlist.append(1)
                            perpronoundict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1
    returnlist = [perarticledict, perpronoundict, totarticlenumber, allforms]
    return returnlist


def perseustbs(treebank, perarticledict, perpronoundict, totarticlenumber, allforms):
    froot = treebank.getroot()
    for body in froot:
        for sentence in body:
            allwordsinsent = sentence.findall(".*[@form]")
            # Loops through every word.
            for word in allwordsinsent:
                # Creates all the values that will go into a single element.
                if word.get('lemma') == 'ὁ':
                    articlenumber = allwordsinsent.index(word)
                    artform = word.get('form')
                    if artform not in allforms:
                        allforms.append(artform)
                    if body.get('jewish') == 'yes':
                        jewish = 'yes'
                    else:
                        jewish = 'no'
                    mlformatlist = [jewish]
                    nextwordid = articlenumber + 1
                    try:
                        form = deaccent(allwordsinsent[nextwordid].get('form'))
                        mlformatlist.append(form)
                        if form not in allforms:
                            allforms.append(form)
                    except IndexError:
                        mlformatlist.append('OOR')
                    if word.get('postag')[0] == 'l':
                        mlformatlist.append(0)
                        perarticledict[totarticlenumber] = mlformatlist
                    else:
                        mlformatlist.append(1)
                        perpronoundict[totarticlenumber] = mlformatlist
                    perarticledict[totarticlenumber] = mlformatlist
                    totarticlenumber += 1

    returnlist = [perarticledict, perpronoundict, totarticlenumber, allforms]
    return returnlist


treebankFolder = '/home/chris/Desktop/Treebanks/'

outTrainPath = Path('/home/chris/Desktop/MLTrain.csv')
outTestPath = Path('/home/chris/Desktop/MLTest.csv')
formListPath = Path('/home/chris/Desktop/Formlist.txt')

os.chdir(treebankFolder)
indir = os.listdir(treebankFolder)

perArticleDict = {}
perPronounDict = {}
totArticleNumber = 1
allForms = ['OOR', 'yes', 'no', 'Article', 'Pronoun']

for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        print(file_name)
        tb = Et.parse(file_name)
        tbroot = tb.getroot()
        if tbroot.tag == 'proiel':
            perArticleDict, perPronounDict, totArticleNumber, allForms = proieltbs(tb, perArticleDict, perPronounDict,
                                                                                   totArticleNumber, allForms)
        else:
            perArticleDict, perPronounDict, totArticleNumber, allForms = perseustbs(tb, perArticleDict, perPronounDict,
                                                                                    totArticleNumber, allForms)
labelList = ['Jewish', '1Form', 'Answer']
dfArt = pd.DataFrame.from_dict(perArticleDict, orient='index')
dfPro = pd.DataFrame.from_dict(perPronounDict, orient='index')
dfProSize = int(dfPro.shape[0])
dfArt = dfArt.sample(n=dfProSize).reset_index(drop=True)
frames = [dfArt, dfPro]
df = pd.concat(frames)
df.columns = labelList
df = df.sample(frac=1).reset_index(drop=True)
dfSize = int(df.shape[0])
splitNum = int(df.shape[0]*.8)
dfTrain = df[:splitNum]
dfTest = df[splitNum:]
dfTrain.to_csv(outTrainPath, index=False)
dfTest.to_csv(outTestPath, index=False)
with open(formListPath, "w") as output:
    for s in allForms:
        output.write("%s\n" % s)
print(len(allForms), 'forms in lemma list.')
print(len(perPronounDict), 'pronouns.')
print(dfSize, 'o lemmas.')
