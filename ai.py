import os, ctypes, speech_recognition as sr, pyttsx3
import screen_brightness_control as sbc
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ── Engine setup ────────────────────────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 165)

def speak(text: str) -> None:
    print(f"[Assistant] {text}")
    engine.say(text)
    engine.runAndWait()

def listen() -> str | None:
    r, mic = sr.Recognizer(), sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening…")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            return r.recognize_google(audio).lower()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None
        except sr.RequestError as e:
            speak(f"Speech service error: {e}")
            return None

# ── Volume helper ────────────────────────────────────────────────────────────
def _get_volume_interface():
    dev = AudioUtilities.GetSpeakers()
    iface = dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return iface.QueryInterface(IAudioEndpointVolume)

# ── Command handlers ─────────────────────────────────────────────────────────
def launch_app(cmd: str) -> None:
    apps = {"notepad": "notepad.exe", "calculator": "calc.exe",
            "browser": "msedge.exe", "explorer": "explorer.exe",
            "paint": "mspaint.exe", "word": "winword.exe"}
    for name, path in apps.items():
        if name in cmd:
            try:
                os.startfile(path); speak(f"Opening {name}")
            except OSError:
                speak(f"Could not open {name}")
            return
    speak("App not recognised. Say notepad, calculator, browser, paint, or explorer.")

def set_volume(cmd: str) -> None:
    try:
        vol = _get_volume_interface()
        if "mute" in cmd:
            vol.SetMute(1, None); speak("Muted")
        elif "unmute" in cmd:
            vol.SetMute(0, None); speak("Unmuted")
        else:
            level = next((int(w) for w in cmd.split() if w.isdigit()), None)
            if level is not None:
                vol.SetMasterVolumeLevelScalar(max(0, min(level, 100)) / 100, None)
                speak(f"Volume set to {level} percent")
            else:
                speak("Please say a number between 0 and 100.")
    except Exception as e:
        speak(f"Volume error: {e}")

def set_brightness(cmd: str) -> None:
    try:
        level = next((int(w) for w in cmd.split() if w.isdigit()), None)
        if level is not None:
            sbc.set_brightness(max(0, min(level, 100)))
            speak(f"Brightness set to {level} percent")
        else:
            speak("Please say a brightness level between 0 and 100.")
    except Exception as e:
        speak(f"Brightness error: {e}")

def lock_pc(_: str) -> None:
    speak("Locking the PC. Goodbye!")
    ctypes.windll.user32.LockWorkStation()

# ── Dispatcher ───────────────────────────────────────────────────────────────
COMMANDS = {
    ("open", "launch", "start"):          launch_app,
    ("volume", "mute", "unmute"):         set_volume,
    ("brightness", "screen"):             set_brightness,
    ("lock", "lock pc", "lock computer"): lock_pc,
}

def dispatch(cmd: str) -> bool:
    if any(k in cmd for k in ("exit", "quit", "stop")):
        speak("Shutting down. Bye!"); return False
    for keywords, handler in COMMANDS.items():
        if any(k in cmd for k in keywords):
            handler(cmd); return True
    speak("I didn't understand that. Try: open notepad, volume 50, brightness 70, or lock.")
    return True

# ── Main loop ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    speak("Voice assistant ready. How can I help?")
    while True:
        command = listen()
        if command:
            print(f"[You] {command}")
            if not dispatch(command):
                break