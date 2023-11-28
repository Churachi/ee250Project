import sounddevice as sd
import numpy as np
import time
import grovepi
import grove_rgb_lcd as lcd
import paho.mqtt.client as mqtt
import time


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

def on_connect(client, userdata, flags, rc):
    print("here")
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("finalproject/laptop")
    client.message_callback_add("finalproject/laptop",laptop_callback)

def laptop_callback(client, userdata, message):
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
            comment = 'Your child passed!'
        else:
            comment = "Your child did not pass"
        client.publish("finalproject/rpi", comment)

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

if __name__ == '__main__':
#this section is covered in publisher_and_subscriber_example.py
client = mqtt.Client()
# client.on_message = on_message
client.on_connect = on_connect
client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
client.loop_forever()
