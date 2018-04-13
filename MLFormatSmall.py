import xml.etree.ElementTree as ET
import os
import pandas as pd


def proieltbs(treebank, perarticledict, totarticlenumber, alllemmas, allforms, allmorphs):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            for sentence in division:
                alltokesinsent = sentence.findall('token')
                for token in alltokesinsent:
                    if not token.get('lemma') in alllemmas:
                        alllemmas.append(token.get('lemma'))
                    if not token.get('form') in allforms:
                        allforms.append(token.get('form'))
                    if not token.get('morphology'):
                        allmorphs.append(token.get('morphology'))
                    if token.get('lemma') == 'ὁ':
                        form = token.get('form')
                        morph = token.get('morphology')
                        articlenumber = alltokesinsent.index(token)
                        mlformatlist = [form, morph]
                        headwordplace = int(token.get('head-id')) - int(token.get('id'))
                        i = -2
                        while i < 0:
                            nextwordid = articlenumber + i
                            try:
                                form = alltokesinsent[nextwordid].get('form')
                                lemma = alltokesinsent[nextwordid].get('lemma')
                                morph = alltokesinsent[nextwordid].get('morphology')
                                mlformatlist.extend([form, lemma, morph])
                            except IndexError:
                                mlformatlist.extend(['ellipsed', 'ellipsed', 'ellipsed'])
                            i += 1
                        i += 1
                        while i < 4:
                            nextwordid = articlenumber + i
                            try:
                                form = alltokesinsent[nextwordid].get('form')
                                lemma = alltokesinsent[nextwordid].get('lemma')
                                morph = alltokesinsent[nextwordid].get('morphology')
                                mlformatlist.extend([form, lemma, morph])
                            except IndexError:
                                mlformatlist.extend(['ellipsed', 'ellipsed', 'ellipsed'])
                            i += 1
                        perarticledict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1
                        if alltokesinsent[headwordplace].get('empty-token-sort') or headwordplace < -2\
                                or headwordplace > 4:
                            fanswer = 'ellipsed'
                        else:
                            fanswer = headwordplace
                        mlformatlist.extend([fanswer])
    returnlist = [perarticledict, totarticlenumber, alllemmas, allforms, allmorphs]
    return returnlist


os.chdir('/home/chris/Desktop/CustomTB')
indir = os.listdir('/home/chris/Desktop/CustomTB')
perArticleDict = {}
totArticleNumber = 1
allLemmas = []
allForms = []
allMorphs = []
for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = ET.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            returnedList = proieltbs(tb, perArticleDict, totArticleNumber, allLemmas, allForms, allMorphs)
            perArticleDict = returnedList[0]
            totArticleNumber = returnedList[1]
            allLemmas = returnedList[2]
            allForms = returnedList[3]
            allMorphs = returnedList[4]

labelList = ['Article', 'Morph']
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

outTrainName = 'SmallMLTrain.csv'
outTestName = 'SmallMLTest.csv'
outdir = '/home/chris/Desktop'
outTrainPath = os.path.join(outdir, outTrainName)
outTestPath = os.path.join(outdir, outTestName)
dfTrain.to_csv(outTrainPath, index=False)
dfTest.to_csv(outTestPath, index=False)
