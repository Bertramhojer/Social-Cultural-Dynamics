# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

# epochs
n = 10

# Setting up the model layers
# initial model with 2, 128-node dense layers with activation function relu and 1 final classification dense-layer.
model = keras.Sequential([
	keras.layers.Dense(128, activation = 'relu'),
	keras.layers.Dense(128, activation = 'relu'),
	keras.layers.Dense(2)
	])

# Compiling the model
model.compile(optimizer = 'adam',
	loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
	metrics = ['accuracy'])

# fitting the model
model.fit(train_data, train_labels, epochs = n)

# evauluating the model
loss, test_acc = model.evaluate(test_data, test_labels, verbose = 2)
print('\nTest Accuracy:', test_acc)