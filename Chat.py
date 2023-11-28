import sounddevice as sd
import numpy as np
import time
import grovepi
import grove_rgb_lcd as lcd

# Define pitch ranges
pitch_ranges = {
    'D4': 293.66,
    'E4': 329.63,
    'G4': 392.00,
    'A4': 440.00
}

# Define the melody sequence
melody_sequence = ['D4', 'E4', 'G4', 'A4', 'G4', 'E4', 'G4', 'A4', 'G4']

# Grovepi setup
PORT_BUTTON = 4     # D4
grovepi.pinMode(PORT_BUTTON, "INPUT")
lcd.setRGB(204, 153, 255) # initializes to a nice faint purple

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

# Main loop
try:
    while True:
        # Check for input
        if grovepi.digitalRead(PORT_BUTTON):
            print("3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)
            print("0")
            time.sleep(1)
        
            for i in melody_sequence:
                lcd.setText_norefresh("Play Note")
                detected_note = detect_melody(3)  # Adjust the duration based on your requirement
                if detected_note == melody_sequence[i]:
                    lcd.setText_norefresh("Note%d: Correct" %(i + 1))
                    time.sleep(1)
                else:
                    lcd.setText_norefresh("Note%d: Incorrect" %(i + 1))
                    time.sleep(1)
                    break
                

"""
            if detected_note == melody_sequence[0]:
                lcd.setText_norefresh("Note1: Correct")
                # If the first note is detected, check for the entire melody sequence
        
                time.sleep(0.5)  # Add a short delay between notes
                detected_note = detect_melody(3)  # Record the next note
                if detected_note == melody_sequence[1]:
                    lcd.setText_norefresh("Note2: Correct")

                    time.sleep(0.5)  # Add a short delay between notes
                    detected_note = detect_melody(3)  # Record the next note

                    if detected_note == melody_sequence[2]:
                        lcd.setText_norefresh("Note3: Correct")

                        time.sleep(0.5)  # Add a short delay between notes
                        detected_note = detect_melody(3)  # Record the next note

                        if detected_note == melody_sequence[3]:
                            lcd.setText_norefresh("Note3: Correct")

                            time.sleep(0.5)  # Add a short delay between notes
                            detected_note = detect_melody(3)  # Record the next note

                        else:
                            lcd.setText_norefresh("Note3: Incorrect.")

                    else:
                        lcd.setText_norefresh("Note3: Incorrect.")

                else:
                    lcd.setText_norefresh("Note2: Incorrect.")

            else:
                lcd.setText_norefresh("Note1: Incorrect.")
"""
except KeyboardInterrupt:
    grovepi.cleanup()