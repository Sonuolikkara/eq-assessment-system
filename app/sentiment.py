import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

sia = None

def load_sentiment_model():
    global sia
    if sia is None:
        sia = SentimentIntensityAnalyzer()
    return sia

def analyze_sentiment(text):
    model = load_sentiment_model()
    scores = model.polarity_scores(text)
    compound = scores['compound']
    normalized = (compound + 1) / 2
    return normalized

def calculate_eq_score(responses):
    avg_sentiment = sum(responses) / len(responses)
    base_score = int(avg_sentiment * 100)
    return max(20, min(100, base_score))
