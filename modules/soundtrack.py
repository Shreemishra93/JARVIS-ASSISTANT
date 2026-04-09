"""
Iron Man Soundtrack Player Module
Plays background music using pygame mixer.
Supports play, pause, resume, stop, and volume control.
"""
import os

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class SoundtrackPlayer:
    SOUNDS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds")

    def __init__(self):
        if not PYGAME_AVAILABLE:
            raise ImportError("pygame is not installed. Install with: pip install pygame")
        pygame.mixer.init()
        self.is_playing = False
        self.current_track = None

    def play(self, filename=None):
        """
        Play a soundtrack file from the sounds/ directory.
        If no filename given, plays the first .mp3/.wav found.
        """
        if filename:
            filepath = os.path.join(self.SOUNDS_DIR, filename)
        else:
            filepath = self._find_first_track()

        if not filepath or not os.path.exists(filepath):
            print(f"  [No soundtrack file found in {self.SOUNDS_DIR}]")
            print(f"  [Place your Iron Man .mp3/.wav files in the 'sounds' folder]")
            return False

        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(0.3)  # Background volume
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.is_playing = True
            self.current_track = os.path.basename(filepath)
            print(f"  [Now playing: {self.current_track}]")
            return True
        except Exception as e:
            print(f"  [Could not play soundtrack: {e}]")
            return False

    def _find_first_track(self):
        """Find the first audio file in the sounds directory."""
        if not os.path.exists(self.SOUNDS_DIR):
            os.makedirs(self.SOUNDS_DIR, exist_ok=True)
            return None
        for f in sorted(os.listdir(self.SOUNDS_DIR)):
            if f.lower().endswith(('.mp3', '.wav', '.ogg')):
                return os.path.join(self.SOUNDS_DIR, f)
        return None

    def pause(self):
        """Pause the current track."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            print("  [Music paused]")

    def resume(self):
        """Resume playback."""
        if not self.is_playing:
            pygame.mixer.music.unpause()
            self.is_playing = True
            print("  [Music resumed]")

    def stop(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.current_track = None
        print("  [Music stopped]")

    def set_volume(self, level):
        """Set volume (0.0 to 1.0)."""
        level = max(0.0, min(1.0, level))
        pygame.mixer.music.set_volume(level)
        print(f"  [Volume set to {int(level * 100)}%]")

    def play_startup_sound(self):
        """Play a short startup chime if available."""
        startup = os.path.join(self.SOUNDS_DIR, "startup.wav")
        if os.path.exists(startup):
            try:
                sound = pygame.mixer.Sound(startup)
                sound.set_volume(0.5)
                sound.play()
                return True
            except Exception:
                pass
        return False
