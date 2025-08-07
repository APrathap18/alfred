import light_modules.control_lights as control_lights
import light_modules.listen as listen
import speech_recognition as sr
import time

# Recognizer and mic instances handle recording, capturing, and processing audio
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Whenever some non-silent noise is made, this gets that as an AudioData object
# with recognizer.listen(). This is passed to the callback and processed
# This is listening in the background while program is running
start_listening = recognizer.listen_in_background(mic, listen.callback)

# Keeps the program running
try:
    while True:
        # Pauses the CPU momentarily so it isn't running 100%
        time.sleep(0.1)
except KeyboardInterrupt:
    # Stops the program and background listening if interrupted
    start_listening(wait_for_stop = False)
    print('Program stopped')
