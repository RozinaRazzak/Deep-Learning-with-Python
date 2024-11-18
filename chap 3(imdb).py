# -*- coding: utf-8 -*-
"""IMDB.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11hB7zc4LpuUYm4c35OMt4hM2DEPh2Hn8

# Binary Classification
## Two class Classification

# Loading the IMDB dataset
"""

from keras.datasets import imdb

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words = 10000 )

train_data[0]

train_labels[0]

max([max(sequence) for sequence in train_data])

word_index = imdb.get_word_index()
reverse_word_index = dict(
    [(value, key) for (key, value) in word_index.items()])
decoded_review = " ".join(
    [reverse_word_index.get(i - 3,"?") for i in train_data[0]])

word_index

"""# Encoding the integer sequences into binary matrix"""

import numpy as np
def vectorize_sequences(sequences, dimension = 10000):
  results = np.zeros((len(sequences), dimension))
  for i, sequence in enumerate(sequences):
    results[i, sequence] = 1.
  return results


x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

x_train[0]

y_train = np.asarray(train_labels).astype("float32")
y_test = np.asarray(test_labels).astype("float32")

y_train

y_test

"""# The Model Definition"""

from keras import models
from keras import layers

model = models.Sequential()
model.add(layers.Dense(16, activation = "relu",input_shape = (10000,)))
model.add(layers.Dense(16, activation = "relu"))
model.add(layers.Dense(1, activation = "sigmoid"))

"""# Compiling the Model"""

model.compile(optimizer = "rmsprop",
              loss = "binary_crossentropy",
              metrics = ["accuracy"])

"""# Configuring the optimizer"""

from keras import optimizers
model.compile(optimizer = optimizers.RMSprop(learning_rate = 0.001),
              loss = "binary_crossentropy",
              metrics = ["accuracy"])

"""# Using custom losses and metrics"""

from keras import losses
from keras import metrics

model.compile(optimizer = optimizers.RMSprop(learning_rate =0.001),
              loss = losses.binary_crossentropy,
              metrics = ["metrics.binary_accuracy"])

"""# Setting aside a validation set"""

x_val = x_train[:10000]
partial_x_train = x_train[10000:]

y_val = y_train[:10000]
partial_y_train = y_train[10000:]

"""# Train your model"""

model.compile(optimizer = "rmsprop",
              loss = "binary_crossentropy",
              metrics = ["acc"])

history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs = 20,
                    batch_size = 512,
                    validation_data = (x_val, y_val))

history_dict = history.history
history_dict.keys()

"""# Plotting the training and validation loss"""

import matplotlib.pyplot as plt

history_dict = history.history
loss_values = history_dict["loss"]
val_loss_values = history_dict["val_loss"]

epochs = range(1,21)

plt.plot(epochs, loss_values, "bo", label = "Training loss") # bo is for blue dot
plt.plot(epochs, val_loss_values, "b", label = "Validation") # b is for "solid blue line"
plt.title("Training and Validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

"""# Plotting the training and validation accuracy"""

plt.clf()
acc = history_dict["acc"]
val_acc= history_dict["val_acc"]

plt.plot(epochs, acc, "bo", label = "Training acc")
plt.plot(epochs, val_acc, "b", label = "Validation acc")
plt.title("Training and Validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()

plt.show()

"""# Retraining a model from scratch"""

model =  models.Sequential()
model.add(layers.Dense(16, activation = "relu", input_shape = (10000,)))
model.add(layers.Dense(16, activation = "relu"))
model.add(layers.Dense(1, activation = "sigmoid"))

model.compile(optimizer = "rmsprop",
              loss = "binary_crossentropy",
              metrics = ["accuracy"])

model.fit(x_train, y_train, epochs = 4, batch_size = 512)
results = model.evaluate(x_test, y_test)

results

"""# Using a trained network to generate predictions on new data"""

model.predict(x_test)
