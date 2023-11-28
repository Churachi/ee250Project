import sounddevice as sd
import numpy as np
import time
import grovepi
import grove_rgb_lcd as lcd
from tkinter import *
from tkinter import ttk
import sys
import os

export DISPLAY=localhost:0.0

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

pitch_ranges = {
    'C4': 523.33,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 2375.66,
    'A4': 440.00,
    'B4': 493.88
}

# Define the melody sequence
melody_sequence = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4']

# Grovepi setup
PORT_BUTTON = 4     # D4
grovepi.pinMode(PORT_BUTTON, "INPUT")
lcd.setRGB(204, 153, 255) # initializes to a nice faint purple

class PianoTest:

    def __init__(self, root):
        master = Tkinter.Tk()
        master.title("Piano Test")

        # mainframe = ttk.Frame(root, padding="20 20 12 12")
        # mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
       
        self.numcorrect = StringVar()

        self.passed = StringVar()
        ttk.Label(mainframe, text="Piano Test").grid(column=2, row=1, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.passed).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Start new test", command=self.test).grid(column=3, row=4, sticky=(W, S))

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # feet_entry.focus()
        root.bind("<Return>", self.test)
        
    def test(self):
        try:
            done = False
            passed = True
            while done == False:
                if grovepi.digitalRead(PORT_BUTTON):
                    done = True
                    for i in range(0, len(melody_sequence)):
                        lcd.setText_norefresh("Play Note")
                        detected_note = detect_melody(3)  # Adjust the duration based on your requirement
                        if detected_note == melody_sequence[i]:
                            lcd.setText_norefresh("Note%d: Correct" %(i + 1))
                            time.sleep(1)
                        else:
                            lcd.setText_norefresh("Note%d: Incorrect \nThe note is %s" %(i + 1, melody_sequence[i]))
                            time.sleep(1)
                            passed = False
                            break    
            if passed == True:
                # value = float(self.feet.get())
                self.passed.set('You passed!')
            else: 
                self.passed.set('You did not pass')
        except ValueError:
            pass

# Function to check if the input frequency matches any pitch range
def check_pitch(frequency):
    print("Checking pitch")
    for note, pitch in pitch_ranges.items():
        print(frequency)
        if pitch - 5 <= frequency <= pitch + 5:
            return note
    return None

# Function to record audio and analyze the melody
def detect_melody(duration):
    sample_rate = 44100  # Adjust this based on your microphone's sample rate

    # Record audio
    print("I am recording")
    audio_data = sd.rec(int(sample_rate * duration), channels=1, dtype='int16')
    sd.wait()
    print("I am done recording")

    # Perform Fourier transform
    print("Performing Fourier")
    fft_result = np.fft.fft(audio_data[:, 0])
    freqs = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
    freqs = freqs[:len(freqs) // 2]
    fft_result = np.abs(fft_result[:len(fft_result) // 2])

    # Find the dominant frequency
    dominant_frequency = freqs[np.argmax(fft_result)]

    # Check if the dominant frequency corresponds to a note in the melody
    return check_pitch(dominant_frequency)


master = Tk()
PianoTest(master)
master.mainloop()
