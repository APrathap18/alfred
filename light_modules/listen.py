import speech_recognition as sr
import whisper
import io
import numpy as np
import soundfile as sf
import light_modules.control_lights as control_lights

#***************************************************************
# FILE: listen
# DEVELOPED BY: Adarsh Prathap
# DATE: 8/6/2025
# DESCRIPTION: This file handles listening and transcribing the
#              the audio using a speech recognizer. The mic is
#              listening in the background with callback and
#              the turn on/off part of the program starts when
#              the activation word 'torch' is said.
# GITHUB: https://github.com/APrathap18/lumos
#***************************************************************

"""
**********************************************
Title:          callback
Parameters:     recognizer, raw_audio
Return:         None
Description:    Takes in audio, processes and
                transcribes it, then sends to
                be read
**********************************************
"""
def callback(recognizer, raw_audio, model):
    # Listen to the microphone as the audio source
    print("Heard something")
        
    # # Raw audio recorded as an AudioData object
    # raw_audio = recognizer.listen(source)
        
    # Convert into byte string
    raw_audio_bytes = raw_audio.get_wav_data()
        
    # Create a file-like object from these bytes
    # Saved as a buffer, not on disk
    audio_buffer = io.BytesIO(raw_audio_bytes)

    # Read from buffer using soundfile
    # Returns a numpy array of the raw audio samples (represented in numbers)
    # sr_rate is sample rate, tells how many samples per second the audio is getting in Hz
    audio_np, sr_rate = sf.read(audio_buffer)

    # Converts to float32 since its required for the model
    # float32 is a float, while float64 is a double
    audio_np = audio_np.astype(np.float32)

    try:
        # Transcribe that audio into a dictionary
        result = model.transcribe(audio_np, fp16 = False, language = 'en')
                
        # Accessed at 'text' key
        audio_text = result["text"].lower()

        print(audio_text)

        # Checks if activation word was said
        if 'alfred' in audio_text:
            # Plays sound to indicate
            respond()

            # Check if lights on or lights off was said
            control_lights.read_text(audio_text)
    except sr.UnknownValueError:
        # If the audio cannot be converted to text (unrecognized), skip
        pass
    except sr.RequestError as e:
        print(f"API error: {e}")

def respond():
    # PLAY ACTIVATION NOISE
    print('Activation word detected: Beginning listening')