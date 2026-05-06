import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import pyautogui
import datetime
import requests

# ==============================
# 🔊 TEXT TO SPEECH
# ==============================
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# ==============================
# 🎤 SPEECH TO TEXT
# ==============================
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        return ""

# ==============================
# 💻 SYSTEM CONTROL
# ==============================
def open_app(app):
    os.system(f"start {app}")

def close_app(app):
    os.system(f"taskkill /f /im {app}.exe")

def shutdown():
    os.system("shutdown /s /t 5")

def restart():
    os.system("shutdown /r /t 5")

def screenshot():
    img = pyautogui.screenshot()
    img.save("screenshot.png")

def volume_up():
    pyautogui.press("volumeup")

def volume_down():
    pyautogui.press("volumedown")

def type_text(text):
    pyautogui.write(text)

def scroll_down():
    pyautogui.scroll(-500)

# ==============================
# 🌐 WEB + API
# ==============================
def open_website(url):
    webbrowser.open(url)

def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_weather(city="Kathmandu"):
    api_key = "YOUR_API_KEY"  # Replace with your key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        return f"{temp}°C in {city}"
    except:
        return "Weather not available"

# ==============================
# 🧠 COMMAND HANDLER
# ==============================
def handle_command(command):
    if "hello" in command:
        speak("Hello! How can I help you?")

    elif "open chrome" in command:
        open_app("chrome")
        speak("Opening Chrome")

    elif "close chrome" in command:
        close_app("chrome")
        speak("Closing Chrome")

    elif "shutdown" in command:
        speak("Shutting down system")
        shutdown()

    elif "restart" in command:
        speak("Restarting system")
        restart()

    elif "volume up" in command:
        volume_up()

    elif "volume down" in command:
        volume_down()

    elif "screenshot" in command:
        screenshot()
        speak("Screenshot taken")

    elif "type" in command:
        speak("What should I type?")
        text = listen()
        type_text(text)

    elif "scroll down" in command:
        scroll_down()

    elif "open youtube" in command:
        open_website("https://youtube.com")
        speak("Opening YouTube")

    elif "search" in command:
        query = command.replace("search", "")
        search_google(query)
        speak(f"Searching for {query}")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {time}")

    elif "date" in command:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {date}")

    elif "weather" in command:
        weather = get_weather()
        speak(weather)

    elif "exit" in command:
        speak("Goodbye!")
        return False

    else:
        speak("I didn't understand that")

    return True

# ==============================
# 🚀 MAIN LOOP
# ==============================
def main():
    WAKE_WORD = "assistant"
    speak("Assistant is now online")

    while True:
        command = listen()

        if WAKE_WORD in command:
            speak("Yes?")
            command = listen()

        if command:
            if not handle_command(command):
                break

if __name__ == "__main__":
    main()