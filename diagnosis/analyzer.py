# import required module
import os
import math, random
import tensorflow as tf
import torch
import torchaudio
from torchaudio import transforms
from IPython.display import Audio
import torchvision.transforms as T
from PIL import Image
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import wave, sys
import matplotlib.pyplot as plt

# assign directory
directory = 'D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\demo_data\\'

# shows the sound waves
def visualize(path: str):
   
    # reading the audio file
    raw = wave.open(path)
     
    # reads all the frames
    # -1 indicates all or max frames
    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype ="int16")
     
    # gets the frame rate
    f_rate = raw.getframerate()
 
    time = np.linspace(
        0, # start
        len(signal) / f_rate,
        num = len(signal)
    )    
    return (time, signal)

def open(audio_file):
    sig, sr = torchaudio.load(audio_file)
    return (sig, sr)

def pad_trunc(aud, max_ms):
    sig, sr = aud
    num_rows, sig_len = sig.shape
    max_len = sr//1000 * max_ms

    if (sig_len > max_len):
      # Truncate the signal to the given length
      sig = sig[:,:max_len]

    elif (sig_len < max_len):
      # Length of padding to add at the beginning and end of the signal
      pad_begin_len = random.randint(0, max_len - sig_len)
      pad_end_len = max_len - sig_len - pad_begin_len

      # Pad with 0s
      pad_begin = torch.zeros((num_rows, pad_begin_len))
      pad_end = torch.zeros((num_rows, pad_end_len))

      sig = torch.cat((pad_begin, sig, pad_end), 1)
      
    return (sig, sr)

def spectro_gram(aud, n_mels=64, n_fft=1024, hop_len=None):
    sig,sr = aud
    top_db = 80

    # spec has shape [channel, n_mels, time], where channel is mono, stereo
    spec = transforms.MelSpectrogram(sr, n_fft=n_fft, hop_length=hop_len, n_mels=n_mels)(sig)

    # Convert to decibels
    spec = transforms.AmplitudeToDB(top_db=top_db)(spec)
    return (spec)

rec = input("Enter option: ")
print(rec)
aud = open(str(directory)+str(rec)+'.wav')
aud = pad_trunc(aud, 15000)
spec = spectro_gram(aud)
spec = torch.repeat_interleave(spec,3,dim=-3)
transform = T.ToPILImage()
img = transform(spec)
img = img.resize((118,64), resample=0)
img.save('D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\demo_data\\0.jpg')
time, sig = visualize('D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\demo_data\\{}.wav'.format(rec))
plt.plot(time, sig)
plt.savefig('D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\demo_data\\waveform{}.png'.format(rec))
folder = 'D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\demo_data'
model = tf.keras.models.load_model('model.h5')

sub = pd.DataFrame({'image_id':['0.jpg'],'Diagnosis':[0]})
datagen = ImageDataGenerator()
test_generator = datagen.flow_from_dataframe(sub, folder, x_col = 'image_id', y_col=None,
    batch_size=10,
    class_mode=None,
    target_size =(118, 64),  
    shuffle=False,
    color_mode = 'rgb')

# Making predictions and storing it in a variable.
preds = model.predict(test_generator)



