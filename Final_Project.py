import sounddevice as sd
import numpy as np
import time

# Define some settings
device = 1    # LCS USB Audio Mic = port 1
duration = 7  # seconds
fs = 44100    # samples by second
precision = 0.02 # how close to the target pitch do we consider a match

# Password is: DEGAGEGAG (Taylor Swift's You Belong with Me)
pitch_ranges = {
    'D4': 293.66,
    'E4': 329.63,
    'G4': 392.00,
    'A4': 440.00
}

def listen_to_audio():
    # Listen to a bit of sound from the mic, recording it as a numpy array
    return myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, device=device)
    time.sleep(1.1*duration)

def fourier_analysis(myrecording):
    # Calculate the Fourier transform of the recorded signal
    fourier = np.fft.fft(myrecording.ravel())
    # Extract the fundamental frequency from it 
    f_max_index = np.argmax(abs(fourier[:fourier.size/2]))
    # Get the scale of frequencies corresponding to the numpy Fourier transforms definition
    freqs = np.fft.fftfreq(len(fourier))
    # And so the actual fundamental frequency detected is
    return f_detected = freqs[f_max_index]*fs

while True:
    listen_to_audio()
    

