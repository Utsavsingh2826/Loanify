"""Sentiment analysis service."""
from typing import Dict, Any
import random
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SentimentService:
    """Service for analyzing customer sentiment."""
    
    # Keywords for sentiment detection
    POSITIVE_KEYWORDS = [
        "thank", "thanks", "great", "excellent", "good", "happy", "love",
        "perfect", "awesome", "wonderful", "appreciate", "helpful"
    ]
    
    NEGATIVE_KEYWORDS = [
        "bad", "poor", "terrible", "awful", "hate", "angry", "frustrated",
        "disappointed", "worst", "horrible", "useless", "waste"
    ]
    
    URGENT_KEYWORDS = [
        "urgent", "immediately", "asap", "hurry", "quick", "fast", "now"
    ]
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of customer message.
        
        In production, this would use more sophisticated NLP models.
        """
        try:
            text_lower = text.lower()
            
            # Count keyword occurrences
            positive_count = sum(1 for word in self.POSITIVE_KEYWORDS if word in text_lower)
            negative_count = sum(1 for word in self.NEGATIVE_KEYWORDS if word in text_lower)
            urgent = any(word in text_lower for word in self.URGENT_KEYWORDS)
            
            # Determine overall sentiment
            if negative_count > positive_count:
                sentiment = "negative"
                score = -0.5 - (negative_count * 0.1)
            elif positive_count > negative_count:
                sentiment = "positive"
                score = 0.5 + (positive_count * 0.1)
            else:
                sentiment = "neutral"
                score = 0.0
            
            # Cap score between -1 and 1
            score = max(-1.0, min(1.0, score))
            
            # Detect emotions
            emotions = []
            if sentiment == "positive":
                emotions = ["happy", "satisfied"]
            elif sentiment == "negative":
                if "angry" in text_lower or "frustrated" in text_lower:
                    emotions = ["angry", "frustrated"]
                else:
                    emotions = ["disappointed", "concerned"]
            else:
                emotions = ["neutral"]
            
            result = {
                "sentiment": sentiment,
                "score": round(score, 2),
                "confidence": random.uniform(0.75, 0.95),
                "emotions": emotions,
                "urgent": urgent,
                "requires_attention": sentiment == "negative" or urgent
            }
            
            logger.info(
                "sentiment_analyzed",
                sentiment=sentiment,
                score=score,
                urgent=urgent
            )
            
            return result
            
        except Exception as e:
            logger.error("sentiment_analysis_error", error=str(e))
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "error": str(e)
            }
    
    def get_tone_adjustment(self, sentiment: str) -> Dict[str, str]:
        """Get recommended tone adjustment based on sentiment."""
        if sentiment == "negative":
            return {
                "tone": "empathetic and patient",
                "recommendation": "Be extra understanding and offer solutions",
                "example": "I understand your concern. Let me help you with that right away."
            }
        elif sentiment == "positive":
            return {
                "tone": "enthusiastic and supportive",
                "recommendation": "Match their energy and build on the positivity",
                "example": "That's great! I'm excited to help you move forward."
            }
        else:
            return {
                "tone": "professional and friendly",
                "recommendation": "Maintain balanced, helpful approach",
                "example": "I'd be happy to assist you with that."
            }


# Global sentiment service instance
sentiment_service = SentimentService()


