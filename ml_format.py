import xml.etree.ElementTree as Et
import os
import pandas as pd
from utility import deaccent
from pathlib import Path


def proieltbs(treebank, perarticledict, totarticlenumber, alllemmas, allletters, answersdict, allpos):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            for sentence in division:
                alltokesinsent = sentence.findall(".*[@form]")
                # Loops through every word.
                for token in alltokesinsent:
                    # Create lists of words or letters.
                    if not deaccent(token.get('lemma')) in alllemmas:
                        alllemmas.append(deaccent(token.get('lemma')))
                    if not token.get('part-of-speech') in allpos:
                        allpos.append(token.get('part-of-speech'))
                    for letter in token.get('morphology'):
                        if letter not in allletters:
                            allletters.append(letter)
                    # Creates all the values that will go into a single element.
                    if token.get('lemma') == 'ὁ':
                        morph = token.get('morphology')[:8]
                        pos = token.get('part-of-speech')
                        articlenumber = alltokesinsent.index(token)
                        if source.get('jewish') == 'yes':
                            jewish = 'yes'
                        else:
                            jewish = 'no'
                        mlformatlist = [jewish, pos]
                        for letter in morph:
                            mlformatlist.append(letter)
                        headwordplace = int(token.get('head-id')) - int(token.get('id'))
                        nextwordid = articlenumber - 1
                        try:
                            lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                            morph = alltokesinsent[nextwordid].get('morphology')[:8]
                            pos = alltokesinsent[nextwordid].get('part-of-speech')
                            mlformatlist.extend([lemma, pos])
                            for letter in morph:
                                mlformatlist.append(letter)
                        except IndexError:
                            mlformatlist.extend(['ellipsed']*10)
                        i = 1
                        while i < 5:
                            nextwordid = articlenumber + i
                            try:
                                lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                                morph = alltokesinsent[nextwordid].get('morphology')[:8]
                                pos = alltokesinsent[nextwordid].get('part-of-speech')
                                mlformatlist.extend([lemma, pos])
                                for letter in morph:
                                    mlformatlist.append(letter)
                            except IndexError:
                                mlformatlist.extend(['ellipsed']*10)
                            i += 1
                        if headwordplace < -1 or headwordplace > 4:
                            fanswer = 5
                        else:
                            fanswer = answersdict[headwordplace]
                        mlformatlist.append(fanswer)
                        perarticledict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1

    returnlist = [perarticledict, totarticlenumber, alllemmas, allpos, allletters]
    return returnlist


def perseustbs(treebank, perarticledict, totarticlenumber, alllemmas, allletters, answersdict, allpos):

    returnlist = [perarticledict, totarticlenumber, alllemmas, allpos, allletters]
    return returnlist

treebankFolder = '/home/chris/Desktop/CustomTB/'

outTrainPath = Path('/home/chris/Desktop/MLTrain.csv')
outTestPath = Path('/home/chris/Desktop/MLTest.csv')
lemmaListPath = Path('/home/chris/Desktop/Lemmalist.txt')
lettersListPath = Path('/home/chris/Desktop/Letterslist.txt')
ultimateListPath = Path('/home/chris/Desktop/Everythinglist.txt')

os.chdir(treebankFolder)
indir = os.listdir(treebankFolder)

perArticleDict = {}
totArticleNumber = 1
allLemmas = ['yes', 'no']
allLetters = []
allPOS = []
answersDict = {-1: 0,
               1: 1,
               2: 2,
               3: 3,
               4: 4,
               5: 5}

for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = Et.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            returnedList = proieltbs(tb, perArticleDict, totArticleNumber, allLemmas, allPOS, allLetters, answersDict)
        else:
            returnedList = perseustbs(tb, perArticleDict, totArticleNumber, allLemmas, allPOS, allLetters, answersDict)

        perArticleDict = returnedList[0]
        totArticleNumber = returnedList[1]
        allLemmas = returnedList[2]
        allPOS = returnedList[3]
        allLetters = returnedList[4]

labelList = ['Jewish', 'POS', 'Person', 'Number', 'Tense', 'Mood', 'Voice', 'Gender', 'Case', 'Degree', '-1lemma',
             '-1POS', '-1person', '-1number', '-1tense', '-1mood', '-1voice', '-1gender', '-1case', '-1degree']

addedList = allLemmas + allLetters + allPOS
ultimateList = list(set(addedList))

j = 1
while j < 5:
    labelNumber = str(j)
    numLemma = labelNumber + 'lemma'
    numPOS = labelNumber + 'POS'
    numPerson = labelNumber + 'person'
    numNumber = labelNumber + 'number'
    numTense = labelNumber + 'tense'
    numMood = labelNumber + 'mood'
    numVoice = labelNumber + 'voice'
    numGender = labelNumber + 'gender'
    numCase = labelNumber + 'case'
    numDegree = labelNumber + 'degree'
    newList = [numLemma, numPOS, numPerson, numNumber, numTense, numMood, numVoice, numGender,
               numCase, numDegree]
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
with open(lettersListPath, "w") as output:
    for s in allLetters:
        output.write("%s\n" % s)
with open(ultimateListPath, "w") as output:
    for s in ultimateList:
        output.write("%s\n" % s)
print(len(allLemmas), 'lemmas in lemma list.')
print(len(ultimateList), 'entries total in the ultimate list.')
print(len(perArticleDict), 'article entires.')
