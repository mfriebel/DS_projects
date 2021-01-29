#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow.keras
from tensorflow.keras.models import Sequential #allows us to build a model with a sequential order of layers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, BatchNormalization, Dropout, Activation, LeakyReLU, ELU
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K 

#%%
def to_CNN_vector(df):
    X = df.iloc[:,1:]
    y = df.iloc[:,:1]

    X = np.array(X)
    X = X.reshape(len(df), 28, 28, 1)
    y = np.array(y)
    y = to_categorical(y, 10)

    return X, y
#%%
# Get Data
train = pd.read_csv("./fashion-mnist/fashion-mnist_train.csv")
test = pd.read_csv("./fashion-mnist/fashion-mnist_test.csv")
#%%
X_train, y_train = to_CNN_vector(train)
X_test, y_test = to_CNN_vector(test)
#%%%
m = Sequential([
    # 1st CV layer
    Conv2D(32, kernel_size=(3, 3), strides=(2, 2),
           padding="same", activation="relu",
           input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="same"),
    #BatchNormalization(),
    Conv2D(32, kernel_size=(3, 3), strides=(2, 2),
           padding="same", activation="relu",
           input_shape=(28, 28, 1)),
    Conv2D(32, kernel_size=(3, 3), strides=(2, 2),
           padding="same", activation="relu"),
    MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="same"),
    BatchNormalization(),
    Flatten(),
    Dropout(0.3),
    Dense(units=50, activation = 'relu'),
    BatchNormalization(),
    Dense(units=10, activation = 'softmax'),

])
callback = EarlyStopping(monitor='val_loss', patience=3)
m.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

#%%
m.summary()
#%%
for layer in m.layers:
       print(layer)

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
label_dict = {0: "T-shirt", 1: "Trouser", 2: "Pullover", 3: "Dress", 4: "Coat", 5: "Sandal",
                6: "Shirt", 7: "Sneaker", 8: "Bag", 9: "Ankle boot"}
start = 50
y_pred = m.predict(X_test[start:start+10])
y_pred_classes = m.predict_classes(X_test[start:start+10])
y_true = y_test[start:start+10]

y_pred_prob = [prediction.max() for prediction in y_pred]

plt.figure(figsize=(10,10))
for i in range(10):
       
       plt.subplot(3, 4, i+1)
       plt.imshow(X_test[start+i].reshape(28, 28), cmap=plt.cm.Greys)
       plt.title((label_dict[y_pred_classes[i]] + ":    " + str(round(y_pred_prob[i], 4))))

#%%
from sklearn.metrics import accuracy_score
# or use model.evaluate()

y_pred_all = m.predict_classes(X_test)
y_test = np.array(test.iloc[:,:1])
print(f'The accuracy score(test) of the model is: {accuracy_score(y_test, y_pred_all)}')
#%%
K.clear_session()
# %%
