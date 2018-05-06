import xml.etree.ElementTree as ET
import os
import pandas as pd
from utility import deaccent
from pathlib import Path


def proieltbs(treebank, perarticledict, totarticlenumber, alllemmas, allforms, allmorphs, allletters, answersdict):
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
                    if not deaccent(token.get('form')) in allforms:
                        allforms.append(deaccent(token.get('form')))
                    if not token.get('morphology') in allmorphs:
                        allmorphs.append(token.get('morphology'))
                    for letter in token.get('morphology'):
                        if letter not in allletters:
                            allletters.append(letter)
                    # Creates all the values that will go into a single element.
                    if token.get('lemma') == 'ὁ':
                        form = deaccent(token.get('form'))
                        morph = token.get('morphology')
                        articlenumber = alltokesinsent.index(token)
                        if source.get('jewish') == 'yes':
                            jewish = 'yes'
                        else:
                            jewish = 'no'
                        mlformatlist = [form, morph, jewish]
                        for letter in morph:
                            mlformatlist.append(letter)
                        headwordplace = int(token.get('head-id')) - int(token.get('id'))
                        i = -2
                        while i < 0:
                            nextwordid = articlenumber + i
                            try:
                                form = deaccent(alltokesinsent[nextwordid].get('form'))
                                lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                                morph = alltokesinsent[nextwordid].get('morphology')
                                mlformatlist.extend([form, lemma, morph])
                                for letter in morph:
                                    mlformatlist.append(letter)
                            except IndexError:
                                mlformatlist.extend(['ellipsed']*13)
                            i += 1
                        i += 1
                        while i < 4:
                            nextwordid = articlenumber + i
                            try:
                                form = deaccent(alltokesinsent[nextwordid].get('form'))
                                lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                                morph = alltokesinsent[nextwordid].get('morphology')
                                mlformatlist.extend([form, lemma, morph])
                                for letter in morph:
                                    mlformatlist.append(letter)
                            except IndexError:
                                mlformatlist.extend(['ellipsed']*13)
                            i += 1
                        if headwordplace < -2 or headwordplace > 3:
                            fanswer = 5
                        else:
                            fanswer = answersdict[headwordplace]
                        mlformatlist.append(fanswer)
                        perarticledict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1

    returnlist = [perarticledict, totarticlenumber, alllemmas, allforms, allmorphs, allletters]
    return returnlist


def perseustbs(treebank, perarticledict, totarticlenumber, alllemmas, allforms, allmorphs, allletters, answersdict):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for body in froot:
        for sentence in body:
            alltokesinsent = sentence.findall(".*[@form]")
            # Loops through every word.
            for token in alltokesinsent:
                # Create lists of words or letters.
                if not deaccent(token.get('lemma')) in alllemmas:
                    alllemmas.append(deaccent(token.get('lemma')))
                if not deaccent(token.get('form')) in allforms:
                    allforms.append(deaccent(token.get('form')))
                if not token.get('postag') in allmorphs:
                    allmorphs.append(token.get('postag'))
                for letter in token.get('postag'):
                    if letter not in allletters:
                        allletters.append(letter)
                # Creates all the values that will go into a single element.
                if token.get('lemma') == 'ὁ':
                    form = deaccent(token.get('form'))
                    morph = token.get('postag')
                    articlenumber = alltokesinsent.index(token)
                    if source.get('jewish') == 'yes':
                        jewish = 'yes'
                    else:
                        jewish = 'no'
                    mlformatlist = [form, morph, jewish]
                    for letter in morph:
                        mlformatlist.append(letter)
                    headwordplace = int(token.get('head-id')) - int(token.get('id'))
                    i = -2
                    while i < 0:
                        nextwordid = articlenumber + i
                        try:
                            form = deaccent(alltokesinsent[nextwordid].get('form'))
                            lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                            morph = alltokesinsent[nextwordid].get('postag')
                            mlformatlist.extend([form, lemma, morph])
                            for letter in morph:
                                mlformatlist.append(letter)
                        except IndexError:
                            mlformatlist.extend(['ellipsed']*13)
                        i += 1
                    i += 1
                    while i < 4:
                        nextwordid = articlenumber + i
                        try:
                            form = deaccent(alltokesinsent[nextwordid].get('form'))
                            lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                            morph = alltokesinsent[nextwordid].get('postag')
                            mlformatlist.extend([form, lemma, morph])
                            for letter in morph:
                                mlformatlist.append(letter)
                        except IndexError:
                            mlformatlist.extend(['ellipsed']*12)
                        i += 1
                    if headwordplace < -2 or headwordplace > 3:
                        fanswer = 5
                    else:
                        fanswer = answersdict[headwordplace]
                    mlformatlist.append(fanswer)
                    perarticledict[totarticlenumber] = mlformatlist
                    totarticlenumber += 1

    returnlist = [perarticledict, totarticlenumber, alllemmas, allforms, allmorphs, allletters]
    return returnlist


