#%%
import matplotlib.pyplot as plt
import tensorflow.keras
from tensorflow.keras.models import Sequential #allows us to build a model with a sequential order of layers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, BatchNormalization, Dropout, Activation, LeakyReLU, ELU
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K 
from tensorflow.keras.datasets import mnist

#%%
# Get Data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 28, 28, 1)
y_train = to_categorical(y_train, 10)
#%%%
m = Sequential([
    # 1st CV layer
    Conv2D(40, kernel_size=(3, 3), strides=(2, 2),
           padding="same", activation="relu",
           input_shape=(28, 28, 1)),
    #Conv2D(40, kernel_size=(3, 3), strides=(2, 2),
    #       padding="same", activation="relu"),
    MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding="same"),
    BatchNormalization(),
    Conv2D(40, kernel_size=(3, 3), strides=(2, 2),
           padding="same", activation="relu",
           input_shape=(28, 28, 1)),
    Conv2D(40, kernel_size=(3, 3), strides=(2, 2),
           padding="same", activation="relu"),
    MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding="same"),
    BatchNormalization(),
    Flatten(),
    Dropout(0.5),
    Dense(units=50, activation = 'relu'),
    BatchNormalization(),
    Dense(units=10, activation = 'softmax'),

])
callback = EarlyStopping(monitor='val_loss', patience=3)
m.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

#%%
# Train the model
h = m.fit(X_train, y_train, epochs=60, batch_size=1000, callbacks=[callback], validation_split=0.2)

#%%
# Show learning rate
plt.plot(h.history['loss'], label='training')
plt.plot(h.history['val_loss'], label='validation')
plt.title('Learning curve')
plt.ylabel('Loss')
plt.xlabel('epochs')
plt.legend()
plt.show()

plt.plot(h.history['accuracy'], label='training')
plt.plot(h.history['val_accuracy'], label='validation')
plt.title('Learning curve')
plt.ylabel('Accuracy')
plt.xlabel('epochs')
plt.legend()
plt.show()

#%%
K.clear_session()
# %%

# %%
