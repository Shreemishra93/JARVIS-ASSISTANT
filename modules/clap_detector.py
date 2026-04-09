"""
Clap Detection Module - Listens for clap sounds to activate JARVIS
Uses PyAudio to monitor microphone input and detect sharp amplitude spikes.
"""
import struct
import math
import time

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False


class ClapDetector:
    # Audio stream config
    CHUNK = 1024
    FORMAT_PA = 8  # pyaudio.paInt16 = 8
    RATE = 44100

    # Detection thresholds
    CLAP_THRESHOLD = 500        # Lowered default - adjust via settings.env
    CLAP_COOLDOWN = 0.2         # Min gap between two claps (ignore echo)
    DOUBLE_CLAP_WINDOW = 1.5    # Max seconds between two claps to count as double-clap

    def __init__(self, threshold=None):
        if not PYAUDIO_AVAILABLE:
            raise ImportError(
                "PyAudio is not installed. Install it with: pip install pyaudio\n"
                "On Windows you may need: pipwin install pyaudio"
            )
        if threshold:
            self.CLAP_THRESHOLD = threshold
        self.audio = pyaudio.PyAudio()
        self.stream = None

        # Auto-detect mic channels
        info = self.audio.get_default_input_device_info()
        self.channels = int(info["maxInputChannels"])
        print(f"  [Mic detected: {info['name']} ({self.channels}ch)]")

    def _get_rms(self, data):
        """Calculate Root Mean Square (loudness) of audio chunk."""
        count = len(data) // 2
        shorts = struct.unpack(f'{count}h', data)
        sum_squares = sum(s * s for s in shorts)
        rms = math.sqrt(sum_squares / count)
        return rms

    def wait_for_double_clap(self):
        """Block until a double-clap is detected. Returns True when detected."""
        self.stream = self.audio.open(
            format=self.FORMAT_PA,
            channels=self.channels,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        print(f"\n  [Listening for double-clap... threshold={self.CLAP_THRESHOLD}]")
        first_clap_time = None

        try:
            while True:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                rms = self._get_rms(data)

                if rms > self.CLAP_THRESHOLD:
                    now = time.time()

                    if first_clap_time is None:
                        # First clap detected
                        first_clap_time = now
                        print(f"  [First clap! RMS={rms:.0f} - clap again within 1.5s]")
                    elif (now - first_clap_time) > self.CLAP_COOLDOWN:
                        if (now - first_clap_time) <= self.DOUBLE_CLAP_WINDOW:
                            # Double clap confirmed!
                            print(f"  [Double-clap detected! RMS={rms:.0f}]")
                            return True
                        else:
                            # Too slow - reset, treat this as new first clap
                            first_clap_time = now
                            print(f"  [Too slow, reset. Clap! RMS={rms:.0f}]")

                # Reset if first clap is too old
                if first_clap_time and (time.time() - first_clap_time) > self.DOUBLE_CLAP_WINDOW:
                    first_clap_time = None

        except KeyboardInterrupt:
            return False
        finally:
            self.stop()

    def stop(self):
        """Clean up audio resources."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def __del__(self):
        if hasattr(self, 'audio') and self.audio:
            self.audio.terminate()
