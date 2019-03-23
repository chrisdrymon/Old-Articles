from __future__ import absolute_import, division, print_function
import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras import layers

print(tf.VERSION)
print(tf.keras.__version__)

#Preparing dictionaries to convert data into integers. Later they will be turned to one-hots.
dayDict = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,\
           'Friday': 5, 'Saturday': 6}
classDict = {'Druid': 0, 'Hunter': 1, 'Mage': 2, 'Paladin': 3, 'Priest': 4, 'Rogue': 5, 'Shaman': 6,\
             'Warlock': 7, 'Warrior': 8}

df = pd.read_csv('/home/chris/Desktop/KrippWins.csv', sep=',',header=None)
df = df.sample(frac=1)
preNump = []
preLabels = []

for row in df.itertuples():
    # Turning days to hots
    hotNum = dayDict[row[1]]
    hot1 = [0, 0, 0, 0, 0, 0, 0]
    hot1[hotNum] = 1
    # Turning classes to hots
    hotNum = classDict[row[2]]
    hot2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    hot2[hotNum] = 1
    # Combining them into a single tensor.
    combinedTens = hot1 + hot2
    # Normalizing the deck scores before adding them to the tensor.
    combinedTens.append((row[3]-60)/20)
    # Add that tensor to the list of tensors.
    preNump.append(combinedTens)
    # Convert that label to a hot and add to the list of labels.
    hot3 = [0, 0, 0]
    hot3[row[4]] = 1
    preLabels.append(hot3)

splitNum = int(df.shape[0]*.8)
trainData = np.array(preNump[:splitNum])
evalData = np.array(preNump[splitNum:])
trainLabels = np.array(preLabels[:splitNum])
evalLabels = np.array(preLabels[splitNum:])
print(df.shape[0], len(trainData), len(evalData))

model = tf.keras.Sequential([
layers.Dense(20, activation='relu', input_shape=(17,)),
layers.Dense(20, activation='relu'),
layers.Dense(3, activation='softmax')])

model.compile(optimizer=tf.train.AdamOptimizer(0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x=trainData, y=trainLabels, batch_size=30, epochs=50, validation_data=(evalData, evalLabels), shuffle=True)
model.save('/home/chris/Desktop/KrippModel544.h5')
