from __future__ import absolute_import, division, print_function
import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras import layers

print(tf.VERSION)
print(tf.keras.__version__)

# Preparing dictionaries to convert data into integers. Later they will be turned to one-hots.
dayDict = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
           'Friday': 5, 'Saturday': 6}
classDict = {'Druid': 0, 'Hunter': 1, 'Mage': 2, 'Paladin': 3, 'Priest': 4, 'Rogue': 5, 'Shaman': 6,
             'Warlock': 7, 'Warrior': 8}
deckType = {'Aggro-Control': 0, 'Attrition': 1, 'Classic Aggro': 2, 'Classic Control': 3, 'Mid-Range': 4, 'Tempo': 5}
expansion = {'Vanilla': 0, 'BRM': 1, 'WOG': 2, 'Kara': 3, 'MSG': 4, 'Ungoro': 5, 'KFT': 6, 'KnC': 7, 'Woods': 8,
             'Boomsday': 9, 'Rumble': 10}

df = pd.read_csv('/home/chris/Desktop/KrippWins.csv', sep=',', header=None)
df = df.sample(frac=1)

preNump = []
preLabels = []

for row in df.itertuples():
    # Turning classes to hots.
    hotNum = classDict[row[1]]
    classTens = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    classTens[hotNum] = 1

    # Normalizing the deck scores before adding them to the tensor.
    deckScore = ((row[2]-50)/30)

    # Turning days to hots.
    hotNum = dayDict[row[3]]
    dayHot = [0, 0, 0, 0, 0, 0, 0]
    dayHot[hotNum] = 1

    # Turn day of month in to a hot.
    dateHot = [0]*31
    dateHot[row[4]-1] = 1

    # Turn month into a hot.
    monthHot = [0]*12
    monthHot[row[5]-1] = 1

    # Turn deck type into a hot.
    deckHot = [0]*6
    deckHot[deckType[row[6]]] = 1

    # Turn expansion into a hot.
    expansHot = [0]*11
    expansHot[expansion[row[7]]] = 1

    # Combine data them into a single tensor.
    classTens.append(deckScore)
    combinedTens = classTens + dayHot + dateHot + monthHot + deckHot + expansHot
    print(combinedTens)

    # Add that tensor to the list of tensors.
    preNump.append(combinedTens)

    # Convert that label to a hot and add to the list of labels.
    labelHot = [0, 0, 0]
    labelHot[row[8]] = 1
    preLabels.append(labelHot)

splitNum = int(df.shape[0]*.8)
trainData = np.array(preNump[:splitNum])
evalData = np.array(preNump[splitNum:])
trainLabels = np.array(preLabels[:splitNum])
evalLabels = np.array(preLabels[splitNum:])

model = tf.keras.Sequential([
layers.Dense(20, activation='relu', input_shape=(77,)),
layers.Dense(20, activation='relu'),
layers.Dense(3, activation='softmax')])

model.compile(optimizer=tf.train.AdamOptimizer(0.00001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

callbacks = [tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=30, mode='min', restore_best_weights=True),
             tf.keras.callbacks.TensorBoard(log_dir='/home/chris/Desktop/KrippLog', write_graph=True, write_images=True,
             histogram_freq=1, write_grads=True, update_freq='epoch')]

model.fit(x=trainData, y=trainLabels, batch_size=30, epochs=150, callbacks=callbacks,
          validation_data=(evalData, evalLabels), shuffle=True)

model.save('/home/chris/Desktop/KrippModel.h5')
