import xml.etree.ElementTree as ET
import os
import pandas as pd
from utility import deaccent
from pathlib import Path


def proieltbs(treebank, perarticledict, totarticlenumber, alllemmas, allforms, allmorphs, answersdict):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            for sentence in division:
                alltokesinsent = sentence.findall(".*[@form]")
                for token in alltokesinsent:
                    if not deaccent(token.get('lemma')) in alllemmas:
                        alllemmas.append(deaccent(token.get('lemma')))
                    if not deaccent(token.get('form')) in allforms:
                        allforms.append(deaccent(token.get('form')))
                    if not token.get('morphology') in allmorphs:
                        allmorphs.append(token.get('morphology'))
                    if token.get('lemma') == 'ὁ':
                        form = deaccent(token.get('form'))
                        morph = token.get('morphology')
                        articlenumber = alltokesinsent.index(token)
                        mlformatlist = [form, morph]
                        headwordplace = int(token.get('head-id')) - int(token.get('id'))
                        i = -2
                        while i < 0:
                            nextwordid = articlenumber + i
                            try:
                                form = deaccent(alltokesinsent[nextwordid].get('form'))
                                lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                                morph = alltokesinsent[nextwordid].get('morphology')
                                mlformatlist.extend([form, lemma, morph])
                            except IndexError:
                                mlformatlist.extend(['ellipsed', 'ellipsed', 'ellipsed'])
                            i += 1
                        i += 1
                        while i < 4:
                            nextwordid = articlenumber + i
                            try:
                                form = deaccent(alltokesinsent[nextwordid].get('form'))
                                lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                                morph = alltokesinsent[nextwordid].get('morphology')
                                mlformatlist.extend([form, lemma, morph])
                            except IndexError:
                                mlformatlist.extend(['ellipsed', 'ellipsed', 'ellipsed'])
                            i += 1
                        perarticledict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1
                        if headwordplace < -2 or headwordplace > 3:
                            fanswer = 0
                        else:
                            fanswer = answersdict[headwordplace]
                        mlformatlist.extend([fanswer])
    returnlist = [perarticledict, totarticlenumber, alllemmas, allforms, allmorphs]
    return returnlist


treebankFolder = '/home/chris/Desktop/CustomTB/'
outTrainPath = Path('/home/chris/Desktop/MLTrain.csv')
outTestPath = Path('/home/chris/Desktop/MLTest.csv')
lemmaListPath = Path('/home/chris/Desktop/Lemmalist.txt')
formListPath = Path('/home/chris/Desktop/Formlist.txt')
morphListPath = Path('/home/chris/Desktop/Morphlist.txt')
ultimateListPath = Path('/home/chris/Desktop/Everythinglist.txt')

os.chdir(treebankFolder)
indir = os.listdir(treebankFolder)

perArticleDict = {}
totArticleNumber = 1
allLemmas = []
allForms = []
allMorphs = []
answersDict = {-2: 0,
               -1: 1,
               0: 5,
               1: 2,
               2: 3,
               3: 4}

for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            returnedList = proieltbs(tb, perArticleDict, totArticleNumber, allLemmas, allForms, allMorphs, answersDict)
            perArticleDict = returnedList[0]
            totArticleNumber = returnedList[1]
            allLemmas = returnedList[2]
            allForms = returnedList[3]
            allMorphs = returnedList[4]

labelList = ['Article', 'Morph']
addedList = allLemmas + allForms + allMorphs
ultimateList = list(set(addedList))
j = -2
while j < 0:
    labelNumber = str(j)
    numForm = labelNumber + 'form'
    numLemma = labelNumber + 'lemma'
    numMorph = labelNumber + 'morph'
    newList = [numForm, numLemma, numMorph]
    labelList.extend(newList)
    j += 1
j += 1
while j < 4:
    labelNumber = str(j)
    numForm = labelNumber + 'form'
    numLemma = labelNumber + 'lemma'
    numMorph = labelNumber + 'morph'
    newList = [numForm, numLemma, numMorph]
    labelList.extend(newList)
    j += 1

labelList.extend(['Answer'])
df = pd.DataFrame.from_dict(perArticleDict, orient='index')
df.columns = labelList
df = df.fillna('ellipsed')
df = df.sample(frac=1).reset_index(drop=True)
splitNum = int(df.shape[0]*.8)
dfTrain = df[:splitNum]
dfTest = df[splitNum:]
dfTrain.to_csv(outTrainPath, index=False)
dfTest.to_csv(outTestPath, index=False)
with open(lemmaListPath, "w") as output:
    for s in allLemmas:
        output.write("%s\n" % s)
with open(formListPath, "w") as output:
    for s in allForms:
        output.write("%s\n" % s)
with open(morphListPath, "w") as output:
    for s in allMorphs:
        output.write("%s\n" % s)
with open(ultimateListPath, "w") as output:
    for s in ultimateList:
        output.write("%s\n" % s)
print(len(allLemmas), 'lemmas in lemma list.')
print(len(allForms), 'forms in form list.')
print(len(allMorphs), 'morphologies in morph list.')
print(len(ultimateList), 'entries total in the ultimate list.')
print(len(perArticleDict), 'article entires.')
