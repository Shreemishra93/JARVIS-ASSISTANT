"""
Weather Module - Fetches current weather for Delhi and USA cities
Uses OpenWeatherMap free API.
"""
import requests


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    # Default cities to track
    DEFAULT_CITIES = [
        {"name": "Delhi", "country": "IN"},
        {"name": "New York", "country": "US"},
        {"name": "San Francisco", "country": "US"},
    ]

    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city_name, country_code=""):
        """Fetch current weather for a city."""
        query = f"{city_name},{country_code}" if country_code else city_name
        params = {
            "q": query,
            "appid": self.api_key,
            "units": "metric",
        }
        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp_c": round(data["main"]["temp"], 1),
                "temp_f": round(data["main"]["temp"] * 9 / 5 + 32, 1),
                "feels_like_c": round(data["main"]["feels_like"], 1),
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].title(),
                "wind_speed_kmh": round(data["wind"]["speed"] * 3.6, 1),
            }
        except requests.RequestException as e:
            return {"error": f"Could not fetch weather for {city_name}: {e}"}

    def get_all_weather(self, cities=None):
        """Fetch weather for all configured cities."""
        cities = cities or self.DEFAULT_CITIES
        results = []
        for city in cities:
            data = self.get_weather(city["name"], city.get("country", ""))
            results.append(data)
        return results

    def format_report(self, weather_data_list):
        """Format weather data into a spoken/printed report."""
        lines = []
        for w in weather_data_list:
            if "error" in w:
                lines.append(w["error"])
                continue
            lines.append(
                f"  {w['city']}, {w['country']}: {w['temp_c']}°C ({w['temp_f']}°F), "
                f"{w['description']}, Humidity {w['humidity']}%, "
                f"Wind {w['wind_speed_kmh']} km/h"
            )
        return "\n".join(lines)

    def get_spoken_summary(self, weather_data_list):
        """Return a sentence for JARVIS to speak."""
        parts = []
        for w in weather_data_list:
            if "error" in w:
                continue
            parts.append(
                f"{w['city']} is at {w['temp_c']} degrees celsius with {w['description']}"
            )
        return ". ".join(parts) + "."
