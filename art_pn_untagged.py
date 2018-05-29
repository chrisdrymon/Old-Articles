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
                    # Create lists of words or letters.
                    if not deaccent(token.get('form')) in allforms:
                        allforms.append(deaccent(token.get('form')))
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
                        except IndexError:
                            mlformatlist.append('OOR')
                        if token.get('part-of-speech') == 'S-':

                        fanswer =
                        mlformatlist.append(fanswer)
                        perarticledict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1

    returnlist = [perarticledict, totarticlenumber, allforms]
    return returnlist


def perseustbs(treebank, perarticledict, totarticlenumber, alllemmas, allpos, allletters, answersdict):
    froot = treebank.getroot()
    for body in froot:
        for sentence in body:
            allwordsinsent = sentence.findall(".*[@form]")
            # Loops through every word.
            for word in allwordsinsent:
                # Create lists of words or letters.
                if not deaccent(word.get('lemma')) in alllemmas:
                    alllemmas.append(deaccent(word.get('lemma')))
                for letter in word.get('postag'):
                    if letter not in allletters:
                        allletters.append(letter)
                # Creates all the values that will go into a single element.
                if word.get('lemma') == 'ὁ':
                    morph = word.get('postag')[1:]
                    articlenumber = allwordsinsent.index(word)
                    if body.get('jewish') == 'yes':
                        jewish = 'yes'
                    else:
                        jewish = 'no'
                    mlformatlist = [jewish]
                    for letter in morph:
                        mlformatlist.append(letter)
                    headwordplace = int(word.get('head')) - int(word.get('id'))
                    if headwordplace == 0:
                        print(sentence.get('id'))
                    nextwordid = articlenumber - 1
                    try:
                        lemma = deaccent(allwordsinsent[nextwordid].get('lemma'))
                        morph = allwordsinsent[nextwordid].get('postag')
                        mlformatlist.append(lemma)
                        for letter in morph:
                            mlformatlist.append(letter)
                    except IndexError:
                        mlformatlist.extend(['ellipsed']*10)
                    i = 1
                    while i < 5:
                        nextwordid = articlenumber + i
                        try:
                            lemma = deaccent(allwordsinsent[nextwordid].get('lemma'))
                            morph = allwordsinsent[nextwordid].get('postag')
                            mlformatlist.append(lemma)
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


treebankFolder = '/home/chris/Desktop/Treebanks/'

outTrainPath = Path('/home/chris/Desktop/MLTrain.csv')
outTestPath = Path('/home/chris/Desktop/MLTest.csv')
lemmaListPath = Path('/home/chris/Desktop/Lemmalist.txt')
lettersListPath = Path('/home/chris/Desktop/Letterslist.txt')
ultimateListPath = Path('/home/chris/Desktop/Everythinglist.txt')

os.chdir(treebankFolder)
indir = os.listdir(treebankFolder)

perArticleDict = {}
totArticleNumber = 1
allForms = ['yes', 'no', 'ellipsed']

posDict = {'A-': 'a', 'Df': 'd', 'Dq': 'd', 'S-': 'l', 'Ma': 'm', 'Mo': 'm', 'C-': 'c', 'I-': 'i', 'R-': 'r', 'Pd': 'p',
           'Px': 'p', 'Pp': 'p', 'Pk': 'p', 'Ps': 'p', 'Pc': 'p', 'Pr': 'p', 'Du': 'x', 'Pi': 'x', 'Ne': 'n', 'Nb': 'n',
           'V-': 'v', 'G-': 'G-', 'F-': 'F-'}

for file_name in indir:
    if not file_name == 'README.md' and not file_name == '.git':
        tb = Et.parse(file_name)
        tbroot = tb.getroot()
        print(file_name)
        if tbroot.tag == 'proiel':
            returnedList = proieltbs(tb, perArticleDict, totArticleNumber, allForms)
        else:
            returnedList = perseustbs(tb, perArticleDict, totArticleNumber, allForms, answersDict)

        perArticleDict = returnedList[0]
        totArticleNumber = returnedList[1]
        allForms = returnedList[2]
        allPOS = returnedList[3]
        allLetters = returnedList[4]

labelList = ['Jewish', 'Person', 'Number', 'Tense', 'Mood', 'Voice', 'Gender', 'Case', 'Degree', '-1lemma', '-1POS',
             '-1person', '-1number', '-1tense', '-1mood', '-1voice', '-1gender', '-1case', '-1degree']

addedList = allForms + allLetters + allPOS
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
    newList = [numLemma, numPOS, numPerson, numNumber, numTense, numMood, numVoice, numGender, numCase, numDegree]
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
    for s in allForms:
        output.write("%s\n" % s)
with open(lettersListPath, "w") as output:
    for s in allLetters:
        output.write("%s\n" % s)
with open(ultimateListPath, "w") as output:
    for s in ultimateList:
        output.write("%s\n" % s)
print(len(allForms), 'lemmas in lemma list.')
print(len(ultimateList), 'entries total in the ultimate list.')
print(len(perArticleDict), 'article entires.')
