#%%
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow.keras
from tensorflow.keras.models import Sequential #allows us to build a model with a sequential order of layers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout, Activation, LeakyReLU, ELU
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K 
from tensorflow.keras.datasets import mnist

#%%
# Get Data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

#%%
# Flatten the input for Dense Neural Networks
X_train = X_train.reshape(60000, -1)
y_train = to_categorical(y_train, 10)

#%%
# Define the model
m = Sequential([
    # 1st hidden layer
    Dense(units=50, input_shape=(784,)),
    #Dropout(0.2),
    ELU(),
    BatchNormalization(),
    # 2nd hidden layer
    Dense(units=50),
    #Dropout(0.5),
    ELU(),
    BatchNormalization(),
    # 3rd hidden layer
    Dense(units=50),
    #Dropout(0.5),
    ELU(),
    BatchNormalization(),
    # 4th hidden layer
    Dense(units=50),
    #Dropout(0.5),
    ELU(),
    BatchNormalization(),
    # 5th hidden layer
    Dense(units=50),
    #Dropout(0.5),
    ELU(),
    BatchNormalization(),
    # output layer
    Dense(units=10),
    Activation('softmax')
])

# Compile the model for running in C+
callback = EarlyStopping(monitor='val_loss', patience=3)
m.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

#%%
# Train the model
h = m.fit(X_train, y_train, epochs=100, batch_size=1000, callbacks=[callback], validation_split=0.2)

#%%
# Show learning rate
plt.plot(h.history['loss'])
plt.plot(h.history['val_loss'])
plt.title('Learning curve')
plt.ylabel('Loss')
plt.xlabel('epochs')

#%%
# Predict 
X_test = X_test.reshape(10000, -1)
m.predict(X_test)

# %%
## Show weights

# save a list of np.arrays with the weights
w = m.get_weights()

# see the underlying TensorFlow variables
m.weights

# extract the names of the TF variables
[v.name for v in m.weights]

# plot weights of one layer (for MNIST)

plt.imshow(w[0].reshape((10, 28, 28)))
plt.show()
# %%
K.clear_session()
# %%
