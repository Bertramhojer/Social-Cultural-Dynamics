# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
d_training = pd.read_csv("classify_train.csv", sep = ",")
d_train = d_training.iloc[:,[0,1,2,3]]
train_label = d_training.iloc[:,4]
d_testing = pd.read_csv("classify_test.csv", sep = ",")
d_test = d_testing.iloc[:,[0,1,2,3]]
test_label = d_testing.iloc[:,4]


train_data = []

for i in range(len(d_train)):
	x = d_train.iloc[i, :]
	train_data.append(x)

#train_data = np.transpose(d_train)
train_data = np.asarray(train_data)
train_label = np.asarray(train_label)


print(train_data.shape)
print(train_label.shape)


test_data = []

for i in range(len(d_test)):
	x = d_test.iloc[i, :]
	test_data.append(x)

test_data = np.asarray(test_data)
test_label = np.asarray(test_label)
print(test_data.shape)
print(test_label.shape)

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
model.fit(train_data, train_label, epochs = n)


# evauluating the model
loss, test_acc = model.evaluate(test_data, test_label, verbose = 2)
print('\nTest Accuracy:', test_acc)





"""


d_test = pd.read_csv("sim_test_data.csv", sep = ",")
print(d_test.shape)
test = d_test.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12]]
test_label = d_test.iloc[:,13]

test_data = []

for i in range(len(d_test)):
	x = d_test.iloc[i, :]
	test_data.append(x)

test_data = np.asarray(test_data)
test_label = np.asarray(test_label)


d_train = pd.read_csv("sim_train.csv", sep = ",")
train = d_train.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12]]
train_label = d_train.iloc[:,13]

train_data = []

for i in range(len(d_train)):
	x = d_train.iloc[i, :]
	train_data.append(x)

train_data = np.asarray(train_data)
train_label = np.asarray(train_label)


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
model.fit(train_data, train_label, epochs = n)


# evauluating the model
loss, test_acc = model.evaluate(test_data, test_label, verbose = 2)
print('\nTest Accuracy:', test_acc)

