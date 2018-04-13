import tensorflow as tf
import xml.etree.ElementTree as ET
import os
import pandas as pd


def proieltbs(treebank, perarticledict, totarticlenumber, totwordlist):
    """Creates lists in ML format for each article."""
    froot = treebank.getroot()
    for source in froot:
        for division in source:
            for sentence in division:
                alltokesinsent = sentence.findall('token')
                for token in alltokesinsent:
                    if not token.get('form') in totwordlist:
                        totwordlist.append(token.get('form'))
                    if not token.get('lemma') in totwordlist:
                        totwordlist.append(token.get('lemma'))
                    if not token.get('morphology') in totwordlist:
                        totwordlist.append(token.get('morphology'))
                    if token.get('lemma') == 'ὁ':
                        form = token.get('form')
                        morph = token.get('morphology')
                        articlenumber = alltokesinsent.index(token)
                        mlformatlist = [form, morph]
                        headwordplace = int(token.get('head-id')) - int(token.get('id'))
                        i = -7
                        while i < 0:
                            nextwordid = articlenumber + i
                            try:
                                form = alltokesinsent[nextwordid].get('form')
                                lemma = alltokesinsent[nextwordid].get('lemma')
                                morph = alltokesinsent[nextwordid].get('morphology')
                                mlformatlist.extend([form, lemma, morph])
                            except IndexError:
                                mlformatlist.extend([None, None, None])
                            i += 1
                        i += 1
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
                        if alltokesinsent[headwordplace].get('empty-token-sort'):
                            fanswer = None
                        else:
                            fanswer = str(headwordplace)
                        mlformatlist.extend([fanswer])
                        perarticledict[totarticlenumber] = mlformatlist
                        totarticlenumber += 1
    returnlist = [perarticledict, totarticlenumber, totwordlist]
    return returnlist


def fetchdata():
    os.chdir('/home/chris/Desktop/CustomTB')
    indir = os.listdir('/home/chris/Desktop/CustomTB')
    per_article_dict = {}
    tot_article_number = 1
    totwordlist = ['ellipsed']
    for file_name in indir:
        if not file_name == 'README.md' and not file_name == '.git':
            tb = ET.parse(file_name)
            tbroot = tb.getroot()
            print(file_name)
            if tbroot.tag == 'proiel':
                returnedList = proieltbs(tb, per_article_dict, tot_article_number, totwordlist)
                per_article_dict = returnedList[0]
                tot_article_number = returnedList[1]
                totwordlist = returnedList[2]

    labellist = ['Article', 'Morph']
    j = -7
    while j < 0:
        label_number = str(j)
        num_form = label_number + 'form'
        num_lemma = label_number + 'lemma'
        num_morph = label_number + 'morph'
        new_list = [num_form, num_lemma, num_morph]
        labellist.extend(new_list)
        j += 1
    j += 1
    while j < 14:
        label_number = str(j)
        num_form = label_number + 'form'
        num_lemma = label_number + 'lemma'
        num_morph = label_number + 'morph'
        new_list = [num_form, num_lemma, num_morph]
        labellist.extend(new_list)
        j += 1

    labellist.extend(['Answer'])
    df = pd.DataFrame.from_dict(per_article_dict, orient='index')
    df = df.fillna('ellipsed')
    df.columns = labellist
    df = df.sample(frac=1).reset_index(drop=True)

    split_num = int(df.shape[0]*.8)
    df_train = df[:split_num]
    df_test = df[split_num:]

    out_train_name = 'MLTrain.csv'
    out_test_name = 'MLTest.csv'
    outdir = '/home/chris/Desktop'
    out_train_path = os.path.join(outdir, out_train_name)
    out_test_path = os.path.join(outdir, out_test_name)
    df_train.to_csv(out_train_path)
    df_test.to_csv(out_test_path)

    dftrain_x = tf.constant(df_train)
    dftrain_y = tf.constant(df_train.pop('Answer'))

    dftest_x = tf.constant(df_test)
    dftest_y = tf.constant(df_test.pop('Answer'))

    totwordlist = [i for i in totwordlist if i !=None]

    tuple(totwordlist)

    return (dftrain_x, dftrain_y), (dftest_x, dftest_y), totwordlist, labellist


(trainX, trainY), (testX, testY), totWordList, labelList = fetchdata()

trainXslice = tf.data.Dataset.from_tensor_slices(trainX)

print(trainXslice.output_shapes)