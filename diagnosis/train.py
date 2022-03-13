# Core libraries. Tensorflow for making Neural Networks
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Flatten, Input, Dropout, BatchNormalization
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import *

# sklearn
from sklearn.model_selection import train_test_split

# Data Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Define the folder where all the images are there
folder = 'D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\spectograms'

# Reading the train data
train = pd.read_csv('D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\train.csv')

train_df, val_df = train_test_split(train, test_size=0.2)

datagen = ImageDataGenerator(width_shift_range=[-50,50])

columns = ['Diagnosis']

train_generator =     datagen.flow_from_dataframe(train_df, 
                                                    folder, 
                                                    x_col = 'image_id', 
                                                    y_col = columns, 
                                                    class_mode='raw',
                                                    target_size=(118, 64), 
                                                    batch_size = 10,
                                                    color_mode='rgb', 
                                                    validate_filenames = False, 
                                                    shuffle = True)

val_generator =   datagen.flow_from_dataframe(val_df, 
                                                    folder, 
                                                    x_col = 'image_id', 
                                                    y_col = columns, 
                                                    target_size =(118, 64), 
                                                    class_mode = 'raw', 
                                                    batch_size = 10,
                                                    color_mode='rgb',  
                                                    validate_filenames = False, 
                                                    shuffle = True)

def create_model():
    # Input dimensions of our image (checked above)
    x_input = Input(shape=(118, 64, 3))
    
    # VGG16 network
    vgg = VGG16(weights='imagenet', include_top=False, input_shape=(118, 64, 3))
    
    x = vgg(x_input)
    
    # The output of a VGG network is also 3 dimensional. We need to convert it to 1 dimension and then to 2 outputs
    
    x = Flatten()(x) #Converting to one dimension by concatenating everything
    
    x = Dense(128, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x) # Dropout randomly drops neurons in the network to prevent overfitting. This is kind of an arbitrary value
    x = Dense(64, activation='relu')(x)
    x = Dense(8, activation='softmax')(x)
    
    # Define our full model will inputs and outputs
    model = Model(inputs=x_input, outputs = x)
    
    # We will be using Adam, it is the most common optimizer. This also has hyperparameters, but we are ignoring it for now.
    # Binary Cross Entropy (log loss) is the metric we are optimizing. For our understanding, we are tracking accuracy and AUC (ignore this if you don't know it). Logloss is still the priority
    model.compile(optimizer = "adadelta", loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics = ['accuracy'])
    
    return model

model = create_model()
model.summary() # Plot the architecture of the model

#es = EarlyStopping(monitor='val_accuracy', mode='max', min_delta=0) 

#steps_per_epoch
history = model.fit(train_generator, epochs=8, validation_data = val_generator)

model.save('model.h5')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accurcy')
plt.xlabel('Epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()