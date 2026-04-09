"""
Motivational Quotes Module - Keeps you inspired like Tony Stark
"""
import random


class MotivationService:
    QUOTES = [
        # Tony Stark / Iron Man
        ("I am Iron Man.", "Tony Stark"),
        ("Sometimes you gotta run before you can walk.", "Tony Stark"),
        ("The truth is... I am Iron Man.", "Tony Stark"),
        ("Heroes are made by the path they choose, not the powers they are graced with.", "Tony Stark"),
        ("I told you, I don't want to join your super secret boy band.", "Tony Stark"),

        # Motivational classics
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
        ("Stay hungry, stay foolish.", "Steve Jobs"),
        ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
        ("First, solve the problem. Then, write the code.", "John Johnson"),
        ("The best error message is the one that never shows up.", "Thomas Fuchs"),
        ("It's not about ideas. It's about making ideas happen.", "Scott Belsky"),
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
        ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"),
        ("Hard work beats talent when talent doesn't work hard.", "Tim Notke"),
        ("Dream big. Start small. Act now.", "Robin Sharma"),
        ("Push yourself, because no one else is going to do it for you.", "Unknown"),
        ("Great things never come from comfort zones.", "Unknown"),
        ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),

        # Tech legends
        ("Move fast and break things. Unless you are breaking stuff, you are not moving fast enough.", "Mark Zuckerberg"),
        ("Any sufficiently advanced technology is indistinguishable from magic.", "Arthur C. Clarke"),
        ("The Web as I envisaged it, we have not seen it yet.", "Tim Berners-Lee"),
        ("Simplicity is the ultimate sophistication.", "Leonardo da Vinci"),
        ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ]

    def get_random_quote(self):
        """Return a random motivational quote."""
        quote, author = random.choice(self.QUOTES)
        return {"quote": quote, "author": author}

    def format_quote(self, quote_data):
        """Format for display."""
        return f'  "{quote_data["quote"]}"\n    - {quote_data["author"]}'

    def get_spoken_quote(self, quote_data=None):
        """Return a spoken motivational quote."""
        if not quote_data:
            quote_data = self.get_random_quote()
        return f'Here\'s something to keep you going. {quote_data["quote"]}. That was {quote_data["author"]}.'
