"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System
Personal AI Assistant inspired by Iron Man

Activates on double-clap and delivers:
  - Weather (Delhi + USA)
  - Latest news headlines
  - Indian stock market update with recommendations
  - Teamwork.com task summary
  - Motivational quote
  - Iron Man background soundtrack

Usage:
  python jarvis.py              # Normal mode (double-clap activation)
  python jarvis.py --no-clap    # Skip clap detection, run immediately
  python jarvis.py --loop       # Keep listening for claps in a loop
"""

import os
import sys
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama for Windows color support
init(autoreset=True)

# Load config
load_dotenv(os.path.join(os.path.dirname(__file__), "config", "settings.env"))

# ── Imports ──────────────────────────────────────────
from modules.voice import JarvisVoice
from modules.weather import WeatherService
from modules.news import NewsService
from modules.stocks import StocksService
from modules.teamwork import TeamworkService
from modules.motivation import MotivationService

# Optional modules (may fail if dependencies missing)
try:
    from modules.clap_detector import ClapDetector
    CLAP_AVAILABLE = True
except ImportError:
    CLAP_AVAILABLE = False

try:
    from modules.soundtrack import SoundtrackPlayer
    SOUNDTRACK_AVAILABLE = True
except ImportError:
    SOUNDTRACK_AVAILABLE = False


# ── Display Helpers ──────────────────────────────────

BANNER = f"""
{Fore.CYAN}
       _ _____ ______  _   _ _____ _____
      | |  _  | ___ \\| | | |_   _/  ___|
      | | |_| | |_/ /| | | | | | \\ `--.
  _   | |  _  |    / | | | | | |  `--. \\
 | |__| | | | | |\\ \\ \\ \\_/ /_| |_/\\__/ /
  \\____/\\_| |_\\_| \\_| \\___/ \\___/\\____/
{Style.RESET_ALL}
{Fore.YELLOW}  Just A Rather Very Intelligent System v1.0{Style.RESET_ALL}
{Fore.WHITE}  ---------------------------------------------{Style.RESET_ALL}
"""


def section(title, icon=""):
    """Print a section header."""
    print(f"\n{Fore.CYAN}  {'-' * 50}")
    print(f"  {icon}  {title}")
    print(f"  {'-' * 50}{Style.RESET_ALL}")


def success(text):
    print(f"{Fore.GREEN}  {text}{Style.RESET_ALL}")


def warning(text):
    print(f"{Fore.YELLOW}  {text}{Style.RESET_ALL}")


def error(text):
    print(f"{Fore.RED}  {text}{Style.RESET_ALL}")


# ── Main JARVIS Logic ────────────────────────────────

def run_jarvis():
    """Execute the full JARVIS briefing sequence."""
    owner = os.getenv("OWNER_NAME", "Sir")

    print(BANNER)
    print(f"{Fore.WHITE}  Initializing systems... {datetime.now().strftime('%A, %B %d, %Y %I:%M %p')}{Style.RESET_ALL}")

    # ── Voice Engine ──
    voice = JarvisVoice()

    # ── Soundtrack ──
    player = None
    if SOUNDTRACK_AVAILABLE:
        try:
            player = SoundtrackPlayer()
            player.play_startup_sound()
            player.play()  # Background Iron Man music
        except Exception:
            warning("Soundtrack unavailable. Place .mp3 files in the sounds/ folder.")

    # ── Greeting ──
    voice.greet(owner)

    # ── 1. WEATHER ──
    section("WEATHER REPORT", "***")
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if api_key and api_key != "your_openweathermap_api_key_here":
        weather = WeatherService(api_key)
        data = weather.get_all_weather()
        print(weather.format_report(data))
        voice.speak(weather.get_spoken_summary(data))
    else:
        warning("OpenWeatherMap API key not configured. Edit config/settings.env")
        voice.speak("Weather service is not configured yet, Sir.")

    # ── 2. NEWS ──
    section("LATEST NEWS", "***")
    news_key = os.getenv("NEWS_API_KEY", "")
    if news_key and news_key != "your_newsapi_key_here":
        news = NewsService(news_key)
        articles = news.get_headlines(country="in", count=5)
        print(news.format_report(articles))
        voice.speak(news.get_spoken_summary(articles))
    else:
        warning("NewsAPI key not configured. Edit config/settings.env")
        voice.speak("News service is not configured yet, Sir.")

    # ── 3. STOCKS ──
    section("INDIAN STOCK MARKET - TOP 5", "***")
    stocks = StocksService()
    try:
        stock_data = stocks.get_stock_data()
        print(stocks.format_report(stock_data))
        voice.speak(stocks.get_spoken_summary(stock_data))
    except Exception as e:
        error(f"Stock data unavailable: {e}")
        voice.speak("I couldn't fetch stock data at the moment, Sir.")

    # ── 4. TEAMWORK TASKS ──
    section("TEAMWORK - YOUR TASKS", "***")
    tw_site = os.getenv("TEAMWORK_SITE_NAME", "")
    tw_token = os.getenv("TEAMWORK_API_TOKEN", "")
    if tw_site and tw_token and tw_site != "your_company":
        teamwork = TeamworkService(tw_site, tw_token)
        tasks = teamwork.get_my_tasks()
        print(teamwork.format_report(tasks))
        voice.speak(teamwork.get_spoken_summary(tasks))

        # Show upcoming deadlines
        upcoming = teamwork.get_upcoming_tasks(days=3)
        if upcoming:
            print(f"\n{Fore.YELLOW}  Upcoming deadlines (next 3 days):{Style.RESET_ALL}")
            print(teamwork.format_report(upcoming))
            voice.speak(f"You have {len(upcoming)} tasks due in the next 3 days. Stay on it, {owner}.")
    else:
        warning("Teamwork not configured. Edit config/settings.env")
        voice.speak("Teamwork integration is not configured yet, Sir.")

    # ── 5. MOTIVATION ──
    section("MOTIVATION", "***")
    motivation = MotivationService()
    quote = motivation.get_random_quote()
    print(motivation.format_quote(quote))
    voice.speak(motivation.get_spoken_quote(quote))

    # ── Closing ──
    print(f"\n{Fore.CYAN}  {'=' * 50}")
    print(f"  Briefing complete. Have a productive day, {owner}!")
    print(f"  {'=' * 50}{Style.RESET_ALL}\n")
    voice.speak(f"That concludes your briefing, {owner}. Go make the world a better place.")

    # Keep music playing until user presses Enter
    if player and player.is_playing:
        print(f"{Fore.WHITE}  [Press Enter to stop music and exit]{Style.RESET_ALL}")
        try:
            input()
        except (KeyboardInterrupt, EOFError):
            pass
        player.stop()


def main():
    parser = argparse.ArgumentParser(description="J.A.R.V.I.S. - Your Personal AI Assistant")
    parser.add_argument("--no-clap", action="store_true", help="Skip clap detection, run immediately")
    parser.add_argument("--loop", action="store_true", help="Keep listening for claps in a loop")
    args = parser.parse_args()

    if args.no_clap:
        run_jarvis()
        return

    if not CLAP_AVAILABLE:
        warning("PyAudio not available. Running without clap detection.")
        warning("Install with: pip install pyaudio")
        run_jarvis()
        return

    # Clap-activated mode
    threshold = int(os.getenv("CLAP_THRESHOLD", "1500"))
    detector = ClapDetector(threshold=threshold)

    while True:
        print(f"\n{Fore.CYAN}  *** J.A.R.V.I.S. STANDBY MODE ***{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Double-clap to activate | Ctrl+C to exit{Style.RESET_ALL}")

        detected = detector.wait_for_double_clap()
        if detected:
            run_jarvis()

        if not args.loop:
            break


if __name__ == "__main__":
    main()
