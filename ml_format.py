import xml.etree.ElementTree as Et
import os
import pandas as pd
from utility import deaccent
from pathlib import Path


def proieltbs(treebank, perarticledict, totarticlenumber, alllemmas, allforms, allmorphs, allletters, answersdict, allpos):
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
                    if not token.get('part-of-speech') in allpos:
                        allpos.append(token.get('part-of-speech'))
                    for letter in token.get('morphology'):
                        if letter not in allletters:
                            allletters.append(letter)
                    # Creates all the values that will go into a single element.
                    if token.get('lemma') == 'ὁ':
                        form = deaccent(token.get('form'))
                        morph = token.get('morphology')[:8]
                        pos = token.get('part-of-speech')
                        articlenumber = alltokesinsent.index(token)
                        if source.get('jewish') == 'yes':
                            jewish = 'yes'
                        else:
                            jewish = 'no'
                        mlformatlist = [form, jewish, morph, pos]
                        for letter in morph:
                            mlformatlist.append(letter)
                        headwordplace = int(token.get('head-id')) - int(token.get('id'))
                        nextwordid = articlenumber - 1
                        try:
                            form = deaccent(alltokesinsent[nextwordid].get('form'))
                            lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                            morph = alltokesinsent[nextwordid].get('morphology')[:8]
                            pos = alltokesinsent[nextwordid].get('part-of-speech')
                            mlformatlist.extend([form, lemma, morph, pos])
                            for letter in morph:
                                mlformatlist.append(letter)
                        except IndexError:
                            mlformatlist.extend(['ellipsed']*12)
                        i = 1
                        while i < 5:
                            nextwordid = articlenumber + i
                            try:
                                form = deaccent(alltokesinsent[nextwordid].get('form'))
                                lemma = deaccent(alltokesinsent[nextwordid].get('lemma'))
                                morph = alltokesinsent[nextwordid].get('morphology')[:8]
                                pos = alltokesinsent[nextwordid].get('part-of-speech')
                                mlformatlist.extend([form, lemma, morph, pos])
                                for letter in morph:
                                    mlformatlist.append(letter)
                            except IndexError:
                                mlformatlist.extend(['ellipsed']*12)
                            i += 1
                        if headwordplace < -1 or headwordplace > 4:
                            fanswer = 5
                        else:
                            fanswer = answersdict[headwordplace]
                        mlformatlist.append(fanswer)
                        perarticledict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1

    returnlist = [perarticledict, totarticlenumber, alllemmas, allforms, allmorphs, allletters, allpos]
    return returnlist


def perseustbs(treebank, perarticledict, totarticlenumber, alllemmas, allforms, allmorphs, allletters, answersdict):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for body in froot:
        for sentence in body:
            alltokesinsent = sentence.findall(".*[@form]")
            # Loops through every word.
            for word in alltokesinsent:
                # Create lists of words or letters.
                if not deaccent(word.get('lemma')) in alllemmas:
                    alllemmas.append(deaccent(word.get('lemma')))
                if not deaccent(word.get('form')) in allforms:
                    allforms.append(deaccent(word.get('form')))
                if not word.get('postag') in allmorphs:
                    allmorphs.append(word.get('postag'))
                for letter in word.get('postag'):
                    if letter not in allletters:
                        allletters.append(letter)
                # Creates all the values that will go into a single element.
                if word.get('lemma') == 'ὁ':
                    form = deaccent(word.get('form'))
                    morph = word.get('postag')
                    articlenumber = alltokesinsent.index(word)
                    if body.get('jewish') == 'yes':
                        jewish = 'yes'
                    else:
                        jewish = 'no'
                    mlformatlist = [form, morph, jewish]
                    for letter in morph:
                        mlformatlist.append(letter)
                    headwordplace = int(word.get('head-id')) - int(word.get('id'))
                    i = -1
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
            returnedList = proieltbs(tb, perArticleDict, totArticleNumber, allLemmas, allForms, allMorphs, allLetters,
                                     answersDict, allPOS)
        else:
            returnedList = perseustbs(tb, perArticleDict, totArticleNumber, allLemmas, allForms, allMorphs, allLetters,
                                      answersDict)

        perArticleDict = returnedList[0]
        totArticleNumber = returnedList[1]
        allLemmas = returnedList[2]
        allForms = returnedList[3]
        allMorphs = returnedList[4]
        allLetters = returnedList[5]

labelList = ['Article', 'Jewish', 'Morph', 'POS', 'Person', 'Number', 'Tense', 'Mood', 'Voice', 'Gender', 'Case',
             'Degree', '-1form', '-1lemma', '-1morph', '-1POS', '-1person', '-1number', '-1tense', '-1mood', '-1voice',
             '-1gender', '-1case', '-1degree']
addedList = allLemmas + allForms + allMorphs + allLetters + allPOS
ultimateList = list(set(addedList))

j = 1
while j < 5:
    labelNumber = str(j)
    numForm = labelNumber + 'form'
    numLemma = labelNumber + 'lemma'
    numMorph = labelNumber + 'morph'
    numPOS = labelNumber + 'POS'
    numPerson = labelNumber + 'person'
    numNumber = labelNumber + 'number'
    numTense = labelNumber + 'tense'
    numMood = labelNumber + 'mood'
    numVoice = labelNumber + 'voice'
    numGender = labelNumber + 'gender'
    numCase = labelNumber + 'case'
    numDegree = labelNumber + 'degree'
    newList = [numForm, numLemma, numMorph, numPOS, numPerson, numNumber, numTense, numMood, numVoice, numGender,
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
