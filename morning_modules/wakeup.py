import scheduler
import pyttsx3

engine = pyttsx3.init()

def test():
    engine.say("Hello World! This is a test. Testing.")
    engine.say("Meeting at 10 pm")
    engine.runAndWait()

if __name__ == "__main__":
    test()