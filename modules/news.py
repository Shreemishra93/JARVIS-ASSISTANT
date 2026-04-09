"""
News Module - Fetches latest headlines using NewsAPI
"""
import requests


class NewsService:
    BASE_URL = "https://newsapi.org/v2/top-headlines"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_headlines(self, country="in", category="general", count=5):
        """Fetch top headlines."""
        params = {
            "country": country,
            "category": category,
            "pageSize": count,
            "apiKey": self.api_key,
        }
        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            articles = data.get("articles", [])
            return [
                {
                    "title": a["title"],
                    "source": a["source"]["name"],
                    "url": a.get("url", ""),
                }
                for a in articles
            ]
        except requests.RequestException as e:
            return [{"error": f"Could not fetch news: {e}"}]

    def format_report(self, articles):
        """Format news into a printable report."""
        lines = []
        for i, a in enumerate(articles, 1):
            if "error" in a:
                lines.append(f"  {a['error']}")
                continue
            lines.append(f"  {i}. {a['title']} ({a['source']})")
        return "\n".join(lines)

    def get_spoken_summary(self, articles):
        """Return a brief spoken summary of headlines."""
        headlines = [a["title"] for a in articles if "error" not in a]
        if not headlines:
            return "I couldn't fetch the latest news at the moment."
        intro = f"Here are the top {len(headlines)} headlines. "
        body = ". ".join(f"Number {i}, {h}" for i, h in enumerate(headlines, 1))
        return intro + body
