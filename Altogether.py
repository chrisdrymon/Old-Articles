import tensorflow as tf
import xml.etree.ElementTree as ET
import os
import pandas as pd

batchSize = 100
trainSteps = 100


def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(100).repeat().batch(batch_size)

    # Return the dataset.
    return dataset


def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features = dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset


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
    perArticleDict = {}
    totArticleNumber = 1
    totwordlist = ['ellipsed']
    for file_name in indir:
        if not file_name == 'README.md' and not file_name == '.git':
            tb = ET.parse(file_name)
            tbroot = tb.getroot()
            print(file_name)
            if tbroot.tag == 'proiel':
                returnedList = proieltbs(tb, perArticleDict, totArticleNumber, totwordlist)
                perArticleDict = returnedList[0]
                totArticleNumber = returnedList[1]
                totwordlist = returnedList[2]

    labellist = ['Article', 'Morph']
    j = -7
    while j < 0:
        labelNumber = str(j)
        numForm = labelNumber + 'form'
        numLemma = labelNumber + 'lemma'
        numMorph = labelNumber + 'morph'
        newList = [numForm, numLemma, numMorph]
        labellist.extend(newList)
        j += 1
    j += 1
    while j < 14:
        labelNumber = str(j)
        numForm = labelNumber + 'form'
        numLemma = labelNumber + 'lemma'
        numMorph = labelNumber + 'morph'
        newList = [numForm, numLemma, numMorph]
        labellist.extend(newList)
        j += 1

    labellist.extend(['Answer'])
    df = pd.DataFrame.from_dict(perArticleDict, orient='index')
    df = df.fillna('ellipsed')
    df.columns = labellist
    df = df.sample(frac=1).reset_index(drop=True)
    splitNum = int(df.shape[0]*.8)
    dfTrain = df[:splitNum]
    dfTest = df[splitNum:]

    outTrainName = 'MLTrain.csv'
    outTestName = 'MLTest.csv'
    outdir = '/home/chris/Desktop'
    outTrainPath = os.path.join(outdir, outTrainName)
    outTestPath = os.path.join(outdir, outTestName)
    dfTrain.to_csv(outTrainPath)
    dfTest.to_csv(outTestPath)

    dftrain_x = dfTrain
    dftrain_y = dfTrain.pop('Answer')
    dftest_x = dfTest
    dftest_y = dfTest.pop('Answer')

    totwordlist = [i for i in totwordlist if i !=None]
    tuple(totwordlist)

    return (dftrain_x, dftrain_y), (dftest_x, dftest_y), totwordlist, labellist


# Fetch the data
(train_x, train_y), (test_x, test_y), totwordList, labelList = fetchdata()

my_feature_columns = []
keyAnswer = {}
newLabelList = []
for whatev in labelList:
    if not whatev == 'Answer':
        newLabelList.append(whatev)

for value in newLabelList:
    keyAnswer[value] = totwordList

for key in keyAnswer:
    tempfeature = tf.feature_column.categorical_column_with_vocabulary_list(key=key, vocabulary_list=totwordList,
                                                                            default_value=0)
    my_feature_columns.append(tf.feature_column.indicator_column(tempfeature))

# Build 2 hidden layer DNN with 10, 10 units respectively.
classifier = tf.estimator.DNNClassifier(
    feature_columns=my_feature_columns,
    # Two hidden layers of 200 nodes each.
    hidden_units=[200, 200],
    # The model must choose between 21 classes.
    n_classes=21)

# Train the Model.
classifier.train(
    input_fn=lambda: train_input_fn(train_x, train_y, batchSize),
    steps=trainSteps)

# Evaluate the model.
eval_result = classifier.evaluate(
    input_fn=lambda: eval_input_fn(test_x, test_y, batchSize))

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))


tf.logging.set_verbosity(tf.logging.INFO)

with tf.Session() as sess:
    sess.run()
