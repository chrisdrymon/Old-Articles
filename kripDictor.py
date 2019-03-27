from __future__ import absolute_import, division, print_function
import tensorflow as tf

print(tf.VERSION)
print(tf.keras.__version__)

# We're doing to use this to load a model and predict.
model = tf.keras.models.load_model('/home/chris/Desktop/KrippModel478Per.h5')

# Preparing dictionaries to convert data into integers. Later they will be turned to one-hots.
dayDict = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
           'Friday': 5, 'Saturday': 6}
classDict = {'Druid': 0, 'Hunter': 1, 'Mage': 2, 'Paladin': 3, 'Priest': 4, 'Rogue': 5, 'Shaman': 6,
             'Warlock': 7, 'Warrior': 8}
deckType = {'Aggro-Control': 0, 'Attrition': 1, 'Classic Aggro': 2, 'Classic Control': 3, 'Mid-Range': 4, 'Tempo': 5}
expansion = {'Vanilla': 0, 'BRM': 1, 'WOG': 2, 'Kara': 3, 'MSG': 4, 'Ungoro': 5, 'KFT': 6, 'KnC': 7, 'Woods': 8,
             'Boomsday': 9, 'Rumble': 10}

#     [Class,  Score,  Day,   Date, MM,   Deck Type,       Expansion]
row = ['Rogue', 70, 'Wednesday', 27, 3, 'Tempo', 'Rumble']

# Turning classes to hots.
hotNum = classDict[row[0]]
classTens = [0, 0, 0, 0, 0, 0, 0, 0, 0]
classTens[hotNum] = 1

# Normalizing the deck scores before adding them to the tensor.
deckScore = ((row[1] - 50) / 30)

# Turning days to hots.
hotNum = dayDict[row[2]]
dayHot = [0, 0, 0, 0, 0, 0, 0]
dayHot[hotNum] = 1

# Turn day of month in to a hot.
dateHot = [0] * 31
dateHot[row[3] - 1] = 1

# Turn month into a hot.
monthHot = [0] * 12
monthHot[row[4] - 1] = 1

# Turn deck type into a hot.
deckHot = [0] * 6
deckHot[deckType[row[5]]] = 1

# Turn expansion into a hot.
expansHot = [0] * 11
expansHot[expansion[row[6]]] = 1

# Combine data them into a single tensor.
classTens.append(deckScore)
combinedTens = classTens + dayHot + dateHot + monthHot + deckHot + expansHot

predicTens = [[combinedTens]]
prediction = model.predict(predicTens)
print(prediction)
