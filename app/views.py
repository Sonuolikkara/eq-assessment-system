from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Assessment
from .models_advanced import AdvancedEQAssessmentModel
from .validators import ValidationModule
from .visualization import VisualizationModule
import json

# Initialize assessment model
eq_model = AdvancedEQAssessmentModel()
validator = ValidationModule()
visualizer = VisualizationModule()

PROFESSIONS = list(eq_model.profession_scenarios.keys())

def index(request):
    """
    Landing page: User registration and profession selection
    Uses ValidationModule for input validation
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()
        gender = request.POST.get('gender', '').strip()
        profession = request.POST.get('profession', '').strip()
        
        # Validate user input
        is_valid, errors = validator.validate_user_info(name, age, gender, profession)
        if not is_valid:
            return render(request, 'index.html', {
                'professions': PROFESSIONS,
                'errors': errors
            })
        
        # Sanitize inputs
        name = validator.sanitize_input(name)
        
        # Store in session
        request.session['name'] = name
        request.session['age'] = age
        request.session['gender'] = gender
        request.session['profession'] = profession
        
        # Get scenario and questions from AdvancedEQAssessmentModel
        scenario = eq_model.get_scenario(profession)
        request.session['scenario'] = scenario
        request.session['questions'] = eq_model.get_questions()
        
        return redirect('assessment')
    
    return render(request, 'index.html', {'professions': PROFESSIONS})


def assessment(request):
    """
    Assessment page: Collect emotional responses
    Uses ValidationModule to validate responses
    Uses AdvancedEQAssessmentModel to analyze emotions
    """
    if request.method == 'POST':
        # Collect and validate responses
        raw_responses = []
        for i in range(1, 6):
            response = request.POST.get(f'response_{i}', '').strip()
            raw_responses.append(response)
        
        # Validate all responses
        is_valid, validation_errors = validator.validate_all_responses(raw_responses)
        if not is_valid:
            scenario = request.session.get('scenario')
            questions = request.session.get('questions')
            return render(request, 'assessment.html', {
                'scenario': scenario,
                'questions': questions,
                'errors': validation_errors,
                'previous_responses': raw_responses
            })
        
        # Sanitize responses
        responses = [validator.sanitize_input(r) for r in raw_responses]
        
        # Analyze emotions using AdvancedEQAssessmentModel
        responses_analysis = []
        for response in responses:
            emotional_analysis = eq_model.analyze_emotional_tone(response)
            responses_analysis.append(emotional_analysis)
        
        # Calculate EQ score
        eq_score = eq_model.calculate_eq_score(responses_analysis)
        
        # Generate visualization data
        response_summary = visualizer.generate_response_summary(responses, responses_analysis)
        
        # Generate detailed feedback
        feedback_data = eq_model.generate_detailed_feedback(eq_score, responses_analysis)
        
        # Get user data
        name = request.session.get('name')
        age = int(request.session.get('age'))
        gender = request.session.get('gender')
        profession = request.session.get('profession')
        scenario = request.session.get('scenario')
        
        # Calculate sentiment metrics
        sentiment_scores = [r['normalized_score'] for r in responses_analysis]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        
        # Save assessment to database
        assessment_obj = Assessment.objects.create(
            name=name,
            age=age,
            gender=gender,
            profession=profession,
            scenario=scenario,
            response=' | '.join(responses),
            sentiment_score=avg_sentiment,
            eq_score=eq_score
        )
        
        # Store in session for result page
        request.session['eq_score'] = eq_score
        request.session['sentiment_score'] = avg_sentiment
        request.session['assessment_id'] = assessment_obj.id
        request.session['response_summary'] = response_summary
        request.session['feedback_data'] = feedback_data
        request.session['responses_analysis'] = [
            {k: v for k, v in r.items() if k != 'emotional_valence'} 
            for r in responses_analysis
        ]
        
        return redirect('result')
    
    # GET request - display assessment form
    scenario = request.session.get('scenario')
    questions = request.session.get('questions')
    
    return render(request, 'assessment.html', {
        'scenario': scenario,
        'questions': questions
    })


def result(request):
    """
    Results page: Display EQ score and visualizations
    Uses VisualizationModule to generate charts and breakdowns
    """
    eq_score = request.session.get('eq_score')
    name = request.session.get('name')
    profession = request.session.get('profession')
    sentiment_score = request.session.get('sentiment_score', 0)
    response_summary = request.session.get('response_summary', {})
    feedback_data = request.session.get('feedback_data', {})
    responses_analysis = request.session.get('responses_analysis', [])
    
    # Generate visualizations
    emotion_chart_data = None
    score_breakdown = None
    comparison_metrics = None
    
    if responses_analysis:
        # Prepare emotion data
        emotion_distribution = {
            'positive': sum(1 for r in responses_analysis if r.get('normalized_score', 0) > 0.6),
            'neutral': sum(1 for r in responses_analysis if 0.4 <= r.get('normalized_score', 0) <= 0.6),
            'negative': sum(1 for r in responses_analysis if r.get('normalized_score', 0) < 0.4)
        }
        
        emotion_chart_data = visualizer.generate_emotion_chart_data(emotion_distribution)
        
        # Calculate component scores
        empathy = sum(1 for r in responses_analysis if r.get('positive_score', 0) > 0.3) / len(responses_analysis)
        constructiveness = sum(1 for r in responses_analysis if r.get('normalized_score', 0) > 0.5) / len(responses_analysis)
        
        score_breakdown = visualizer.generate_eq_score_breakdown(
            eq_score, 
            sentiment_score, 
            empathy, 
            constructiveness
        )
    
    comparison_metrics = visualizer.generate_comparison_metrics(eq_score)
    
    context = {
        'name': name,
        'profession': profession,
        'eq_score': eq_score,
        'sentiment_score': round(sentiment_score * 100, 1),
        'feedback': feedback_data.get('details', ''),
        'summary': feedback_data.get('summary', ''),
        'recommendation': feedback_data.get('recommendation', ''),
        'response_summary': response_summary,
        'emotion_chart_data': json.dumps(emotion_chart_data) if emotion_chart_data else None,
        'score_breakdown': score_breakdown,
        'comparison_metrics': comparison_metrics,
    }
    
    return render(request, 'result.html', context)
