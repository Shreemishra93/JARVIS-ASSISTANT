"""
Stocks Module - Tracks Indian top 5 stocks using yfinance
Provides price data and basic recommendation signals.
"""
import yfinance as yf


class StocksService:
    # Top 5 Indian stocks by market cap (NSE tickers)
    INDIAN_TOP_5 = [
        {"symbol": "RELIANCE.NS", "name": "Reliance Industries"},
        {"symbol": "TCS.NS", "name": "Tata Consultancy Services"},
        {"symbol": "HDFCBANK.NS", "name": "HDFC Bank"},
        {"symbol": "INFY.NS", "name": "Infosys"},
        {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel"},
    ]

    def get_stock_data(self, stocks=None):
        """Fetch current price and daily change for each stock."""
        stocks = stocks or self.INDIAN_TOP_5
        results = []
        for stock in stocks:
            try:
                ticker = yf.Ticker(stock["symbol"])
                info = ticker.fast_info
                current = round(info.last_price, 2)
                prev_close = round(info.previous_close, 2)
                change = round(current - prev_close, 2)
                change_pct = round((change / prev_close) * 100, 2) if prev_close else 0

                # Simple recommendation based on daily movement and 50-day trend
                recommendation = self._get_recommendation(ticker, change_pct)

                results.append({
                    "name": stock["name"],
                    "symbol": stock["symbol"],
                    "price": current,
                    "prev_close": prev_close,
                    "change": change,
                    "change_pct": change_pct,
                    "recommendation": recommendation,
                })
            except Exception as e:
                results.append({
                    "name": stock["name"],
                    "symbol": stock["symbol"],
                    "error": str(e),
                })
        return results

    def _get_recommendation(self, ticker, daily_change_pct):
        """Basic recommendation: compare price to 50-day moving average."""
        try:
            hist = ticker.history(period="3mo")
            if len(hist) < 50:
                return "Hold - Insufficient data"
            ma50 = hist['Close'].rolling(50).mean().iloc[-1]
            current = hist['Close'].iloc[-1]
            if current > ma50 * 1.05:
                return "Strong Buy - Above 50-day MA"
            elif current > ma50:
                return "Buy - Trending above 50-day MA"
            elif current > ma50 * 0.95:
                return "Hold - Near 50-day MA"
            else:
                return "Caution - Below 50-day MA"
        except Exception:
            if daily_change_pct > 1:
                return "Positive momentum today"
            elif daily_change_pct < -1:
                return "Negative momentum today"
            return "Hold - Stable"

    def format_report(self, stock_data):
        """Format stock data into a printable report."""
        lines = []
        for s in stock_data:
            if "error" in s:
                lines.append(f"  {s['name']}: Error - {s['error']}")
                continue
            arrow = "+" if s["change"] >= 0 else ""
            lines.append(
                f"  {s['name']} ({s['symbol'].replace('.NS','')}): "
                f"Rs.{s['price']:,.2f}  {arrow}{s['change']} ({arrow}{s['change_pct']}%)"
                f"  | {s['recommendation']}"
            )
        return "\n".join(lines)

    def get_spoken_summary(self, stock_data):
        """Return a brief spoken summary."""
        parts = []
        for s in stock_data:
            if "error" in s:
                continue
            direction = "up" if s["change"] >= 0 else "down"
            parts.append(
                f"{s['name']} is at {s['price']:.0f} rupees, {direction} {abs(s['change_pct'])}%"
            )
        if not parts:
            return "I couldn't fetch stock data at the moment."
        return "Here's the Indian market update. " + ". ".join(parts) + "."
