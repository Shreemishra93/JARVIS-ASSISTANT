"""
JARVIS Voice Engine - Text-to-Speech with Iron Man style personality
"""
import pyttsx3
import datetime


class JarvisVoice:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._configure_voice()

    def _configure_voice(self):
        """Configure voice to sound like JARVIS - deep, calm, British."""
        voices = self.engine.getProperty('voices')
        # Try to find a male/British voice; fallback to first available
        selected = voices[0]
        for voice in voices:
            name = voice.name.lower()
            if 'david' in name or 'daniel' in name or 'british' in name or 'male' in name:
                selected = voice
                break
        self.engine.setProperty('voice', selected.id)
        self.engine.setProperty('rate', 170)    # Calm, measured pace
        self.engine.setProperty('volume', 0.95)

    def speak(self, text):
        """Speak the given text aloud."""
        print(f"\n  JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def greet(self, owner_name="Sir"):
        """Iron Man style greeting based on time of day."""
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = f"Good morning, {owner_name}."
        elif hour < 17:
            greeting = f"Good afternoon, {owner_name}."
        elif hour < 21:
            greeting = f"Good evening, {owner_name}."
        else:
            greeting = f"Burning the midnight oil, {owner_name}?"

        self.speak(greeting)
        self.speak("J.A.R.V.I.S. at your service. All systems are online and ready.")
        return greeting
