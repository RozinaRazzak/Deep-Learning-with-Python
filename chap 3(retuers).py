# -*- coding: utf-8 -*-
"""Reuters.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_pNgy-j1q-gRcMquj8tCaj_94WZHwoZO

# Multiclass Classification

# Loading the Reuters dataset
"""

from keras.datasets import reuters

(train_data, train_labels), (test_data, test_labels) = reuters.load_data(num_words = 10000)

len(train_data)

len(test_data)

train_data[0]

"""# Decoding newswires back to text"""

word_index =reuters.get_word_index()
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
decoded_newswire = " ".join([reverse_word_index.get(i - 3, "?") for i in train_data[0]])

train_labels[10]

"""# Encoding the data"""

import numpy as np

def vectorize_sequences(sequences, dimension = 10000):
  results = np.zeros((len(sequences), dimension))
  for i, sequence in enumerate(sequences):
    results[i, sequence] = 1.
  return results


x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

def to_one_hot(labels, dimension = 46):
  results = np.zeros((len(labels), dimension))
  for i, label in enumerate(labels):
    results[i, label] = 1.
  return results

one_hot_train_labels = to_one_hot(train_labels)
one_hot_test_labels = to_one_hot(test_labels)

!pip install keras.utils

from keras.utils import to_categorical

one_hot_train_labels = to_categorical(train_labels)
one_hot_test_labels = to_categorical(test_labels)

"""# Model Definition"""

from keras import models
from keras import layers

model = models.Sequential()
model.add(layers.Dense(64, activation= "relu", input_shape = (10000,)))
model.add(layers.Dense(64, activation = "relu"))
model.add(layers.Dense(46, activation = "softmax"))

"""# Compiling the model"""

model.compile(optimizer = "rmsprop",
              loss = "categorical_crossentropy",
              metrics = ["accuracy"])

"""# Setting aside a validation set"""

x_val = x_train[:1000]
partial_x_train = x_train[1000:]

y_val = one_hot_train_labels[:1000]
partial_y_train = one_hot_train_labels[1000:]

"""# Training the model"""

history = model.fit(partial_x_train,
                     partial_y_train,
                     epochs = 20,
                     batch_size = 512,
                     validation_data = (x_val, y_val))

"""# Plotting the training and validation loss"""

import matplotlib.pyplot as plt

loss = history.history["loss"]
val_loss = history.history["val_loss"]

epochs = range(1, len(loss)+1)

plt.plot(epochs, loss, "bo", label = "Training loss")
plt.plot(epochs , val_loss,"b", label = "Validation loss")

plt.title("Training and Validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

"""# Plotting the training and validation accuracy"""

plt.clf()

acc = history.history["accuracy"]
val_acc = history.history["val_accuracy"]

plt.plot(epochs, acc, "bo", label = "Training acc")
plt.plot(epochs, val_acc, "b", label = "Validation acc")
plt.title("Training and Validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()

plt.show()

"""# Retraining a model from scratch"""

model = models.Sequential()
model.add(layers.Dense(64, activation = "relu", input_shape = (10000,)))
model.add(layers.Dense(64, activation = "relu"))
model.add(layers.Dense(46, activation = "softmax"))

model.compile(optimizer = "rmsprop",
              loss = "categorical_crossentropy",
              metrics = ["accuracy"])

model.fit(partial_x_train,
          partial_y_train,
          epochs = 9,
          batch_size = 512,
          validation_data = (x_val, y_val))

results = model.evaluate(x_test, one_hot_test_labels)

results

import copy
test_labels_copy = copy.copy(test_labels)
np.random.shuffle(test_labels_copy)
hits_array = np.array(test_labels) == np.array(test_labels_copy)
float(np.sum(hits_array)) / len(test_labels)

"""# Generating predictions for new data"""

predictions = model.predict(x_test)

predictions[0].shape

np.sum(predictions[0])

np.argmax(predictions[0])

"""# A different  way to handle the labels and the loss"""

y_train = np.array(train_labels)
y_test = np.array(test_labels)

model.compile(optimizer="rmsprop",
              loss = "sparse_categorical_crossentropy",
              metrics = ["acc"])

"""# A model with an information bottleneck"""

model = models.Sequential()

model.add(layers.Dense(64, activation = "relu", input_shape = (10000,)))
model.add(layers.Dense(4, activation = "relu"))
model.add(layers.Dense(46, activation = "softmax"))

model.compile(optimizer="rmsprop",
              loss = "categorical_crossentropy",
              metrics = ["accuracy"])

model.fit(partial_x_train,
          partial_y_train,
          epochs = 20,
          batch_size = 128,
          validation_data = (x_val, y_val))

