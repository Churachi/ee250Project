import sounddevice as sd

# Define some settings
device = 0    # we use my USB sound card device
duration = 0.5  # seconds
fs = 44100    # samples by second
precision=0.02 # how close to the target pitch do we consider a match

# Listen to a bit of sound from the mic, recording it as a numpy array
myrecording = sd.rec(duration * fs, samplerate=fs, channels=1, device=device)
time.sleep(1.1*duration)