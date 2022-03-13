import matplotlib.pyplot as plt
import numpy as np
import wave, sys

acc = np.loadtxt('D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\demo_data\\acc_normal.txt')
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
 
    # to Plot the x-axis in seconds
    # you need get the frame rate
    # and divide by size of your signal
    # to create a Time Vector
    # spaced linearly with the size
    # of the audio file
    time = np.linspace(
        0, # start
        len(signal) / f_rate,
        num = len(signal)
    )    
    return (time, signal)

time, sig = visualize('D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\demo_data\\Recording_normal.wav')
plt.plot(time,sig)
plt.show(block=True)
plt.plot(acc)
plt.show(block=True)