treebankFolder = '/home/chris/Desktop/CustomTB/'

outTrainPath = Path('/home/chris/Desktop/MLTrain.csv')
outTestPath = Path('/home/chris/Desktop/MLTest.csv')
lemmaListPath = Path('/home/chris/Desktop/Lemmalist.txt')
formListPath = Path('/home/chris/Desktop/Formlist.txt')
morphListPath = Path('/home/chris/Desktop/Morphlist.txt')
lettersListPath = Path('/home/chris/Desktop/Letterslist.txt')
ultimateListPath = Path('/home/chris/Desktop/Everythinglist.txt')

os.chdir(treebankFolder)
indir = os.listdir(treebankFolder)

perArticleDict = {}
totArticleNumber = 1
allLemmas = ['yes', 'no']
allForms = []
allMorphs = []
allLetters = []
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
            returnedList = proieltbs(tb, perArticleDict, totArticleNumber, allLemmas, allForms, allMorphs, allLetters,
                                     answersDict)
        else:
            returnedList = perseustbs(tb, perArticleDict, totArticleNumber, allLemmas, allForms, allMorphs, allLetters,
                                      answersDict)

        perArticleDict = returnedList[0]
        totArticleNumber = returnedList[1]
        allLemmas = returnedList[2]
        allForms = returnedList[3]
        allMorphs = returnedList[4]
        allLetters = returnedList[5]

labelList = ['Article', 'Morph', 'Jewish', 'Person', 'Number', 'Tense', 'Mood', 'Voice', 'Gender', 'Case', 'Degree',
             'Strength', 'Inflection']
addedList = allLemmas + allForms + allMorphs + allLetters
ultimateList = list(set(addedList))
j = -2
while j < 0:
    labelNumber = str(j)
    numForm = labelNumber + 'form'
    numLemma = labelNumber + 'lemma'
    numMorph = labelNumber + 'morph'
    numPerson = labelNumber + 'person'
    numNumber = labelNumber + 'number'
    numTense = labelNumber + 'tense'
    numMood = labelNumber + 'mood'
    numVoice = labelNumber + 'voice'
    numGender = labelNumber + 'gender'
    numCase = labelNumber + 'case'
    numDegree = labelNumber + 'degree'
    numStrength = labelNumber + 'strength'
    numInflection = labelNumber + 'inflection'
    newList = [numForm, numLemma, numMorph, numPerson, numNumber, numTense, numMood, numVoice, numGender, numCase,
               numDegree, numStrength, numInflection]
    labelList.extend(newList)
    j += 1
j += 1
while j < 4:
    labelNumber = str(j)
    numForm = labelNumber + 'form'
    numLemma = labelNumber + 'lemma'
    numMorph = labelNumber + 'morph'
    numPerson = labelNumber + 'person'
    numNumber = labelNumber + 'number'
    numTense = labelNumber + 'tense'
    numMood = labelNumber + 'mood'
    numVoice = labelNumber + 'voice'
    numGender = labelNumber + 'gender'
    numCase = labelNumber + 'case'
    numDegree = labelNumber + 'degree'
    numStrength = labelNumber + 'strength'
    numInflection = labelNumber + 'inflection'
    newList = [numForm, numLemma, numMorph, numPerson, numNumber, numTense, numMood, numVoice, numGender, numCase,
               numDegree, numStrength, numInflection]
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
with open(lettersListPath, "w") as output:
    for s in allLetters:
        output.write("%s\n" % s)
with open(ultimateListPath, "w") as output:
    for s in ultimateList:
        output.write("%s\n" % s)
print(len(allLemmas), 'lemmas in lemma list.')
print(len(allForms), 'forms in form list.')
print(len(allMorphs), 'morphologies in morph list.')
print(len(ultimateList), 'entries total in the ultimate list.')
print(len(perArticleDict), 'article entires.')
