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
df.sample(frac=1)
tempList = []

for row in df.itertuples():
    hotNum = dayDict[row[1]]
    hot1 = [0, 0, 0, 0, 0, 0, 0]
    hot1[hotNum] = 1
    hotNum = classDict[row[2]]
    hot2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    hot2[hotNum] = 1
    preNump = hot1 + hot2
    preNump.append((row[3]-60)/20)
    preNump.append(row[4])

    tempList.append(readyMat)
splitNum = int(df.shape[0]*.8)
trainData = df.head(splitNum)
evalData = df.tail(df.shape[0]-splitNum)
trainLabels = trainData.pop(3)
evalLabels = evalData.pop(3)
print(trainLabels)
print(df.shape[0], trainData.shape[0], evalData.shape[0])
formatted = np.array(tempList)

model = tf.keras.Sequential([
layers.Dense(10, activation='relu', input_shape=(17,)),
layers.Dense(10, activation='relu'),
layers.Dense(3, activation='softmax')])

model.compile(optimizer=tf.train.AdamOptimizer(0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

#train_labels = np.array(y_binary)
#print(train_labels)

#model.fit(x=train_samples, y=train_labels, batch_size=4, epochs=10, shuffle=True)
