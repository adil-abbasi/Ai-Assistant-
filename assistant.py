import pyttsx3
import speech_recognition as sr
import openai
import os, datetime, pywhatkit, requests
from config import OPENAI_API_KEY, WEATHER_API_KEY
from utils.email_handler import send_email

openai.api_key = OPENAI_API_KEY

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except:
            speak("Sorry, I didn't catch that.")
            return ""

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

def run_command(command):
    if "open notepad" in command:
        os.system("notepad")
    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak("Current time is " + time)
    elif "youtube" in command:
        speak("What should I search on YouTube?")
        query = listen()
        pywhatkit.playonyt(query)
    elif "weather" in command:
        city = "Karachi"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The weather in {city} is {desc} with {temp}°C temperature.")
    elif "email" in command:
        speak("To whom should I send the email?")
        to = listen()
        speak("What is the subject?")
        subject = listen()
        speak("What is the message?")
        body = listen()
        send_email(to, subject, body)
        speak("Email sent successfully.")
    else:
        reply = ask_gpt(command)
        speak(reply)
