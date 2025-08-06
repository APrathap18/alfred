import modules.control_lights as control_lights
import modules.listen as listen

# listen_for_trigger() will wait till lumos is said
user_input = listen.listen_for_trigger()

if user_input:
    if('lights on' in user_input):
        control_lights.turn_on()
    elif('lights off' in user_input):
        control_lights.turn_off()
    