import light_modules.listen as listen
import speech_recognition as sr
import time
import threading
import whisper
import morning_modules.scheduler as scheduler
import morning_modules.wakeup as wakeup
import pyttsx3

# TTS engine
engine = pyttsx3.init()

# Makes the speech slower
newVoiceRate = 120
engine.setProperty('rate', newVoiceRate)

# Speech-to-text model
# Using base due to RAM limitations on Pi
model = whisper.load_model('base')

def start_listening():
    # Recognizer and mic instances handle recording, capturing, and processing audio
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Whenever some non-silent noise is made, this gets that as an AudioData object
    # with recognizer.listen(). This is passed to the callback and processed
    # This is listening in the background while program is running
    # lambda is a wrapper that makes it possible for listen_in_background to receive the model
    # since it can only accept two arguments. r is the recognizer object and a is the audio
    stop_listening = recognizer.listen_in_background(mic, lambda r, a: listen.callback(r, a, model))

    # Keeps the listening running
    try:
        while True:
            # Pauses the CPU momentarily so it isn't running 100%
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Stops the listening if interrupted
        stop_listening(wait_for_stop = False)
        print('Listening stopped')

def speak_all():
    # wakeup.speak_intro(engine)
    # time.sleep(1)
    # wakeup.speak_datetime(engine)
    # time.sleep(1)
    # wakeup.speak_weather(engine)
    # time.sleep(1)
    # wakeup.speak_events(engine)
    # time.sleep(1)
    wakeup.speak_news(engine)

if __name__ == "__main__":
    #events = scheduler.start_scheduler()

    speak_all()
    
    engine.runAndWait()

    # Creates a listening thread that runs in the background
    # Daemon makes it so the thread stops when the main program stops
    #listen_thread = threading.Thread(target = start_listening, daemon=True)

    # Start the thread
    #listen_thread.start()
    
    # Keep the thread going
    # try:
    #     while True:
    #         time.sleep(0.5)
    # except KeyboardInterrupt:
    #     # Stops the program if interrupted
    #     print("Ending program")

    #     # Stops both threads
    #     listen_thread.join()
        

