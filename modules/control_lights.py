def turn_on():
    print("Lights turned on!")

def turn_off():
    print("lights turned off!")

def read_text(audio_text):
    if 'lights off' in audio_text:
        turn_off()
    elif 'lights on' in audio_text:
        turn_on()
    