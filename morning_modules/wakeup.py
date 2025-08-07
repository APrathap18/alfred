import morning_modules.scheduler as scheduler
import pyttsx3
from datetime import datetime
import random
import time
import requests

# From https://www.weatherapi.com/
WEATHER_API_KEY = 'bfa0780246834c6c891201958250708'

def speak_events(engine):
    # Gets upcoming events
    events = scheduler.start_scheduler()

    # Formats it into a list
    formatted_events = format_events_for_tts(events)

    # Speaks
    engine.say('Here are your events for today')

    # # Says immediately
    # engine.runAndWait()

    # # Short pause
    # time.sleep(0.25)
    
    transitions = ["First", "Then", "Next", "After", "Finally"]

    # Goes through each event
    for i, (start,summary) in enumerate(formatted_events):
        # Picks the transition word
        if (i == len(formatted_events) - 1):
            trans_word = "Finally"
        elif i < len(transitions) - 1:
            trans_word = transitions[i]
        else:
            # Random int from 1 to 3, inclusive
            rand_int = random.randint(1, 3)
            trans_word = transitions[rand_int]

        # Converts from time string to speech
        time_str = format_time_for_speech(start)

        # Speaks
        engine.say(f"{trans_word}, {summary} at {time_str}")

        # Short pause
        time.sleep(0.5)
    # Speak all queued up speech
    engine.runAndWait()
    

def format_events_for_tts(events):
    formatted = [] 

    # Formats events as a list
    for event in events:
        start = event['start'].get("dateTime", event['start'].get("date"))
        summary = event.get('summary', 'No Title')
        formatted.append((start,summary))
    return formatted

def format_time_for_speech(iso_str):
    # Only date provided, no time
    if "T" not in iso_str:
        return "all day"
    
    # Parses ISO datetime
    dt = datetime.fromisoformat(iso_str)

    # Returns a formatted time in AM/PM
    return dt.strftime("%-I:%M %p")

def speak_intro(engine):
    creds = scheduler.get_creds()

    if creds and creds.valid:
        user_info = get_user_info(creds)
        
        first_name = user_info.get('name').split(" ")[0]

        engine.say(f'Good morning {first_name}')
    else:
        print("No valid credentials")

def speak_datetime(engine):
    # Current datetime
    now = datetime.now()

    # Current (12-hour time in AM/PM) on Weekday, Month, Day
    date_string_1 = now.strftime("It is currently %I:%M %p on %A, %B %d.")

    engine.say(date_string_1)

def get_location():
    # free geolocation API
    response = requests.get("http://ip-api.com/json")
    data = response.json()

    # returns the latitude, longitude, and city
    return data['lat'], data['lon'], data['city']

def get_user_info(creds):
    # Google endpoint that returns profile info about user
    userinfo_endpoint = 'https://www.googleapis.com/oauth2/v3/userinfo'
    
    # HTTP headers, includes OAuth2 access token
    headers = {'Authorization': f'Bearer {creds.token}'}

    # Result, either info or error
    response = requests.get(userinfo_endpoint, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching user info: ", response.text)
        return None

def speak_weather(engine):
    # Gets the city the Pi is in
    lat, lon, city = get_location()

    # URL for weather API
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=1&aqi=no&alerts=no"

    response = requests.get(url)
    data = response.json()

    location = data['location']['name'] # The location of the Pi
    current_temp = data['current']['temp_f'] # Temp in Fahrenheit
    condition = data['current']['condition']['text'] # Current condition
    high = data['forecast']['forecastday'][0]['day']['maxtemp_f'] # Max temp in deg F
    low = data['forecast']['forecastday'][0]['day']['mintemp_f'] # Max temp in deg F

    # Hourly forecast for rain
    hourly_forecast = data['forecast']['forecastday'][0]['hour']
    rain_periods = []

    # Adds all the hours where there will be rain to the list
    for hour in hourly_forecast:
        if hour['chance_of_rain'] >= 50:
            time = hour['time'].split(" ")[1]
            rain_periods.append(time)
    
    # Find start and end of likely rain periods
    rain_range = ""
    if rain_periods:
        rain_range = f" Showers expected between {rain_periods[0]} and {rain_periods[-1]}"
    else:
        rain_range = " No significant rain expected."

    # Compiled string of weather
    weather_string = f"In {location}, it is currently {condition.lower()}, and {current_temp} degrees Fahrenheit. Today's high will be {high} degrees Fahrenheit and the low will be {low} degrees Fahrenheit." + rain_range

    engine.say(weather_string)

if __name__ == "__main__":
    speak_weather()