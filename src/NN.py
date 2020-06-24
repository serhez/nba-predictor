import tensorflow as tf
import numpy as np
import Generator

path = "../Data/2017-2018/traditional.csv"
(x, y) = Generator.generate(path)
n_train = int(len(x) * 0.8)
x_train = np.array(x[:n_train])
y_train = np.array(y[:n_train])
x_test = np.array(x[n_train:])
y_test = np.array(y[n_train:])

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(512, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10)
[loss, mae] = model.evaluate(x_test, y_test, verbose=0)