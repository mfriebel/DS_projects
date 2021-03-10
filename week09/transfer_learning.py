#%%
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Dense

#%%
m = MobileNetV2() 

base_model = MobileNetV2(
    include_top=False, # remove the top dense layers
    input_shape=(224,224,3),
    pooling='avg' # average pooling transforms 4d tensor to 2d feature matrix
)

#%%
m.summary()
#%%
base_model.summary()
#%%
for layer in base_model.layers:
    print(layer)
#%%
# freeze all layers in the base model
for layer in base_model.layers[:120]:
    layer.trainable = False

#%%
model = Sequential()
model.add(base_model)
# add custom layer on top of base model
model.add(Dense(3, activation='softmax'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy')
# %%
