import speech_recognition as sr
import whisper
import io
import numpy as np
import soundfile as sf
import modules.control_lights
# Speech recognizer
recognizer = sr.Recognizer()

# Speech-to-text model
# Using base due to RAM limitations on Pi
model = whisper.load_model("base")

def callback(recognizer, raw_audio):
    # Listen to the microphone as the audio source
    with sr.Microphone() as source:
        print("Say something")
        
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
            if 'torch' in audio_text:
                # Plays sound to indicate
                respond()

                # Check if lights on or lights off was said
                modules.control_lights.read_text(audio_text)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"API error: {e}")

def respond():
     print('Activation word detected: Beginning listening')