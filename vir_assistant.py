import speech_recognition as sr
import pyttsx3
import time
import datetime as dt
import pywhatkit as pk
import wikipedia as wiki
import playsound
from gtts import gTTS
import random
import webbrowser
import os

listener = sr.Recognizer()
speaker = pyttsx3.init()

# RATE
rate = speaker.getProperty('rate')
speaker.setProperty('rate', 125)

# VOICE
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[0].id)

def speak(text):
    speaker.say('Yes Boss, ' + text)
    speaker.runAndWait()

def speak_ex(text):
    speaker.say(text)
    speaker.runAndWait()

va_name = 'jarvis'
voice_data = ''

speak('I am your ' + va_name + ' Tell me boss.')

class Person:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

def record_audio(ask=False):
    global voice_data
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = listener.listen(source)
        voice_data = ''
        try:
            voice_data = listener.recognize_google(audio)
        except sr.UnknownValueError:
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down')
        print(f">> {voice_data.lower()}")
        return voice_data.lower()

def respond(voice_data, person_obj):
    if there_exists(['hey', 'hi', 'hello']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings)-1)]
        speak(greet)

    if there_exists(["What is your name", "what's your name", "tell me your name"]):
        if person_obj.name:
            speak("my name is " + va_name)
        else:
            speak("my name is " + va_name + ". What's your name?")

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        speak(f"okay, I will remember that {person_name}")
        person_obj.setName(person_name)

    if there_exists(["how are you", "how are you doing"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")

    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')

    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f"Here is what I found for {search_term} on youtube")

    if there_exists(["exit", "quit", "goodbye"]):
        speak("See you again boss. I will be there whenever you call me.")
        exit()

person_obj = Person()

while True:
    user_command = record_audio()
    if 'close' in user_command:
        speak('See you again boss. I will be there whenever you call me.')
        break
    elif 'time' in user_command:
        cur_time = dt.datetime.now().strftime("%I:%M %p")
        print(cur_time)
        speak(cur_time)
    elif 'play' in user_command:
        user_command = user_command.replace('play ', '')
        print('Playing ' + user_command)
        speak('Playing ' + user_command + ', enjoy boss.')
        pk.playonyt(user_command)
        break
    elif 'search' in user_command or 'google' in user_command:
        user_command = user_command.replace('search ', '')
        user_command = user_command.replace('google ', '')
        print('Searching for ' + user_command)
        speak('Searching for ' + user_command)
        pk.search(user_command)
    elif 'who is' in user_command:
        user_command = user_command.replace('who is ', '')
        info = wiki.summary(user_command, 2)
        print(info)
        speak(info)
    elif 'what is' in user_command:
        user_command = user_command.replace('what is ', '')
        info = wiki.summary(user_command, 2)
        print(info)
        speak(info)
    elif 'when' in user_command:
        user_command = user_command.replace('when ', '')
        info = wiki.summary(user_command, 2)
        print(info)
        speak(info)
    elif 'who are you' in user_command:
        speak_ex('I am your virtual Assistant.')
    else:
        respond(user_command, person_obj)
