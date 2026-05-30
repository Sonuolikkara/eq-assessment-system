import json
from typing import Dict, List


class VisualizationModule:
    """
    Generates data structures for visualization:
    - Bar charts for emotion scores
    - Response breakdowns
    - Performance comparisons
    """
    
    @staticmethod
    def generate_emotion_chart_data(emotion_scores: Dict[str, float]) -> Dict:
        """Generate data for emotion distribution bar chart"""
        return {
            'type': 'bar',
            'labels': list(emotion_scores.keys()),
            'data': list(emotion_scores.values()),
            'backgroundColor': [
                'rgba(255, 107, 107, 0.7)',  # Anger - Red
                'rgba(255, 193, 7, 0.7)',    # Disgust - Orange
                'rgba(52, 211, 153, 0.7)',   # Fear - Green
                'rgba(96, 165, 250, 0.7)',   # Sadness - Blue
                'rgba(168, 85, 247, 0.7)',   # Happiness - Purple
            ]
        }
    
    @staticmethod
    def generate_eq_score_breakdown(eq_score: int, sentiment_avg: float, empathy: float, constructiveness: float) -> Dict:
        """Generate breakdown of EQ score components"""
        return {
            'total_score': eq_score,
            'components': [
                {
                    'name': 'Emotional Sentiment',
                    'score': int(sentiment_avg * 100),
                    'weight': 40,
                    'color': 'rgba(255, 107, 107, 0.7)'
                },
                {
                    'name': 'Empathy Indicators',
                    'score': int(empathy * 100),
                    'weight': 35,
                    'color': 'rgba(52, 211, 153, 0.7)'
                },
                {
                    'name': 'Constructiveness',
                    'score': int(constructiveness * 100),
                    'weight': 25,
                    'color': 'rgba(96, 165, 250, 0.7)'
                }
            ]
        }
    
    @staticmethod
    def generate_response_summary(responses: List[str], emotional_analyses: List[Dict]) -> Dict:
        """Generate detailed response summary"""
        summary = []
        for i, (response, analysis) in enumerate(zip(responses, emotional_analyses), 1):
            summary.append({
                'question_number': i,
                'response_preview': response[:100] + '...' if len(response) > 100 else response,
                'full_response': response,
                'sentiment': analysis.get('normalized_score', 0),
                'emotional_valence': analysis.get('emotional_valence', 'neutral'),
                'positive_score': analysis.get('positive_score', 0),
                'negative_score': analysis.get('negative_score', 0),
                'sentiment_label': VisualizationModule._get_sentiment_label(analysis.get('normalized_score', 0.5))
            })
        return {
            'total_responses': len(responses),
            'responses': summary
        }
    
    @staticmethod
    def _get_sentiment_label(score: float) -> str:
        """Get label for sentiment score"""
        if score >= 0.7:
            return 'Very Positive'
        elif score >= 0.5:
            return 'Positive'
        elif score >= 0.4:
            return 'Neutral'
        elif score >= 0.2:
            return 'Slightly Negative'
        else:
            return 'Negative'
    
    @staticmethod
    def generate_comparison_metrics(current_score: int) -> Dict:
        """Generate comparison metrics for results"""
        return {
            'score': current_score,
            'percentile': VisualizationModule._estimate_percentile(current_score),
            'range': VisualizationModule._get_score_range(current_score),
            'comparison': {
                'average_score': 60,  # Assumed average
                'your_score': current_score,
                'above_average': current_score > 60
            }
        }
    
    @staticmethod
    def _estimate_percentile(score: int) -> int:
        """Estimate percentile rank"""
        if score >= 75:
            return 85
        elif score >= 60:
            return 65
        elif score >= 45:
            return 40
        else:
            return 20
    
    @staticmethod
    def _get_score_range(score: int) -> str:
        """Get score range label"""
        if score >= 75:
            return 'Excellent (75-100)'
        elif score >= 60:
            return 'Good (60-74)'
        elif score >= 45:
            return 'Average (45-59)'
        else:
            return 'Developmental (20-44)'
    
    @staticmethod
    def generate_html_chart(chart_data: Dict) -> str:
        """Generate HTML/JavaScript for Chart.js visualization"""
        labels = json.dumps(chart_data['labels'])
        data = json.dumps(chart_data['data'])
        colors = json.dumps(chart_data['backgroundColor'])
        
        html = f"""
        <canvas id="emotionChart" width="400" height="100"></canvas>
        <script>
            var ctx = document.getElementById('emotionChart').getContext('2d');
            var chart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {labels},
                    datasets: [{{
                        label: 'Emotion Scores',
                        data: {data},
                        backgroundColor: {colors},
                        borderColor: 'rgba(0, 0, 0, 0.1)',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            max: 5
                        }}
                    }}
                }}
            }});
        </script>
        """
        return html
