from textblob import TextBlob
from collections import Counter
import re
import numpy as np
from sklearn.linear_model import LinearRegression

# ==========================================
# 1. SENTIMENT ANALYSIS (ML/NLP)
# ==========================================
def analyze_sentiment(text):
    """Blog text ka sentiment detect karega (Positive/Negative/Neutral)"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 se +1 tak
    
    if polarity > 0.1:
        return "Positive 😊", polarity
    elif polarity < -0.1:
        return "Negative 😞", polarity
    else:
        return "Neutral 😐", polarity

# ==========================================
# 2. WORD FREQUENCY ANALYSIS
# ==========================================
def word_frequency(text, top_n=10):
    """Sab se zyada aane wale words nikaalega"""
    # Common words (stopwords) hatao
    stopwords = {'the', 'is', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that', 'it', 'as', 'are', 'was', 'were', 'be', 'been', 'has', 'have', 'had', 'will', 'would', 'can', 'could', 'should', 'may', 'might', 'must', 'our', 'we', 'you', 'your', 'they', 'their', 'i', 'my', 'me'}
    
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
    common = Counter(filtered_words).most_common(top_n)
    return dict(common)

# ==========================================
# 3. COST PREDICTION (Linear Regression - ML)
# ==========================================
def train_cost_model():
    """Linear Regression model train karega (input length se cost predict)"""
    # Training data (input length vs cost)
    X = np.array([[100], [200], [300], [400], [500], [600], [700], [800], [900], [1000]])
    y = np.array([0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.010])
    
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_cost(input_length, model=None):
    """Input length ke basis par future cost predict karega"""
    if model is None:
        model = train_cost_model()
    predicted = model.predict([[input_length]])[0]
    return max(0, predicted)  # Negative cost nahi ho sakti

# ==========================================
# 4. INPUT/OUTPUT LENGTH ANALYSIS
# ==========================================
def length_analysis(input_text, outputs):
    """Input vs Output length analyze karega"""
    return {
        "input_chars": len(input_text),
        "input_words": len(input_text.split()),
        "output_chars": sum(len(o) for o in outputs),
        "output_words": sum(len(o.split()) for o in outputs),
        "compression_ratio": round(sum(len(o) for o in outputs) / len(input_text), 2) if len(input_text) > 0 else 0
    }