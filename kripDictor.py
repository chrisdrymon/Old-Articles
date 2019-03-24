from __future__ import absolute_import, division, print_function
import tensorflow as tf

print(tf.VERSION)
print(tf.keras.__version__)

# We're doing to use this to load a model and predict.
model = tf.keras.models.load_model('/home/chris/Desktop/KrippModel324.h5')

# Preparing dictionaries to convert data into integers. Later they will be turned to one-hots.
dayDict = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
           'Friday': 5, 'Saturday': 6}
classDict = {'Druid': 0, 'Hunter': 1, 'Mage': 2, 'Paladin': 3, 'Priest': 4, 'Rogue': 5, 'Shaman': 6,
             'Warlock': 7, 'Warrior': 8}

testList = ['Sunday', 'Warlock', 75]

hotNum = dayDict[testList[0]]
hot1 = [0, 0, 0, 0, 0, 0, 0]
hot1[hotNum] = 1
# Turning classes to hots
hotNum = classDict[testList[1]]
hot2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
hot2[hotNum] = 1
# Combining them into a single tensor.
combinedTens = hot1 + hot2
# Normalizing the deck scores before adding them to the tensor.
combinedTens.append((testList[2] - 60) / 20)
predicTens = [[combinedTens]]
prediction = model.predict(predicTens)
print(prediction)
