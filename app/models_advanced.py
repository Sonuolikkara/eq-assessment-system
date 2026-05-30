import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)


class AdvancedEQAssessmentModel:
    """
    Core class containing all EQ assessment logic:
    - Scenario generation
    - Question formulation  
    - Response validation
    - Emotional analysis
    - EQ scoring
    """
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.profession_scenarios = self._init_scenarios()
        self.questions = self._init_questions()
        self.emotion_categories = ['happiness', 'sadness', 'anger', 'fear', 'disgust']
    
    def _init_scenarios(self):
        """Initialize profession-based scenarios"""
        return {
            'Software Engineer': {
                'scenario': 'Your team is working on a critical deadline. A junior developer is frustrated because their code keeps getting rejected in review. They are stressed and demotivated. How would you respond?',
                'context': 'technical_leadership'
            },
            'Doctor': {
                'scenario': 'A patient is upset because they had to wait 2 hours for their appointment despite booking on time. They are expressing their frustration. How would you handle this?',
                'context': 'patient_care'
            },
            'Teacher': {
                'scenario': 'A student failed an important exam and is crying in your office. They say they worked hard but could not pass. How would you respond?',
                'context': 'student_support'
            },
            'Manager': {
                'scenario': 'Two of your team members had a conflict during a meeting. One of them is now avoiding collaboration. How would you resolve this?',
                'context': 'conflict_resolution'
            },
            'Sales Executive': {
                'scenario': 'A major client is upset because a promised feature was delayed by 2 months. They are threatening to switch to a competitor. How would you address this?',
                'context': 'client_management'
            },
            'Designer': {
                'scenario': 'A colleague harshly criticized your design in a public meeting. You feel embarrassed and angry. How would you respond professionally?',
                'context': 'feedback_handling'
            }
        }
    
    def _init_questions(self):
        """Initialize reflective questions"""
        return [
            "How would you respond emotionally to this situation?",
            "What would be your first action to address the issue?",
            "How would you demonstrate empathy in this scenario?",
            "What would you say to comfort or reassure the person?",
            "How would you prevent similar situations in the future?"
        ]
    
    def get_scenario(self, profession):
        """Get scenario for a profession"""
        if profession in self.profession_scenarios:
            return self.profession_scenarios[profession]['scenario']
        return "Handle an emotional workplace situation with empathy and maturity."
    
    def get_questions(self):
        """Get all assessment questions"""
        return self.questions
    
    def analyze_emotional_tone(self, text):
        """
        Analyze emotional tone of response using transformer proxy (NLTK VADER)
        Returns: sentiment scores and emotion indicators
        """
        scores = self.sia.polarity_scores(text)
        
        emotion_analysis = {
            'positive_score': scores['pos'],
            'negative_score': scores['neg'],
            'neutral_score': scores['neu'],
            'compound_score': scores['compound'],  # -1 to 1
            'normalized_score': (scores['compound'] + 1) / 2,  # 0 to 1
            'emotional_valence': self._classify_emotion(scores['compound'])
        }
        
        return emotion_analysis
    
    def _classify_emotion(self, compound_score):
        """Classify general emotion from compound score"""
        if compound_score >= 0.5:
            return 'positive'
        elif compound_score >= 0.1:
            return 'neutral_positive'
        elif compound_score >= -0.1:
            return 'neutral'
        elif compound_score >= -0.5:
            return 'neutral_negative'
        else:
            return 'negative'
    
    def calculate_eq_score(self, responses_analysis):
        """
        Calculate EQ score from analyzed responses
        Considers: emotional awareness, empathy indicators, constructiveness
        """
        sentiment_scores = [r['normalized_score'] for r in responses_analysis]
        
        # Average sentiment
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        
        # Empathy indicators (negative scores in emotional responses show awareness)
        empathy_score = self._calculate_empathy(responses_analysis)
        
        # Constructiveness (balance of positive without dismissing)
        constructive_score = self._calculate_constructiveness(responses_analysis)
        
        # Weighted calculation
        eq_score = int(
            (avg_sentiment * 0.4) +
            (empathy_score * 0.35) +
            (constructive_score * 0.25)
        ) * 100
        
        # Bound between 20-100
        return max(20, min(100, eq_score))
    
    def _calculate_empathy(self, responses_analysis):
        """Calculate empathy from responses"""
        # More nuanced response analysis indicates empathy
        emotional_words = ['understand', 'feel', 'support', 'help', 'care', 'appreciate', 'recognize']
        empathy_count = 0
        
        for response in responses_analysis:
            # This is simplified - in production, use more sophisticated NLP
            empathy_count += sum(1 for word in emotional_words if word in str(response).lower())
        
        return min(1.0, empathy_count / (len(responses_analysis) * 2))
    
    def _calculate_constructiveness(self, responses_analysis):
        """Calculate constructiveness of responses"""
        positive_count = sum(1 for r in responses_analysis if r['emotional_valence'] in ['positive', 'neutral_positive'])
        return positive_count / len(responses_analysis)
    
    def generate_detailed_feedback(self, eq_score, responses_analysis):
        """Generate detailed feedback"""
        if eq_score >= 75:
            summary = "Excellent emotional intelligence!"
            details = "You demonstrate strong awareness of emotions, genuine empathy, and constructive problem-solving approaches."
        elif eq_score >= 60:
            summary = "Good emotional intelligence."
            details = "You show awareness of emotions and handle most situations reasonably well. Focus on deepening empathy in responses."
        elif eq_score >= 45:
            summary = "Average emotional intelligence."
            details = "Consider reflecting more on emotional responses and how your words impact others."
        else:
            summary = "Developmental area."
            details = "Invest time in building emotional awareness skills and practicing empathetic communication."
        
        # Add emotional breakdown
        emotion_distribution = self._get_emotion_distribution(responses_analysis)
        
        return {
            'summary': summary,
            'details': details,
            'emotion_breakdown': emotion_distribution,
            'recommendation': self._get_recommendation(eq_score)
        }
    
    def _get_emotion_distribution(self, responses_analysis):
        """Get distribution of emotion types"""
        emotions = [r['emotional_valence'] for r in responses_analysis]
        distribution = {}
        for emotion in self.emotion_categories:
            distribution[emotion] = emotions.count(emotion) if emotion in emotions else 0
        return distribution
    
    def _get_recommendation(self, eq_score):
        """Get personalized recommendation"""
        if eq_score >= 75:
            return "Consider mentoring others in emotional intelligence and conflict resolution."
        elif eq_score >= 60:
            return "Practice active listening and seek feedback from colleagues on your empathy."
        elif eq_score >= 45:
            return "Take a course on emotional intelligence or mindfulness to improve self-awareness."
        else:
            return "Work with a coach or mentor to develop emotional awareness and communication skills."
