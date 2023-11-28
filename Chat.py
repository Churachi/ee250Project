import sounddevice as sd
import numpy as np
import time
import RPi.GPIO as GPIO

# Define pitch ranges
pitch_ranges = {
    'D4': 293.66,
    'E4': 329.63,
    'G4': 392.00,
    'A4': 440.00
}

# Define the melody sequence
melody_sequence = ['D4', 'E4', 'G4', 'A4', 'G4', 'E4', 'G4', 'A4', 'G4']

# GPIO setup
GPIO.setmode(GPIO.BCM)
GREEN_LED_PIN = 18  # Change this to the GPIO pin connected to your green LED
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

# Function to check if the input frequency matches any pitch range
def check_pitch(frequency):
    for note, pitch in pitch_ranges.items():
        if pitch - 5 <= frequency <= pitch + 5:
            return note
    return None

# Function to record audio and analyze the melody
def detect_melody(duration):
    sample_rate = 44100  # Adjust this based on your microphone's sample rate

    # Record audio
    audio_data = sd.rec(int(sample_rate * duration), channels=1, dtype='int16')
    sd.wait()

    # Perform Fourier transform
    fft_result = np.fft.fft(audio_data[:, 0])
    freqs = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
    freqs = freqs[:len(freqs) // 2]
    fft_result = np.abs(fft_result[:len(fft_result) // 2])

    # Find the dominant frequency
    dominant_frequency = freqs[np.argmax(fft_result)]

    # Check if the dominant frequency corresponds to a note in the melody
    detected_note = check_pitch(dominant_frequency)

    if detected_note == melody_sequence[0]:
        # If the first note is detected, check for the entire melody sequence
        melody_detected = True
        for i in range(1, len(melody_sequence)):
            time.sleep(0.5)  # Add a short delay between notes
            detect_melody(1)  # Record the next note
            if detected_note != melody_sequence[i]:
                melody_detected = False
                break

        if melody_detected:
            GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
            print("Melody detected: DEGAGEGAG")
        else:
            GPIO.output(GREEN_LED_PIN, GPIO.LOW)
            print("Melody not detected")

# Main loop
try:
    while True:
        detect_melody(7)  # Adjust the duration based on your requirement
        time.sleep(1)  # Add a delay between each detection to avoid false positives
except KeyboardInterrupt:
    GPIO.cleanup()