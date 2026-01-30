from textblob import TextBlob
import yfinance as yf

class SentimentAnalyzer:
    @staticmethod
    def get_sentiment(symbol):
        """Analyzes news headlines to determine market mood."""
        ticker = yf.Ticker(symbol)
        news = ticker.news
        
        if not news:
            return 0.0 # Neutral if no news
        
        scores = []
        for item in news:
            analysis = TextBlob(item['title'])
            scores.append(analysis.sentiment.polarity)
        
        # Calculate average sentiment
        avg_sentiment = sum(scores) / len(scores)
        return avg_sentiment