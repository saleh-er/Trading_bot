from textblob import TextBlob
import yfinance as yf

class SentimentAnalyzer:
    @staticmethod
    def get_sentiment(symbol):
        """Analyzes news headlines safely using .get() to avoid KeyErrors."""
        ticker = yf.Ticker(symbol)
        try:
            news = ticker.news
        except Exception:
            return 0.0 # Return neutral if API fails
        
        if not news:
            return 0.0 
        
        scores = []
        for item in news:
            # Use .get('title') which returns None instead of crashing if 'title' is missing
            title = item.get('title')
            
            if title:
                analysis = TextBlob(title)
                scores.append(analysis.sentiment.polarity)
        
        # Avoid division by zero if no valid titles were found
        if not scores:
            return 0.0
            
        return sum(scores) / len(scores)