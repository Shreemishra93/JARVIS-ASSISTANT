# J.A.R.V.I.S.
### Just A Rather Very Intelligent System

Personal AI assistant inspired by Iron Man. Activates on a **double-clap** and delivers your daily briefing.

## Features

- **Double-Clap Activation** - Listens via microphone, activates on two quick claps
- **Weather** - Real-time weather for Delhi, New York, San Francisco
- **News** - Top 5 Indian headlines
- **Stocks** - Indian top 5 (Reliance, TCS, HDFC Bank, Infosys, Bharti Airtel) with buy/hold recommendations
- **Teamwork.com Tasks** - Your assigned tasks and upcoming deadlines
- **Motivational Quotes** - Tony Stark + tech legends + classic motivation
- **Iron Man Soundtrack** - Background music loop from the sounds/ folder
- **JARVIS Voice** - Text-to-speech with a calm, measured voice

## Quick Setup

### 1. Install Python dependencies

```bash
cd C:\JARVIS
pip install -r requirements.txt
```

> **Note:** If `pyaudio` fails on Windows, try: `pip install pipwin && pipwin install pyaudio`

### 2. Get your free API keys

| Service | URL | Free? |
|---------|-----|-------|
| OpenWeatherMap | https://openweathermap.org/api | Yes (1000 calls/day) |
| NewsAPI | https://newsapi.org/register | Yes (100 calls/day) |
| Teamwork.com | Your Profile > API & Auth > API Tokens | Included |

### 3. Configure

Edit `config/settings.env` with your keys:

```env
OWNER_NAME=Your name
OPENWEATHER_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
TEAMWORK_SITE_NAME=yourcompany
TEAMWORK_API_TOKEN=your_token_here
```

### 4. Add Iron Man Soundtrack

Place `.mp3` or `.wav` files in the `sounds/` folder. Optionally add a `startup.wav` for the boot-up chime.

### 5. Run

```bash
# Double-clap activated
python jarvis.py

# Skip clap, run immediately
python jarvis.py --no-clap

# Keep listening for claps in a loop
python jarvis.py --loop
```

## Project Structure

```
C:\JARVIS\
  jarvis.py              # Main orchestrator
  requirements.txt       # Python dependencies
  config/
    settings.env         # Your API keys and config
  modules/
    voice.py             # JARVIS TTS voice engine
    clap_detector.py     # Double-clap microphone detection
    weather.py           # OpenWeatherMap integration
    news.py              # NewsAPI headlines
    stocks.py            # Indian stocks via yfinance
    teamwork.py          # Teamwork.com task reader
    motivation.py        # Motivational quotes
    soundtrack.py        # Iron Man background music player
  sounds/
    (place .mp3/.wav files here)
```

## Troubleshooting

- **PyAudio won't install**: `pip install pipwin && pipwin install pyaudio`
- **No sound from JARVIS voice**: Check Windows default audio output device
- **Stock data empty**: Market may be closed; yfinance returns last available data
- **Teamwork 401 error**: Verify your API token is correct and not expired
- **Clap not detected**: Lower `CLAP_THRESHOLD` in settings.env (try 800-1000)
