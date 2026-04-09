"""
Clap Level Tester - Shows your microphone's actual amplitude levels.
Clap a few times and note the peak numbers to calibrate detection.
"""
import struct
import math
import pyaudio

CHUNK = 1024
RATE = 44100

audio = pyaudio.PyAudio()

# Get default mic info
info = audio.get_default_input_device_info()
channels = int(info["maxInputChannels"])
print(f"Mic: {info['name']}")
print(f"Channels: {channels}")
print(f"Sample Rate: {int(info['defaultSampleRate'])}")
print(f"\n  Clap a few times! Watch the levels below.")
print(f"  Press Ctrl+C to stop.\n")

stream = audio.open(
    format=pyaudio.paInt16,
    channels=channels,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
)

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        count = len(data) // 2
        shorts = struct.unpack(f'{count}h', data)
        rms = math.sqrt(sum(s * s for s in shorts) / count)
        peak = max(abs(s) for s in shorts)

        bar_len = int(rms / 100)
        bar = "#" * min(bar_len, 60)

        if rms > 500:
            print(f"  RMS: {rms:8.1f}  PEAK: {peak:6d}  |{bar}|  <-- LOUD!")
        elif rms > 200:
            print(f"  RMS: {rms:8.1f}  PEAK: {peak:6d}  |{bar}|")
except KeyboardInterrupt:
    print("\n  Done! Use the RMS values you saw during claps to set CLAP_THRESHOLD.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
