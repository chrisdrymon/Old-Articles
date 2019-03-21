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
    readyMat = hot1 + hot2
    readyMat.append((row[3]-60)/20)
    tempList.append(readyMat)
formatted = np.array(tempList)
print(formatted)

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
