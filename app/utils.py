PROFESSIONS = ['Software Engineer', 'Doctor', 'Teacher', 'Manager', 'Sales Executive', 'Designer']

SCENARIOS = {
    'Software Engineer': 'Your team is working on a critical deadline. A junior developer is frustrated because their code keeps getting rejected in review. They are stressed and demotivated. How would you respond to this situation?',
    'Doctor': 'A patient is upset because they had to wait 2 hours for their appointment despite booking on time. They are expressing their frustration. How would you handle this?',
    'Teacher': 'A student failed an important exam and is crying in your office. They say they worked hard but could not pass. How would you respond?',
    'Manager': 'Two of your team members had a conflict during a meeting. One of them is now avoiding collaboration. How would you resolve this?',
    'Sales Executive': 'A major client is upset because a promised feature was delayed by 2 months. They are threatening to switch to a competitor. How would you address this?',
    'Designer': 'A colleague harshly criticized your design in a public meeting. You feel embarrassed and angry. How would you respond professionally?'
}

QUESTIONS = [
    "How would you respond emotionally?",
    "What would be your first action?",
    "How would you show empathy in this situation?",
    "What would you say to comfort them?",
    "How would you prevent similar situations in the future?"
]

def get_scenario(profession):
    return SCENARIOS.get(profession, "Handle an emotional workplace situation with empathy and maturity.")

def get_questions():
    return QUESTIONS
