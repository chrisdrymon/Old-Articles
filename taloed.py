from __future__ import absolute_import, division, print_function
import tensorflow as tf
import pandas as pd
import numpy as np
import talos
from tensorflow.keras import layers, callbacks
import os

print(tf.VERSION)
print(tf.keras.__version__)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# Preparing dictionaries to convert data into integers. Later they will be turned to one-hots.

classDict = {'Druid': 0, 'Hunter': 1, 'Mage': 2, 'Paladin': 3, 'Priest': 4, 'Rogue': 5, 'Shaman': 6,
             'Warlock': 7, 'Warrior': 8}
deckType = {'Aggro-Control': 0, 'Attrition': 1, 'Classic Aggro': 2, 'Classic Control': 3, 'Mid-Range': 4, 'Tempo': 5}
expansion = {'Vanilla': 0, 'BRM': 1, 'WOG': 2, 'Kara': 3, 'MSG': 4, 'Ungoro': 5, 'KFT': 6, 'KnC': 7, 'Woods': 8,
             'Boomsday': 9, 'Rumble': 10, 'RoS': 11}

df = pd.read_csv('/home/chris/Desktop/KrippDateless.csv', sep=',', header=None)
df = df.sample(frac=1)

preNump = []
preLabels = []
best = 0

for row in df.itertuples():

    # Turning classes to hots.
    hotNum = classDict[row[1]]
    classTens = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    classTens[hotNum] = 1

    # Normalizing the deck scores before adding them to the tensor.
    deckScore = ((row[2]-50)/30)

    # Turn deck type into a hot.
    deckHot = [0]*6
    deckHot[deckType[row[3]]] = 1

    # Turn expansion into a hot.
    expansHot = [0]*12
    expansHot[expansion[row[4]]] = 1

    # Combine data them into a single tensor.
    classTens.append(deckScore)
    combinedTens = classTens + deckHot + expansHot

    # Add that tensor to the list of tensors.
    preNump.append(combinedTens)

    # Convert that label to a hot and add to the list of labels.
    labelHot = [0, 0, 0]
    labelHot[row[5]] = 1
    preLabels.append(labelHot)

splitnum = int(df.shape[0]*.8)
traindata = np.array(preNump[:splitnum])
evaldata = np.array(preNump[splitnum:])
trainlabels = np.array(preLabels[:splitnum])
evallabels = np.array(preLabels[splitnum:])


def runnn(x_train, y_train, x_val, y_val, params):

    model = tf.keras.Sequential([layers.Dense(fdense1, kernel_regularizer=tf.keras.regularizers.l1(freg1),
                                               activation=factivation1, input_shape=(28,)),
                                 layers.Dropout(fdropout1),
                                 layers.Dense(fdense2, activation=factivation2),
                                 layers.Dropout(fdropout2),
                                 layers.Dense(3, activation='softmax')])

    optimizer = tf.keras.optimizers.Adam(lr=flearningrate)

    model.compile(optimizer=optimizer,
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])

    history = model.fit(x=x_train, y=y_train, batch_size=fbatchsize, epochs=400, verbose=0,
                           validation_data=(fevaldata, fevallabels), shuffle=True,
                           initial_epoch=0)

    return history, model



theBest = 0
samples = []

i = 1
while i < 51:
    graph = tf.Graph()
    with tf.Session(graph=graph):
        dense1, dropout1, reg1, dense2, dropout2, reg2, batchSize, learningRate, theModel = runnn(cbk, preNump,
                                                                                                  preLabels)
        print(i, dense1, dropout1, reg1, dense2, dropout2, reg2, batchSize, learningRate)
        item = 0
        tempBest = 0
        while item < len(theModel.history['acc']):
            if theModel.history['acc'][item] < theModel.history['val_acc'][item]:
                theWorst = theModel.history['acc'][item]
            else:
                theWorst = theModel.history['val_acc'][item]
            if theWorst > theBest:
                theBest = theWorst
                bestModel = i
                bestDense1 = dense1
                bestDropout1 = dropout1
                bestReg1 = reg1
                bestDense2 = dense2
                bestDropout2 = dropout2
                bestReg2 = reg2
                bestBatchSize = batchSize
                bestLearningRate = learningRate
                bestEpoch = item + 1
            if theWorst > tempBest:
                tempBest = theWorst
            item += 1
    tempParameters = [dense1, dropout1, reg1, dense2, dropout2, reg2, batchSize, learningRate, tempBest]
    samples.append(tempParameters)
    i += 1
hyperParameters = np.asarray(samples)
np.savetxt('/home/chris/Desktop/datelessparams.csv', hyperParameters, delimiter=',')
print("Best Model:", bestModel)
print("Layer 1:", bestDense1, "nodes,", bestDropout1 * 100, "% dropout.")
print("Layer 2:", bestDense2, "nodes,", bestDropout2 * 100, "% dropout.")
print("Batch Size:", bestBatchSize)
print("Learning Rate:", bestLearningRate)
print('The best accuracy is', theBest * 100, '% at epoch', bestEpoch)
