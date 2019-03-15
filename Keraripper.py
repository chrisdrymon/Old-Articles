import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras import layers

print(tf.VERSION)
print(tf.keras.__version__)

model = tf.keras.Sequential([
    layers.Dense(10, activation='relu', input_shape=(3,)),
    layers.Dense(10, activation='relu'),
    layers.Dense(3, activation='softmax')])

model.compile(optimizer=tf.train.AdamOptimizer(0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

train_samples = [['Tuesday', 'Paladin', 71.8], ['Tuesday', 'Rogue', 72.7], ['Tuesday', 'Warrior', 71.1], \
                 ['Wednesday', 'Mage', 69.4]]

train_labels = [2, 2, 0, 1]

model.fit(x=train_samples, y=train_labels, batch_size=4, epochs=10, shuffle=True)
