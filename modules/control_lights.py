import asyncio
from kasa import SmartPlug

#***************************************************************
# FILE: control_lights
# DEVELOPED BY: Adarsh Prathap
# DATE: 8/6/2025
# DESCRIPTION: This file handles controlling the smart plug.
#              It gets the IP of the plug with kasa discover
#              Then, it uses the kasa library and built-in 
#              functions to turn the plug on and off. 
#              Asynchronous functions are used so that the program
#              doesn't have to run line-by-line like usual, and
#              can pause when necessary with await.
# GITHUB: https://github.com/APrathap18/lumos
#***************************************************************

# Get the unique static IP of the plug 
PLUG_IP = '192.168.1.xxx'

"""
**********************************************
Title:          lights_on
Parameters:     None
Return:         None
Description:    This asynchronous function 
                turns on the lights by calling
                control plug
**********************************************
"""
async def lights_on():
    print("Lights turned on!")
    await asyncio.run(control_plug('on'))

"""
**********************************************
Title:          lights_off
Parameters:     None
Return:         None
Description:    This asynchronous function 
                turns off the lights by calling
                control plug
**********************************************
"""
async def lights_off():
    print("lights turned off!")
    await asyncio.run(control_plug('off'))

"""
**********************************************
Title:          read_text
Parameters:     audio_text
Return:         None
Description:    Calling function to turn the
                lights on and off
**********************************************
"""
async def read_text(audio_text):
    if 'lights off' in audio_text:
        await lights_off()
    elif 'lights on' in audio_text:
        await lights_on()

"""
**********************************************
Title:          control_plug
Parameters:     command
Return:         None
Description:    Uses the built-in kasa functions
                to turn the plug on and off
**********************************************
"""
async def control_plug(command):
    plug = SmartPlug(PLUG_IP)

    await plug.update()
    print('State:', plug.state)
    
    if command == 'on':
        await plug.turn_on()
    elif command == 'off':
        await plug.turn_off()
    
