def listen_for_trigger():
    print('Trigger heard')

    raw_audio = input('Say something: ').lower()

    if 'lumos' in raw_audio:
        respond()
        audio_array = raw_audio.split(" ")
        lumos_index = audio_array.index('lumos')
        input_audio = " ".join(audio_array[lumos_index:])

    else:
        input_audio = None

    return input_audio

def respond():
    print('Noise notification')